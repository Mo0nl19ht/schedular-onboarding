from pydantic import BaseModel


class MemberCreateDto(BaseModel):
    login_id: str
    password: str
    name: str
    email: str
    type: str
