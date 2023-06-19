from fastapi import APIRouter

from schemas.index import HealthCheck

router = APIRouter(tags=["Maintenance"])


@router.get("/", response_model=HealthCheck)
def healthcheck():
    return HealthCheck()
