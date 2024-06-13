import discord
from discord.ext import tasks, commands

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
                # 10秒ごとに前回チェックした投稿日時以降の投稿をすべて参照するように
                # 初回実行時は実行時の日時にして、過去の大量の投稿を読み込まれないようにする。
                async for message in channel.history(limit=100):
                    # 勝手に招待リンクを貼ったら削除
                    if "https://discord.gg/" in message.content:  # 禁止された文字列を含むメッセージを検出
                        await message.delete()  # メッセージを削除

    @check_messages.before_loop
    async def before_check_messages(self):
        await self.bot.wait_until_ready()  # ボットが準備完了するまで待機

def setup(bot):
    bot.add_cog(BanCog(bot))