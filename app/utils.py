from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def verify_password(hashed, plain_passwd):
    return pwd_context.verify(plain_passwd, hashed)