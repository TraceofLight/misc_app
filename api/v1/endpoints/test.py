from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/api/v1/test")
async def hello_world():
    return Response("hello, world")
