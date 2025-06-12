import discord
from discord.ext import commands

import config
from guild_config import fetch_config
from sqlalchemy.dialects.postgresql import insert as pg_insert
from db import user_warnings


class BanCog(commands.Cog):
    """スパム検知とBAN処理を行うCog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if "https://discord.gg/" in message.content:
            roles = [role.id for role in getattr(message.author, "roles", [])]
            conf = None
            if message.guild:
                conf = await fetch_config(self.bot.db_engine, message.guild.id)
            allow_role = conf.ban_allow_role_id if conf else config.BAN_ALLOW_ROLE_ID
            if allow_role not in roles:
                await message.delete()
                await message.author.ban(reason="スパム検出")
                async with self.bot.db_engine.begin() as conn:
                    stmt = pg_insert(user_warnings).values(
                        user_id=message.author.id,
                        guild_id=message.guild.id if message.guild else 0,
                        message_content=message.content,
                    )
                    await conn.execute(stmt)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BanCog(bot))

