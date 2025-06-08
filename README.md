# Discord Bot

このリポジトリは、Discord サーバーのチャンネル管理を自動化する Bot です。

## 主な機能

- 24 時間ごとに登録されたチャンネルを確認し、オーナーが 30 日以上発言していない場合にアーカイブカテゴリーへ移動
- オーナーが発言すると自動でアーカイブを解除
- `discord.gg` を含むメッセージを検知し、許可ロールを持たないユーザーは削除・BAN
- BAN したユーザー情報をデータベースに保存し、他コミュニティーと共有可能
- `ping` コマンドで Bot の応答確認

## 環境構築

1. Python 3.10 以降を用意し、必要であれば仮想環境を作成します。
2. 依存関係をインストールします。
   ```bash
   pip install -r requirements.txt
   ```
3. `config.py` が参照する以下の環境変数を設定します。`.env` ファイルにまとめておくと便利です。
   - `API_KEY`: Discord Bot のトークン
   - `DATABASE_URL`: PostgreSQL などの接続文字列
   - `ARCHIVE_CATEGORY_ID`: アーカイブ用カテゴリーの ID
   - `BAN_ALLOW_ROLE_ID`: 招待リンク送信を許可するロール ID
   - `TESTING_GUILD_ID` (任意): テスト用ギルド ID

例:

```env
API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@localhost/dbname
ARCHIVE_CATEGORY_ID=1234567890123
BAN_ALLOW_ROLE_ID=9876543210987
```

## データベース初期化

`sql/` ディレクトリにテーブル作成用 SQL が用意されています。PostgreSQL での実行例:

```bash
psql -f sql/create_discord_channels_table.sql
psql -f sql/create_user_warnings_table.sql
```

## 実行方法

```bash
python bot.py
```

必要に応じて `server.py` を起動すると外部サービスからの稼働チェックに利用できます。

## 開発者向け情報

詳細なコード構成や開発手順については [DEVELOPMENT.md](DEVELOPMENT.md) を参照してください。
