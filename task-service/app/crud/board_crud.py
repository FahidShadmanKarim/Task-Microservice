import httpx
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.board_model import Board
from app.models.board_members import BoardMembers
from app.schemas.board_schema import BoardCreate, BoardUpdate, BoardResponse
from app.core.config import get_db
from datetime import datetime
from typing import Optional, List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from uuid import UUID
from app.services.user_service import UserService,get_user_service

class BoardRepository:

    def __init__(self, db: AsyncSession,user_service:UserService):
        self.db = db
        self.user_service = user_service
    
    async def create_board(self, board: BoardCreate) -> BoardResponse:
        
        exists = await self.user_service.validate_user(board.created_by)
      
        if not exists:
            raise HTTPException(status_code=404, detail="User does not exist")

       
        new_board = Board(
            name=board.name,
            description=board.description,
            created_by=board.created_by,
           
        )

        self.db.add(new_board)
        await self.db.commit() 
        await self.db.refresh(new_board) 
        return BoardResponse.from_orm(new_board)
    
    async def add_user_to_board(self, board_id: UUID, user_id: UUID, role: str = "MEMBER") -> BoardResponse:


        exists = await self.user_service.validate_user(user_id)

        existing_member = await self.db.execute(select(BoardMembers).filter(
            BoardMembers.board_id == board_id,
            BoardMembers.user_id == user_id
        ))

        existing_member = existing_member.scalar_one_or_none() 

        if existing_member:
            raise HTTPException(status_code=400, detail="User is already a member of the board")

        board_member = BoardMembers(board_id=board_id, user_id=user_id, role=role)
        self.db.add(board_member)
        await self.db.commit()

        return {"message": "User added to board successfully"}

    async def update_board(self, board_id: int, board_update: BoardUpdate) -> Optional[BoardResponse]:

        result = await self.db.execute(select(Board).filter(Board.id == board_id))
        board = result.scalar_one_or_none() 
        if not board:
            return None

        update_data = board_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(board, key, value)

        board.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(board)
        return BoardResponse.from_orm(board)

    async def get_board_by_id(self, board_id: int) -> Optional[BoardResponse]:
        result = await self.db.execute(select(Board).filter(Board.id == board_id))
        board = result.scalar_one_or_none() 
        return BoardResponse.from_orm(board) if board else None

    async def get_boards(self) -> Page[BoardResponse]:
        query = select(Board)
        result = await self.db.execute(query)
        boards = result.scalars().all()  
        return paginate(boards) 

    async def get_boards_by_user(self, user_id: UUID) -> List[BoardResponse]:
        result = await self.db.execute(select(Board).filter(Board.created_by == user_id))
        boards = result.scalars().all()
        return [BoardResponse.from_orm(board) for board in boards]

    async def delete_board(self, board_id: int) -> bool:
        result = await self.db.execute(select(Board).filter(Board.id == board_id))
        board = result.scalar_one_or_none() 
        if not board:
            return False
        await self.db.delete(board) 
        await self.db.commit() 
        return True

def get_board_repository(
    db: AsyncSession = Depends(get_db), 
    user_service: UserService = Depends(get_user_service)
) -> BoardRepository:
    return BoardRepository(db, user_service)
