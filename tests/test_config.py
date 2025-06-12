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
    monkeypatch.setenv('TESTING_GUILD_ID', guild_id_env) if guild_id_env else monkeypatch.delenv('TESTING_GUILD_ID', raising=False)
    import importlib
    import config
    importlib.reload(config)
    assert config.testing_guild_id == expected


def test_create_engine_uses_env(monkeypatch):
    url = 'postgresql://user:pass@localhost/db'
    monkeypatch.setenv('DATABASE_URL', url)
    import importlib
    import config
    importlib.reload(config)
    import db
    importlib.reload(db)
    with mock.patch.object(db, 'create_async_engine') as fake_create:
        db.create_engine()
        fake_create.assert_called_once_with(url, echo=False)

