from fastapi.params import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    count: int


async def get_pagination(page: int = Query(ge=0), count: int = Query(ge=0)):
    return Pagination(page=page, count=count)
