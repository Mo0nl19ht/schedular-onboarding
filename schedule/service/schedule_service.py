from datetime import datetime

from fastapi import Depends, HTTPException
from starlette import status

from member.repository.user_repository import UserRepository
from schedule.domain.schedule import Schedule
from schedule.dto.schedule_create_dto import ScheduleCreateDto
from schedule.dto.schedule_get_dto import ScheduleGetDto
from schedule.repository.schedule_repository import ScheduleRepository


class ScheduleService:
    def __init__(
        self, schedule_repository: ScheduleRepository, user_repository: UserRepository
    ):
        self.user_repository = user_repository
        self.schedule_repository = schedule_repository

    def create(
        self, schedule_create_dto: ScheduleCreateDto, login_id: str
    ) -> ScheduleGetDto:
        user = self.user_repository.find_by_login_id(login_id)
        self._validate_member(user)

        self._validate_date_format(schedule_create_dto)
        schedule = Schedule.from_create_dto(schedule_create_dto, user.id)
        self._validate_date_order(schedule)
        self._validate_schedule(schedule)

        return ScheduleGetDto.from_orm(
            self.schedule_repository.create(schedule), login_id
        )

    def _validate_member(self, member):
        if not member:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="등록된 사용자가 아닙니다"
            )

    def _validate_date_order(self, schedule: Schedule):
        if schedule.start >= schedule.end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="일정 시작이 완료보다 선행되어야합니다"
            )

    def _validate_date_format(self, schedule_create_dto: ScheduleCreateDto):
        try:
            date_format = "%Y-%m-%d-%H:%M"
            datetime.strptime(schedule_create_dto.start, date_format)
            datetime.strptime(schedule_create_dto.end, date_format)
        except:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 시간 형식입니다",
            )

    def _validate_schedule(self, schedule):
        if self.schedule_repository.find_by_start_and_end(schedule.start, schedule.end):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 schedule 입니다"
            )
