from pydantic import BaseModel, Field


class TestSchema(BaseModel):
    input: str
    output: str


class TaskCreateSchema(BaseModel):
    title: str
    text: str
    input_format: str
    time: float = Field(gt=0)
    memory: int = Field(gt=0)
    example_tests: list[TestSchema] = Field(min_length=1)


class TaskInDBSchema(TaskCreateSchema):
    id: int
