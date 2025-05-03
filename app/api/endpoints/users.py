from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserResponse
from app.crud.user import update_user_avatar
from app.auth.security import get_current_user, get_current_active_verified_user
from app.models.user import User
from app.utils.cloudinary import upload_image

router = APIRouter()

try:
    rate_limit = [Depends(RateLimiter(times=10, seconds=60))]
except:
    rate_limit = []

@router.get("/me", response_model=UserResponse, dependencies=rate_limit)
async def read_users_me(current_user: User = Depends(get_current_active_verified_user)):
    return current_user


@router.post("/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        avatar_url = await upload_image(file, f"user_{current_user.id}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    return update_user_avatar(db, current_user.id, avatar_url)
