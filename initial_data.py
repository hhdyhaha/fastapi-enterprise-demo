import logging

from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import SessionLocal
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """
    初始化数据库，创建超级用户
    """
    # 检查是否已有超级用户
    user = crud.user.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = schemas.UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="管理员",
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        logger.info(f"超级用户已创建: {user.email}")
    else:
        logger.info(f"超级用户已存在: {user.email}")


def main() -> None:
    """
    主函数
    """
    logger.info("正在创建初始数据")
    db = SessionLocal()
    init_db(db)
    logger.info("初始数据创建完成")


if __name__ == "__main__":
    main() 