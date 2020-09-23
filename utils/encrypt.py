from passlib.hash import bcrypt


def hash_password(password):
    return bcrypt.hash(password)


def check_password(password, hashed):
    return bcrypt.verify(password, hashed)
