from pydantic import BaseModel


class MemberUpdateDto(BaseModel):
    login_id: str
    email: str
    name: str
