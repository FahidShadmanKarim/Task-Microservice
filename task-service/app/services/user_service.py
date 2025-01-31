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
        print(f"User service URL: {self.user_service_url}")

    async def validate_user(self, user_id: uuid.UUID) -> bool:
        print(f"Validating user with ID: {user_id}")  # Print user ID
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.user_service_url}/users/{user_id}/exists")
                print(f"User validation response: {response.status_code}")  # Print response status
                
                if response.status_code != 200:
                    raise HTTPException(status_code=404, detail="User not found")
                
                print(f"Response data: {response.json()}")  # Print response data if available

            except httpx.RequestError as e:
                print(f"Error occurred: {e}")  # Print any error
                raise HTTPException(status_code=500, detail="User service validation failed")
    
            return True

def get_user_service() -> UserService:
    return UserService()
