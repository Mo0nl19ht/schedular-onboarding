from pydantic import BaseModel


class Jwt(BaseModel):
    access_token: str
    token_type: str
    login_id: str
    type: str
