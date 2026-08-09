"""用户查询工具：把普通函数封装成 Agent 可调用的 Tool。"""
from langchain.tools import tool

from database.db import query_user


@tool
def get_user(user_id: int) -> str:
    """查询用户（员工）信息。参数 user_id 是员工编号（整数）。"""
    return query_user(user_id)
