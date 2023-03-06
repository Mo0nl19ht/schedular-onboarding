from datetime import datetime

from pydantic import BaseModel


class MemberGetDto(BaseModel):
    login_id: str
    name: str
    email: str
    type: str

    class Config:
        orm_mode = True


class UserGetDto(MemberGetDto):
    id: int
    created_at: datetime
    updated_at: datetime
