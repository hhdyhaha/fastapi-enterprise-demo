from typing import List, Optional
import os
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 尝试导入密钥管理服务，如果不可用则跳过
try:
    # 这里可以导入您选择的密钥管理服务的SDK
    # 例如: import boto3 for AWS Secrets Manager
    # 或者自定义的密钥获取模块
    HAS_SECRET_MANAGER = False  # 设置为True当实际引入了密钥管理服务
except ImportError:
    HAS_SECRET_MANAGER = False

def get_secret(secret_name: str, default_value: str = None) -> str:
    """从密钥管理服务或环境变量获取密钥"""
    # 优先从环境变量获取
    value = os.environ.get(secret_name)
    if value:
        return value
        
    # 如果有密钥管理服务，尝试获取
    if HAS_SECRET_MANAGER:
        try:
            # 实现从密钥管理服务获取密钥的逻辑
            # 例如: 
            # client = boto3.client('secretsmanager')
            # response = client.get_secret_value(SecretId=secret_name)
            # return response['SecretString']
            pass
        except Exception as e:
            logging.warning(f"从密钥管理服务获取密钥 {secret_name} 失败: {str(e)}")
    
    # 返回默认值或从.env文件获取的值
    return default_value

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI企业级Demo"
    DEBUG: bool = False
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 数据库配置 - 优先从密钥服务获取
    DATABASE_URL: str = None
    
    # JWT配置 - 优先从密钥服务获取
    SECRET_KEY: str = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 覆盖敏感配置，优先使用密钥管理服务
        self.DATABASE_URL = get_secret("DATABASE_URL", self.DATABASE_URL)
        self.SECRET_KEY = get_secret("SECRET_KEY", self.SECRET_KEY)


settings = Settings() 