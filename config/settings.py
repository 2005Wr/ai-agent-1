"""统一配置管理：从 .env 读取，不写死密钥。"""
import os

from dotenv import load_dotenv

load_dotenv()

# ===== DeepSeek API =====
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# ===== Ollama 嵌入（本机）=====
# 注意：必须显式写 127.0.0.1，不能依赖 OLLAMA_HOST 环境变量。
# 你的机器设了 OLLAMA_HOST=0.0.0.0，客户端连 0.0.0.0 在 Windows 上会失败。
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "bge-m3")

# ===== 虚拟机里的 Redis =====
REDIS_HOST = os.getenv("REDIS_HOST", "192.168.184.138")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# ===== 向量库持久化目录 =====
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./vector_db")
