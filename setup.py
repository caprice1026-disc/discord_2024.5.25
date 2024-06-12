import asyncio
import logging
import logging.handlers
import os
from typing import List, Optional

import discord
from discord.ext import commands
from aiohttp import ClientSession
import asyncpg  # ReplitのPostgreSQLに接続するためにasyncpgを使用

class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,  # DB接続プールを保持するための変数
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        intents: discord.Intents,  # intents を追加
        prefix: str,  # prefix を追加
        **kwargs,
    ):
        super().__init__(command_prefix=prefix, intents=intents, *args, **kwargs)  # command_prefix と intents を追加
        self.db_pool = db_pool  # データベースプールをインスタンス変数に格納
        self.web_client = web_client  # HTTPクライアントセッションをインスタンス変数に格納
        self.testing_guild_id = testing_guild_id  # テスト用ギルドID
        self.initial_extensions = initial_extensions  # 起動時にロードする拡張機能
        self.tree = discord.app_commands.CommandTree(self)  # CommandTree を追加

    async def setup_hook(self) -> None:
        # 拡張機能をロードする
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # テストギルドが指定されている場合、そのギルドにコマンドを同期する
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

        # 全体のコマンドを同期
        await self.tree.sync()  # Global sync を追加

async def main():
    # ロギング設定
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # ログファイルの最大サイズ
        backupCount=5,  # ログファイルのバックアップ数
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # HTTPセッションとデータベースプールを非同期で管理
    async with ClientSession() as our_client, asyncpg.create_pool(dsn=os.environ['DATABASE_URL'], command_timeout=30) as pool:
        exts = ['general', 'mod', 'dice']  # 起動時にロードする拡張機能
        intents = discord.Intents.all()  # 全てのインテンツを有効にする
        prefix = "/"  # プレフィックスを設定

        async with CustomBot(
            initial_extensions=exts,
            db_pool=pool,
            web_client=our_client,
            testing_guild_id=None,  # 必要に応じてテストギルドIDを設定
            intents=intents,  # intents を渡す
            prefix=commands.when_mentioned_or(prefix),  # prefix を渡す
        ) as bot:
            await bot.start(os.getenv('API_KEY'))  # ボットを起動

asyncio.run(main())
