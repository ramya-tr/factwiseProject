from enum import Enum

from pydantic import BaseModel, constr, PositiveInt


class TaskStatus(str, Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'


class BoardBase(BaseModel):
    name: constr(max_length=64)
    description: constr(max_length=128)
    team_id: PositiveInt


class BoardResponse(BaseModel):
    id: PositiveInt


class TaskBase(BaseModel):
    board_id: PositiveInt
    title: constr(max_length=64)
    description: constr(max_length=128)
    user_id: PositiveInt


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class BoardList(BoardBase):
    id: PositiveInt
    board_status: str


class TaskList(TaskBase):
    id: PositiveInt
    task_status: TaskStatus
