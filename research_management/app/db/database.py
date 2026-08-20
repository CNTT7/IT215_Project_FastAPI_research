from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# 1. Khởi tạo Engine: "Động cơ" kết nối từ app của bạn tới MySQL
engine = create_engine(settings.DATABASE_URL)

# 2. Khởi tạo SessionLocal: Mỗi lần có request, ta sẽ tạo một phiên làm việc (session) từ đây
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Khởi tạo Base: Lớp cơ sở mà tất cả các file Model (bảng trong DB) sẽ kế thừa
Base = declarative_base()

# 4. Dependency get_db(): Hàm này cung cấp session cho các API
# Đặt ở đây để quản lý chung phần database, các file khác chỉ cần import để dùng
def get_db():
    db = SessionLocal() # Mở kết nối
    try:
        yield db        # Trả kết nối cho Router sử dụng
    finally:
        db.close()      # Luôn luôn đóng kết nối khi xử lý xong (tránh tràn RAM/Connection)