from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

# Enum quy định quyền hạn người dùng
class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users" # Tên bảng trong MySQL

    # Các cột dữ liệu
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Quan hệ (Relationships): Giúp query dữ liệu liên kết dễ dàng
    # back_populates phải khớp với tên biến quan hệ ở các model khác
    owned_projects = relationship("ResearchProject", back_populates="owner")
    tasks = relationship("ResearchTask", back_populates="assignee")
    project_memberships = relationship("ResearchMember", back_populates="user")