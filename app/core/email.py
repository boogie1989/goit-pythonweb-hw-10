import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from jose import jwt
from datetime import timedelta, datetime

from app.core.config import settings
from app.auth.security import SECRET_KEY, ALGORITHM

DEFAULT_EMAIL = "noreply@example.com"

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME or "",
    MAIL_PASSWORD=settings.MAIL_PASSWORD or "",
    MAIL_FROM=settings.MAIL_FROM or DEFAULT_EMAIL,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=bool(settings.MAIL_USERNAME and settings.MAIL_PASSWORD),
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates"
)


async def send_verification_email(email: EmailStr, user_id: int):
    expiration = datetime.utcnow() + timedelta(hours=48)
    token_data = {
        "sub": str(user_id),
        "exp": expiration.timestamp()
    }
    verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    verification_link = f"http://localhost:8000/api/v1/auth/verify/{user_id}/{verification_token}"
    
    fm = FastMail(conf)
    
    message = MessageSchema(
        subject="Verify your email address",
        recipients=[email],
        template_body={
            "username": email.split('@')[0],  # Use first part of email as name
            "verification_link": verification_link
        },
        subtype=MessageType.html
    )
    
    await fm.send_message(message, template_name="verification.html")
