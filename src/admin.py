from sqladmin import Admin

from admin.admin_models import UserAdmin, TaskAdmin
from database import async_engine
from main import app

admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
