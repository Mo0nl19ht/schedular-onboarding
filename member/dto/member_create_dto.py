from pydantic import BaseModel


class MemberCreateDto(BaseModel):
    login_id: str
    password: str
    name: str
    email: str
    type: str

    # @validator('login_id')
    # def not_empty(cls, v):
    #     if not v or not v.strip():
    #         raise ValueError('빈 값은 허용되지 않습니다.')
    #     return v
