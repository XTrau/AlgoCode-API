from fastapi import APIRouter, status

from test_system.config import test_system_config
from test_system.schemas import LanguageResponseSchema

test_system_router = APIRouter()


@test_system_router.get("/languages", status_code=status.HTTP_200_OK)
async def get_languages() -> list[LanguageResponseSchema]:
    languages: dict[str, dict] = test_system_config.languages_data
    return [
        LanguageResponseSchema(title=values["title"], mark=key)
        for key, values in languages.items()
    ]
