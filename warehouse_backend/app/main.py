"""
Warehouse Scanner Backend API
FastAPI application with Odoo 15 integration
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from app.config import settings
from app.routers import auth, warehouse

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Warehouse Scanner API",
    description="Backend API for warehouse scanner mobile application with Odoo 15 integration",
    version="1.0.0",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json"
)

# CORS middleware - configure for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Log
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration:.3f}s"
    )

    return response


# Include routers
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(warehouse.router, prefix=settings.api_prefix)


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Warehouse Scanner API",
        "version": "1.0.0",
        "docs": f"{settings.api_prefix}/docs",
        "status": "running"
    }


# Health check endpoint
@app.get(f"{settings.api_prefix}/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Odoo connection
        from app.services.odoo_client import get_odoo_client
        odoo = get_odoo_client()
        odoo_status = "connected" if odoo.uid else "disconnected"
    except Exception as e:
        logger.error(f"Health check - Odoo connection error: {e}")
        odoo_status = "error"

    return {
        "status": "healthy",
        "odoo_connection": odoo_status,
        "version": "1.0.0"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "path": str(request.url.path)
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting Warehouse Scanner API")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Odoo URL: {settings.odoo_url}")
    logger.info(f"Odoo DB: {settings.odoo_db}")

    # Test Odoo connection
    try:
        from app.services.odoo_client import get_odoo_client
        odoo = get_odoo_client()
        logger.info(f"Successfully connected to Odoo as user ID: {odoo.uid}")
    except Exception as e:
        logger.error(f"Failed to connect to Odoo: {e}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down Warehouse Scanner API")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
