from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import PositiveInt

from .controller import TeamBase
from .schema import (
    TeamCreateRequest,
    TeamCreateResponse,
    TeamListResponse,
    TeamAddRemoveUsersRequest,
    UsersInTeamListResponse,
)

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)

team_base = TeamBase()


@router.post("/teams", status_code=status.HTTP_201_CREATED, response_model=TeamCreateResponse)
async def create_team(team: TeamCreateRequest):
    try:
        team_id = team_base.create_team(team)
        return {"id": team_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/teams", response_model=List[TeamListResponse])
async def list_teams():
    return team_base.list_teams()


@router.get("/teams/{team_id}", response_model=TeamListResponse)
async def describe_team(team_id: PositiveInt):
    try:
        team_detail = team_base.describe_team({"id": team_id})
        if team_detail:
            return team_detail
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_team(team_id: PositiveInt, team: TeamCreateRequest):
    try:
        team_base.update_team({"id": team_id, "team": team})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/teams/{team_id}/users", status_code=status.HTTP_204_NO_CONTENT)
async def add_users_to_team(team_id: int, users: TeamAddRemoveUsersRequest):
    try:
        team_base.add_users_to_team(team_id, users)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/teams/{team_id}/users", status_code=status.HTTP_204_NO_CONTENT)
async def remove_users_from_team(team_id: int, users: TeamAddRemoveUsersRequest):
    try:
        team_base.remove_users_from_team(team_id, users)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/teams/{team_id}/users", response_model=List[UsersInTeamListResponse])
async def list_team_users(team_id: int):
    try:
        return team_base.list_team_users(team_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
