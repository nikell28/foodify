import uuid
import datetime
import pydantic


class OrmBaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


class BaseModel(OrmBaseModel):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
