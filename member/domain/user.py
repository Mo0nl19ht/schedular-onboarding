from sqlalchemy.orm import relationship

from member.domain.member import Member


class User(Member):
    __mapper_args__ = {"polymorphic_identity": "user"}

    schedules = relationship("Schedule", back_populates="user")
