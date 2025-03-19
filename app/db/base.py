# 导入所有模型，以便Alembic可以检测到它们
from app.db.base_class import Base
from app.models.user import User
from app.models.item import Item 