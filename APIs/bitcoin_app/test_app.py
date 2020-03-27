from apistar import test
from app import app, users, ID_NOT_FOUND

client = test.TestClient(app)

def test_list_users():
    response = client.get('/')
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1000
    assert type(users) == list
    user = users[0]
    expected = {"id":1,"first_name":"Sterne","last_name":"Gell",\
                "bitcoin_address":"15czwRiYGZ6PGM8EjkMS38XBNmkiohSExs",\
                "social_security_number":"283-62-6536"}
    assert user == expected
    last_id = users[-1]["id"]
    assert last_id == 1000

def test_create_user():
    data = dict(first_name="Kevin",
                last_name="Bisner",
                bitcoin_address="15czwRiYG78SGM8EjkMS38XBNmkiohSExs",
                social_security_number="110-51-1732")
    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(users) == 1001

    response = client.get('/1001/')
    assert response.status_code == 200
    expected = {"id":1001, "first_name":"Kevin", "last_name":"Bisner",\
                "bitcoin_address":"15czwRiYG78SGM8EjkMS38XBNmkiohSExs",\
                "social_security_number":"110-51-1732"}
    assert response.json() == expected
        
def test_create_user_missing_field():
    data = {'key': 1}
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors['social_security_number'] ==\
        'The "social_security_number" field is required.'

def test_create_user_field_validation():
    data = {'bitcoin_address': 'x'*35,
            'social_security_number': 123456789}
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors['bitcoin_address'] == 'Must have no more than 34 characters.'
    assert errors['social_security_number'] == 'Must have at least 11 characters.'

def test_get_user():
    response = client.get('/813/')
    assert response.status_code == 200

    expected = {"id":813,"first_name":"Keven","last_name":"Jirka",
                "bitcoin_address":"1HdhruUcmU1z3fDhz9b6FzajLuE3LrzoB8",
                "social_security_number":"898-62-9881"}
    assert response.json() == expected

def test_get_user_notfound():
    response = client.get('/11111/')
    assert response.status_code == 404
    assert response.json() == {'error': ID_NOT_FOUND}

def test_update_user():
    data = {'first_name': 'Kevin',
            'last_name': 'Bisner',
            'bitcoin_address': 'HG7thak2968HJkLllaiw82FGlQ32K103hZ',
            'social_security_number': '100-33-1129'}
    response = client.put('/777/', data=data)
    assert response.status_code == 200

    #test put response
    expected = {'id': 777, 'first_name': 'Kevin',
                'last_name': 'Bisner',
                'bitcoin_address': 'HG7thak2968HJkLllaiw82FGlQ32K103hZ',
                'social_security_number': '100-33-1129'}
    assert response.json() == expected

    #check if data persisted == wiped our previous data car 777
    response = client.get('/777/')
    assert response.json() == expected

def test_update_user_notfound():
    data = {'first_name': 'Kevin',
            'last_name': 'Bisner',
            'bitcoin_address': 'HG7thak2968HJkLllaiw82FGlQ32K103hZ',
            'social_security_number': '100-33-1129'}
    response = client.put('/11111/', data=data)

    assert response.status_code == 404
    assert response.json() == {'error': ID_NOT_FOUND}

def test_update_user_validation():
    data = {'first_name': 'Kevin',
            'last_name': 'Bisner',
            'bitcoin_address': 's' * 35,
            'social_security_number': '123456789'}
    response = client.put('/777/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors ['bitcoin_address'] == 'Must have no more than 34 characters.'
    assert errors ['social_security_number'] == 'Must have at least 11 characters.'

def test_delete_user():
    user_count = len(users)

    for i in (11, 22, 33):
        response = client.delete(f'/{i}/')
        assert response.status_code == 204
        
        response = client.get(f'/{i}/')
        assert response.status_code == 404 #user_gone

    assert len(users) == user_count - 3