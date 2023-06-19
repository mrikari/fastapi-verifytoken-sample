from fastapi import APIRouter

from routes import index, sample

router = APIRouter()

router.include_router(index.router)
router.include_router(sample.router)
