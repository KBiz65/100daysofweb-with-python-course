from apistar import test
from app import app, cars, CAR_NOT_FOUND

client = test.TestClient(app)

def test_list_cars():
    response = client.get('/')
    assert response.status_code == 200
    cars = response.json()
    assert len(cars) == 1000
    assert type(cars) == list
    car = cars[0]
    expected = {"id":1,"manufacturer":"Chevrolet","model":"Equinox",\
                "year":2008,"vin":"1J4PN2GK8BW312399"}
    assert car == expected
    last_id = cars[-1]["id"]
    assert last_id == 1000

def test_create_car():
    data = dict(manufacturer="Chevrolet",
                   model='Equinox',
                   year=2018,
                   vin='123')
    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(cars) == 1001

    response = client.get('/1001/')
    assert response.status_code == 200
    expected = {"id":1001, "manufacturer":"Chevrolet", "model":"Equinox",\
                "year":2018, "vin":"123"}
    assert response.json() == expected
        
def test_create_car_missing_field():
    data = {'key': 1}
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors['manufacturer'] == 'The "manufacturer" field is required.'
    assert errors['model'] == 'The "model" field is required.'
    assert errors['year'] == 'The "year" field is required.'

def test_create_car_field_validation():
    data = {'manufacturer': 'Opel',
            'model': 'x'*51,
            'year': 2051}
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert "Must be one of" in errors['manufacturer']
    assert errors['model'] == 'Must have no more than 50 characters.'
    assert errors['year'] == 'Must be less than or equal to 2050.'

def test_get_car():
    response = client.get('/777/')
    assert response.status_code == 200

    expected = {"id":777, "manufacturer":"Infiniti", "model":"QX", "year":1997,
                "vin":"2C3CDXEJ2FH079479"}
    assert response.json() == expected

def test_get_car_notfound():
    response = client.get('/11111/')
    assert response.status_code == 404
    assert response.json() == {'error': CAR_NOT_FOUND}

def test_update_car():
    data = {'manufacturer': 'Honda',
            'model': 'some_model',
            'year': 2018}
    response = client.put('/777/', data=data)
    assert response.status_code == 200

    #test put response
    expected = {'id': 777, 'manufacturer': 'Honda',
                'model': 'some_model', 'year': 2018, 'vin': ''}
    assert response.json() == expected

    #check if data persisted == wiped our previous data car 777
    response = client.get('/777/')
    assert response.json() == expected

def test_update_car_notfound():
    data = {'manufacturer': 'Honda',
            'model': 'some_model',
            'year': 2018}
    response = client.put('/11111/', data=data)

    assert response.status_code == 404
    assert response.json() == {'error': CAR_NOT_FOUND}

def test_update_car_validation():
    data = {'manufacturer': 'nonsesnse',
    'model': 's' * 51,
    'year': 1899}
    response = client.put('/777/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert "Must be one of" in errors['manufacturer']
    assert errors ['year'] == 'Must be greater than or equal to 1900.'
    assert errors ['model'] == 'Must have no more than 50 characters.'

def test_delete_car():
    car_count = len(cars)

    for i in (11, 22, 33):
        response = client.delete(f'/{i}/')
        assert response.status_code == 204
        
        response = client.get(f'/{i}/')
        assert response.status_code == 404 #car_gone

    assert len(cars) == car_count - 3


