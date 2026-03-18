"""
Linear algebra problem generators for Fisher App 3.0.
Covers 21 nodes: linalg-vectors through linalg-svd.

All answers are scalars or simple fractions to stay within the answer checker.
Matrix/vector notation is display-only; students enter a single numeric value.

Drop at: backend/app/services/generators/linear_algebra.py
In problem_generator.py add:
    from .generators.linear_algebra import GENERATORS as LINALG_GENERATORS
    GENERATORS.update(LINALG_GENERATORS)
"""
import random
from fractions import Fraction
from math import gcd, sqrt, isqrt


# ── helpers ───────────────────────────────────────────────────────────────────

def _frac_str(p, q):
    """Reduced fraction string; return int string if denominator is 1."""
    f = Fraction(p, q)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

def _mat2(a, b, c, d):
    """LaTeX 2x2 matrix."""
    return f"\\begin{{pmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{pmatrix}}"

def _vec2(a, b):
    return f"\\begin{{pmatrix}} {a} \\\\ {b} \\end{{pmatrix}}"

def _vec3(a, b, c):
    return f"\\begin{{pmatrix}} {a} \\\\ {b} \\\\ {c} \\end{{pmatrix}}"

def _det2(a, b, c, d):
    return a*d - b*c

def _rand_inv2x2():
    """Return (a,b,c,d) for a 2x2 matrix with det = ±1 or small nonzero."""
    while True:
        a = random.randint(-3, 3)
        b = random.randint(-3, 3)
        c = random.randint(-3, 3)
        d = random.randint(-3, 3)
        det = _det2(a, b, c, d)
        if det != 0:
            return a, b, c, d, det


# ── linalg-vectors ────────────────────────────────────────────────────────────

def _gen_linalg_vectors():
    """Dot product, squared magnitude, or scalar multiple of a 2D vector."""
    variant = random.choice(['dot', 'norm_sq', 'scalar'])
    if variant == 'dot':
        # V1: dot product u·v
        u = [random.randint(-4, 4) for _ in range(2)]
        v = [random.randint(-4, 4) for _ in range(2)]
        ans = u[0]*v[0] + u[1]*v[1]
        return {
            "problem_text": (
                f"Find the dot product \\(\\mathbf{{u}} \\cdot \\mathbf{{v}}\\) for "
                f"\\(\\mathbf{{u}} = {_vec2(*u)}\\) and \\(\\mathbf{{v}} = {_vec2(*v)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Dot product: multiply corresponding components and sum the results."},
                {"level": 2, "text": f"Compute \\({u[0]} \\cdot {v[0]} + {u[1]} \\cdot {v[1]}\\)."},
                {"level": 3, "text": f"\\({u[0]*v[0]} + {u[1]*v[1]} = {ans}\\)."},
            ],
        }
    elif variant == 'norm_sq':
        # V2: squared magnitude ||u||²
        u = [random.randint(-4, 4) for _ in range(2)]
        ans = u[0]**2 + u[1]**2
        return {
            "problem_text": (
                f"Find \\(\\|\\mathbf{{u}}\\|^2\\) for "
                f"\\(\\mathbf{{u}} = {_vec2(*u)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "\\(\\|\\mathbf{u}\\|^2 = u_1^2 + u_2^2\\)."},
                {"level": 2, "text": f"\\({u[0]}^2 + {u[1]}^2\\)."},
                {"level": 3, "text": f"\\({u[0]**2} + {u[1]**2} = {ans}\\)."},
            ],
        }
    else:
        # V3: scalar multiple — find first component of w = c·u
        c = random.choice([-3, -2, -1, 2, 3, 4])
        u = [random.randint(1, 4), random.randint(1, 4)]
        ans = c * u[0]
        return {
            "problem_text": (
                f"Find the scalar multiple: if \\(\\mathbf{{w}} = {c} \\cdot \\mathbf{{u}}\\), "
                f"what is the first component of \\(\\mathbf{{w}}\\)? "
                f"Given \\(\\mathbf{{u}} = {_vec2(*u)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Scalar multiplication multiplies every component of the vector by the scalar."},
                {"level": 2, "text": f"The first component of \\(\\mathbf{{w}}\\) is \\({c} \\cdot {u[0]}\\)."},
                {"level": 3, "text": f"\\({c} \\times {u[0]} = {ans}\\)."},
            ],
        }


# ── linalg-matrix-ops ─────────────────────────────────────────────────────────

def _gen_linalg_matrix_ops():
    """Add or subtract two 2x2 matrices; or find the trace of A+B."""
    A = [[random.randint(-4, 4) for _ in range(2)] for _ in range(2)]
    B = [[random.randint(-4, 4) for _ in range(2)] for _ in range(2)]
    variant = random.choice(['entry_add', 'trace_add', 'entry_sub'])
    if variant == 'entry_add':
        # V1: specific entry of A + B
        r, c = random.randint(0, 1), random.randint(0, 1)
        ans = A[r][c] + B[r][c]
        rc_label = f"({r+1},{c+1})"
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\) and "
                f"\\(B = {_mat2(*[B[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the \\({rc_label}\\) entry of \\(A + B\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Matrix addition is entry-wise: \\((A+B)_{ij} = A_{ij} + B_{ij}\\)."},
                {"level": 2, "text": f"Add the \\({rc_label}\\) entries: \\({A[r][c]} + {B[r][c]}\\)."},
                {"level": 3, "text": f"\\({A[r][c]} + {B[r][c]} = {ans}\\)."},
            ],
        }
    elif variant == 'trace_add':
        # V2: trace of A + B
        ans = (A[0][0] + B[0][0]) + (A[1][1] + B[1][1])
        d00 = A[0][0] + B[0][0]; d11 = A[1][1] + B[1][1]
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\) and "
                f"\\(B = {_mat2(*[B[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the trace of \\(A + B\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The trace of a matrix is the sum of its diagonal entries."},
                {"level": 2, "text": f"First compute \\(A+B\\), then sum its diagonal: \\({d00} + {d11}\\)."},
                {"level": 3, "text": f"\\(\\text{{tr}}(A+B) = {d00} + {d11} = {ans}\\)."},
            ],
        }
    else:
        # V3: specific entry of A - B
        r, c = random.randint(0, 1), random.randint(0, 1)
        ans = A[r][c] - B[r][c]
        rc_label = f"({r+1},{c+1})"
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\) and "
                f"\\(B = {_mat2(*[B[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the \\({rc_label}\\) entry of \\(A - B\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Matrix subtraction is entry-wise: \\((A-B)_{ij} = A_{ij} - B_{ij}\\)."},
                {"level": 2, "text": f"Subtract the \\({rc_label}\\) entries: \\({A[r][c]} - {B[r][c]}\\)."},
                {"level": 3, "text": f"\\({A[r][c]} - {B[r][c]} = {ans}\\)."},
            ],
        }


# ── linalg-matrix-mult ────────────────────────────────────────────────────────

def _gen_linalg_matrix_mult():
    """Multiply two 2x2 matrices; return one entry, trace of AB, or entry of A²."""
    A = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
    B = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
    variant = random.choice(['entry_AB', 'trace_AB', 'entry_Asq'])
    if variant == 'entry_AB':
        # V1: specific entry of AB
        r, c = random.randint(0, 1), random.randint(0, 1)
        ans = sum(A[r][k] * B[k][c] for k in range(2))
        rc_label = f"({r+1},{c+1})"
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\) and "
                f"\\(B = {_mat2(*[B[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the \\({rc_label}\\) entry of \\(AB\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": f"The \\({rc_label}\\) entry of \\(AB\\) is the dot product of row {r+1} of \\(A\\) with column {c+1} of \\(B\\)."},
                {"level": 2, "text": f"Compute \\({A[r][0]} \\cdot {B[0][c]} + {A[r][1]} \\cdot {B[1][c]}\\)."},
                {"level": 3, "text": f"\\({A[r][0]*B[0][c]} + {A[r][1]*B[1][c]} = {ans}\\)."},
            ],
        }
    elif variant == 'trace_AB':
        # V2: trace of AB
        ab00 = sum(A[0][k]*B[k][0] for k in range(2))
        ab11 = sum(A[1][k]*B[k][1] for k in range(2))
        ans = ab00 + ab11
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\) and "
                f"\\(B = {_mat2(*[B[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the trace of \\(AB\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The trace of a matrix is the sum of its diagonal entries."},
                {"level": 2, "text": f"Compute the (1,1) entry of \\(AB\\) = \\({ab00}\\) and the (2,2) entry = \\({ab11}\\), then sum them."},
                {"level": 3, "text": f"\\(\\text{{tr}}(AB) = {ab00} + {ab11} = {ans}\\)."},
            ],
        }
    else:
        # V3: specific entry of A²
        r, c = random.randint(0, 1), random.randint(0, 1)
        ans = sum(A[r][k] * A[k][c] for k in range(2))
        rc_label = f"({r+1},{c+1})"
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the \\({rc_label}\\) entry of \\(A^2\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": f"\\(A^2 = A \\cdot A\\). The \\({rc_label}\\) entry is the dot product of row {r+1} of \\(A\\) with column {c+1} of \\(A\\)."},
                {"level": 2, "text": f"Compute \\({A[r][0]} \\cdot {A[0][c]} + {A[r][1]} \\cdot {A[1][c]}\\)."},
                {"level": 3, "text": f"\\({A[r][0]*A[0][c]} + {A[r][1]*A[1][c]} = {ans}\\)."},
            ],
        }


# ── linalg-transpose ──────────────────────────────────────────────────────────

def _gen_linalg_transpose():
    """Transpose a 2x2 matrix; return an entry of A^T, trace of A^T, or entry of A+A^T."""
    A = [[random.randint(-4, 4) for _ in range(2)] for _ in range(2)]
    variant = random.choice(['entry_AT', 'trace_AT', 'entry_sym'])
    if variant == 'entry_AT':
        # V1: specific entry of A^T
        r, c = random.randint(0, 1), random.randint(0, 1)
        ans = A[c][r]   # A^T[r][c] = A[c][r]
        rc_label = f"({r+1},{c+1})"
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the \\({rc_label}\\) entry of \\(A^T\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The transpose swaps rows and columns: \\((A^T)_{ij} = A_{ji}\\)."},
                {"level": 2, "text": f"Entry \\({rc_label}\\) of \\(A^T\\) equals entry \\(({c+1},{r+1})\\) of \\(A\\)."},
                {"level": 3, "text": f"\\(A_{{{c+1},{r+1}}} = {ans}\\)."},
            ],
        }
    elif variant == 'trace_AT':
        # V2: trace of A^T (equals trace of A)
        ans = A[0][0] + A[1][1]
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the trace of \\(A^T\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The trace of a matrix is the sum of its diagonal entries. Note that \\(\\text{tr}(A^T) = \\text{tr}(A)\\)."},
                {"level": 2, "text": f"The diagonal of \\(A^T\\) equals the diagonal of \\(A\\): entries \\({A[0][0]}\\) and \\({A[1][1]}\\)."},
                {"level": 3, "text": f"\\(\\text{{tr}}(A^T) = {A[0][0]} + {A[1][1]} = {ans}\\)."},
            ],
        }
    else:
        # V3: specific entry of A + A^T
        r, c = random.randint(0, 1), random.randint(0, 1)
        ans = A[r][c] + A[c][r]   # (A + A^T)[r][c] = A[r][c] + A^T[r][c] = A[r][c] + A[c][r]
        rc_label = f"({r+1},{c+1})"
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find the \\({rc_label}\\) entry of \\(A + A^T\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\((A + A^T)_{ij} = A_{ij} + A_{ji}\\)."},
                {"level": 2, "text": f"The \\({rc_label}\\) entry is \\(A_{{{r+1},{c+1}}} + A_{{{c+1},{r+1}}} = {A[r][c]} + {A[c][r]}\\)."},
                {"level": 3, "text": f"\\({A[r][c]} + {A[c][r]} = {ans}\\)."},
            ],
        }


# ── linalg-row-reduce ─────────────────────────────────────────────────────────

def _gen_linalg_row_reduce():
    """Row reduce an augmented matrix for a 2x2 system; ask for x, y, or x+y."""
    # Build a clean 2x2 system with integer solution
    x = random.randint(-3, 4)
    y = random.randint(-3, 4)
    a = random.randint(1, 3);  b = random.randint(1, 3)
    c = random.randint(1, 3);  d = random.randint(1, 3)
    while a*d - b*c == 0:      # ensure nonsingular
        c = random.randint(1, 3); d = random.randint(1, 3)
    r1 = a*x + b*y
    r2 = c*x + d*y
    variant = random.choice(['ask_x', 'ask_y', 'ask_sum'])
    if variant == 'ask_x':
        # V1: solve for x
        return {
            "problem_text": (
                f"Row-reduce the augmented matrix "
                f"\\(\\left[\\begin{{array}}{{cc|c}} {a} & {b} & {r1} \\\\ {c} & {d} & {r2} \\end{{array}}\\right]\\) "
                f"to solve for \\(x\\)."
            ),
            "correct_answer": str(x), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Use row operations to create zeros below (or above) the pivot. Then back-substitute."},
                {"level": 2, "text": f"Eliminate the \\(y\\)-term from one equation, then solve for \\(x\\)."},
                {"level": 3, "text": f"The solution is \\(x={x}\\), \\(y={y}\\). So \\(x = {x}\\)."},
            ],
        }
    elif variant == 'ask_y':
        # V2: solve for y
        return {
            "problem_text": (
                f"Row-reduce the augmented matrix "
                f"\\(\\left[\\begin{{array}}{{cc|c}} {a} & {b} & {r1} \\\\ {c} & {d} & {r2} \\end{{array}}\\right]\\) "
                f"to solve for \\(y\\)."
            ),
            "correct_answer": str(y), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Use row operations to create zeros below (or above) the pivot. Then back-substitute."},
                {"level": 2, "text": f"Eliminate the \\(x\\)-term from one equation, then solve for \\(y\\)."},
                {"level": 3, "text": f"The solution is \\(x={x}\\), \\(y={y}\\). So \\(y = {y}\\)."},
            ],
        }
    else:
        # V3: find x + y
        ans = x + y
        return {
            "problem_text": (
                f"Row-reduce the augmented matrix "
                f"\\(\\left[\\begin{{array}}{{cc|c}} {a} & {b} & {r1} \\\\ {c} & {d} & {r2} \\end{{array}}\\right]\\) "
                f"to solve the system. What is \\(x + y\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "First solve the system by row reduction, then compute \\(x + y\\)."},
                {"level": 2, "text": f"Row-reduce to find both \\(x\\) and \\(y\\), then add them."},
                {"level": 3, "text": f"The solution is \\(x={x}\\), \\(y={y}\\). So \\(x+y = {x}+{y} = {ans}\\)."},
            ],
        }


# ── linalg-determinant ────────────────────────────────────────────────────────

def _gen_linalg_determinant():
    """Determinant of a 2x2 matrix, det(A^T), or singular value of k."""
    variant = random.choice(['det_A', 'det_AT', 'singular_k'])
    if variant == 'det_A':
        # V1: find det(A)
        a, b, c, d = [random.randint(-4, 4) for _ in range(4)]
        ans = _det2(a, b, c, d)
        return {
            "problem_text": f"Find \\(\\det(A)\\) for \\(A = {_mat2(a,b,c,d)}\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For a 2×2 matrix \\(\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}\\), \\(\\det = ad - bc\\)."},
                {"level": 2, "text": f"Compute \\({a} \\cdot {d} - {b} \\cdot {c}\\)."},
                {"level": 3, "text": f"\\({a*d} - {b*c} = {ans}\\)."},
            ],
        }
    elif variant == 'det_AT':
        # V2: find det(A^T) — equals det(A)
        a, b, c, d = [random.randint(-4, 4) for _ in range(4)]
        ans = _det2(a, b, c, d)
        return {
            "problem_text": f"Find \\(\\det(A^T)\\) for \\(A = {_mat2(a,b,c,d)}\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "A key property: \\(\\det(A^T) = \\det(A)\\)."},
                {"level": 2, "text": f"Compute \\(\\det(A) = {a} \\cdot {d} - {b} \\cdot {c}\\)."},
                {"level": 3, "text": f"\\(\\det(A^T) = \\det(A) = {a*d} - {b*c} = {ans}\\)."},
            ],
        }
    else:
        # V3: for what value of k is the matrix singular?
        # Use matrix [[k, b],[c, d]] with d=1 so k = b*c
        b = random.randint(1, 4)
        c = random.randint(1, 4)
        d = 1
        k = b * c   # det = k*d - b*c = k - b*c = 0 → k = b*c
        e = random.randint(1, 4)  # off-diagonal entry shown
        return {
            "problem_text": (
                f"For what value of \\(k\\) is the matrix "
                f"\\({_mat2('k', b, c, d)}\\) singular?"
            ),
            "correct_answer": str(k), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "A matrix is singular when its determinant equals zero."},
                {"level": 2, "text": f"Set \\(\\det = k \\cdot {d} - {b} \\cdot {c} = 0\\) and solve for \\(k\\)."},
                {"level": 3, "text": f"\\(k = {b} \\cdot {c} = {k}\\)."},
            ],
        }


# ── linalg-inverse ────────────────────────────────────────────────────────────

def _gen_linalg_inverse():
    """Entry of A⁻¹, entry of (A⁻¹)^T, or entry of A·A⁻¹."""
    a, b, c, d, det = _rand_inv2x2()
    # A^{-1} = (1/det) * [[d, -b], [-c, a]]
    variant = random.choice(['entry_Ainv', 'entry_AinvT', 'entry_identity'])
    if variant == 'entry_Ainv':
        # V1: entry of A^{-1}
        entries = {"(1,1)": (d, det), "(1,2)": (-b, det), "(2,1)": (-c, det), "(2,2)": (a, det)}
        label, (num, denom) = random.choice(list(entries.items()))
        ans = _frac_str(num, denom)
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(a,b,c,d)}\\). "
                f"Find the \\({label}\\) entry of \\(A^{{-1}}\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "For a 2×2 matrix, \\(A^{-1} = \\frac{1}{\\det(A)}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}\\)."},
                {"level": 2, "text": f"\\(\\det(A) = {a}\\cdot{d} - {b}\\cdot{c} = {det}\\). Form the adjugate, then divide by \\({det}\\)."},
                {"level": 3, "text": f"\\(A^{{-1}} = \\frac{{1}}{{{det}}}{_mat2(d,-b,-c,a)}\\). Entry \\({label}\\) is \\({ans}\\)."},
            ],
        }
    elif variant == 'entry_AinvT':
        # V2: entry of (A^{-1})^T  — the (r,c) entry of (A^{-1})^T = (c,r) entry of A^{-1}
        # A^{-1} rows: [(d/det, -b/det), (-c/det, a/det)]
        # (A^{-1})^T = [[d/det, -c/det], [-b/det, a/det]]
        entries_invT = {"(1,1)": (d, det), "(1,2)": (-c, det), "(2,1)": (-b, det), "(2,2)": (a, det)}
        label, (num, denom) = random.choice(list(entries_invT.items()))
        ans = _frac_str(num, denom)
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(a,b,c,d)}\\). "
                f"Find the \\({label}\\) entry of \\((A^{{-1}})^T\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "\\((A^{-1})^T = (A^T)^{-1}\\). First find \\(A^{-1}\\), then transpose it."},
                {"level": 2, "text": f"\\(A^{{-1}} = \\frac{{1}}{{{det}}}{_mat2(d,-b,-c,a)}\\). Transpose this matrix."},
                {"level": 3, "text": f"\\((A^{{-1}})^T = \\frac{{1}}{{{det}}}{_mat2(d,-c,-b,a)}\\). Entry \\({label}\\) is \\({ans}\\)."},
            ],
        }
    else:
        # V3: entry of A·A^{-1} = I (identity matrix)
        r, c_idx = random.randint(0, 1), random.randint(0, 1)
        ans = 1 if r == c_idx else 0
        rc_label = f"({r+1},{c_idx+1})"
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(a,b,c,d)}\\). "
                f"What is the \\({rc_label}\\) entry of \\(A A^{{-1}}\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "By definition, \\(A A^{-1} = I\\), the identity matrix."},
                {"level": 2, "text": f"The identity matrix has 1s on the diagonal and 0s elsewhere."},
                {"level": 3, "text": f"Entry \\({rc_label}\\) of \\(I\\) is \\({ans}\\)."},
            ],
        }


# ── linalg-linear-systems ─────────────────────────────────────────────────────

def _gen_linalg_linear_systems():
    """Solve a 2x2 linear system using elimination or substitution."""
    x = random.randint(-3, 4)
    y = random.randint(-3, 4)
    a = random.randint(1, 3); b = random.randint(1, 3)
    c = random.randint(1, 3); d = random.randint(1, 3)
    while a*d - b*c == 0:
        c = random.randint(1, 3); d = random.randint(1, 3)
    r1 = a*x + b*y; r2 = c*x + d*y
    ask_x = random.randint(0, 1)
    ans = x if ask_x else y
    var = "x" if ask_x else "y"
    b_str = f"+ {b}y" if b > 1 else ("+ y" if b == 1 else (f"- {abs(b)}y" if b < -1 else "- y"))
    d_str = f"+ {d}y" if d > 1 else ("+ y" if d == 1 else (f"- {abs(d)}y" if d < -1 else "- y"))
    ax_str = f"{a}x" if a != 1 else "x"
    cx_str = f"{c}x" if c != 1 else "x"
    return {
        "problem_text": (
            f"Solve the system: \\({ax_str} {b_str} = {r1}\\) and \\({cx_str} {d_str} = {r2}\\). "
            f"Find \\({var}\\)."
        ),
        "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Use elimination: multiply equations to match a coefficient, then subtract to eliminate a variable."},
            {"level": 2, "text": f"Eliminate \\({'y' if ask_x else 'x'}\\) by multiplying equations appropriately and subtracting."},
            {"level": 3, "text": f"The solution is \\(x={x}\\), \\(y={y}\\). So \\({var} = {ans}\\)."},
        ],
    }


# ── linalg-span-independence ──────────────────────────────────────────────────

def _gen_linalg_span_independence():
    """Linear dependence/independence: find scalar c, check independence, or find c for zero combo."""
    variant = random.choice(['dep_scalar', 'indep_check', 'zero_combo'])
    if variant == 'dep_scalar':
        # V1: find c such that v2 = c*v1 (dependent case)
        c = random.choice([-3, -2, -1, 2, 3])
        v1 = [random.randint(1, 4), random.randint(1, 4)]
        v2 = [c*v1[0], c*v1[1]]
        return {
            "problem_text": (
                f"The vectors \\(\\mathbf{{v}}_1 = {_vec2(*v1)}\\) and "
                f"\\(\\mathbf{{v}}_2 = {_vec2(*v2)}\\) are linearly dependent. "
                f"Find the scalar \\(c\\) such that \\(\\mathbf{{v}}_2 = c\\,\\mathbf{{v}}_1\\)."
            ),
            "correct_answer": str(c), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "If \\(\\mathbf{v}_2 = c\\,\\mathbf{v}_1\\), every component of \\(\\mathbf{v}_2\\) equals \\(c\\) times the corresponding component of \\(\\mathbf{v}_1\\)."},
                {"level": 2, "text": f"Divide the first component: \\({v2[0]} \\div {v1[0]}\\)."},
                {"level": 3, "text": f"\\(c = {v2[0]} / {v1[0]} = {c}\\). Check: \\({c} \\cdot {v1[1]} = {v2[1]}\\). ✓"},
            ],
        }
    elif variant == 'indep_check':
        # V2: are these vectors linearly independent? (answer: 1=yes, 0=no)
        # Make them independent: pick v1, then pick v2 that is NOT a multiple
        v1 = [random.randint(1, 3), random.randint(1, 3)]
        # v2 must not be k*v1 for any scalar k
        v2 = [random.randint(1, 3), random.randint(1, 3)]
        while v1[1] * v2[0] == v1[0] * v2[1]:  # cross-product == 0 means dependent
            v2 = [random.randint(1, 3), random.randint(1, 3)]
        ans = 1
        return {
            "problem_text": (
                f"Are \\(\\mathbf{{v}}_1 = {_vec2(*v1)}\\) and "
                f"\\(\\mathbf{{v}}_2 = {_vec2(*v2)}\\) linearly independent? "
                f"Enter 1 for yes, 0 for no."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Two vectors in \\(\\mathbb{R}^2\\) are linearly independent iff neither is a scalar multiple of the other."},
                {"level": 2, "text": f"Check: is \\({v2[0]}/{v1[0]}\\) equal to \\({v2[1]}/{v1[1]}\\)?"},
                {"level": 3, "text": f"\\({v1[1]*v2[0]} \\neq {v1[0]*v2[1]}\\), so the vectors are linearly independent. Answer: 1."},
            ],
        }
    else:
        # V3: find scalar c such that c*v1 + v2 = 0 (where v2 = -k*v1, so c = k)
        k = random.choice([2, 3, 4])
        v1 = [random.randint(1, 3), random.randint(1, 3)]
        v2 = [-k*v1[0], -k*v1[1]]
        ans = k
        return {
            "problem_text": (
                f"Find the scalar \\(c\\) such that "
                f"\\(c\\,\\mathbf{{v}}_1 + \\mathbf{{v}}_2 = \\mathbf{{0}}\\), "
                f"where \\(\\mathbf{{v}}_1 = {_vec2(*v1)}\\) and \\(\\mathbf{{v}}_2 = {_vec2(*v2)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(c\\,\\mathbf{v}_1 + \\mathbf{v}_2 = \\mathbf{0}\\) means \\(c\\,\\mathbf{v}_1 = -\\mathbf{v}_2\\), so \\(c = -v_{2,1}/v_{1,1}\\)."},
                {"level": 2, "text": f"Compute \\(c = -{v2[0]} \\div {v1[0]}\\)."},
                {"level": 3, "text": f"\\(c = {-v2[0]} / {v1[0]} = {ans}\\)."},
            ],
        }


# ── linalg-subspaces ──────────────────────────────────────────────────────────

def _gen_linalg_subspaces():
    """Column space dimension, null space dimension, or number of pivot columns."""
    variant = random.choice(['col_space', 'null_space', 'pivot_cols'])
    if variant == 'col_space':
        # V1: dimension of column space (rank)
        choice = random.randint(0, 1)
        if choice == 0:
            # rank-2 matrix
            a = random.randint(1, 3); b = 0; c = 0; d = random.randint(1, 3)
            ans = 2
            hint3 = f"\\(\\det = {a*d} \\neq 0\\), so the columns are independent and \\(\\dim(\\text{{col}}) = 2\\)."
        else:
            # rank-1 matrix
            a = random.randint(1, 3); k = random.randint(2, 4)
            b = k*a; c = random.randint(1, 3); d = k*c
            ans = 1
            hint3 = f"Column 2 = {k} × column 1, so rank = 1."
        return {
            "problem_text": (
                f"What is the dimension of the column space of "
                f"\\(A = {_mat2(a,b,c,d)}\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The dimension of the column space equals the rank (number of pivot columns after row reduction)."},
                {"level": 2, "text": "Check whether the columns are linearly independent by computing the determinant."},
                {"level": 3, "text": hint3},
            ],
        }
    elif variant == 'null_space':
        # V2: dimension of null space (nullity = n - rank)
        # Use rank-1 2x2 matrix → nullity = 2 - 1 = 1
        a = random.randint(1, 3); k = random.randint(2, 4)
        b = k*a; c = random.randint(1, 3); d = k*c
        ans = 1   # nullity
        return {
            "problem_text": (
                f"What is the dimension of the null space of "
                f"\\(A = {_mat2(a,b,c,d)}\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "By the Rank-Nullity Theorem, \\(\\text{nullity} = n - \\text{rank}\\) where \\(n\\) is the number of columns."},
                {"level": 2, "text": f"Column 2 = {k} × column 1, so rank = 1. Then nullity = 2 − 1."},
                {"level": 3, "text": f"\\(\\text{{nullity}} = 2 - 1 = 1\\)."},
            ],
        }
    else:
        # V3: how many pivot columns does A have?
        choice = random.randint(0, 1)
        if choice == 0:
            # rank-2 (2 pivots)
            a = random.randint(1, 3); b = 0; c = 0; d = random.randint(1, 3)
            ans = 2
            hint3 = f"\\(\\det = {a*d} \\neq 0\\), so there are 2 pivot columns."
        else:
            # rank-1 (1 pivot)
            a = random.randint(1, 3); k = random.randint(2, 4)
            b = k*a; c = random.randint(1, 3); d = k*c
            ans = 1
            hint3 = f"Column 2 = {k} × column 1, so only 1 pivot column."
        return {
            "problem_text": (
                f"How many pivot columns does "
                f"\\(A = {_mat2(a,b,c,d)}\\) have?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The number of pivot columns equals the rank of the matrix."},
                {"level": 2, "text": "Row-reduce \\(A\\) and count the leading 1s."},
                {"level": 3, "text": hint3},
            ],
        }


# ── linalg-rank-nullity ───────────────────────────────────────────────────────

def _gen_linalg_rank_nullity():
    """Rank-nullity theorem: find nullity, rank, or nullity of A^T."""
    n = random.randint(3, 5)   # number of columns
    rank = random.randint(1, n-1)
    nullity = n - rank
    variant = random.choice(['find_nullity', 'find_rank', 'nullity_AT'])
    if variant == 'find_nullity':
        # V1: given rank and cols, find nullity
        return {
            "problem_text": (
                f"A matrix has \\({n}\\) columns and rank \\({rank}\\). "
                f"What is the nullity of the matrix?"
            ),
            "correct_answer": str(nullity), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Rank-Nullity Theorem: \\(\\text{rank} + \\text{nullity} = n\\) (number of columns)."},
                {"level": 2, "text": f"\\(\\text{{nullity}} = {n} - \\text{{rank}} = {n} - {rank}\\)."},
                {"level": 3, "text": f"\\(\\text{{nullity}} = {n} - {rank} = {nullity}\\)."},
            ],
        }
    elif variant == 'find_rank':
        # V2: given nullity and cols, find rank
        return {
            "problem_text": (
                f"A matrix has \\({n}\\) columns and nullity \\({nullity}\\). "
                f"What is the rank of the matrix?"
            ),
            "correct_answer": str(rank), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Rank-Nullity Theorem: \\(\\text{rank} + \\text{nullity} = n\\) (number of columns)."},
                {"level": 2, "text": f"\\(\\text{{rank}} = {n} - \\text{{nullity}} = {n} - {nullity}\\)."},
                {"level": 3, "text": f"\\(\\text{{rank}} = {n} - {nullity} = {rank}\\)."},
            ],
        }
    else:
        # V3: find nullity of A^T
        # A is m×n with given rank. A^T is n×m. nullity(A^T) = m - rank(A^T) = m - rank(A).
        m = random.randint(rank, rank + 3)   # rows ≥ rank
        nullity_AT = m - rank
        return {
            "problem_text": (
                f"A matrix has \\({m}\\) rows, \\({n}\\) columns, and rank \\({rank}\\). "
                f"What is the nullity of \\(A^T\\)?"
            ),
            "correct_answer": str(nullity_AT), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(A^T\\) has \\(m\\) columns (where \\(m\\) = rows of \\(A\\)). \\(\\text{nullity}(A^T) = m - \\text{rank}(A^T) = m - \\text{rank}(A)\\)."},
                {"level": 2, "text": f"\\(A^T\\) has \\({m}\\) columns and rank \\({rank}\\)."},
                {"level": 3, "text": f"\\(\\text{{nullity}}(A^T) = {m} - {rank} = {nullity_AT}\\)."},
            ],
        }


# ── linalg-linear-transforms ─────────────────────────────────────────────────

def _gen_linalg_linear_transforms():
    """Apply T(x) = Ax: find a component of T(v), ||T(v)||², or an entry of matrix A."""
    A = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
    x = [random.randint(-3, 3) for _ in range(2)]
    result = [sum(A[i][k]*x[k] for k in range(2)) for i in range(2)]
    variant = random.choice(['component', 'norm_sq', 'matrix_entry'])
    if variant == 'component':
        # V1: find component r of T(v)
        r = random.randint(0, 1)
        ans = result[r]
        return {
            "problem_text": (
                f"The linear transformation \\(T: \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2\\) is defined by "
                f"\\(T(\\mathbf{{x}}) = A\\mathbf{{x}}\\) where \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find component {r+1} of \\(T{_vec2(*x)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Compute \\(A\\mathbf{x}\\) by matrix-vector multiplication: component \\(i\\) is the dot product of row \\(i\\) of \\(A\\) with \\(\\mathbf{x}\\)."},
                {"level": 2, "text": f"Row {r+1} of \\(A\\) is \\(({A[r][0]}, {A[r][1]})\\). Dot with \\(({x[0]}, {x[1]})\\)."},
                {"level": 3, "text": f"\\({A[r][0]} \\cdot {x[0]} + {A[r][1]} \\cdot {x[1]} = {A[r][0]*x[0]} + {A[r][1]*x[1]} = {ans}\\)."},
            ],
        }
    elif variant == 'norm_sq':
        # V2: find ||T(v)||²
        ans = result[0]**2 + result[1]**2
        return {
            "problem_text": (
                f"The linear transformation \\(T: \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2\\) is defined by "
                f"\\(T(\\mathbf{{x}}) = A\\mathbf{{x}}\\) where \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\). "
                f"Find \\(\\|T{_vec2(*x)}\\|^2\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "First compute \\(T(\\mathbf{v}) = A\\mathbf{v}\\), then square each component and sum."},
                {"level": 2, "text": f"\\(T(\\mathbf{{v}}) = {_vec2(*result)}\\). Then \\(\\|T(\\mathbf{{v}})\\|^2 = {result[0]}^2 + {result[1]}^2\\)."},
                {"level": 3, "text": f"\\({result[0]**2} + {result[1]**2} = {ans}\\)."},
            ],
        }
    else:
        # V3: find the (r,c) entry of the transformation matrix A
        r, c = random.randint(0, 1), random.randint(0, 1)
        ans = A[r][c]
        rc_label = f"({r+1},{c+1})"
        return {
            "problem_text": (
                f"The linear transformation \\(T: \\mathbb{{R}}^2 \\to \\mathbb{{R}}^2\\) is given by "
                f"\\(T(\\mathbf{{x}}) = A\\mathbf{{x}}\\) where \\(A = {_mat2(*[A[i][j] for i in range(2) for j in range(2)])}\\). "
                f"What is the \\({rc_label}\\) entry of the transformation matrix \\(A\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Read the entry directly from the matrix \\(A\\)."},
                {"level": 2, "text": f"Row {r+1}, column {c+1} of \\(A\\)."},
                {"level": 3, "text": f"The \\({rc_label}\\) entry is \\({ans}\\)."},
            ],
        }


# ── linalg-change-basis ───────────────────────────────────────────────────────

def _gen_linalg_change_basis():
    """Coordinate of a vector in a new basis: first coord, second coord, or sum of coords."""
    # Use basis B = {(a,0), (0,d)} (scaled standard basis) for clean coordinates
    a = random.randint(1, 3)
    d = random.randint(1, 3)
    # v = c1*(a,0) + c2*(0,d)  → c1 = v[0]/a, c2 = v[1]/d
    c1 = random.randint(-3, 4)
    c2 = random.randint(-3, 4)
    v = [c1*a, c2*d]
    variant = random.choice(['first_coord', 'second_coord', 'sum_coords'])
    if variant == 'first_coord':
        # V1: first B-coordinate
        return {
            "problem_text": (
                f"In the basis \\(\\mathcal{{B}} = \\left\\{{{_vec2(a,0)},\\, {_vec2(0,d)}\\right\\}}\\), "
                f"express \\(\\mathbf{{v}} = {_vec2(*v)}\\) in \\(\\mathcal{{B}}\\)-coordinates. "
                f"What is the first coordinate?"
            ),
            "correct_answer": str(c1), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Find scalars \\(c_1, c_2\\) such that \\(\\mathbf{v} = c_1 \\mathbf{b}_1 + c_2 \\mathbf{b}_2\\)."},
                {"level": 2, "text": f"The basis vectors are \\(({a},0)\\) and \\((0,{d})\\). The first coordinate is determined by dividing the first component of \\(\\mathbf{{v}}\\) by {a}."},
                {"level": 3, "text": f"\\(c_1 = {v[0]} \\div {a} = {c1}\\)."},
            ],
        }
    elif variant == 'second_coord':
        # V2: second B-coordinate
        return {
            "problem_text": (
                f"In the basis \\(\\mathcal{{B}} = \\left\\{{{_vec2(a,0)},\\, {_vec2(0,d)}\\right\\}}\\), "
                f"express \\(\\mathbf{{v}} = {_vec2(*v)}\\) in \\(\\mathcal{{B}}\\)-coordinates. "
                f"What is the second coordinate?"
            ),
            "correct_answer": str(c2), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Find scalars \\(c_1, c_2\\) such that \\(\\mathbf{v} = c_1 \\mathbf{b}_1 + c_2 \\mathbf{b}_2\\)."},
                {"level": 2, "text": f"The basis vectors are \\(({a},0)\\) and \\((0,{d})\\). The second coordinate is determined by dividing the second component of \\(\\mathbf{{v}}\\) by {d}."},
                {"level": 3, "text": f"\\(c_2 = {v[1]} \\div {d} = {c2}\\)."},
            ],
        }
    else:
        # V3: sum of B-coordinates
        ans = c1 + c2
        return {
            "problem_text": (
                f"In the basis \\(\\mathcal{{B}} = \\left\\{{{_vec2(a,0)},\\, {_vec2(0,d)}\\right\\}}\\), "
                f"express \\(\\mathbf{{v}} = {_vec2(*v)}\\) in \\(\\mathcal{{B}}\\)-coordinates. "
                f"What is the sum of the \\(\\mathcal{{B}}\\)-coordinates of \\(\\mathbf{{v}}\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Find both \\(c_1\\) and \\(c_2\\) such that \\(\\mathbf{v} = c_1 \\mathbf{b}_1 + c_2 \\mathbf{b}_2\\), then add them."},
                {"level": 2, "text": f"\\(c_1 = {v[0]} \\div {a} = {c1}\\) and \\(c_2 = {v[1]} \\div {d} = {c2}\\)."},
                {"level": 3, "text": f"\\(c_1 + c_2 = {c1} + {c2} = {ans}\\)."},
            ],
        }


# ── linalg-eigenvalues ────────────────────────────────────────────────────────

def _gen_linalg_eigenvalues():
    """Find an eigenvalue of a 2x2 matrix: largest, smallest, or product."""
    l1 = random.randint(-3, 4)
    l2 = random.randint(-3, 4)
    while l1 == l2: l2 = random.randint(-3, 4)
    # Build matrix: diagonal or perturbed (both have eigenvalues l1, l2)
    choice = random.randint(0, 1)
    if choice == 0:
        a, b, c, d = l1, 0, 0, l2
    else:
        k = random.randint(1, 2)
        a, b, c, d = l1+k, k, -k, l2-k
    variant = random.choice(['larger', 'smaller', 'product'])
    if variant == 'larger':
        # V1: larger eigenvalue
        lam = max(l1, l2)
        return {
            "problem_text": (
                f"Find the larger eigenvalue of \\(A = {_mat2(a,b,c,d)}\\). "
                f"(Hint: solve \\(\\det(A - \\lambda I) = 0\\).)"
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "The characteristic equation is \\(\\det(A - \\lambda I) = 0\\). Expand the determinant."},
                {"level": 2, "text": f"\\(\\det\\begin{{pmatrix}}{a}-\\lambda & {b} \\\\ {c} & {d}-\\lambda\\end{{pmatrix}} = ({a}-\\lambda)({d}-\\lambda) - ({b})({c}) = 0\\)."},
                {"level": 3, "text": f"The eigenvalues are \\(\\lambda = {l1}\\) and \\(\\lambda = {l2}\\). The larger is \\({lam}\\)."},
            ],
        }
    elif variant == 'smaller':
        # V2: smaller eigenvalue
        lam = min(l1, l2)
        return {
            "problem_text": (
                f"Find the smaller eigenvalue of \\(A = {_mat2(a,b,c,d)}\\). "
                f"(Hint: solve \\(\\det(A - \\lambda I) = 0\\).)"
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "The characteristic equation is \\(\\det(A - \\lambda I) = 0\\). Expand the determinant."},
                {"level": 2, "text": f"\\(\\det\\begin{{pmatrix}}{a}-\\lambda & {b} \\\\ {c} & {d}-\\lambda\\end{{pmatrix}} = ({a}-\\lambda)({d}-\\lambda) - ({b})({c}) = 0\\)."},
                {"level": 3, "text": f"The eigenvalues are \\(\\lambda = {l1}\\) and \\(\\lambda = {l2}\\). The smaller is \\({lam}\\)."},
            ],
        }
    else:
        # V3: product of eigenvalues (= det(A))
        lam = l1 * l2
        return {
            "problem_text": (
                f"Find the product of the eigenvalues of \\(A = {_mat2(a,b,c,d)}\\). "
                f"(Hint: solve \\(\\det(A - \\lambda I) = 0\\).)"
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "The product of the eigenvalues equals \\(\\det(A)\\)."},
                {"level": 2, "text": f"Find the eigenvalues by solving \\(\\det(A - \\lambda I) = 0\\), or just compute \\(\\det(A) = {a}\\cdot{d} - {b}\\cdot{c}\\)."},
                {"level": 3, "text": f"The eigenvalues are \\({l1}\\) and \\({l2}\\). Their product = \\({l1} \\times {l2} = {lam}\\)."},
            ],
        }


# ── linalg-diagonalization ────────────────────────────────────────────────────

def _gen_linalg_diagonalization():
    """Given a diagonal matrix, find an entry of A^n, trace of A^n, or entry of A^n + cI."""
    l1 = random.choice([2, 3])
    l2 = random.choice([-1, 0, 1])
    n  = random.randint(2, 4)
    lams = [l1, l2]
    variant = random.choice(['entry_An', 'trace_An', 'entry_An_shift'])
    if variant == 'entry_An':
        # V1: specific diagonal entry of A^n
        r = random.randint(0, 1)
        ans = lams[r] ** n
        rc_str = '1,1' if r == 0 else '2,2'
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(l1,0,0,l2)}\\) (a diagonal matrix with eigenvalues \\({l1}\\) and \\({l2}\\)). "
                f"Find the \\(({rc_str})\\) entry of \\(A^{{{n}}}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "For a diagonal matrix, \\(A^n\\) is diagonal with each diagonal entry raised to the \\(n\\)-th power."},
                {"level": 2, "text": f"The \\(({rc_str})\\) entry of \\(A\\) is \\({lams[r]}\\). Raise it to the power \\({n}\\)."},
                {"level": 3, "text": f"\\({lams[r]}^{{{n}}} = {ans}\\)."},
            ],
        }
    elif variant == 'trace_An':
        # V2: trace of A^n = l1^n + l2^n
        ans = l1**n + l2**n
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(l1,0,0,l2)}\\) (a diagonal matrix with eigenvalues \\({l1}\\) and \\({l2}\\)). "
                f"Find the trace of \\(A^{{{n}}}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "For a diagonal matrix, \\(A^n\\) is diagonal. The trace is the sum of the diagonal entries."},
                {"level": 2, "text": f"\\(\\text{{tr}}(A^{{{n}}}) = {l1}^{{{n}}} + {l2}^{{{n}}} = {l1**n} + {l2**n}\\)."},
                {"level": 3, "text": f"\\(\\text{{tr}}(A^{{{n}}}) = {l1**n} + {l2**n} = {ans}\\)."},
            ],
        }
    else:
        # V3: entry of A^n + c*I
        c = random.randint(1, 4)
        r = random.randint(0, 1)
        ans = lams[r]**n + c
        rc_str = '1,1' if r == 0 else '2,2'
        return {
            "problem_text": (
                f"Let \\(A = {_mat2(l1,0,0,l2)}\\) (a diagonal matrix with eigenvalues \\({l1}\\) and \\({l2}\\)). "
                f"Find the \\(({rc_str})\\) entry of \\(A^{{{n}}} + {c}I\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "For a diagonal matrix, \\(A^n + cI\\) is diagonal. Compute \\(A^n\\) first, then add \\(c\\) to each diagonal entry."},
                {"level": 2, "text": f"The \\(({rc_str})\\) entry of \\(A^{{{n}}}\\) is \\({lams[r]}^{{{n}}} = {lams[r]**n}\\). Adding \\({c}\\) gives \\({lams[r]**n} + {c}\\)."},
                {"level": 3, "text": f"\\({lams[r]}^{{{n}}} + {c} = {lams[r]**n} + {c} = {ans}\\)."},
            ],
        }


# ── linalg-symmetric-spectral ─────────────────────────────────────────────────

def _gen_linalg_symmetric_spectral():
    """Eigenvalue of a 2x2 symmetric matrix: larger, smaller, or sum of eigenvalues."""
    # [[a,b],[b,a]] has eigenvalues a+b (larger) and a-b (smaller when b>0)
    a = random.randint(1, 4)
    b = random.randint(1, 3)
    lam1 = a + b; lam2 = a - b
    variant = random.choice(['larger', 'smaller', 'sum'])
    if variant == 'larger':
        # V1: larger eigenvalue
        return {
            "problem_text": (
                f"Find the larger eigenvalue of the symmetric matrix "
                f"\\(A = {_mat2(a,b,b,a)}\\)."
            ),
            "correct_answer": str(lam1), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Use the characteristic equation \\(\\det(A - \\lambda I) = 0\\)."},
                {"level": 2, "text": f"\\(({a}-\\lambda)^2 - {b}^2 = 0 \\Rightarrow ({a}-\\lambda) = \\pm {b}\\)."},
                {"level": 3, "text": f"Eigenvalues: \\({a}+{b} = {lam1}\\) and \\({a}-{b} = {lam2}\\). Larger: \\({lam1}\\)."},
            ],
        }
    elif variant == 'smaller':
        # V2: smaller eigenvalue
        return {
            "problem_text": (
                f"Find the smaller eigenvalue of the symmetric matrix "
                f"\\(A = {_mat2(a,b,b,a)}\\)."
            ),
            "correct_answer": str(lam2), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Use the characteristic equation \\(\\det(A - \\lambda I) = 0\\)."},
                {"level": 2, "text": f"\\(({a}-\\lambda)^2 - {b}^2 = 0 \\Rightarrow ({a}-\\lambda) = \\pm {b}\\)."},
                {"level": 3, "text": f"Eigenvalues: \\({a}+{b} = {lam1}\\) and \\({a}-{b} = {lam2}\\). Smaller: \\({lam2}\\)."},
            ],
        }
    else:
        # V3: sum of eigenvalues = trace of A = 2a
        ans = lam1 + lam2   # = 2a
        return {
            "problem_text": (
                f"Find the sum of the eigenvalues of the symmetric matrix "
                f"\\(A = {_mat2(a,b,b,a)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The sum of the eigenvalues equals the trace of \\(A\\) (sum of diagonal entries)."},
                {"level": 2, "text": f"\\(\\text{{tr}}(A) = {a} + {a} = {ans}\\). Alternatively, find both eigenvalues and add."},
                {"level": 3, "text": f"Eigenvalues \\({lam1}\\) and \\({lam2}\\). Sum = \\({lam1} + {lam2} = {ans}\\)."},
            ],
        }


# ── linalg-orthogonality ──────────────────────────────────────────────────────

def _gen_linalg_orthogonality():
    """Orthogonality: find missing component, check if orthogonal, or find k for orthogonality."""
    variant = random.choice(['missing_comp', 'check_orth', 'find_k'])
    if variant == 'missing_comp':
        # V1: find missing component so vectors are orthogonal
        a = random.randint(1, 4)
        b = random.choice([-3,-2,-1,1,2,3])
        c_num = random.randint(1, 4)
        prod = a * c_num
        if prod % b != 0:
            c_num = abs(b)
            prod = a * c_num
        ans = -prod // b
        return {
            "problem_text": (
                f"Vectors \\(\\mathbf{{u}} = {_vec2(a,b)}\\) and \\(\\mathbf{{v}} = {_vec2(c_num,'?')}\\) "
                f"are orthogonal. Find the missing component \\(?\\) of \\(\\mathbf{{v}}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Two vectors are orthogonal iff their dot product is zero."},
                {"level": 2, "text": f"Set \\({a} \\cdot {c_num} + {b} \\cdot ? = 0\\) and solve for \\(?\\)."},
                {"level": 3, "text": f"\\({prod} + {b} \\cdot ? = 0 \\Rightarrow ? = {ans}\\)."},
            ],
        }
    elif variant == 'check_orth':
        # V2: are these vectors orthogonal? (1=yes, 0=no)
        # Half the time make them orthogonal, half not
        if random.randint(0, 1) == 0:
            # orthogonal: u = (a, b), v = (-b, a)
            a = random.randint(1, 3); b = random.randint(1, 3)
            u = [a, b]; v = [-b, a]
            ans = 1
        else:
            # not orthogonal: u = (a, b), v = (a, b) (parallel)
            a = random.randint(1, 3); b = random.randint(1, 3)
            u = [a, b]; v = [a+1, b]
            ans = 0
        dot = u[0]*v[0] + u[1]*v[1]
        return {
            "problem_text": (
                f"Are \\(\\mathbf{{u}} = {_vec2(*u)}\\) and \\(\\mathbf{{v}} = {_vec2(*v)}\\) orthogonal? "
                f"Enter 1 for yes, 0 for no."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Two vectors are orthogonal iff their dot product is zero."},
                {"level": 2, "text": f"Compute \\(\\mathbf{{u}} \\cdot \\mathbf{{v}} = {u[0]} \\cdot {v[0]} + {u[1]} \\cdot {v[1]} = {dot}\\)."},
                {"level": 3, "text": f"Dot product = \\({dot}\\). {'Zero, so they ARE orthogonal. Answer: 1.' if ans==1 else 'Nonzero, so they are NOT orthogonal. Answer: 0.'}"},
            ],
        }
    else:
        # V3: find k such that (k, a) and (b, c) are orthogonal
        # k*b + a*c = 0 → k = -a*c / b; pick b != 0 and ensure integer
        b = random.choice([-3,-2,-1,1,2,3])
        a = random.randint(1, 4)
        c = random.randint(1, 4)
        prod = a * c
        # ensure divisible by b
        if prod % b != 0:
            c = abs(b)
            prod = a * c
        k = -prod // b
        return {
            "problem_text": (
                f"Find the value of \\(k\\) such that \\({_vec2('k', a)}\\) and "
                f"\\({_vec2(b, c)}\\) are orthogonal."
            ),
            "correct_answer": str(k), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Two vectors are orthogonal iff their dot product is zero."},
                {"level": 2, "text": f"Set \\(k \\cdot {b} + {a} \\cdot {c} = 0\\) and solve for \\(k\\)."},
                {"level": 3, "text": f"\\(k = -{prod} / {b} = {k}\\)."},
            ],
        }


# ── linalg-gram-schmidt ───────────────────────────────────────────────────────

def _gen_linalg_gram_schmidt():
    """Gram-Schmidt: find projection coefficient, first component of projection, or ||u1||²."""
    u1 = [random.randint(1, 3), random.randint(1, 3)]
    c = random.randint(1, 3)  # projection coefficient numerator
    u1_norm_sq = u1[0]**2 + u1[1]**2
    t = random.randint(1, 2)
    v2 = [c*u1[0] + t*(-u1[1]), c*u1[1] + t*(u1[0])]
    dot = v2[0]*u1[0] + v2[1]*u1[1]
    frac = Fraction(dot, u1_norm_sq)
    coeff_ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    variant = random.choice(['proj_coeff', 'proj_first_comp', 'u1_norm_sq'])
    if variant == 'proj_coeff':
        # V1: projection coefficient
        return {
            "problem_text": (
                f"In the Gram-Schmidt process, let \\(\\mathbf{{u}}_1 = {_vec2(*u1)}\\). "
                f"Find the projection coefficient \\(\\frac{{\\mathbf{{v}}_2 \\cdot \\mathbf{{u}}_1}}{{\\mathbf{{u}}_1 \\cdot \\mathbf{{u}}_1}}\\) "
                f"for \\(\\mathbf{{v}}_2 = {_vec2(*v2)}\\)."
            ),
            "correct_answer": coeff_ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Compute the dot products \\(\\mathbf{v}_2 \\cdot \\mathbf{u}_1\\) and \\(\\mathbf{u}_1 \\cdot \\mathbf{u}_1\\)."},
                {"level": 2, "text": f"\\(\\mathbf{{v}}_2 \\cdot \\mathbf{{u}}_1 = {v2[0]*u1[0]} + {v2[1]*u1[1]} = {dot}\\). \\(\\|\\mathbf{{u}}_1\\|^2 = {u1[0]**2} + {u1[1]**2} = {u1_norm_sq}\\)."},
                {"level": 3, "text": f"Coefficient \\(= \\frac{{{dot}}}{{{u1_norm_sq}}} = {coeff_ans}\\)."},
            ],
        }
    elif variant == 'proj_first_comp':
        # V2: first component of the projection of v2 onto u1
        # proj = coeff * u1, first component = coeff * u1[0] = (dot/u1_norm_sq) * u1[0]
        proj_num = dot * u1[0]   # numerator before reduction
        proj_frac = Fraction(proj_num, u1_norm_sq)
        proj_ans = str(proj_frac.numerator) if proj_frac.denominator == 1 else f"{proj_frac.numerator}/{proj_frac.denominator}"
        return {
            "problem_text": (
                f"In the Gram-Schmidt process, let \\(\\mathbf{{u}}_1 = {_vec2(*u1)}\\) "
                f"and \\(\\mathbf{{v}}_2 = {_vec2(*v2)}\\). "
                f"Find the first component of the projection of \\(\\mathbf{{v}}_2\\) onto \\(\\mathbf{{u}}_1\\)."
            ),
            "correct_answer": proj_ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "The projection is \\(\\text{proj}_{\\mathbf{u}_1}\\mathbf{v}_2 = \\frac{\\mathbf{v}_2 \\cdot \\mathbf{u}_1}{\\mathbf{u}_1 \\cdot \\mathbf{u}_1} \\mathbf{u}_1\\)."},
                {"level": 2, "text": f"Projection coefficient = \\({coeff_ans}\\). Multiply by the first component of \\(\\mathbf{{u}}_1 = {u1[0]}\\)."},
                {"level": 3, "text": f"First component of projection = \\({coeff_ans} \\times {u1[0]} = {proj_ans}\\)."},
            ],
        }
    else:
        # V3: find ||u1||²
        ans = u1_norm_sq
        return {
            "problem_text": (
                f"In the Gram-Schmidt process, what is \\(\\|\\mathbf{{u}}_1\\|^2\\) "
                f"for \\(\\mathbf{{u}}_1 = {_vec2(*u1)}\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\|\\mathbf{u}_1\\|^2 = u_{1,1}^2 + u_{1,2}^2\\)."},
                {"level": 2, "text": f"\\({u1[0]}^2 + {u1[1]}^2 = {u1[0]**2} + {u1[1]**2}\\)."},
                {"level": 3, "text": f"\\(\\|\\mathbf{{u}}_1\\|^2 = {ans}\\)."},
            ],
        }


# ── linalg-orthogonal-projection ──────────────────────────────────────────────

def _gen_linalg_orthogonal_projection():
    """Orthogonal projection of b onto a: first/second component, or squared length of projection."""
    a = [random.randint(1, 3), 0]   # keep simple: a = (k, 0) for clean projection
    k = a[0]
    b = [random.randint(-3, 4), random.randint(-3, 4)]
    # proj_a(b) = (b·a / a·a) * a = (b[0]/k) * (k, 0) = (b[0], 0)
    proj = [b[0], 0]
    variant = random.choice(['first_comp', 'second_comp', 'length_sq'])
    if variant == 'first_comp':
        # V1: first component of projection
        ans = proj[0]
        return {
            "problem_text": (
                f"Find the first component of the orthogonal projection of "
                f"\\(\\mathbf{{b}} = {_vec2(*b)}\\) onto \\(\\mathbf{{a}} = {_vec2(*a)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(\\text{proj}_{\\mathbf{a}} \\mathbf{b} = \\frac{\\mathbf{b} \\cdot \\mathbf{a}}{\\mathbf{a} \\cdot \\mathbf{a}} \\mathbf{a}\\)."},
                {"level": 2, "text": f"\\(\\mathbf{{b}} \\cdot \\mathbf{{a}} = {b[0]*k}\\). \\(\\mathbf{{a}} \\cdot \\mathbf{{a}} = {k**2}\\). Scalar = \\({b[0]}/{k}\\). Projection = scalar \\(\\times\\, \\mathbf{{a}}\\)."},
                {"level": 3, "text": f"Projection \\(= {_vec2(*proj)}\\). The first component is \\({ans}\\)."},
            ],
        }
    elif variant == 'second_comp':
        # V2: second component of projection
        ans = proj[1]   # always 0 since a=(k,0)
        return {
            "problem_text": (
                f"Find the second component of the orthogonal projection of "
                f"\\(\\mathbf{{b}} = {_vec2(*b)}\\) onto \\(\\mathbf{{a}} = {_vec2(*a)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(\\text{proj}_{\\mathbf{a}} \\mathbf{b} = \\frac{\\mathbf{b} \\cdot \\mathbf{a}}{\\mathbf{a} \\cdot \\mathbf{a}} \\mathbf{a}\\)."},
                {"level": 2, "text": f"Since \\(\\mathbf{{a}} = {_vec2(*a)}\\), the projection points entirely in the first-component direction."},
                {"level": 3, "text": f"Projection \\(= {_vec2(*proj)}\\). The second component is \\({ans}\\)."},
            ],
        }
    else:
        # V3: squared length of projection = b[0]^2
        ans = proj[0]**2
        return {
            "problem_text": (
                f"Find \\(\\|\\text{{proj}}_{{\\mathbf{{a}}}} \\mathbf{{b}}\\|^2\\), "
                f"the squared length of the orthogonal projection of "
                f"\\(\\mathbf{{b}} = {_vec2(*b)}\\) onto \\(\\mathbf{{a}} = {_vec2(*a)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "First compute the projection vector, then find its squared length."},
                {"level": 2, "text": f"Projection \\(= {_vec2(*proj)}\\). Squared length = \\({proj[0]}^2 + {proj[1]}^2\\)."},
                {"level": 3, "text": f"\\(\\|\\text{{proj}}\\|^2 = {proj[0]**2} + {proj[1]**2} = {ans}\\)."},
            ],
        }


# ── linalg-least-squares ──────────────────────────────────────────────────────

def _gen_linalg_least_squares():
    """Least squares: find c_hat, the residual at first point, or predicted value at x=1."""
    x1 = random.randint(1, 3); x2 = random.randint(1, 3)
    while x2 == x1: x2 = random.randint(1, 3)
    c_true = random.randint(1, 4)
    y1 = c_true * x1 + random.choice([-1, 1])
    y2 = c_true * x2 + random.choice([-1, 1])
    num = x1*y1 + x2*y2
    denom = x1**2 + x2**2
    frac = Fraction(num, denom)
    c_hat_str = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    variant = random.choice(['find_chat', 'residual', 'predicted'])
    if variant == 'find_chat':
        # V1: find c_hat
        return {
            "problem_text": (
                f"Find the least-squares estimate \\(\\hat{{c}}\\) for the model \\(y = cx\\) "
                f"given the data points \\(({x1}, {y1})\\) and \\(({x2}, {y2})\\). "
                f"Use the normal equation \\(\\hat{{c}} = \\frac{{\\sum x_i y_i}}{{\\sum x_i^2}}\\)."
            ),
            "correct_answer": c_hat_str, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "The normal equation for \\(y = cx\\) is \\(\\hat{c} = \\frac{\\sum x_i y_i}{\\sum x_i^2}\\)."},
                {"level": 2, "text": f"Numerator: \\({x1} \\cdot {y1} + {x2} \\cdot {y2} = {num}\\). Denominator: \\({x1}^2 + {x2}^2 = {denom}\\)."},
                {"level": 3, "text": f"\\(\\hat{{c}} = \\frac{{{num}}}{{{denom}}} = {c_hat_str}\\)."},
            ],
        }
    elif variant == 'residual':
        # V2: residual at first data point: y1 - c_hat * x1
        res_frac = Fraction(y1) - frac * x1
        res_ans = str(res_frac.numerator) if res_frac.denominator == 1 else f"{res_frac.numerator}/{res_frac.denominator}"
        return {
            "problem_text": (
                f"For the least-squares fit \\(y = cx\\) through \\(({x1}, {y1})\\) and \\(({x2}, {y2})\\), "
                f"find the residual at the first data point: \\(y_1 - \\hat{{c}} x_1\\)."
            ),
            "correct_answer": res_ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "First find \\(\\hat{c}\\) using the normal equation, then compute \\(y_1 - \\hat{c} x_1\\)."},
                {"level": 2, "text": f"\\(\\hat{{c}} = {c_hat_str}\\). Residual = \\({y1} - {c_hat_str} \\cdot {x1}\\)."},
                {"level": 3, "text": f"Residual \\(= {y1} - {c_hat_str} \\cdot {x1} = {res_ans}\\)."},
            ],
        }
    else:
        # V3: predicted value at x = 1: y_hat = c_hat * 1 = c_hat
        pred_ans = c_hat_str
        return {
            "problem_text": (
                f"For the least-squares fit \\(y = cx\\) through \\(({x1}, {y1})\\) and \\(({x2}, {y2})\\), "
                f"find the predicted value \\(\\hat{{y}}\\) at \\(x = 1\\)."
            ),
            "correct_answer": pred_ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Find \\(\\hat{c}\\) using the normal equation, then evaluate \\(\\hat{y} = \\hat{c} \\cdot x\\) at \\(x=1\\)."},
                {"level": 2, "text": f"\\(\\hat{{c}} = {c_hat_str}\\). At \\(x=1\\): \\(\\hat{{y}} = {c_hat_str} \\cdot 1\\)."},
                {"level": 3, "text": f"\\(\\hat{{y}} = {pred_ans}\\)."},
            ],
        }


# ── linalg-svd ────────────────────────────────────────────────────────────────

def _gen_linalg_svd():
    """Singular values of a diagonal or rank-1 matrix: largest, nonzero, or product."""
    variant = random.choice(['largest_diag', 'nonzero_rank1', 'product_diag'])
    if variant == 'largest_diag':
        # V1: largest singular value of diagonal matrix
        s1 = random.randint(2, 5); s2 = random.randint(1, s1-1)
        ans = s1
        return {
            "problem_text": (
                f"Find the largest singular value of \\(A = {_mat2(s1,0,0,s2)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "For a diagonal matrix, the singular values are the absolute values of the diagonal entries."},
                {"level": 2, "text": f"The diagonal entries are \\({s1}\\) and \\({s2}\\). Take their absolute values."},
                {"level": 3, "text": f"Singular values: \\({s1}\\) and \\({s2}\\). The largest is \\({ans}\\)."},
            ],
        }
    elif variant == 'nonzero_rank1':
        # V2: nonzero singular value of rank-1 matrix
        a = random.randint(2, 4); b = random.randint(2, 4)
        ans = a * b
        return {
            "problem_text": (
                f"The matrix \\(A = {_mat2(a*b,0,0,0)}\\) has rank 1. "
                f"What is its nonzero singular value?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "The singular values of \\(A\\) are the square roots of the eigenvalues of \\(A^T A\\)."},
                {"level": 2, "text": f"\\(A^T A = {_mat2((a*b)**2,0,0,0)}\\). Its nonzero eigenvalue is \\({(a*b)**2}\\)."},
                {"level": 3, "text": f"Nonzero singular value \\(= \\sqrt{{{(a*b)**2}}} = {ans}\\)."},
            ],
        }
    else:
        # V3: product of singular values of diagonal matrix = |det(A)|
        s1 = random.randint(2, 5); s2 = random.randint(1, s1-1)
        ans = s1 * s2
        return {
            "problem_text": (
                f"Find the product of the singular values of \\(A = {_mat2(s1,0,0,s2)}\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "For a diagonal matrix, the singular values are the absolute values of the diagonal entries."},
                {"level": 2, "text": f"The singular values are \\({s1}\\) and \\({s2}\\). Multiply them together."},
                {"level": 3, "text": f"Product \\(= {s1} \\times {s2} = {ans}\\)."},
            ],
        }


# ── GENERATORS dict ───────────────────────────────────────────────────────────

GENERATORS = {
    "linalg-vectors":               _gen_linalg_vectors,
    "linalg-matrix-ops":            _gen_linalg_matrix_ops,
    "linalg-matrix-mult":           _gen_linalg_matrix_mult,
    "linalg-transpose":             _gen_linalg_transpose,
    "linalg-row-reduce":            _gen_linalg_row_reduce,
    "linalg-determinant":           _gen_linalg_determinant,
    "linalg-inverse":               _gen_linalg_inverse,
    "linalg-linear-systems":        _gen_linalg_linear_systems,
    "linalg-span-independence":     _gen_linalg_span_independence,
    "linalg-subspaces":             _gen_linalg_subspaces,
    "linalg-rank-nullity":          _gen_linalg_rank_nullity,
    "linalg-linear-transforms":     _gen_linalg_linear_transforms,
    "linalg-change-basis":          _gen_linalg_change_basis,
    "linalg-eigenvalues":           _gen_linalg_eigenvalues,
    "linalg-diagonalization":       _gen_linalg_diagonalization,
    "linalg-symmetric-spectral":    _gen_linalg_symmetric_spectral,
    "linalg-orthogonality":         _gen_linalg_orthogonality,
    "linalg-gram-schmidt":          _gen_linalg_gram_schmidt,
    "linalg-orthogonal-projection": _gen_linalg_orthogonal_projection,
    "linalg-least-squares":         _gen_linalg_least_squares,
    "linalg-svd":                   _gen_linalg_svd,
}
