from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service, auth_service # Import cả 2 service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Đẩy xuống user_service xử lý việc tạo
    return user_service.create_user(db=db, user_in=user_in)

@router.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Nhờ auth_service xác thực
    user = auth_service.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    
    # 2. Nhờ auth_service tạo token
    tokens = auth_service.generate_tokens_for_user(email=user.email)
    return tokens