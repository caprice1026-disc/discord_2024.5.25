from typing import List, Optional
import os
import discord
from discord.ext import commands

# ボットの設定
# cogを追加するたびにここに追加していく
initial_extensions: List[str] = ['cog.archive', 'cog.ban', 'cog.general']
intents = discord.Intents.all()
prefix = "!"

# データベース接続情報
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///:memory:')

# テストギルドID (必要に応じて設定)
testing_guild_id: Optional[int] = None

# その他環境変数
ARCHIVE_CATEGORY_ID = int(os.getenv('ARCHIVE_CATEGORY_ID', 0))
BAN_ALLOW_ROLE_ID = int(os.getenv('BAN_ALLOW_ROLE_ID', 0))
API_KEY = os.getenv('API_KEY')

