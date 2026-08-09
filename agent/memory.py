"""多轮对话记忆：存到虚拟机里的 Redis（Windows 主机只做客户端）。

用 redis-py 直接把消息存成 JSON 列表（每会话一个 key：chat:{session_id}）。

为什么不用 langchain-redis 的 RedisChatMessageHistory？
它依赖 Redis 的 RediSearch 模块（FT.INFO 命令），而虚拟机里是原生 Redis，
没有该模块。这里用纯 redis 命令实现，原生 Redis 即可跑。
"""
import json

import redis

from config import settings

_pool: redis.ConnectionPool | None = None


def _client() -> redis.Redis:
    global _pool
    if _pool is None:
        _pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True,
            socket_connect_timeout=5,
        )
    return redis.Redis(connection_pool=_pool)


class SessionHistory:
    """极简会话历史：messages 列表 + 追加消息，落 Redis 的 JSON 字符串。"""

    def __init__(self, session_id: str, key_prefix: str = "chat:"):
        self._key = f"{key_prefix}{session_id}"
        self._client = _client()

    @property
    def messages(self) -> list[dict]:
        data = self._client.get(self._key)
        return json.loads(data) if data else []

    def _append(self, role: str, content: str) -> None:
        messages = self.messages
        messages.append({"role": role, "content": content})
        self._client.set(
            self._key,
            json.dumps(messages, ensure_ascii=False),
            ex=60 * 60 * 24,  # 1 天后自动过期
        )

    def add_user_message(self, content: str) -> None:
        self._append("user", content)

    def add_ai_message(self, content: str) -> None:
        self._append("assistant", content)


def get_session_history(session_id: str) -> SessionHistory:
    return SessionHistory(session_id)
