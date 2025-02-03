import enum
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from repository import GenericRepository


class LanguageModel(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)

    compiled: Mapped[bool] = mapped_column(nullable=False)
    compile: Mapped[str] = mapped_column(nullable=True)
    run: Mapped[str] = mapped_column(nullable=False)
    extension: Mapped[str] = mapped_column(nullable=False)


class SolutionStatus(enum.Enum):
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
        default=datetime.utcnow,
    )
    test_number: Mapped[int] = mapped_column(nullable=False, default=1)
    status: Mapped[ENUM] = mapped_column(
        ENUM(SolutionStatus, name="solution_status_enum"),
        nullable=False,
        default=SolutionStatus.RUNNING,
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)


solutions_repo = GenericRepository(SolutionModel)
language_repo = GenericRepository(SolutionModel)
