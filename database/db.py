"""模拟用户数据库。

真实项目请替换为 SQLite / MySQL / PostgreSQL。
"""
import os
import sqlite3

# 如果存在 data.db 就用 SQLite，否则用内存字典模拟
DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

users = {
    1: {"name": "张三", "age": 22, "department": "研发部"},
    2: {"name": "李四", "age": 28, "department": "销售部"},
}


def query_user(user_id: int) -> dict | str:
    """按员工编号查询用户信息。"""
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute(
                "SELECT id, name, age, department FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
            conn.close()
            if row:
                return {"id": row[0], "name": row[1], "age": row[2], "department": row[3]}
            return "用户不存在"
        except sqlite3.Error:
            pass
    return users.get(user_id, "用户不存在")


def init_sqlite() -> None:
    """建表并把字典数据灌入 SQLite（可选，用于演示真实替换）。"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, department TEXT)")
    conn.executemany(
        "INSERT INTO users (id, name, age, department) VALUES (?, ?, ?, ?)",
        [(uid, u["name"], u["age"], u["department"]) for uid, u in users.items()],
    )
    conn.commit()
    conn.close()
    print(f"SQLite 已初始化: {DB_PATH}")


if __name__ == "__main__":
    init_sqlite()
