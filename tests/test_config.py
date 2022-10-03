import os


def test_env_vars():
    assert 'sqlite:///db.sqlite3' in list(os.environ.values()), (
        'Check environment variable with connection to database settings '
        'availabilty with the value sqlite:///db.sqlite3'
    )


def test_config(default_app):
    assert default_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite3', (
        'Check if config key SQLALCHEMY_DATABASE_URI is assigned a value with '
        'connection to database settings'
    )
    assert default_app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'), (
        'Check if config key SECRET_KEY is assigned a value'
    )
