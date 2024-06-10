import discord
from discord.ext import tasks, commands
import datetime

class ArchiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.archive_check.start()

    def cog_unload(self):
        self.archive_check.cancel()

    @tasks.loop(hours=24)
    async def archive_check(self):
        now = datetime.datetime.utcnow()
        for guild in self.bot.guilds:
            for category in guild.categories:
                # 特定のカテゴリーを確認する条件をここに設定
                if category.name == "特定のカテゴリー名":
                    for channel in category.channels:
                        # 最後のメッセージの時間を確認
                        last_message = await channel.history(limit=1).flatten()
                        if last_message:
                            last_message_time = last_message[0].created_at
                            if (now - last_message_time).days >= 30:
                                # アーカイブ処理
                                # ここでは名前を変更してアーカイブする例
                                await channel.edit(name=f"archived-{channel.name}")
                                # または、特定のアーカイブカテゴリーに移動するなどの処理を追加

    @archive_check.before_loop
    async def before_archive_check(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(ArchiveCog(bot))