from fastapi.params import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    count: int


async def get_pagination(page: int = Query(gt=0), count: int = Query(gt=0)):
    return Pagination(page=page, count=count)
