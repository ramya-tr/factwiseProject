from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, PositiveInt


class TeamCreateRequest(BaseModel):
    name: str = Field(..., max_length=64)
    description: str = Field(..., max_length=128)
    admin: PositiveInt


class TeamCreateResponse(BaseModel):
    id: int


class TeamListResponse(BaseModel):
    id: int
    name: str
    description: str
    creation_time: datetime
    admin: int


class UsersInTeamListResponse(BaseModel):
    user_id: int
    user_name: str
    display_name: str


class TeamAddRemoveUsersRequest(BaseModel):
    users: List[int] = Field(..., max_items=50)
