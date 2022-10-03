import pytest

from yacut.models import URL_map

py_url = 'https://www.python.org'


def test_create_id(client):
    got = client.post('/api/id/', json={
        'url': py_url,
        'custom_id': 'py',
    })
    assert got.status_code == 201, (
        'When creating a short link, 201 starus code should be returned'
    )
    assert list(got.json.keys()) == ['short_link', 'url'], (
        'When creating a short link, keys `url, short_link` should be in the response'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/py',
    }, 'When creating a short link, API response body is different from expected.'


def test_create_empty_body(client):
    try:
        got = client.post('/api/id/')
    except Exception:
        raise AssertionError(
            'If no information was passed in the request body, raise the exception.'
        )
    assert got.status_code == 400, (
        'In response to an empty POST request to the endpoint `/api/id/` a '
        'status code 400 should be returned.'
    )
    assert list(got.json.keys()) == ['message'], (
        'In response to an empty POST request to the endpoint `/api/id/` '
        'should be key `message`'
    )
    assert got.json == {'message': 'Request body missing'}, (
        'The message in the response body when creating a short link without '
        'request body does not match the specification'
    )


@pytest.mark.parametrize('json_data', [
    ({'url': py_url, 'custom_id': '.,/!?'}),
    ({'url': py_url, 'custom_id': 'Hodor-Hodor'}),
    ({'url': py_url, 'custom_id': 'h@k$r'}),
    ({'url': py_url, 'custom_id': '$'}),
    ({'url': py_url, 'custom_id': 'п'}),
    ({'url': py_url, 'custom_id': 'l l'}),
])
def test_invalid_short_url(json_data, client):
    got = client.post('/api/id/', json=json_data)
    assert got.status_code == 400, (
        'If the short link name is invalid, the response status should be 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'If the short link name is invalid, key `message` shoud be in the response'
    )
    assert got.json == {'message': 'Invalid name specified for short link'}, (
        'If the short link name is invalid, a message is returned that does '
        'not conform to the specification.'
    )
    unique_id = URL_map.query.filter_by(original=py_url).first()
    assert not unique_id, (
        'In short link shoud be allowed to use a strictly defined set of '
        'characters. Refer to the text of the assignment'
    )


def test_no_required_field(client):
    try:
        got = client.post('/api/id/', json={
            'short_link': 'python',
        })
    except Exception:
        raise AssertionError(
            'If the request body to the `/api/id/` endpoint is different than expected, ',
            'raise an exception.',
        )
    assert got.status_code == 400, (
        'If the request body to the `/api/id/` endpoint is different than expected, '
        'return 400 status code.'
    )
    assert list(got.json.keys()) == ['message'], (
        'If the request body to the `/api/id/` endpoint is different than expected, '
        'return the response with `message` key.'
    )
    assert got.json == {'message': '\"url\" is required field!'}, (
        'The message in the response body with an incorrect request body '
        'does not match the specification'
    )


def test_url_already_exists(client, short_python_url):
    try:
        got = client.post('/api/id/', json={
            'url': py_url,
            'custom_id': 'py',
        })
    except Exception:
        raise AssertionError(
            'When trying to create short link name that is already taken ',
            'raise an exception.',
        )
    assert got.status_code == 400, (
        'When trying to create short link name that is already taken '
        'return 400 status code.'
    )
    assert list(got.json.keys()) == ['message'], (
        'When trying to create short link name that is already taken '
        'return the response with `message` key.'
    )
    assert got.json == {'message': 'Name "py" is already taken.'}, (
        'When trying to create short link name that is already taken '
        'a message is returned with text that does not match the specification.'
    )


@pytest.mark.parametrize('json_data', [
    ({'url': py_url, 'custom_id': None}),
    ({'url': py_url, 'custom_id': ''}),
])
def test_generated_unique_short_id(json_data, client):
    try:
        got = client.post('/api/id/', json=json_data)
    except Exception:
        raise AssertionError(
            'For a request where short_id is missing or contains an empty '
            'string, generate a unique short_id.'
        )
    assert got.status_code == 201, (
        'When creating a short link without an explicitly specified name, '
        'status code 201 should be returned'
    )
    unique_id = URL_map.query.filter_by(original=py_url).first()
    assert unique_id, (
        'When creating a short link without an explicitly specified name, '
        'you need to generate the relative part of the link from numbers and '
        'Latin characters and save the link in the database'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/' + unique_id.short,
    }, (
        'When creating a short link without an explicitly specified name, '
        'you need to generate the relative part of the link from numbers and '
        'Latin characters and return the link in the API response.'
    )


def test_get_url_endpoint(client, short_python_url):
    got = client.get(f'/api/id/{short_python_url.short}/')
    assert got.status_code == 200, (
        'In response to a GET request to the `/api/id/<short_id>/` endpoint, '
        'status code 200 should be returned'
    )
    assert list(got.json.keys()) == ['url'], (
        'In response to a GET request to the `/api/id/<short_id>/` endpoint, '
        'key `url` must be passed'
    )
    assert got.json == {'url': py_url}, (
        'In response to a GET request to the `/api/id/<short_id>/` endpoint, '
        'a response is returned that does not match the specification.'
    )


def test_get_url_not_found(client):
    got = client.get('/api/id/{enexpected}/')
    assert got.status_code == 404, (
        'In response to a GET request to non-existing link, '
        'status code 404 should be returned.'
    )
    assert list(got.json.keys()) == ['message'], (
        'In response to a GET request to non-existing link, key `message` '
        'should be passed '
    )
    assert got.json == {'message': 'Specified id was not found'}, (
        'In response to a GET request to non-existing link, '
        'a response is returned that does not match the specification.'
    )


def test_len_short_id_api(client):
    long_string = 'CuriosityisnotasinHarryHoweverfromtimetotimeyoushouldexercisecaution'
    got = client.post('/api/id/', json={
        'url': py_url,
        'custom_id': long_string,
    })
    assert got.status_code == 400, (
        'If, during POST request to `/api/id/` endpoint, the `short_id` '
        'field contains a string longer than 16 characters, you need to '
        'return the status code 400.'
    )
    assert list(got.json.keys()) == ['message'], (
        'If, during POST request to `/api/id/` endpoint, the `short_id` '
        'field contains a string longer than 16 characters, key `message` '
        'should in the response.'
    )
    assert got.json == {'message': 'Invalid name specified for short link'}, (
        'When a POST request is made to the `/api/id/` endpoint, in the '
        '`short_id` field of which a string longer than 16 characters is '
        'passed, a response that does not comply with the specification is '
        'returned.'
    )


def test_len_short_id_autogenerated_api(client):
    client.post('/api/id/', json={
        'url': py_url,
    })
    unique_id = URL_map.query.filter_by(original=py_url).first()
    assert len(unique_id.short) == 6, (
        'For a POST request that does not contain a short link in the body, '
        'a short link with a length of 6 characters should be generated.'
    )
