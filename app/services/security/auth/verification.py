def verification_password(username: str, password: str):
    return (
        username == password
    )

def create_hash_password(password: str):

    return password