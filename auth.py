VALID_USERS = {
    "admin": "admin123",
    "manager": "pmsecure"
}
def authenticate(username, password):
    return VALID_USERS.get(username) == password