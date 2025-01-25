from fastapi import APIRouter, Depends, HTTPException
from app.core.config import get_db
from app.crud.board_crud import BoardRepository, get_board_repository
from app.schemas.board_schema import BoardCreate, BoardResponse, BoardUpdate
from fastapi_pagination import Page
from typing import List


router = APIRouter()

@router.post("/boards",response=BoardResponse)
def create_board(board:BoardCreate,current_user: UUID,board_repo:BoardRepository = Depends(get_board_repository)):
    return board_repo.create_board(board)



@router.get("/boards", response_model=Page[BoardResponse])
def get_all_boards(board_repo: BoardRepository = Depends(get_board_repository)):
    return board_repo.get_boards()


@router.get("/boards/{board_id}")
def get_board_by_id(board_repo:BoardRepository = Depends(get_board_repository)):
    board = board_repo.get_board_by_id(board_id)
    if not board:
        raise HTTPException(status_code = 404,detail="Board not found")
    return Board


@router.get("/boards/users/{user_id}")
def get_board_by_users(board_repo:BoardRepository = Depends(get_board_repository)):
    boards = board_repo.get_boards_by_user(user_id)
    if not boards:
        raise HTTPException(status_code=404, detail="No boards found for this user.")
    return boards


@router.put("/boards/{board_id}", response_model=BoardResponse)
def update_board(board_id: int, board_update: BoardUpdate, board_repo: BoardRepository = Depends(get_board_repository)):
    updated_board = board_repo.update_board(board_id, board_update)
    if not updated_board:
        raise HTTPException(status_code=404, detail="Board not found")
    return updated_board


@router.delete("/boards/{board_id}", response_model=dict)
def delete_board(board_id: int, board_repo: BoardRepository = Depends(get_board_repository)):
    success = board_repo.delete_board(board_id)
    if not success:
        raise HTTPException(status_code=404, detail="Board not found")
    return {"detail": "Board deleted successfully"}
