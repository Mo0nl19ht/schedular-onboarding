from pydantic import BaseModel


class LoginDto(BaseModel):
    login_id: str
    password: str
