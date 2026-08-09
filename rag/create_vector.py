"""创建向量库：knowledge/*.txt -> 切分 -> Ollama(bge-m3) 嵌入 -> 存入 vector_db/

运行（在项目根目录）：
    python rag/create_vector.py

知识内容更新后，重新运行本脚本即可增量重建。
"""
import glob
import os
import sys

# 让 `python rag/create_vector.py` 也能 import 到项目根目录的包（config 等）
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


def _vector_dir() -> str:
    if os.path.isabs(settings.VECTOR_DB_DIR):
        return settings.VECTOR_DB_DIR
    return os.path.join(ROOT, settings.VECTOR_DB_DIR)


def main() -> None:
    # 1. 加载所有知识文档
    files = glob.glob(os.path.join(ROOT, "knowledge", "*.txt"))
    if not files:
        print("knowledge/ 下没有 .txt 文件，请先填写知识内容。")
        return

    docs = []
    for path in files:
        print(f"加载: {os.path.relpath(path, ROOT)}")
        docs.extend(TextLoader(path, encoding="utf-8").load())
    print(f"共加载 {len(docs)} 个文档")

    # 2. 切分
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"切分为 {len(chunks)} 个文本块")

    # 3. 嵌入（Ollama bge-m3，必须显式 base_url，原因见 config/settings.py 注释）
    embedding = OllamaEmbeddings(
        model=settings.OLLAMA_EMBED_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )

    # 4. 入库
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=_vector_dir(),
    )
    print(f"向量数据库创建完成: {_vector_dir()}")


if __name__ == "__main__":
    main()
