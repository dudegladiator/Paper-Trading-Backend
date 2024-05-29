from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import uvicorn
from routes import dashboard_routes, extension_routes, health_routes

class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_PORT: str
    LOG_KEY: str

    class Config:
        env_file = ".env"

app = FastAPI()
setting = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the extension routes
app.include_router(extension_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(health_routes.router)

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": "The requested resource was not found"}
    )
    



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
