import json
from pathlib import Path

import docker
from docker import DockerClient

from config import settings
from test_system.exceptions import CompileError
from test_system.schemas import LanguageEnum, LanguageSchema

docker_client: DockerClient = docker.from_env()


class TestSystemSettings:
    HOST_TESTS_PATH = settings.UPLOAD_PATH
    languages_file_path = Path(__file__).parent / "languages.json"
    languages_data: dict[str, dict] = {}

    def __init__(self):
        with open(self.languages_file_path) as file_in:
            self.languages_data: dict[str, dict] = json.load(file_in)

    def get_lang_scheme(self, language: LanguageEnum) -> LanguageSchema:
        res = self.languages_data.get(language.value, None)
        if res is None:
            raise CompileError()
        return LanguageSchema.model_validate(res, from_attributes=True)


test_system_config = TestSystemSettings()
