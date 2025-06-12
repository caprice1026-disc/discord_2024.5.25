import importlib
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest


def reload_modules():
    if 'config' in globals():
        importlib.reload(config)
    else:
        import config
    importlib.reload(config)
    importlib.reload(db)


@pytest.mark.parametrize('guild_id_env, expected', [
    ('12345', 12345),
    (None, None),
])
def test_testing_guild_id(monkeypatch, guild_id_env, expected):
    print(f"TESTING_GUILD_ID={guild_id_env}")
    if guild_id_env:
        monkeypatch.setenv('TESTING_GUILD_ID', guild_id_env)
    else:
        monkeypatch.delenv('TESTING_GUILD_ID', raising=False)
    import importlib
    import config
    importlib.reload(config)
    print(f"testing_guild_id -> {config.testing_guild_id}")
    assert config.testing_guild_id == expected


def test_create_engine_uses_env(monkeypatch):
    url = 'postgresql://user:pass@localhost/db'
    print(f"DATABASE_URL={url}")
    monkeypatch.setenv('DATABASE_URL', url)
    import importlib
    import config
    importlib.reload(config)
    import db
    importlib.reload(db)
    with mock.patch.object(db, 'create_async_engine') as fake_create:
        db.create_engine()
        fake_create.assert_called_once_with(url, echo=False)
    print("create_engine called with expected URL")


def test_env_values_from_system():
    import importlib
    import config
    env_archive = os.getenv('ARCHIVE_CATEGORY_ID')
    env_ban_role = os.getenv('BAN_ALLOW_ROLE_ID')
    print(f"ARCHIVE_CATEGORY_ID={env_archive}")
    print(f"BAN_ALLOW_ROLE_ID={env_ban_role}")
    importlib.reload(config)
    assert config.ARCHIVE_CATEGORY_ID == int(env_archive)
    assert config.BAN_ALLOW_ROLE_ID == int(env_ban_role)
    print("環境変数から設定が読み込まれました")

