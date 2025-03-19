from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logger import logger

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
)

# 设置CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", include_in_schema=False)
def root():
    """
    重定向到API文档
    """
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    """
    应用启动时的事件
    """
    logger.info("应用程序启动")


@app.on_event("shutdown")
async def shutdown_event():
    """
    应用关闭时的事件
    """
    logger.info("应用程序关闭") 