from datetime import datetime

from pydantic import BaseModel


class SolutionCreateSchema(BaseModel):
    language_id: int
    code: str


class SolutionSchema(SolutionCreateSchema):
    status: str
    test_number: int
    date_of_create: datetime
