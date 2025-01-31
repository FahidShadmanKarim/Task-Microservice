import httpx
import uuid
import os
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

class UserService:
    def __init__(self):
        self.user_service_url = os.getenv("USER_SERVICE_URL")
        if not self.user_service_url:
            raise ValueError("USER_SERVICE_URL is not set in the environment variables")

    async def validate_user(self, user_id: uuid.UUID) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.user_service_url}/users/{user_id}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        
        return True

def get_user_service() -> UserService:
    return UserService()