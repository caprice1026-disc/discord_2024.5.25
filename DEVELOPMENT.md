# 開発者向けガイド

このドキュメントでは、Bot の拡張や運用を行う際に役立つ情報をまとめています。

## ディレクトリ構成

- `bot.py` - Bot のエントリーポイント
- `cog/` - 機能ごとの Discord Cog を配置
- `config.py` - 環境変数の読み込みと設定値
- `sql/` - データベース初期化用 SQL スクリプト
- `server.py` - 簡易 Web サーバー (keep_alive 用)
- `old/` - 旧バージョンのコード

## Cog を追加する手順

1. `cog` ディレクトリに新しい Python ファイルを作成します。
2. `config.py` の `initial_extensions` リストにモジュール名を追加します。
3. Bot を再起動すると自動でロードされます。

## 開発サイクル

- 依存関係のインストールや Bot の起動方法は README を参照してください。
- コードを編集したら `python -m py_compile $(git ls-files '*.py')` を実行して構文エラーがないか確認すると安全です。
- 実行中のログは `discord.log` に出力されます。デバッグの際に利用してください。

## データベースについて

Bot は `asyncpg.create_pool` で PostgreSQL などへ接続します。接続情報は `config.DATABASE_URL` で設定できます。テーブル作成用 SQL は `sql/` 配下にまとめています。

## テスト

現時点では自動テストは用意されていません。必要に応じて `pytest` などを導入してテストを書いてください。
