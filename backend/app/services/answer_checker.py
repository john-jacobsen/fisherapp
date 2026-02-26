"""
Answer checker using SymPy for symbolic math verification.
"""
from typing import Literal

try:
    from sympy import simplify, sympify, SympifyError
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False


AnswerType = Literal["symbolic", "numeric", "multiple_choice"]


def check_answer(student_answer: str, correct_answer: str, answer_type: AnswerType = "symbolic") -> bool:
    """
    Check if a student's answer matches the correct answer.

    For symbolic: use SymPy simplification
    For numeric: allow tolerance ±0.01
    For multiple_choice: exact string match (case-insensitive)
    """
    student = student_answer.strip()
    correct = correct_answer.strip()

    if answer_type == "multiple_choice":
        return student.lower() == correct.lower()

    if answer_type == "numeric":
        try:
            sv = float(student)
            cv = float(correct)
            return abs(sv - cv) <= 0.01
        except ValueError:
            return student == correct

    # Symbolic (default)
    if not SYMPY_AVAILABLE:
        return student == correct

    try:
        s_expr = sympify(student)
        c_expr = sympify(correct)
        diff = simplify(s_expr - c_expr)
        return diff == 0
    except (SympifyError, Exception):
        # Fall back to string comparison if SymPy can't parse
        return student == correct
