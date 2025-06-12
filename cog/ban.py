import discord
from discord.ext import commands

import config
from guild_config import fetch_config


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
                conf = await fetch_config(self.bot.db_pool, message.guild.id)
            allow_role = conf.ban_allow_role_id if conf else config.BAN_ALLOW_ROLE_ID
            if allow_role not in roles:
                await message.delete()
                await message.author.ban(reason="スパム検出")
                async with self.bot.db_pool.acquire() as conn:
                    await conn.execute(
                        "INSERT INTO user_warnings (user_id, guild_id, message_content) VALUES ($1, $2, $3)",
                        message.author.id,
                        message.guild.id if message.guild else 0,
                        message.content,
                    )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BanCog(bot))

