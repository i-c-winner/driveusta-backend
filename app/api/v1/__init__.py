from fastapi import APIRouter
from . import cars

router = APIRouter()
router.include_router(cars.router, prefix="/v1")