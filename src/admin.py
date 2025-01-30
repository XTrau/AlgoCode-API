from sqladmin import ModelView

from auth.models import UserModel
from tasks.models import TaskModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.username,
        UserModel.email,
    ]


class TaskAdmin(ModelView, model=TaskModel):
    column_list = [
        TaskModel.id,
        TaskModel.title,
    ]
