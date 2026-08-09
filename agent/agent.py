"""Agent 核心：把 LangGraph Agent + Redis 多轮记忆封装成 chat()。

Redis 未就绪时自动降级为进程内内存记忆（服务照常可用），
Redis 配好后（config/settings.py 里的地址密码）自动切回 Redis。
"""
from langchain_core.chat_history import InMemoryChatMessageHistory

from agent.graph import agent
from agent.memory import get_session_history

# Redis 不可用时降级用的内存记忆（key 为 session_id）
_memory_fallback: dict[str, InMemoryChatMessageHistory] = {}


def _get_history(session_id: str):
    try:
        return get_session_history(session_id)
    except Exception:
        return _memory_fallback.setdefault(session_id, InMemoryChatMessageHistory())


def chat(session_id: str, message: str) -> str:
    """带多轮记忆的对话入口（优先 Redis，不可用则降级内存）。

    流程：
      1. 取出该会话的历史
      2. 把用户新消息追加进历史（Redis 模式下立即落盘）
      3. 把整段历史交给 Agent（LangGraph 图）执行
      4. 把 AI 回答保存回历史
    """
    history = _get_history(session_id)
    history.add_user_message(message)

    result = agent.invoke({"messages": [*history.messages]})
    answer = result["messages"][-1].content

    history.add_ai_message(answer)
    return answer
