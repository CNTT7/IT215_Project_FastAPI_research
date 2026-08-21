from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.services import user_service
from app.core.security import verify_password, create_access_token, create_refresh_token

def authenticate_user(db: Session, email: str, password: str):
    """Xác thực người dùng khi Đăng nhập"""
    # 1. Gọi user_service để lấy thông tin
    user = user_service.get_user_by_email(db, email)
    
    # 2. Kiểm tra mật khẩu và trạng thái
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email hoặc mật khẩu không chính xác"
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản bị vô hiệu hóa")
        
    return user

def generate_tokens_for_user(email: str):
    """Nghiệp vụ sinh cặp Token (Access & Refresh)"""
    return {
        "access_token": create_access_token(data={"sub": email}),
        "refresh_token": create_refresh_token(data={"sub": email}),
        "token_type": "bearer"
    }