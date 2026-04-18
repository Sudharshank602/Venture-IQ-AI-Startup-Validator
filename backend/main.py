"""
FastAPI Application Entry Point
Production-grade ASGI app with middleware, CORS, and error handling.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from backend.api.routes import router
from backend.core.config import settings
from backend.core.logger import logger


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered startup validation and business intelligence platform.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request timing middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(round(time.time() - start, 4))
        return response

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "type": type(exc).__name__}
        )

    # Include routers
    app.include_router(router)

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
        logger.info(f"Environment: {settings.APP_ENV}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Application shutting down...")

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info",
    )
