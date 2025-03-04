import ast
from time import time

from tasks.models import TaskModel
from test_system.runners.code_runner import CodeRunner
from test_system.exceptions import *
from test_system.schemas import LanguageSchema


class PyRunner(CodeRunner):
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
        self.main_file_extension = "py"

    def analyze_code(self):
        tree = ast.parse(self.solution_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.FORBIDDEN_MODULES:
                        raise CompileError(f"Disabled import '{alias.name}'")
            elif isinstance(node, ast.ImportFrom):
                if node.module in self.FORBIDDEN_MODULES:
                    raise CompileError(f"Disabled import '{node.module}'")

    def run_test(self, test_number: int) -> str:
        test_file_name = f"input{test_number}"
        test_file_path = f"{self.TESTS_PATH}/{test_file_name}"

        start_time = time()
        exit_code, output = self.container.exec_run(
            f'bash -c "cat {test_file_path} | python3 {self._get_main_file_path()}"'
        )
        end_time = time()
        runtime_time = end_time - start_time
        print(f"RunTime: {runtime_time}")
        if runtime_time > self.task.time:
            raise TimeLimitException()

        if exit_code != 0:
            raise RunTimeException(output)
        return output.decode().strip(" ").strip("\n")
