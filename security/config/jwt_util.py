from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365
SECRET_KEY = "8e132a5bffd31e6ed1d1361153fcef90133827bdffc33f59c03732007ca9150b"
ALGORITHM = "HS256"
TOKEN_TYPE = "bearer"

# 원래는 tokenUrl을 입력하라 하는데 정확하게 얘가 어떻게 동작하는지를 모르겠네
# 없어도 되는거같은데 정확하게 왜 그런지는 모르겠음
oauth2_user_scheme = OAuth2PasswordBearer(tokenUrl="")


def get_current_member(token: str = Depends(oauth2_user_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 JWT 입니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login_id: str = payload.get("sub")
        if login_id is None:
            raise credentials_exception

        return login_id
    except JWTError:
        raise credentials_exception
