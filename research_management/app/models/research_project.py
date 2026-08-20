from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

class MemberRole(str, enum.Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"

class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Khóa ngoại trỏ về bảng users
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="owned_projects")
    tasks = relationship("ResearchTask", back_populates="project")
    members = relationship("ResearchMember", back_populates="project")


class ResearchMember(Base):
    __tablename__ = "research_members"

    # Đây là bảng trung gian (n-n), dùng Khóa chính kép (Composite Primary Key)
    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(SQLEnum(MemberRole), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    project = relationship("ResearchProject", back_populates="members")
    user = relationship("User", back_populates="project_memberships")