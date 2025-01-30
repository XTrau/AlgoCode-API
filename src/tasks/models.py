from datetime import datetime

from sqlalchemy import Text, JSON, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    time: Mapped[float] = mapped_column(nullable=False)
    memory: Mapped[int] = mapped_column(nullable=False)
    example_tests: Mapped[list] = mapped_column(JSON, nullable=False)


class LanguageModel(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


class TestModel(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    number: Mapped[int] = mapped_column(nullable=False)


class SolutionModel(Base):
    __tablename__ = "solutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False)
    date_of_create: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    success_status: Mapped[bool] = mapped_column(nullable=False, default=False)

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    language_id: Mapped[int] = mapped_column(
        ForeignKey("languages.id"), primary_key=True, nullable=False
    )
