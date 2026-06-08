"""
Calculator Tool - Safe math evaluation for the agents.
"""
import ast
import operator
from typing import Union
from src.utils.logger import app_logger


# Safe operators only
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def safe_eval(expression: str) -> Union[float, str]:
    """
    Safely evaluate a mathematical expression.
    No exec/eval - uses AST parsing only.
    """
    try:
        tree = ast.parse(expression, mode='eval')
        return _eval_node(tree.body)
    except Exception as e:
        app_logger.warning(f"Calculator error for '{expression}': {e}")
        return f"Error: {str(e)}"


def _eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op)}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return op(left, right)
    elif isinstance(node, ast.UnaryOp):
        op = SAFE_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op)}")
        return op(_eval_node(node.operand))
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")


def calculate(expression: str) -> str:
    """
    Main calculator interface for agents.
    
    Args:
        expression: Math expression as string (e.g., "2 + 2 * 10")
    
    Returns:
        Result as string
    """
    app_logger.info(f"🔢 Calculating: {expression}")
    result = safe_eval(expression)
    app_logger.info(f"📊 Result: {result}")
    return str(result)