def test_example():
    assert 1 + 2 == 3

def test_index(client):
    response = client.get('/')
    assert 200 == response.status_code