from tasks.models import TaskModel
from test_system.runners.code_runner import CodeRunner
from test_system.exceptions import *
from test_system.schemas import LanguageSchema

import re


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
        self.code_run_str = "python"
        self.main_file_extension = "py"
        self.run_file_extension = "py"
        self.re_modules = r"\s\*import\s+{lib}\s+|\s\*from\s+{lib}\s+import\s+"

    def analyze_code(self):
        for module in self.FORBIDDEN_MODULES:
            pattern = self.re_modules.format(lib=module)
            m = re.match(pattern, self.solution_code)
            if m is not None:
                raise CompileError(m)
