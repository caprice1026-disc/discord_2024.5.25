-- チャンネル情報を保存するテーブルを作成
CREATE TABLE IF NOT EXISTS discord_channels (
    channel_id BIGINT PRIMARY KEY,      -- チャンネルのID、プライマリキー
    guild_id BIGINT NOT NULL,           -- サーバーID
    channel_name TEXT NOT NULL,         -- チャンネル名
    owner_name TEXT NOT NULL,           -- チャンネルのオーナーの名前
    owner_user_id BIGINT NOT NULL       -- チャンネルのオーナーのユーザーID
);

-- インデックスの作成 (必要に応じて)
CREATE INDEX IF NOT EXISTS idx_owner_user_id ON discord_channels (owner_user_id);
CREATE INDEX IF NOT EXISTS idx_guild_id ON discord_channels (guild_id);
