from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user, get_current_admin
from app.services import user_service

router = APIRouter()

# 1. API Lấy thông tin cá nhân (Cần đăng nhập - Token hợp lệ)
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Trả về thông tin của user đang đăng nhập.
    Nhờ có hàm Depends(get_current_user), FastAPI đã tự động giải mã Token
    và lấy sẵn object User từ DB lên cho chúng ta.
    """
    return current_user 

# 2. API Lấy danh sách toàn bộ Users (Chỉ ADMIN mới có quyền truy cập)
@router.get("/", response_model=List[UserResponse])
def get_all_users(
    name: Optional[str] = Query(None, description="Tìm theo tên gần đúng"),
    email: Optional[str] = Query(None, description="Tìm theo email gần đúng"),
    is_active: Optional[bool] = Query(None, description="Lọc theo trạng thái hoạt động"),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin) # Bức tường bảo vệ: Chặn user thường
):
    """
    Lấy danh sách người dùng. Có hỗ trợ lọc theo tên, email, trạng thái.
    """
    # Đẩy toàn bộ công việc truy vấn và lọc dữ liệu xuống tầng Service
    users = user_service.get_all_users(
        db=db, 
        name=name, 
        email=email, 
        is_active=is_active
    )
    return users