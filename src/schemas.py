from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    count: int
