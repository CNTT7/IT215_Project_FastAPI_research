from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    """Tìm user theo email (Dùng chung cho nhiều nơi)"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    """Nghiệp vụ tạo người dùng mới"""
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email đã được đăng ký.")
    
    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=get_password_hash(user_in.password) # Băm mật khẩu
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session, name: str = None, email: str = None, is_active: bool = None):
    """Nghiệp vụ lọc và tìm kiếm người dùng (Dành cho Admin)"""
    query = db.query(User)
    if name:
        query = query.filter(User.full_name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()