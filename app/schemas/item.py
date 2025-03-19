from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# 共享的物品属性基础模型
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    is_active: Optional[bool] = True


# 创建物品时需要的属性
class ItemCreate(ItemBase):
    title: str
    price: int = Field(..., ge=0)  # 确保价格大于等于0


# 更新物品时可以更新的属性
class ItemUpdate(ItemBase):
    pass


# 从数据库读取物品时的模型
class ItemInDBBase(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 返回给API的物品模型
class Item(ItemInDBBase):
    pass


# 数据库中存储的物品模型
class ItemInDB(ItemInDBBase):
    pass 