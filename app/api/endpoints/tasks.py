from fastapi import APIRouter, status


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", status_code=status.HTTP_200_OK,)
async def index():
    return {"status": "fastapi task_manager service is running."}