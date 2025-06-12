from dataclasses import dataclass
from typing import Optional
import asyncpg

@dataclass
class GuildConfig:
    """ギルドごとの設定情報"""
    archive_category_id: int
    ban_allow_role_id: int

async def fetch_config(pool: asyncpg.Pool, guild_id: int) -> Optional[GuildConfig]:
    """設定を取得します"""
    row = await pool.fetchrow(
        "SELECT archive_category_id, ban_allow_role_id FROM guild_configs WHERE guild_id=$1",
        guild_id,
    )
    if row:
        return GuildConfig(row["archive_category_id"], row["ban_allow_role_id"])
    return None

async def set_config(pool: asyncpg.Pool, guild_id: int, archive_id: int, ban_role_id: int) -> None:
    """設定を挿入または更新します"""
    await pool.execute(
        """
        INSERT INTO guild_configs (guild_id, archive_category_id, ban_allow_role_id)
        VALUES ($1, $2, $3)
        ON CONFLICT (guild_id) DO UPDATE
        SET archive_category_id = EXCLUDED.archive_category_id,
            ban_allow_role_id = EXCLUDED.ban_allow_role_id
        """,
        guild_id,
        archive_id,
        ban_role_id,
    )

async def update_archive_category(pool: asyncpg.Pool, guild_id: int, archive_id: int) -> None:
    """アーカイブカテゴリーのみ更新"""
    await pool.execute(
        """UPDATE guild_configs SET archive_category_id=$2 WHERE guild_id=$1""",
        guild_id,
        archive_id,
    )

async def update_ban_role(pool: asyncpg.Pool, guild_id: int, ban_role_id: int) -> None:
    """BAN 除外ロールのみ更新"""
    await pool.execute(
        """UPDATE guild_configs SET ban_allow_role_id=$2 WHERE guild_id=$1""",
        guild_id,
        ban_role_id,
    )

