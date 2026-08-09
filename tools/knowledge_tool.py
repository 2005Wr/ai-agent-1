"""知识库工具：把 RAG 检索封装成 Agent 可调用的 Tool。"""
from langchain.tools import tool

from rag.retriever import search


@tool
def knowledge_search(question: str) -> str:
    """查询企业知识库（RAG 检索），返回与问题最相关的知识片段。"""
    return search(question)
