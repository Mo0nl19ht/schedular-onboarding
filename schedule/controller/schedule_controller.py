from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from schedule.dto.schedule_dto import ScheduleCreateDto, ScheduleUpdateCreateDto
from schedule.dto.schedule_get_dto import ScheduleGetDto
from schedule.service.schedule_service import ScheduleService
from security.config.jwt_util import get_current_member


class ScheduleController:
    def __init__(self, schedule_service: ScheduleService):
        self.router = APIRouter(prefix="/v1/schedule")
        self.schedule_service = schedule_service

        self.router.add_api_route("", self.create, methods=["POST"])
        self.router.add_api_route(
            "/{schedule_id}",
            self.delete,
            methods=["DELETE"],
            status_code=status.HTTP_202_ACCEPTED,
        )
        self.router.add_api_route("", self.update, methods=["put"])
        self.router.add_api_route("", self.find_all_by_status, methods=["get"])

    def create(
        self,
        schedule_dto: ScheduleCreateDto,
        login_id: str = Depends(get_current_member),
    ) -> ScheduleGetDto:
        return self.schedule_service.create(schedule_dto, login_id)

    def update(
        self,
        schedule_update_dto: ScheduleUpdateCreateDto,
        login_id: str = Depends(get_current_member),
    ) -> ScheduleGetDto:
        return self.schedule_service.update(schedule_update_dto, login_id)

    def delete(self, schedule_id: int, login_id: str = Depends(get_current_member)):
        self.schedule_service.delete(schedule_id, login_id)

    # 1달 단위 조회
    # 주 단위 조회
    # 모든 일정 조회
    # 시작일자로 정렬
    # 페이징?
    def find_all_by_status(
        self, status_value: str, login_id: str = Depends(get_current_member)
    ) -> List[ScheduleGetDto]:
        return self.schedule_service.find_all_by_status(status_value, login_id)
