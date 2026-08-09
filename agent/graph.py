"""LangGraph 流程：Agent 核心图。

用 langchain.agents.create_agent 构建，返回的就是一个编译好的 LangGraph StateGraph：

    START -> [model] --有工具调用--> [tools] --执行完--> 回到 model
                       |
                       +--无工具调用--> 输出最终回答

（model 节点 + tools 节点 + 条件边，即 Agent 自主规划 + Tool Calling 循环）
"""
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from config import settings
from tools.calculator import calculator
from tools.knowledge_tool import knowledge_search
from tools.user_tool import get_user

SYSTEM_PROMPT = """你是企业智能 Agent。

你可以：
1. 查询员工信息（get_user）
2. 查询企业知识库（knowledge_search）
3. 执行数学计算（calculator）

规则：
- 需要数据时必须调用工具，不要编造。
- 回答用中文，简洁准确。"""


def build_agent():
    """构建并返回编译好的 LangGraph Agent 图。"""
    model = init_chat_model(
        "deepseek-chat",
        model_provider="openai",
        base_url="https://api.deepseek.com",
        api_key=settings.DEEPSEEK_API_KEY,
    )
    tools = [get_user, calculator, knowledge_search]
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


agent = build_agent()
