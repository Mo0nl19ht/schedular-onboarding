from fastapi import APIRouter, Depends

from schedule.dto.schedule_dto import ScheduleDto, ScheduleUpdateDto
from schedule.dto.schedule_get_dto import ScheduleGetDto
from schedule.service.schedule_service import ScheduleService
from security.config.jwt_util import get_current_member


class ScheduleController:
    def __init__(self, schedule_service: ScheduleService):
        self.router = APIRouter(prefix="/v1/schedule")
        self.schedule_service = schedule_service

        self.router.add_api_route("", self.create, methods=["POST"])
        # self.router.add_api_route("", self.delete, methods=["DELETE"])
        self.router.add_api_route("", self.update, methods=["put"])
        # self.router.add_api_route("", self.find_by_login_id, methods=["get"])

    def create(
        self,
        schedule_dto: ScheduleDto,
        login_id: str = Depends(get_current_member),
    ) -> ScheduleGetDto:
        return self.schedule_service.create(schedule_dto, login_id)

    def update(
        self,
        schedule_update_dto: ScheduleUpdateDto,
        login_id: str = Depends(get_current_member),
    ) -> ScheduleGetDto:
        return self.schedule_service.update(schedule_update_dto, login_id)
