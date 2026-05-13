from db import DB_Manager
from jwt_manager import JWT_Manager

db = DB_Manager()

jwt_manager = JWT_Manager()

token = jwt_manager.encode({
    "id": 1,
    "role": "admin"
})

print(token)

decoded = jwt_manager.decode(token)

print(decoded)