from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import PositiveInt

from .controller import UserController
from .schema import UserRequest, UserResponse, UserListResponse, UserUpdateRequest, UserTeamResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_controller = UserController()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(request: UserRequest):
    try:
        user_id = user_controller.create_user(request)
        return {"id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/users", response_model=List[UserListResponse])
async def list_users():
    try:
        return user_controller.list_users()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/users/{user_id}", response_model=UserListResponse)
async def describe_user(user_id: PositiveInt):
    try:
        return user_controller.describe_user({"id": user_id})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(user_id: PositiveInt, request: UserUpdateRequest):
    try:
        user_id = user_controller.update_user({"id": user_id, "user": request.dict()})
        return {"id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/users/{user_id}/teams", response_model=List[UserTeamResponse])
async def get_user_teams(user_id: PositiveInt):
    try:
        return user_controller.get_user_teams(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
