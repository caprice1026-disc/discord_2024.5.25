from typing import List, Optional
import discord
from discord.ext import commands

# ボットの設定
#cogを追加するたびにここに追加していく
initial_extensions: List[str] = ['cog.ban', 'cog.general']
intents = discord.Intents.all()
prefix = "/"

# データベース接続情報
DATABASE_URL = "your_database_url_here"  # 環境変数から取得する場合: os.environ['DATABASE_URL']

# テストギルドID (必要に応じて設定)
testing_guild_id: Optional[int] = None