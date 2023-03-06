from enum import Enum


class Status(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


def is_in_status(str_value: str) -> bool:
    for status in Status:
        if str_value == status.value:
            return True
    return False
