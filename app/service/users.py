
from fastapi import HTTPException
from app.repository import users as users_repository
from app.schemas import UserResponse
from sqlalchemy.orm import Session

  
    

def create_user(db:Session, login: str) -> UserResponse:
    if users_repository.get_user(db, login): 
        raise HTTPException(
          status_code=400,
          detail=f"User already exist"
        )
    
    user = users_repository.create_user(db, login)
    db.commit()
    return UserResponse.model_validate(user)