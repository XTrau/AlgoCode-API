from tasks.models import TaskModel
from test_system.exceptions import CompileError
from test_system.runners.code_runner import CodeRunner
from test_system.runners.python.py_runner import PyRunner
from test_system.schemas import LanguageEnum, LanguageSchema
from test_system.config import test_system_config


class CodeRunnerFactory:
    code_runner_classes: dict[str, type[CodeRunner]] = {"python": PyRunner}

    def get_code_runner(
        self, code: str, language: LanguageEnum, task_model: TaskModel
    ) -> CodeRunner:
        language_schema: LanguageSchema = test_system_config.get_lang_scheme(language)
        code_runner_cls = self.code_runner_classes.get(language.value)
        if code_runner_cls is None:
            raise CompileError()
        code_runner: CodeRunner = code_runner_cls(code, language_schema, task_model)
        return code_runner


code_runner_factory = CodeRunnerFactory()
