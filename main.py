import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi.openapi.utils import get_openapi

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="API for managing contacts with user authentication",
        routes=app.routes,
    )
    

    for path, path_item in openapi_schema["paths"].items():
        if path == "/api/v1/auth/token":
            if "post" in path_item:

                path_item["post"]["requestBody"] = {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["email", "password"],
                                "properties": {
                                    "email": {
                                        "type": "string",
                                        "format": "email",
                                        "example": "user@example.com"
                                    },
                                    "password": {
                                        "type": "string",
                                        "format": "password",
                                        "example": "securepassword"
                                    }
                                }
                            }
                        }
                    }
                }
    

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    

    for path, path_item in openapi_schema["paths"].items():
        if path != "/api/v1/auth/token" and path != "/api/v1/auth/register" and path != "/api/v1/auth/verify/{user_id}/{verification_token}":
            for method in path_item:
                if method in ["get", "post", "put", "delete"]:
                    path_item[method]["security"] = [{"BearerAuth": []}]
                    

    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
async def startup():
    try:
        r = await redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(r)
        print("Rate limiting enabled with Redis")
    except redis.exceptions.ConnectionError:
        print("WARNING: Redis not available - rate limiting is disabled")

@app.get("/", response_class=RedirectResponse, status_code=302)
def read_root():
    return "/docs"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
