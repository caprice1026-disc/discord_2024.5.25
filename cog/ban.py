import discord
from discord.ext import tasks, commands
import asyncpg

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_messages.start()

    def cog_unload(self):
        self.check_messages.cancel()

    @tasks.loop(seconds=10.0)  # 10秒ごとに実行
    async def check_messages(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                async for message in channel.history(limit=100):
                    if "https://discord.gg/" in message.content:
                        roles = [role.id for role in message.author.roles]
                        if "特定のロールID" not in roles:
                            await message.delete()
                            await message.author.ban()
                            # ユーザーのIDをDBに控える（非同期版）
                            async with self.bot.db_pool.acquire() as conn:
                                await conn.execute("INSERT INTO user_warnings (user_id, message_content) VALUES ($1, $2)", message.author.id, message.content)

    @check_messages.before_loop
    async def before_check_messages(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(BanCog(bot))