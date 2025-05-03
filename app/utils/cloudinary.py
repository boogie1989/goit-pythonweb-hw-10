import io
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from slugify import slugify
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


async def upload_image(file: UploadFile, public_id_prefix: str) -> str:
    contents = await file.read()
    
    filename = file.filename.split(".")[0]
    public_id = f"{public_id_prefix}_{slugify(filename)}"
    
    result = cloudinary.uploader.upload(
        io.BytesIO(contents),
        public_id=public_id,
        folder="contacts_app",
        overwrite=True
    )
    
    return result["secure_url"]
