from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncEngine

from db import guild_configs

@dataclass
class GuildConfig:
    """ギルドごとの設定情報"""
    archive_category_id: int
    ban_allow_role_id: int

async def fetch_config(engine: AsyncEngine, guild_id: int) -> Optional[GuildConfig]:
    """設定を取得します"""
    async with engine.connect() as conn:
        result = await conn.execute(
            select(
                guild_configs.c.archive_category_id,
                guild_configs.c.ban_allow_role_id,
            ).where(guild_configs.c.guild_id == guild_id)
        )
        row = result.mappings().first()
    if row:
        return GuildConfig(row["archive_category_id"], row["ban_allow_role_id"])
    return None

async def set_config(engine: AsyncEngine, guild_id: int, archive_id: int, ban_role_id: int) -> None:
    """設定を挿入または更新します"""
    stmt = (
        pg_insert(guild_configs)
        .values(
            guild_id=guild_id,
            archive_category_id=archive_id,
            ban_allow_role_id=ban_role_id,
        )
        .on_conflict_do_update(
            index_elements=[guild_configs.c.guild_id],
            set_={
                "archive_category_id": archive_id,
                "ban_allow_role_id": ban_role_id,
            },
        )
    )
    async with engine.begin() as conn:
        await conn.execute(stmt)

async def update_archive_category(engine: AsyncEngine, guild_id: int, archive_id: int) -> None:
    """アーカイブカテゴリーのみ更新"""
    stmt = (
        update(guild_configs)
        .where(guild_configs.c.guild_id == guild_id)
        .values(archive_category_id=archive_id)
    )
    async with engine.begin() as conn:
        await conn.execute(stmt)

async def update_ban_role(engine: AsyncEngine, guild_id: int, ban_role_id: int) -> None:
    """BAN 除外ロールのみ更新"""
    stmt = (
        update(guild_configs)
        .where(guild_configs.c.guild_id == guild_id)
        .values(ban_allow_role_id=ban_role_id)
    )
    async with engine.begin() as conn:
        await conn.execute(stmt)

