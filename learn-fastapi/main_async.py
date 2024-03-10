from typing import Union

from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.testclient import TestClient

import time

app = FastAPI()

"""
任务 (Tasks)
学习内容: 在 FastAPI 中执行后台任务和周期性任务。
"""


def write_notification(email: str, message=""):
    with open("notifications.txt", "a") as file:
        file.write(f"Notification for {email}: {message}\n")


def send_notifications(emails, message):
    with BackgroundTasks() as background_tasks:
        for email in emails:
            background_tasks.add_task(write_notification, email, message)


@app.get("/send-notifications/{message}")
def send_notifications_endpoint(message: str):
    emails = ["user1@example.com", "user2@example.com", "user3@example.com"]
    send_notifications(emails, message)
    return {"message": "Notifications will be sent in the background"}


"""
测试 (Testing)
学习内容: 使用 pytest 等测试框架对 FastAPI 应用程序进行单元测试和集成测试。
"""
client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_item():
    payload = {"name": "Item 1", "price": 9.99}
    response = client.post("/items/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Item 1"
    assert data["price"] == 9.99


"""
安全性 (Security)
学习内容: 使用 FastAPI 提供的安全功能,如 OAuth2、JWT 认证、API 密钥等。
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     # 在这里验证用户凭据
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     # 在这里生成访问令牌
#     access_token = create_access_token(user)
#     return {"access_token": access_token, "token_type": "bearer"}


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


"""
部署 (Deployment)
学习内容: 将 FastAPI 应用程序部署到不同环境,如 Docker、Kubernetes、AWS
"""

"""
# Dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
