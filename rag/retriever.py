"""向量库检索：按问题语义相似度取回最相关的知识片段。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from config import settings

# 模块级复用，避免每次调用都重新加载
_db = None


def _vector_dir() -> str:
    if os.path.isabs(settings.VECTOR_DB_DIR):
        return settings.VECTOR_DB_DIR
    return os.path.join(ROOT, settings.VECTOR_DB_DIR)


def _get_db() -> Chroma:
    global _db
    if _db is None:
        _db = Chroma(
            persist_directory=_vector_dir(),
            embedding_function=OllamaEmbeddings(
                model=settings.OLLAMA_EMBED_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
            ),
        )
    return _db


def search(question: str, k: int = 3) -> str:
    """检索与问题最相关的 k 段知识，返回拼接文本。"""
    try:
        docs = _get_db().similarity_search(question, k=k)
        return "\n".join(d.page_content for d in docs)
    except Exception as exc:  # 向量库还没建时会走到这里，给出友好提示
        return f"知识库未就绪，请先运行 python rag/create_vector.py。原因: {exc}"
