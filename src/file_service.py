from tasks.schemas import TestSchema
from config import settings
import shutil


def create_test_files(task_id, task_tests: list[TestSchema]):
    task_path = settings.UPLOAD_PATH / str(task_id)
    task_path.mkdir(exist_ok=True)
    for index, test in enumerate(task_tests):
        with open(task_path / f"input{index + 1}", "w") as file:
            file.write(test.input)

        with open(task_path / f"output{index + 1}", "w") as file:
            file.write(test.output)


def clear_upload_folder():
    for item in settings.UPLOAD_PATH.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
