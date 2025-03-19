from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.logger import logger

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取所有物品
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新物品
    """
    try:
        item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
        logger.info(f"用户 {current_user.email} 创建了新物品: {item.title}")
        return item
    except Exception as e:
        logger.error(f"创建物品失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建物品时发生错误")


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., title="物品ID", ge=1),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过ID获取物品
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        logger.warning(f"物品不存在: {id}")
        raise HTTPException(status_code=404, detail="物品不存在")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        logger.warning(f"用户 {current_user.email} 尝试访问不属于他的物品 {id}")
        raise HTTPException(status_code=400, detail="权限不足")
    return item


@router.put("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., title="物品ID", ge=1),
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新物品
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="权限不足")
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    logger.info(f"用户 {current_user.email} 更新了物品: {item.title}")
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Path(..., title="物品ID", ge=1),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    删除物品
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="权限不足")
    item = crud.item.remove(db=db, id=id)
    logger.info(f"用户 {current_user.email} 删除了物品: {item.title}")
    return item 