from fastapi import APIRouter, Depends

from security.auth import verify_token

router = APIRouter(prefix="/sample", tags=["Sample"])


@router.get("/")
def sample_get():
    return {"detail": "パブリックな内容を返却します。"}


@router.get("/me")
def sample_get_private(_=Depends(verify_token)):
    return {"detail": "認証済みのユーザーです。"}
