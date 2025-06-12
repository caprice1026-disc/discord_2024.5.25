-- ギルドごとの設定を保存するテーブル
CREATE TABLE IF NOT EXISTS guild_configs (
    guild_id BIGINT PRIMARY KEY,         -- サーバーID
    archive_category_id BIGINT NOT NULL, -- アーカイブ用カテゴリーID
    ban_allow_role_id BIGINT NOT NULL    -- BAN除外ロールID
);

CREATE INDEX IF NOT EXISTS idx_guild_configs_guild_id ON guild_configs (guild_id);
