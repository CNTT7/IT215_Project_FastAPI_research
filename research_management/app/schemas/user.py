from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.user import UserRole

# 1. Base Schema: Chứa các thuộc tính chung nhất
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: Optional[bool] = True

# 2. Create Schema: Dùng khi người dùng gửi Request tạo tài khoản
class UserCreate(UserBase):
    password: str

# 3. Response Schema: Dùng để trả dữ liệu cho Frontend (Ẩn password đi)
class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    # Bật tính năng chuyển đổi từ SQLAlchemy model sang Pydantic schema
    model_config = ConfigDict(from_attributes=True)