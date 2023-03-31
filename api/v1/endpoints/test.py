from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/api/v1/itsGrey/test")
async def hello_world():
    return Response("Your Request Has Arrived Successfully!")
