from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def main() -> str:
    """稼働確認用エンドポイント"""
    return "Bot is alive!"

def run() -> None:
    """Flask アプリを起動"""
    app.run("0.0.0.0", port=8080)

def keep_alive() -> None:
    """スレッドを起動し Web サーバーを常駐させる"""
    t = Thread(target=run)
    t.start()
