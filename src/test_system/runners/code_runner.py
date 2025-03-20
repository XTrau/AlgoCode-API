from docker.models.containers import Container

from tasks.models import TaskModel
from test_system.exceptions import CompileError, TimeLimitException, RunTimeException
from test_system.runners.utils import get_output_and_runtime
from test_system.schemas import LanguageSchema

from test_system.config import docker_client, test_system_config


class CodeRunner:
    SOURCE_PATH = "/solution"
    TESTS_PATH = "/solution/tests"

    code_run_str = ""
    main_file_extension = ""
    run_file_extension = ""
    container: Container | bytes

    def __init__(
        self, solution_code: str, language_schema: LanguageSchema, task_model: TaskModel
    ):
        tests_path = str(test_system_config.HOST_TESTS_PATH / f"{task_model.id}")

        self.container: Container | bytes = docker_client.containers.run(
            language_schema.docker_image_name,
            cpu_count=1,
            mem_limit=f"{task_model.memory}m",
            stdin_open=True,
            network_disabled=True,
            detach=True,
            volumes={
                f"{tests_path}": {
                    "bind": self.TESTS_PATH,
                    "mode": "rw",
                }
            },
        )

        self.solution_code = solution_code
        self.language: LanguageSchema = language_schema
        self.task: TaskModel = task_model

    def _get_main_file_path(self):
        return f"{self.SOURCE_PATH}/main.{self.main_file_extension}"

    def _get_main_runfile_path(self):
        return f"{self.SOURCE_PATH}/main.{self.run_file_extension}"

    def create_file(self) -> None:
        exit_code, output = self.container.exec_run(
            f'bash -c "echo -e \\"{self.solution_code}\\" > {self._get_main_file_path()}"'
        )
        if exit_code != 0:
            raise CompileError(output)

    def analyze_code(self) -> None:
        pass

    def compile_code(self) -> None:
        pass

    def run_test(self, test_number: int) -> str:
        test_file_name = f"input{test_number}"
        test_file_path = f"{self.TESTS_PATH}/{test_file_name}"
        exit_code, output = self.container.exec_run(
            f'timeout {self.task.time + 0.5}s bash -c "time cat {test_file_path} | {self.code_run_str} {self._get_main_runfile_path()}"'
        )
        if exit_code == 124:
            raise TimeLimitException(self.task.time + 0.5)
        if exit_code != 0:
            raise RunTimeException(output.decode())
        output, runtime = get_output_and_runtime(output)
        if runtime > self.task.time:
            raise TimeLimitException(runtime)
        return output.strip(" ").strip("\n")

    def __del__(self):
        self.container.stop()
        self.container.remove()
