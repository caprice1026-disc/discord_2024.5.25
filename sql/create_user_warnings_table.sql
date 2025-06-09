-- BANや警告を受けたユーザーのリストを保存するテーブルを作成
CREATE TABLE IF NOT EXISTS user_warnings (
    warning_id SERIAL PRIMARY KEY,       -- 自動インクリメントされる警告ID
    user_id BIGINT NOT NULL,             -- 警告を受けたユーザーのディスコードID
    guild_id BIGINT NOT NULL,            -- サーバーID
    message_content TEXT NOT NULL,       -- 警告を受けた投稿の内容
    warning_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(), -- 警告を受けた日時（日本時間）
    flag BOOLEAN NOT NULL DEFAULT FALSE  -- フラグの有無 (例: 特定の行動のための警告)
);

-- インデックスの作成 (必要に応じて)
CREATE INDEX IF NOT EXISTS idx_user_id ON user_warnings (user_id);
CREATE INDEX IF NOT EXISTS idx_warning_timestamp ON user_warnings (warning_timestamp);
CREATE INDEX IF NOT EXISTS idx_user_warnings_guild_id ON user_warnings (guild_id);
