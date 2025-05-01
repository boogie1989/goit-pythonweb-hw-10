"""Email service for sending verification emails.

This module provides functionality for sending verification emails to users.
"""

import logging
from pathlib import Path
from typing import Optional

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import SecretStr

from src.services.auth import create_email_verification_token
from src.conf.config import settings

# Configure logging
logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=SecretStr(settings.MAIL_PASSWORD),
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
)


async def send_email(email: str, username: str, host: str) -> bool:
    """Send a verification email to a user.
    
    Args:
        email: The recipient's email address
        username: The recipient's username
        host: The base URL of the application
        
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    try:
        # Create verification token with user's email as subject
        token = create_email_verification_token(payload={"sub": email})
        
        # Create message schema
        message = MessageSchema(
            subject="Verify your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token,
            },
            subtype=MessageType.html,
        )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message, template_name="verification_email.html")
        logger.info(f"Verification email sent to {email}")
        return True
        
    except ConnectionErrors as e:
        logger.error(f"Failed to send verification email to {email}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending verification email to {email}: {str(e)}")
        return False
