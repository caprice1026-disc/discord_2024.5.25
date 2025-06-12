import datetime
from dataclasses import dataclass

import discord
from discord.ext import tasks, commands

import config
from guild_config import fetch_config
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from db import discord_channels


@dataclass
class ChannelOwnerRecord:
    channel_id: int
    owner_user_id: int


class ArchiveCog(commands.Cog):
    """チャンネルの自動アーカイブ処理を行うCog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.archive_check.start()

    def cog_unload(self) -> None:
        self.archive_check.cancel()

    @commands.hybrid_command(name="setowner", description="チャンネルの持ち主を設定します")
    async def set_owner(self, ctx: commands.Context, channel: discord.TextChannel, owner: discord.Member) -> None:
        """チャンネルのオーナーをDBに登録"""
        async with self.bot.db_engine.begin() as conn:
            stmt = (
                pg_insert(discord_channels)
                .values(
                    channel_id=channel.id,
                    guild_id=channel.guild.id,
                    channel_name=channel.name,
                    owner_name=owner.display_name,
                    owner_user_id=owner.id,
                )
                .on_conflict_do_update(
                    index_elements=[discord_channels.c.channel_id],
                    set_={
                        "owner_name": owner.display_name,
                        "owner_user_id": owner.id,
                        "guild_id": channel.guild.id,
                    },
                )
            )
            await conn.execute(stmt)
        await ctx.reply(f"{channel.mention} の持ち主を {owner.display_name} に設定しました。")

    @tasks.loop(hours=24)
    async def archive_check(self) -> None:
        """オーナーが30日以上発言していないチャンネルをアーカイブ"""
        now = datetime.datetime.now(datetime.timezone.utc)
        async with self.bot.db_engine.connect() as conn:
            result = await conn.execute(
                select(
                    discord_channels.c.channel_id,
                    discord_channels.c.owner_user_id,
                )
            )
            rows = result.mappings().all()
        records = [
            ChannelOwnerRecord(r["channel_id"], r["owner_user_id"]) for r in rows
        ]
        for record in records:
            channel = self.bot.get_channel(record.channel_id)
            if not isinstance(channel, discord.TextChannel):
                continue
            conf = await fetch_config(self.bot.db_engine, channel.guild.id)
            archive_id = conf.archive_category_id if conf else config.ARCHIVE_CATEGORY_ID
            owner = channel.guild.get_member(record.owner_user_id)
            if not owner:
                continue
            last_owner_msg = None
            async for message in channel.history(limit=100):
                if message.author.id == owner.id:
                    last_owner_msg = message
                    break
            if not last_owner_msg or (now - last_owner_msg.created_at).days >= 30:
                if channel.category_id != archive_id:
                    archive_category = discord.utils.get(channel.guild.categories, id=archive_id)
                    if archive_category:
                        await channel.edit(category=archive_category)
            else:
                if channel.category_id == archive_id:
                    # アーカイブ解除: 最初のカテゴリーに戻す
                    target_category = next((c for c in channel.guild.categories if c.id != archive_id), None)
                    await channel.edit(category=target_category)

    @archive_check.before_loop
    async def before_archive_check(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ArchiveCog(bot))
