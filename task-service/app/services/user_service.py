import httpx
from fastapi import HTTPException

class UserService:
    def __init__(self, user_service_url: str):
        self.user_service_url = user_service_url

    async def validate_user(self, user_id: uuid.UUID) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.user_service_url}/users/{user_id}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        
        return True
