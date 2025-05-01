"""Utility module for exceptions and API documentation helpers."""

from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class BaseHTTPException(HTTPException):
    """Base class for all custom HTTP exceptions."""
    
    def __init__(self, status_code: int, detail: str, headers: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the HTTP exception.
        
        Args:
            status_code: HTTP status code
            detail: Detailed error message
            headers: Optional HTTP headers to include in the response
        """
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class HTTPNotFoundException(BaseHTTPException):
    """Exception raised when a requested resource is not found."""
    
    def __init__(self, detail: str = "Resource not found") -> None:
        """
        Initialize a 404 Not Found exception.
        
        Args:
            detail: Detailed error message (default: "Resource not found")
        """
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class HTTPConflictException(BaseHTTPException):
    """Exception raised when there's a conflict with the current state of the resource."""
    
    def __init__(self, detail: str = "Conflict with existing resource") -> None:
        """
        Initialize a 409 Conflict exception.
        
        Args:
            detail: Detailed error message (default: "Conflict with existing resource")
        """
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class HTTPUnprocessableEntityException(BaseHTTPException):
    """Exception raised when the server understands the content but cannot process it."""
    
    def __init__(self, detail: str = "Unprocessable entity") -> None:
        """
        Initialize a 422 Unprocessable Entity exception.
        
        Args:
            detail: Detailed error message (default: "Unprocessable entity")
        """
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class HTTPUnauthorizedException(BaseHTTPException):
    """Exception raised when authentication is required but not provided or invalid."""
    
    def __init__(self, detail: str = "Not authenticated") -> None:
        """
        Initialize a 401 Unauthorized exception.
        
        Args:
            detail: Detailed error message (default: "Not authenticated")
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class HTTPForbiddenException(BaseHTTPException):
    """Exception raised when the client does not have access rights to the content."""
    
    def __init__(self, detail: str = "Access forbidden") -> None:
        """
        Initialize a 403 Forbidden exception.
        
        Args:
            detail: Detailed error message (default: "Access forbidden")
        """
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestModel(BaseModel):
    detail: str
    status_code: int = 400


class NotFoundModel(BaseModel):
    detail: str
    status_code: int = 404


# Standard API documentation for common error responses
bad_request_response_docs = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid input data"},
            }
        },
    }
}

unauthorized_response_docs = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {"detail": "Not authenticated"},
            }
        },
    }
}

forbidden_response_docs = {
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Access forbidden"},
            }
        },
    }
}

not_found_response_docs = {
    404: {
        "model": NotFoundModel,
        "description": "Not found",
    },
}

conflict_response_docs = {
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {
                "example": {"detail": "Resource already exists"},
            }
        },
    }
}

unprocessable_entity_response_docs = {
    422: {
        "description": "Unprocessable Entity",
        "content": {
            "application/json": {
                "example": {"detail": "Validation error"},
            }
        },
    }
}
