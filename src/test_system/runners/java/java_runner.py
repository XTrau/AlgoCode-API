from tasks.models import TaskModel
from test_system.exceptions import TimeLimitException, RunTimeException
from test_system.runners.code_runner import CodeRunner
from test_system.runners.utils import get_output_and_runtime
from test_system.schemas import LanguageSchema


class JavaRunner(CodeRunner):
    FORBIDDEN_MODULES = {
        "os",
        "sys",
        "subprocess",
        "shutil",
        "importlib",
        "multiprocessing",
        "signal",
    }

    def __init__(
        self, solution_code: str, language_schema: LanguageSchema, task_model: TaskModel
    ):
        super().__init__(solution_code, language_schema, task_model)
        self.code_run_str = "java"
        self.main_file_extension = "java"
        self.run_file_extension = "java"

    def analyze_code(self):
        pass

    def compile_code(self) -> None:
        pass
