# Enterprise AI Agent Assistant（企业智能 Agent 助手平台）

基于 Python 3.13 + LangChain/LangGraph + DeepSeek + Ollama(bge-m3) + Chroma + Redis 的企业知识 Agent。

## 架构

```
用户 → FastAPI → LangGraph Agent（DeepSeek）
                    ├─ get_user          → 数据库（dict / SQLite）
                    ├─ calculator        → 安全数学计算
                    ├─ knowledge_search  → Chroma 向量库 ← Ollama bge-m3 嵌入
                    └─ 多轮记忆          → Redis（在 VMware 虚拟机里）
```

## 首次运行

```bash
# 1. 填好 .env（DeepSeek Key、Redis 虚拟机 IP/密码）

# 2. 写知识内容到 knowledge/*.txt，然后建向量库（只需一次）
python rag/create_vector.py

# 3. 启动服务
python main.py
```

## 使用

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "公司的退款规则是什么", "session_id": "user001"}'
```

多轮记忆：同一 `session_id` 的对话会记住上文（存在 Redis，key 前缀 `chat:`）。

## 备注

- 嵌入走本机 Ollama（`bge-m3`），**必须在代码里显式指定 `base_url=http://127.0.0.1:11434`**，
  因为你的机器 `OLLAMA_HOST=0.0.0.0:11434`，客户端连 `0.0.0.0` 在 Windows 上会失败。
- 更新知识后重新执行 `python rag/create_vector.py` 即可。
