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

### 环境要求
 
 - Python 版本建议 3.10 左右，因为 3.13 会有兼容性问题

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

## 安全配置管理

本项目提供了多种方式安全存储和管理敏感配置（如数据库密码、密钥等）：

### 开发环境

1. **使用.env文件（仅限本地开发）**
   - 复制`.env.example`为`.env`并填入本地开发所需的配置
   - 确保`.env`已添加到`.gitignore`中，不要提交到代码仓库
   - 限制`.env`文件的访问权限：`chmod 600 .env`（Linux/Mac）

2. **使用环境变量**
   - 直接在系统或IDE中设置环境变量
   - 例如：`export DATABASE_URL=postgresql://user:password@localhost/db`
   - 这些变量会覆盖`.env`文件中的同名配置

### 生产环境

1. **容器环境变量**
   - 在容器编排工具（Docker Compose、Kubernetes）中设置环境变量
   - 可以从CI/CD系统中获取敏感信息并注入环境变量

2. **使用密钥管理服务**
   - AWS Secrets Manager、Azure Key Vault、HashiCorp Vault等
   - 项目已集成密钥获取接口，需配置相应SDK（见`app/core/config.py`）
   - 示例：
     ```python
     # 在config.py中完成如下配置
     import boto3
     
     def get_aws_secret(secret_name):
         client = boto3.client('secretsmanager')
         response = client.get_secret_value(SecretId=secret_name)
         return response['SecretString']
     ```

3. **容器编排密钥管理**
   - Docker Swarm Secrets: `docker secret create db_password ./password.txt`
   - Kubernetes Secrets: `kubectl create secret generic db-secret --from-literal=password=mypassword`

### 最佳实践

- 不同环境使用不同的密钥
- 定期轮换密钥
- 使用最小权限原则配置访问控制
- 记录密钥访问日志
- 避免在日志中输出敏感信息
- 考虑使用密钥加密服务进行额外保护 