"""启动入口：FastAPI 服务。

运行：python main.py
访问：
    http://localhost:8000        中文聊天页面
    http://localhost:8000/docs   API 文档
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agent.agent import chat

app = FastAPI(title="企业智能 Agent 助手")

# 前端页面路径（相对本文件定位，任意工作目录都能找到）
FRONTEND = Path(__file__).parent / "static" / "index.html"


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"  # 同一 session_id 复用同一段 Redis 记忆


@app.get("/", response_class=FileResponse)
def root():
    """返回中文聊天前端页面。"""
    return FileResponse(FRONTEND)


@app.post("/chat")
def chat_api(req: ChatRequest):
    try:
        answer = chat(req.session_id, req.message)
        return {"answer": answer}
    except Exception as exc:
        return {"error": str(exc)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
