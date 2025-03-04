from datetime import datetime

from pydantic import BaseModel

from test_system.schemas import LanguageEnum


class SolutionCreateSchema(BaseModel):
    language: LanguageEnum
    code: str


class SolutionSchema(SolutionCreateSchema):
    id: int
    status: str
    test_number: int
    date_of_create: datetime
