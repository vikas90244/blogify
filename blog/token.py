from datetime import datetime, timedelta, timezone
import jwt
SECRET_KEY = "f8871057688404f9bdad2b6b9d24340303ad2d152c69301dff1972b195017eb91a7f9caa456d5027b54d8598eb05533709f6a973bc6f3979d9dc3cae356c0077"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()


    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta
    
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        print(expire)


    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

