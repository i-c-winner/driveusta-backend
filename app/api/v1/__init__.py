from fastapi import APIRouter
from . import cars, participants, addresses

router = APIRouter()
router.include_router(cars.router, prefix="/v1")
router.include_router(participants.router, prefix="/v1")
router.include_router(addresses.router, prefix="/v1")