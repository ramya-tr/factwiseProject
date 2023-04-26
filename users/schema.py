from datetime import datetime

from pydantic import BaseModel, constr


class UserRequest(BaseModel):
    """
    Request format for create and update user methods
    """
    name: constr(max_length=64)
    display_name: constr(max_length=128)
    description: constr(max_length=256)


class UserResponse(BaseModel):
    """
    Response format for create user method
    """
    id: int


class UserListResponse(BaseModel):
    """
    Response format for list users method
    """
    id: int
    name: str
    display_name: str
    description: str
    creation_time: datetime


class UserUpdateRequest(BaseModel):
    """
    Request format for update user method
    """
    display_name: constr(max_length=128)
    description: constr(max_length=256)


class UserTeamResponse(BaseModel):
    """
    Response format for get user teams method
    """
    name: str
    description: str
    creation_time: datetime
