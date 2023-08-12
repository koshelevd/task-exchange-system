from fastapi import APIRouter

from controllers.routers.v1.healthcheck import router as healthcheck_router
from controllers.routers.v1.user.user_routers import router as user_router

router = APIRouter(prefix="/api/v1")

router.include_router(healthcheck_router)
router.include_router(user_router)
