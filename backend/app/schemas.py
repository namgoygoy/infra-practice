from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MemoBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""


class MemoCreate(MemoBase):
    pass


class MemoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = None


class MemoResponse(MemoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
