from enum import Enum


class Status(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
