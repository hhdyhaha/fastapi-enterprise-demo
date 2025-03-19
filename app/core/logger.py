import sys
import logging
from loguru import logger
from pathlib import Path
from app.core.config import settings

# 日志文件路径
LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_FOLDER / "app.log"

# 配置日志器
logger.remove()  # 移除默认处理器
logger.add(
    LOG_FILE,
    rotation="10 MB",  # 日志文件达到10MB时轮转
    retention="7 days",  # 保留7天的日志
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    encoding="utf-8",
)
logger.add(
    sys.stderr,
    level="DEBUG" if settings.DEBUG else "INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# 将标准logging库设置为使用loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 获取对应的Loguru级别
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 找到调用者
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# 配置所有标准库logger使用我们的拦截器
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# 替换所有已存在的logger处理器
for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers = [InterceptHandler()] 