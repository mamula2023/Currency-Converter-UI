def authorize(username: str, password: str) -> bool:
    if username == 'admin' and password == 'admin':
        return True
    return False
