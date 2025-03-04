from sqlalchemy import Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from repository import GenericAsyncRepository, GenericSyncRepository


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    time: Mapped[float] = mapped_column(nullable=False)
    memory: Mapped[int] = mapped_column(nullable=False)
    example_tests: Mapped[list] = mapped_column(JSON, nullable=False)
    test_count: Mapped[int] = mapped_column(nullable=False)


task_async_repo = GenericAsyncRepository(TaskModel)
task_sync_repo = GenericSyncRepository(TaskModel)
