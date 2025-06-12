from __future__ import annotations

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    BigInteger,
    Integer,
    Text,
    Boolean,
    TIMESTAMP,
    func,
)
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

import config

metadata = MetaData()

guild_configs = Table(
    "guild_configs",
    metadata,
    Column("guild_id", BigInteger, primary_key=True),
    Column("archive_category_id", BigInteger, nullable=False),
    Column("ban_allow_role_id", BigInteger, nullable=False),
)

discord_channels = Table(
    "discord_channels",
    metadata,
    Column("channel_id", BigInteger, primary_key=True),
    Column("guild_id", BigInteger, nullable=False),
    Column("channel_name", Text, nullable=False),
    Column("owner_name", Text, nullable=False),
    Column("owner_user_id", BigInteger, nullable=False),
)

user_warnings = Table(
    "user_warnings",
    metadata,
    Column("warning_id", Integer, primary_key=True),
    Column("user_id", BigInteger, nullable=False),
    Column("guild_id", BigInteger, nullable=False),
    Column("message_content", Text, nullable=False),
    Column("warning_timestamp", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
    Column("flag", Boolean, nullable=False, server_default="false"),
)


def create_engine() -> AsyncEngine:
    """設定ファイルから AsyncEngine を生成"""
    return create_async_engine(config.DATABASE_URL, echo=False)
