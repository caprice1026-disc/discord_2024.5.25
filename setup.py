import asyncio
import logging
import logging.handlers
import os
from aiohttp import ClientSession
import asyncpg
from discord.ext import commands
import config  # 設定ファイルをインポート

class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        db_pool: asyncpg.Pool,
        web_client: ClientSession,
        **kwargs,
    ):
        super().__init__(command_prefix=commands.when_mentioned_or(config.prefix), intents=config.intents, *args, **kwargs)
        self.db_pool = db_pool
        self.web_client = web_client
        self.testing_guild_id = config.testing_guild_id
        self.initial_extensions = config.initial_extensions
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        await self.tree.sync()

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with ClientSession() as our_client, asyncpg.create_pool(dsn=config.DATABASE_URL, command_timeout=30) as pool:
        async with CustomBot(
            db_pool=pool,
            web_client=our_client,
        ) as bot:
            await bot.start(os.getenv('API_KEY'))

asyncio.run(main())