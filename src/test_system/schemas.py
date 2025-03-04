import enum

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
