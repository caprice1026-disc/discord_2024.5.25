import discord
from discord.ext import tasks, commands
import datetime
import os

class ArchiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.archive_check.start()

    def cog_unload(self):
        self.archive_check.cancel()

    @tasks.loop(hours=24)
    async def archive_check(self):
        now = datetime.datetime.now()
        for guild in self.bot.guilds:
            for category in guild.categories:
                # 特定のカテゴリーを確認する条件をここに設定
                if category.name == "特定のカテゴリー名":
                    async with self.bot.db_pool.acquire() as conn:
                        for channel in category.channels:
                            # チャンネルIDに基づいてオーナーのユーザーIDを取得
                            owner_id = await conn.fetchval('SELECT owner_user_id FROM discord_channels WHERE channel_id = $1', channel.id)
                            if owner_id:
                                # オーナーの最後のメッセージを取得
                                owner = guild.get_member(owner_id)
                                if owner:
                                    last_message = await owner.history(limit=1).flatten()
                                    if last_message:
                                        last_message_time = last_message[0].created_at
                                        if (now - last_message_time).days >= 14:
                                            # アーカイブ処理
                                            await channel.edit(category=os.getenv('ARCHIVE_CATEGORY_ID'))
                                            # ロギングを追加
                                            print(f'{channel.name}をアーカイブしました。')
                                            
    @archive_check.before_loop
    async def before_archive_check(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(ArchiveCog(bot))