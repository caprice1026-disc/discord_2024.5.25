"""Discord Bot エントリーポイント"""
import asyncio
import logging
import logging.handlers
import os

import discord
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncEngine
from discord.ext import commands

import db

import config


class CustomBot(commands.Bot):
    def __init__(self, *args, db_engine: AsyncEngine, web_client: ClientSession, **kwargs) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(config.prefix), intents=config.intents, *args, **kwargs)
        self.db_engine = db_engine
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


async def main() -> None:
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with ClientSession() as our_client:
        engine = db.create_engine()
        try:
            async with CustomBot(db_engine=engine, web_client=our_client) as bot:
                await bot.start(config.API_KEY)
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

