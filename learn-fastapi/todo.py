"""
这个代码使用 FastAPI 创建了一个简单的 TODO 应用。
该应用包含以下功能:
用户登录
获取所有 TODO
创建 TODO
获取单个 TODO
更新 TODO
删除 TODO
该代码使用了以下 Fast
"""
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


# 定义数据库模型
class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


# 定义用户模型
class User(BaseModel):
    username: str
    password: str


# 模拟数据库
database = {
    "todos": [
        Todo(id=1, title="Write a blog post", description="Write a blog post about FastAPI", completed=False),
        Todo(id=2, title="Learn about asyncio", description="Learn about asyncio and how it can be used with FastAPI",
             completed=True),
    ],
    "users": {
        "johndoe": User(username="johndoe", password="secret"),
        "janedoe": User(username="janedoe", password="secret123"),
    },
}

# 定义 OAuth2 密码授权
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# 定义依赖项
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = database["users"].get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


# 创建 FastAPI 应用
app = FastAPI()


# 登录
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = database["users"].get(form_data.username)
    if not user or form_data.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


# 获取所有 TODO
@app.get("/todos", response_model=list[Todo])
async def get_todos(user: User = Depends(get_current_user)):
    return database["todos"]


# 创建 TODO
@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo, user: User = Depends(get_current_user)):
    todo.id = len(database["todos"]) + 1
    database["todos"].append(todo)
    return todo


# 获取单个 TODO
@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, user: User = Depends(get_current_user)):
    todo = next((todo for todo in database["todos"] if todo.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# 更新 TODO
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo, user: User = Depends(get_current_user)):
    existing_todo = next((todo for todo in database["todos"] if todo.id == todo_id), None)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.completed = todo.completed
    return existing_todo


# 删除 TODO
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, user: User = Depends(get_current_user)):
    todo = next((todo for todo in database["todos"] if todo.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    database["todos"].remove(todo)


# 运行应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
