"""计算工具：安全的数学表达式求值（替代裸 eval，防止任意代码执行）。"""
import ast
import math
import operator

from langchain.tools import tool

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def _safe_eval(node):
    """只允许：数字、四则运算、括号、math 库函数；其余一律拒绝。"""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        op = _BINOPS.get(type(node.op))
        if op is None:
            raise ValueError("不支持的运算符")
        return op(_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -_safe_eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +_safe_eval(node.operand)
        raise ValueError("不支持的运算符")
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and hasattr(math, node.func.id):
            args = [_safe_eval(a) for a in node.args]
            return getattr(math, node.func.id)(*args)
        raise ValueError("不支持的函数")
    raise ValueError("不支持的表达式")


@tool
def calculator(expression: str) -> float:
    """数学计算工具。示例：'100*20'、'sqrt(144)+2'、'(3+5)*7'"""
    return _safe_eval(ast.parse(expression, mode="eval"))
