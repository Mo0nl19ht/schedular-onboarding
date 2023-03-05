from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException
from starlette import status

from member.repository.user_repository import UserRepository
from schedule.common.config import DATE_FORMAT
from schedule.domain.schedule import Schedule
from schedule.domain import status_enum
from schedule.dto.schedule_dto import ScheduleCreateDto, ScheduleUpdateCreateDto
from schedule.dto.schedule_get_dto import ScheduleGetDto
from schedule.repository.schedule_repository import ScheduleRepository


class ScheduleService:
    def __init__(
        self, schedule_repository: ScheduleRepository, user_repository: UserRepository
    ):
        self.user_repository = user_repository
        self.schedule_repository = schedule_repository

    def create(self, schedule_dto: ScheduleCreateDto, login_id: str) -> ScheduleGetDto:
        user = self._get_current_user(login_id)

        self._validate_date_format(schedule_dto)
        schedule = Schedule.from_create_dto(schedule_dto, user.id)
        self._validate_date_order(schedule)
        self._validate_schedule_by_start_end(schedule.start, schedule.end, user.id)

        return ScheduleGetDto.from_orm(
            self.schedule_repository.create(schedule), login_id
        )

    def update(
        self, schedule_update_dto: ScheduleUpdateCreateDto, login_id: str
    ) -> Schedule:
        user = self._get_current_user(login_id)
        schedule = self.schedule_repository.find_by_id(schedule_update_dto.id)

        self._validate_schedule(schedule)
        self._validate_for_update(schedule, schedule_update_dto, user.id)

        schedule.update(schedule_update_dto)
        self._validate_date_order(schedule)
        return ScheduleGetDto.from_orm(
            self.schedule_repository.update(schedule), login_id
        )

    def _get_current_user(self, login_id: str):
        user = self.user_repository.find_by_login_id(login_id)
        self._validate_user(user)
        return user

    def _validate_user(self, user):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="등록된 사용자가 아닙니다"
            )

    def _validate_date_order(self, schedule: Schedule):
        if schedule.start >= schedule.end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="일정 시작이 완료 보다 선행 되어야 합니다",
            )

    def _validate_date_format(self, schedule_dto: ScheduleCreateDto):
        try:
            datetime.strptime(schedule_dto.start, DATE_FORMAT)
            datetime.strptime(schedule_dto.end, DATE_FORMAT)
        except:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 시간 형식입니다",
            )

    def _validate_schedule_by_start_end(
        self, start: datetime, end: datetime, user_id: int
    ):
        if self.schedule_repository.find_by_start_and_end(start, end, user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 schedule 입니다"
            )

    def _validate_for_update(
        self,
        schedule: Schedule,
        schedule_update_dto: ScheduleUpdateCreateDto,
        user_id: int,
    ):
        # 이게 본인의 스케줄인지
        self._validate_schedule_by_user_id(schedule, user_id)
        # 원래 일정의 시간과 다르다면 본인의 다른 일정들과 중복되는게 없는지
        start = datetime.strptime(schedule_update_dto.start, DATE_FORMAT)
        end = datetime.strptime(schedule_update_dto.end, DATE_FORMAT)
        if schedule.start != start or schedule.end != end:
            self._validate_schedule_by_start_end(start, end, user_id)

    def _validate_schedule_by_user_id(self, schedule: Schedule, user_id: int):
        if user_id != schedule.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="다른 사람의 schedule은 접근 불가능 합니다",
            )

    def _validate_schedule(self, schedule: Schedule):
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 schedule입니다"
            )

    def delete(self, schedule_id: int, login_id: str):
        user = self._get_current_user(login_id)

        schedule = self.schedule_repository.find_by_id(schedule_id)
        self._validate_schedule(schedule)
        self._validate_schedule_by_user_id(schedule, user.id)

        self.schedule_repository.delete(schedule)

    def find_all_by_status(
        self, status_value: str, login_id: str
    ) -> List[ScheduleGetDto]:
        self._validate_status(status_value)
        user = self._get_current_user(login_id)
        scheduels = []
        for scheduel in self.schedule_repository.find_all_by_status(status_value, user):
            scheduels.append(ScheduleGetDto.from_orm(scheduel, login_id))
        return scheduels

    def _validate_status(self, status_value):
        if not status_enum.is_in(status_value):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 status 입니다"
            )
