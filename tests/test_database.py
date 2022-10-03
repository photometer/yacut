from sqlalchemy import inspect

from yacut.models import URL_map


def test_fields(_app):
    inspector = inspect(URL_map)
    fields = [column.name for column in inspector.columns]
    assert all(field in fields for field in ['id', 'original', 'short', 'timestamp']), (
        'Not all the required fields were found in the model. '
        'Check the model: id, original, short and timestamp fields should be in it.'
    )
