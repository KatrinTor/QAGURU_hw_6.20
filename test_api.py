import json

import pytest
import requests
from jsonschema.validators import validate

name = 'morpheus'
job = 'leader'


def test_create_user():
    response = requests.post(
        url='https://reqres.in/api/users',
        data={'name': name, 'job': job}
    )

    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_create_user_schema():
    with open('schemas/post_create_user_schema.json') as file:
        schema = json.loads(file.read())
    response = requests.post(
        url='https://reqres.in/api/users',
        data={'name': name, 'job': job}
    )
    validate(instance=response.json(), schema=schema)


@pytest.mark.parametrize('id', [2, 'trr'])
def test_get_single_user(id):
    response = requests.get(url=f'https://reqres.in/api/users/{id}')
    print(response.status_code)
    if id is int:
        assert response.status_code == 200
    elif id is str:
        assert response.status_code == 404


def test_single_user_schema():
    with open('schemas/get_single_user_schema.json') as file:
        schema = json.loads(file.read())
    response = requests.get(url='https://reqres.in/api/users/2')
    validate(instance=response.json(), schema=schema)


@pytest.mark.parametrize('id', [2, 3])
def test_single_resource(id):
    response = requests.get(url=f'https://reqres.in/api/unknown/{id}')
    assert response.status_code == 200
    assert response.json()['data']['id'] == id


def test_single_resource_schema():
    with open('schemas/get_single_resource_schema.json') as file:
        schema = json.loads(file.read())
    response = requests.get(url=f'https://reqres.in/api/unknown/2')
    validate(instance=response.json(), schema=schema)


# LOGIN TESTS

email = "eve.holt@reqres.in"
password = 'cityslicka'


def test_login_unsuccessful():
    response = requests.post(url='https://reqres.in/api/login',
                             data={'email': email})
    assert response.status_code == 400
    assert response.json()["error"] in "Missing password"


def test_login_unsuccessful_schema():
    with open('schemas/post_login_unsuccessful_schema.json') as file:
        schema = json.loads(file.read())
    response = requests.post(url='https://reqres.in/api/login',
                             data={'email': email})
    validate(instance=response.json(), schema=schema)


def test_login_successful():
    response = requests.post(url='https://reqres.in/api/login',
                             data={"email": email,
                                   "password": password})
    assert response.status_code == 200
    assert response.json()["token"] in "QpwL5tke4Pnpja7X4"


def test_login_successful_schema():
    with open('schemas/post_login_successful_schema.json') as file:
        schema = json.loads(file.read())
    response = requests.post(url='https://reqres.in/api/login',
                             data={"email": email,
                                   "password": password})
    validate(instance=response.json(), schema=schema)
