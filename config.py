from typing import List, Optional
import os
import discord
from dotenv import load_dotenv

load_dotenv()

# ボットの設定
# cogを追加するたびにここに追加していく
initial_extensions: List[str] = ['cog.archive', 'cog.ban', 'cog.general', 'cog.setup']
intents = discord.Intents.all()
prefix = "!"

# データベース接続情報
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///:memory:')

# テストギルドID (必要に応じて設定)
_test_id_str = os.getenv("TESTING_GUILD_ID")
testing_guild_id: Optional[int] = int(_test_id_str) if _test_id_str else None

# その他環境変数
ARCHIVE_CATEGORY_ID = int(os.getenv('ARCHIVE_CATEGORY_ID', 0))
BAN_ALLOW_ROLE_ID = int(os.getenv('BAN_ALLOW_ROLE_ID', 0))
API_KEY = os.getenv('API_KEY')

