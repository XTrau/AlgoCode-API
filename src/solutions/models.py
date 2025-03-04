import enum
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from repository import GenericAsyncRepository, GenericSyncRepository
from test_system.schemas import LanguageEnum


class SolutionStatus(enum.Enum):
    WAITING = "Ожидание"
    COMPILING = "Компилируется"
    RUNNING = "Выполняется"
    ACCEPTED = "Полное решение"
    WRONG_ANSWER = "Неправильный ответ"
    RUNTIME_ERROR = "Ошибка исполнения"
    COMPILE_ERROR = "Ошибка компиляции"
    TIME_LIMIT = "Превышение лимита времени"
    MEMORY_LIMIT = "Превышение лимита памяти"


class SolutionModel(Base):
    __tablename__ = "solutions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(nullable=False)
    date_of_create: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=func.now(),
    )
    test_number: Mapped[int] = mapped_column(nullable=False, default=1)
    status: Mapped[ENUM] = mapped_column(
        ENUM(SolutionStatus, name="solution_status_enum"),
        nullable=False,
        default=SolutionStatus.WAITING,
    )
    language: Mapped[ENUM] = mapped_column(
        ENUM(LanguageEnum, name="solution_language_enum"), nullable=False
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


solutions_async_repo = GenericAsyncRepository(SolutionModel)
solutions_sync_repo = GenericSyncRepository(SolutionModel)
