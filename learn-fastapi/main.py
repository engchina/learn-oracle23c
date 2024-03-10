import time
from typing import Union

from fastapi import FastAPI, Request, BackgroundTasks, WebSocket, Depends
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


"""
1. 中间件 (Middleware)
中间件是一种特殊的代码,可以在请求和响应的生命周期中执行一些操作。它们可以修改传入的请求或传出的响应,也可以执行一些额外的逻辑,如记录、认证等。
"""


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    添加进程时间标头到HTTP响应的中间件函数。

    参数:
        request (Request): 传入的HTTP请求。
        call_next: 调用链中下一个中间件的函数。

    返回:
        带有添加的'X-Process-Time'标头的HTTP响应。
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


"""
后台任务 (Background Tasks)
有时候,我们需要在请求完成后执行一些异步操作,但不想让客户端等待这些操作完成。
这时候就可以使用后台任务。后台任务会在请求完成后异步执行,不会阻塞主请求处理流程。
"""


def write_notification(email: str, message=""):
    """
    写入给定电子邮件地址和消息的通知到日志文件。

    :param email: str, 要发送通知的电子邮件地址
    :param message: str, 要包含在通知中的消息（默认为空字符串）
    :return: None
    """
    with open("log.txt", "a") as email_file:
        email_file.write(f"notification for {email}: {message}\n")


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks, message: str = ""):
    background_tasks.add_task(write_notification, email, message)
    return {"message": "Notification will be sent in the background"}


"""
WebSockets
WebSocket 是一种计算机通信协议,可以在客户端和服务器之间建立全双工通信连接。
FastAPI 支持使用 WebSockets 开发实时应用程序,如聊天应用程序、实时监控系统等。
"""


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


"""
依赖注入 (Dependency Injection)
依赖注入是一种设计模式,它可以帮助我们管理对象之间的依赖关系。在 FastAPI 中,我们可以使用依赖注入来共享和复用代码逻辑。
"""


def get_query(query: str):
    return query


@app.get("/search")
async def search(query: str = Depends(get_query)):
    """
    用于搜索带有查询参数的异步函数。

    参数:
    - query: 通过使用get_query依赖项获得的字符串

    返回:
    - 包含查询内容的字典
    """
    return {"query": query}


"""
静态文件服务 (Static File Serving)
FastAPI 可以很容易地为静态文件(如 CSS、JavaScript 和图片文件)提供服务。这对于构建包含前端资源的 Web 应用程序非常有用。

在这个例子中,我们使用 app.mount 函数将 /static 路径映射到本地 static 目录。
这意味着任何位于 static 目录下的文件都可以通过 /static 路径访问。
例如,如果我们有一个 static/css/styles.css 文件,就可以通过 /static/css/styles.css 路径访问它。
"""
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    """
    一个处理根端点的函数。它不接受任何参数，并返回一个具有键“Hello”和值“World”的字典。
    """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    一个用于读取具有给定 item_id 和可选查询参数的项目的函数。

    参数:
    - item_id: 代表项目 id 的整数
    - q: 一个字符串或 None，表示可选的查询参数

    返回:
    - 一个包含 item_id 和查询参数的字典
    """
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    更新具有给定item_id的项目，并返回包含项目名称和id的字典。

    参数:
    - item_id: int
        要更新的项目的唯一标识符。
    - item: Item
        更新后的项目对象。

    返回:
    dict
        包含更新后项目名称和id的字典。
    """
    # return {"item_name": item.name, "item_id": item_id, "price": item.price, **item.dict()}
    return {**item.dict()}
