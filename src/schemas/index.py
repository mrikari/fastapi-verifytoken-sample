from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    detail: str = Field("OK", title="ヘルスチェック内容")
