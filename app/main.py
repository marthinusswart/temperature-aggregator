import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router

# Create FastAPI application
app = FastAPI(
    title="Temperature Aggregator API",
    description="API for temperature data aggregation",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API router
app.include_router(api_v1_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that redirects to the API documentation.
    """
    return {"message": "Welcome to Temperature Aggregator API. Visit /docs for API documentation."}

# Run the application when this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)