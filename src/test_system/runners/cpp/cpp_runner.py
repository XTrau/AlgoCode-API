from tasks.models import TaskModel
from test_system.exceptions import CompileError
from test_system.runners.code_runner import CodeRunner
from test_system.schemas import LanguageSchema


class CppRunner(CodeRunner):
    FORBIDDEN_LIBRARIES = []

    def __init__(
        self, solution_code: str, language_schema: LanguageSchema, task_model: TaskModel
    ):
        super().__init__(solution_code, language_schema, task_model)
        self.code_run_str = ""
        self.main_file_extension = "cpp"
        self.run_file_extension = "exe"

    def analyze_code(self):
        pass

    def compile_code(self) -> None:
        exit_code, output = self.container.exec_run(
            f'bash -c "g++ {self._get_main_file_path()} -o {self._get_main_runfile_path()}"'
        )
        if exit_code != 0:
            raise CompileError(output.decode())
