import ast
import operator
import math

# Operator yang diizinkan
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
}

ALLOWED_FUNCS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "pi": math.pi,
    "e": math.e,
}


class SafeEval(ast.NodeVisitor):
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operator tidak diizinkan: {type(node.op)}")
        return op(left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op = ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operator tidak diizinkan: {type(node.op)}")
        return op(operand)

    def visit_Num(self, node):
        return node.n

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Nilai tidak diizinkan.")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Fungsi tidak diizinkan.")
        func_name = node.func.id
        if func_name not in ALLOWED_FUNCS:
            raise ValueError(f"Fungsi '{func_name}' tidak diizinkan.")
        func = ALLOWED_FUNCS[func_name]
        args = [self.visit(a) for a in node.args]
        return func(*args)

    def visit_Name(self, node):
        if node.id in ALLOWED_FUNCS:
            val = ALLOWED_FUNCS[node.id]
            if isinstance(val, float):
                return val
        raise ValueError(f"Nama '{node.id}' tidak diizinkan.")

    def generic_visit(self, node):
        raise ValueError(f"Node tidak diizinkan: {type(node)}")


def calculator(expression):
    """Hitung ekspresi matematika dengan aman."""
    try:
        expression = expression.strip()
        tree = ast.parse(expression, mode="eval")
        result = SafeEval().visit(tree.body)

        if isinstance(result, float):
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 10)

        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Pembagian dengan nol."
    except Exception as e:
        return f"CALCULATOR ERROR: {e}"
