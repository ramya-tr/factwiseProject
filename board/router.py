from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import PositiveInt
from fastapi.responses import FileResponse

from .controller import ProjectBoardBase
from .schema import (
    BoardBase,
    BoardResponse,
    TaskBase,
    TaskStatusUpdate,
    BoardList,
    TaskList,

)

router = APIRouter(
    prefix="/board",
    tags=["board"]
)

board_base = ProjectBoardBase()


@router.post("/create", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(request: BoardBase):
    try:
        board_id = board_base.create_board(request)
        return BoardResponse(id=board_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/close/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def close_board(board_id: PositiveInt):
    try:
        response = board_base.close_board(board_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/add_task", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def add_task(request: TaskBase):
    try:
        task_id = board_base.add_task(request)
        return BoardResponse(id=task_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/update_task_status/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task_status(task_id: PositiveInt, request: TaskStatusUpdate):
    try:
        board_base.update_task_status(task_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/team/{team_id}", response_model=List[BoardList])
async def list_boards_of_a_team(team_id: PositiveInt):
    try:
        return board_base.list_boards_of_a_team(team_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/tasks/{board_id}", response_model=List[TaskList])
async def list_tasks_in_board(board_id: PositiveInt):
    try:
        return board_base.list_tasks_in_board(board_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[BoardList])
async def list_boards():
    try:
        return board_base.list_boards()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/export_board", response_class=FileResponse(
        path="",
        filename="",
        media_type="text/plain"
    ) )
async def export_board():
    try:
        export_file_path = board_base.export_board()
        return FileResponse(export_file_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
