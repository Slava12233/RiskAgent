"""
Main entry point for the Risk Engine application.
"""

import uvicorn
import logging
from fastapi import FastAPI

from app.routes import router
from app.database import engine
from app.models import Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Risk Engine API",
    description="API for evaluating business risks",
    version="0.1.0",
)

# Include API routes
app.include_router(router)

# Add a root redirect to API docs
@app.get("/", include_in_schema=False)
async def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    logger.info("Starting Risk Engine API")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 