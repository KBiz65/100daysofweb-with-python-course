import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

#helpers

def _load_bitcoin_data():
    with open('bitcoin_data.json') as f:
        data = json.loads(f.read())
        return {user["id"]: user for user in data}

users = _load_bitcoin_data()
VALID_IDS = set([user["id"]
                                for user in users.values()])
ID_NOT_FOUND = 'User ID not found.'

#VALID_SOCIAL_SECURITY = set([user["social_security_number"]
#                                for user in users.values()])
#SOCIAL_NOT_FOUND = "Social security number not found."

#load in data

#definition

class Users(types.Type):
    id = validators.Integer(allow_null=True)
    first_name = validators.String(default='')
    last_name = validators.String(default = '')
    bitcoin_address = validators.String(max_length=34)
    social_security_number = validators.String(min_length=11, max_length=11)

def list_bitcoin() -> List[Users]:
    return [Users(user) for user in users.values()]

def create_user(user: Users) -> JSONResponse:
    user_id = len(users) + 1
    user.id = user_id
    users[user_id] = user
    return JSONResponse(Users(user), 201)

def get_user(user_id: int) -> JSONResponse:
    user = users.get(user_id)
    if not user:
        error = {'error': ID_NOT_FOUND}
        return JSONResponse(error, 404)
    return JSONResponse(Users(user), 200)

def update_user(user_id: int, user: Users) -> JSONResponse:
    if not users.get(user_id):
        error = {'error': ID_NOT_FOUND}
        return JSONResponse(error, 404)
    
    user["id"] = user_id
    users[user_id] = user
    return JSONResponse(Users(user), 200)

def delete_user(user_id:int) -> JSONResponse:
    if not users.get(user_id):
        error = {'error': ID_NOT_FOUND}
        return JSONResponse(error, 404)

    del users[user_id]
    return JSONResponse({}, 204)

routes = [
    Route('/', method='GET', handler=list_bitcoin),
    Route('/', method='POST', handler=create_user),
    Route('/{user_id}/', method='GET', handler=get_user),
    Route('/{user_id}/', method='PUT', handler=update_user),
    Route('/{user_id}/', method='DELETE', handler=delete_user),
    
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)