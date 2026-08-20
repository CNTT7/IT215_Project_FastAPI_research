from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.models.research_project import ResearchProject, ResearchMember, MemberRole
from app.models.research_task import ResearchTask, TaskStatus, TaskPriority
import datetime

def seed_data():
    db = SessionLocal() # Mở kết nối
    try:
        print("Bắt đầu khởi tạo dữ liệu mẫu...")
        
        # 1. Tạo 2 User
        user1 = User(email="truong@it.edu.vn", password_hash="hash123", full_name="Nguyễn Trường", role=UserRole.ADMIN)
        user2 = User(email="sinhvien@it.edu.vn", password_hash="hash123", full_name="Lê Sinh Viên", role=UserRole.USER)
        db.add_all([user1, user2])
        db.commit() # Lưu vào DB

        # 2. Tạo Đề tài
        project1 = ResearchProject(
            name="Xây dựng API Quản lý đề tài",
            description="Đồ án môn học FastAPI",
            owner_id=user1.id
        )
        db.add(project1)
        db.commit()

        # 3. Tạo Nhiệm vụ
        task1 = ResearchTask(
            project_id=project1.id,
            title="Khởi tạo database",
            assignee_id=user1.id,
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH
        )
        db.add(task1)
        db.commit()

        print("✅ Hoàn tất tạo dữ liệu!")
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")
        db.rollback() # Hoàn tác nếu lỗi
    finally:
        db.close() # Nhớ luôn luôn đóng kết nối

if __name__ == "__main__":
    seed_data()