from fastapi import APIRouter

from web.images.publish import publish_image_to_queue

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

@router.get("",)
async def get_users_info():
    data = {
        "first_param": 1,
        "second_param": 2
    }
    
    await publish_image_to_queue(data)