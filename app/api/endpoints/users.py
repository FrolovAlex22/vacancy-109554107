from fastapi import APIRouter, status


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", status_code=status.HTTP_200_OK,)
async def index():
    return {"status": "fastapi task_manager service is running."}