from fastapi import APIRouter

router = APIRouter()

@router.get("/is-alive", status_code=200)
async def is_alive():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "OK"}