import enum
from datetime import datetime

from pydantic import BaseModel


class LanguageEnum(enum.Enum):
    PYTHON = "python"


class LanguageSchema(BaseModel):
    title: str
    docker_image_name: str
    compiled: bool


class LanguageResponseSchema(BaseModel):
    title: str
    mark: str


class SolutionCreateSchema(BaseModel):
    language: LanguageEnum
    code: str


class SolutionSchema(SolutionCreateSchema):
    id: int
    status: str
    test_number: int
    date_of_create: datetime
