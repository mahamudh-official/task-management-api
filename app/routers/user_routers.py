from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create(user)

@router.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.login(user)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
    
