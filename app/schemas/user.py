from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from app.schemas.item import Item

# 共享属性的基础User模型
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None


# 创建用户时需要的属性
class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=8)


# 更新用户时可以更新的属性
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


# 从数据库读取用户时的模型
class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 返回给API的用户模型（不包含密码）
class User(UserInDBBase):
    pass


# 数据库中存储的用户模型（包含哈希密码）
class UserInDB(UserInDBBase):
    hashed_password: str


# 包含用户拥有物品的用户详情
class UserWithItems(User):
    items: List[Item] = [] 