def test_404(client):
    got = client.get('/enexpected')
    assert got.status_code == 404, (
        'Return status code `404` when accessing non-existent page'
    )
    assert (
        'If you entered the URL manually please check your spelling and try again.'
        not in got.data.decode('utf-8')
    ), 'Add handling of access to non-existent pages. You will need a 404.html template'
