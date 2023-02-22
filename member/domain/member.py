from sqlalchemy import Column, String

from common.base_entity import BaseEntity


class Member(BaseEntity):
    __tablename__ = "member"
    __table_args__ = {"extend_existing": True}
    __abstract__ = True

    email = Column(String(255))
    hashed_password = Column(String(255))
    type = Column(String(255))

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "member"}
