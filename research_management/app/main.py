from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import auth, users 
from app.db.database import engine, Base
# Import toàn bộ model để SQLAlchemy nhận diện và tạo bảng
from app.models import user, research_project, research_task 

# Tự động tạo các bảng trong DB nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Research Management API",
    description="Hệ thống quản lý đề tài nghiên cứu cho sinh viên IT",
    version="1.0.0"
)

# Xử lý ngoại lệ (Exception Handling) chung cho toàn hệ thống (Trả về JSON format chuẩn)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": True, 
            "message": "Dữ liệu gửi lên không đúng định dạng", 
            "details": exc.errors()
        }
    )

# API Health-check: Kiểm tra server có sống không
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "success", "message": "API đang hoạt động tốt!"}


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])