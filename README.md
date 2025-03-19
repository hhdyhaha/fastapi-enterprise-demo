# FastAPI 企业级 Demo

这是一个基于 FastAPI 的企业级 CRUD API 示例项目，展示了完整的用户认证、权限控制、数据库交互等功能。

## 功能特性

- 完整的用户认证 (JWT)
- 基于角色的访问控制
- SQLAlchemy ORM 和 Pydantic 模型
- 完整的 CRUD 操作示例
- 日志记录
- 异常处理
- 数据库迁移 (Alembic)
- Docker 部署支持

## 项目结构

```
.
├── alembic/                # 数据库迁移
├── app/                    # 应用主目录
│   ├── api/                # API 路由
│   │   └── api_v1/         # API v1 版本
│   │       ├── endpoints/  # API 端点
│   │       └── api.py      # API 路由器
│   ├── core/               # 核心功能
│   │   ├── config.py       # 配置
│   │   ├── logger.py       # 日志
│   │   └── security.py     # 安全
│   ├── crud/               # CRUD 操作
│   ├── db/                 # 数据库
│   ├── models/             # 数据库模型
│   ├── schemas/            # Pydantic 模型
│   └── main.py             # 主应用入口
├── logs/                   # 日志文件夹
├── .env                    # 环境变量
├── alembic.ini             # Alembic 配置
├── docker-compose.yml      # Docker Compose 配置
├── Dockerfile              # Docker 配置
├── initial_data.py         # 初始数据
├── requirements.txt        # 依赖
└── run.py                  # 运行脚本
```

## 安装与运行

### 本地环境

1. 克隆仓库
2. 创建虚拟环境
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
4. 配置环境变量
   - 复制 `.env.example` 到 `.env` 并根据需要修改配置
5. 创建数据库
   ```bash
   # 确保 PostgreSQL 已安装并运行
   # 创建名为 fastapi_demo 的数据库
   ```
6. 运行数据库迁移
   ```bash
   alembic upgrade head
   ```
7. 创建初始数据
   ```bash
   python initial_data.py
   ```
8. 启动应用
   ```bash
   python run.py
   ```

### Docker 环境

1. 使用 Docker Compose 启动
   ```bash
   docker-compose up -d
   ```
2. 执行数据库迁移
   ```bash
   docker-compose exec web alembic upgrade head
   ```
3. 创建初始数据
   ```bash
   docker-compose exec web python initial_data.py
   ```

## API 文档

启动应用后，可以访问以下URL查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 超级用户

初始超级用户凭据:
- 邮箱: admin@example.com
- 密码: admin123 