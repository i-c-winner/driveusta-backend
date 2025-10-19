from fastapi import APIRouter
from . import cars, participants, addresses, available_cars, photos, streets, type_work_children, type_work_parents, work_shop
from .calendar import holidays, working_hours
from .auth import register

router = APIRouter()
router.include_router(cars.router, prefix="/v1")
router.include_router(participants.router, prefix="/v1")
router.include_router(addresses.router, prefix="/v1")
router.include_router(available_cars.router, prefix="/v1")
router.include_router(photos.router, prefix="/v1")
router.include_router(streets.router, prefix="/v1")
router.include_router(type_work_children.router, prefix="/v1")
router.include_router(type_work_parents.router, prefix="/v1")
router.include_router(work_shop.router, prefix="/v1")
router.include_router(holidays.router, prefix="/v1")
router.include_router(working_hours.router, prefix="/v1")
router.include_router(register.router, prefix="/v1")