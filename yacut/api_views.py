from http import HTTPStatus
from re import fullmatch

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_url():
    PATTERN = r'^[a-zA-Z0-9]{1,16}$'

    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Request body missing')
    if not data.get('url'):
        raise InvalidAPIUsage('"url" is required field!')
    short_id = data.get('custom_id')
    if not short_id:
        data['custom_id'] = get_unique_short_id()
    elif URL_map.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(f'Name "{short_id}" is already taken.')
    elif not fullmatch(PATTERN, short_id):
        raise InvalidAPIUsage('Invalid name specified for short link')
    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED.value


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(
            'Specified id was not found', HTTPStatus.NOT_FOUND.value
        )
    return jsonify(url=url_map.original), HTTPStatus.OK.value
