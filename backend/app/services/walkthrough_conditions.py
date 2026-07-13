"""
Safe evaluation of walkthrough wrong-answer feedback conditions.

Conditions are small Python-like boolean expressions evaluated against:
  answer       — student's answer as float (None if non-numeric)
  answer_int   — as int (None if not a whole number)
  answer_str   — raw stripped string
  plus every numeric key in the walkthrough's variables dict.

Examples of valid conditions:
  "answer == 1"
  "answer == numerator"
  "answer_int is not None and numerator % answer_int == 0 and denominator % answer_int != 0"
  "answer_int is not None and answer_int < gcf and numerator % answer_int == 0 and denominator % answer_int == 0"

Security: we NEVER use a bare eval()/exec() on the raw string. The expression
is parsed with ast.parse(mode="eval") and every node is validated against a
strict allowlist (booleans, comparisons, arithmetic, names, constants). Any
node outside the allowlist — calls, attributes, subscripts, comprehensions,
lambdas, etc. — raises ConditionError, so hostile input like
"__import__('os').system('ls')" is rejected before anything runs.
"""
import ast
import logging
import operator

logger = logging.getLogger(__name__)


class ConditionError(Exception):
    """Raised when a condition string is unparseable or uses disallowed syntax."""


# Allowed AST node types (structure). Anything not here is rejected.
_ALLOWED_NODES = (
    ast.Expression,
    ast.BoolOp,
    ast.UnaryOp,
    ast.BinOp,
    ast.Compare,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.And,
    ast.Or,
    ast.Not,
    ast.USub,
    ast.UAdd,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
)

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
}

_CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
}

_UNARY_OPS = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Not: operator.not_,
}

# Guard against absurd exponents (e.g. 9**9 as a DoS vector) even though Pow is
# allowed for legitimate expressions.
_MAX_POW_EXPONENT = 64


def _validate(node: ast.AST) -> None:
    """Recursively assert every node is in the allowlist; raise otherwise."""
    if not isinstance(node, _ALLOWED_NODES):
        raise ConditionError(f"Disallowed expression element: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _validate(child)


def _eval_node(node: ast.AST, namespace: dict):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, namespace)

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        if node.id in namespace:
            return namespace[node.id]
        raise ConditionError(f"Unknown name: {node.id}")

    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            result = True
            for v in node.values:
                result = _eval_node(v, namespace)
                if not result:
                    return result
            return result
        else:  # Or
            result = False
            for v in node.values:
                result = _eval_node(v, namespace)
                if result:
                    return result
            return result

    if isinstance(node, ast.UnaryOp):
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand, namespace))

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, namespace)
        right = _eval_node(node.right, namespace)
        if isinstance(node.op, ast.Pow) and abs(right) > _MAX_POW_EXPONENT:
            raise ConditionError("Exponent too large")
        return _BIN_OPS[type(node.op)](left, right)

    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, namespace)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval_node(comparator, namespace)
            if not _CMP_OPS[type(op)](left, right):
                return False
            left = right
        return True

    raise ConditionError(f"Disallowed expression element: {type(node).__name__}")


def _build_namespace(answer: str, variables: dict) -> dict:
    """Assemble the evaluation namespace from the answer and numeric variables."""
    answer_str = (answer or "").strip()
    try:
        answer_float = float(answer_str)
        answer_int = int(answer_float) if answer_float == int(answer_float) else None
    except (ValueError, TypeError):
        answer_float = None
        answer_int = None

    namespace = {
        "answer": answer_float,
        "answer_int": answer_int,
        "answer_str": answer_str,
    }
    for key, value in (variables or {}).items():
        # Only expose numeric scalars; skip lists (e.g. _mc_order_N) and strings.
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            namespace[key] = value
        else:
            try:
                fval = float(value)
                namespace[key] = int(fval) if fval == int(fval) else fval
            except (ValueError, TypeError):
                continue
    return namespace


def evaluate_condition(condition: str, answer: str, variables: dict) -> bool:
    """
    Evaluate a boolean condition string safely. Returns the boolean result.

    Raises ConditionError on a parse error or disallowed syntax (so callers can
    fall back to legacy named conditions). Runtime errors during evaluation
    (unknown name, division by zero, type mismatch) are swallowed and return
    False — a broken condition must never 500 a student's submission.
    """
    try:
        tree = ast.parse(condition, mode="eval")
    except SyntaxError as exc:
        raise ConditionError(f"Could not parse condition {condition!r}: {exc}") from exc

    _validate(tree)  # may raise ConditionError — this is the security gate

    namespace = _build_namespace(answer, variables)
    try:
        return bool(_eval_node(tree, namespace))
    except ConditionError:
        # Unknown name / structural issue discovered at eval time — treat as
        # non-matching rather than crashing.
        logger.warning("Condition %r referenced an unknown name; treating as False", condition)
        return False
    except (ZeroDivisionError, TypeError, ValueError) as exc:
        logger.warning("Condition %r failed to evaluate (%s); treating as False", condition, exc)
        return False
