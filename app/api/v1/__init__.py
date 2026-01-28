from fastapi import APIRouter
from .robotyre import router as robotyre_router
from .avito import router as avito_router

v1_router = APIRouter()

v1_router.include_router(robotyre_router)
v1_router.include_router(avito_router)