from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
# python-jose dùng để tạo và giải mã JWT, passlib dùng để băm mật khẩu,
# slowapi dùng để giới hạn số lần request (Rate Limit)

# Khởi tạo công cụ băm mật khẩu bằng thuật toán chuẩn công nghiệp Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra xem mật khẩu người dùng nhập có khớp với mã băm trong DB không"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Băm mật khẩu (Tuyệt đối không lưu plain-text vào DB)"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Tạo Access Token (thẻ thông hành ngắn hạn)"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Tạo Refresh Token (dùng để xin cấp lại Access Token khi hết hạn, thường sống lâu hơn: ví dụ 7 ngày)"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)