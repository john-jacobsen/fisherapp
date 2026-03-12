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
    """Dot product or magnitude of a 2D vector."""
    if random.randint(0, 1) == 0:
        # Dot product: u·v
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
    else:
        # Squared magnitude (avoid sqrt for clean answers)
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


# ── linalg-matrix-ops ─────────────────────────────────────────────────────────

def _gen_linalg_matrix_ops():
    """Add two 2x2 matrices; return the (1,1) entry of the sum."""
    A = [[random.randint(-4, 4) for _ in range(2)] for _ in range(2)]
    B = [[random.randint(-4, 4) for _ in range(2)] for _ in range(2)]
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


# ── linalg-matrix-mult ────────────────────────────────────────────────────────

def _gen_linalg_matrix_mult():
    """Multiply two 2x2 matrices; return one entry of the product."""
    A = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
    B = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
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


# ── linalg-transpose ──────────────────────────────────────────────────────────

def _gen_linalg_transpose():
    """Transpose a 2x2 matrix; return a specific entry of A^T."""
    A = [[random.randint(-4, 4) for _ in range(2)] for _ in range(2)]
    # Transpose swaps row/col: A^T[i][j] = A[j][i]
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


# ── linalg-row-reduce ─────────────────────────────────────────────────────────

def _gen_linalg_row_reduce():
    """Row reduce an augmented matrix for a 2x2 system; return one solution variable."""
    # Build a clean 2x2 system with integer solution
    x = random.randint(-3, 4)
    y = random.randint(-3, 4)
    a = random.randint(1, 3);  b = random.randint(1, 3)
    c = random.randint(1, 3);  d = random.randint(1, 3)
    while a*d - b*c == 0:      # ensure nonsingular
        c = random.randint(1, 3); d = random.randint(1, 3)
    r1 = a*x + b*y
    r2 = c*x + d*y
    ask_x = random.randint(0, 1)
    ans = x if ask_x else y
    var = "x" if ask_x else "y"
    return {
        "problem_text": (
            f"Row-reduce the augmented matrix "
            f"\\(\\left[\\begin{{array}}{{cc|c}} {a} & {b} & {r1} \\\\ {c} & {d} & {r2} \\end{{array}}\\right]\\) "
            f"to solve for \\({var}\\)."
        ),
        "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Use row operations to create zeros below (or above) the pivot. Then back-substitute."},
            {"level": 2, "text": f"Eliminate the \\({'y' if ask_x else 'x'}\\)-term from one equation, then solve for the remaining variable."},
            {"level": 3, "text": f"The solution is \\(x={x}\\), \\(y={y}\\). So \\({var} = {ans}\\)."},
        ],
    }


# ── linalg-determinant ────────────────────────────────────────────────────────

def _gen_linalg_determinant():
    """Determinant of a 2x2 matrix."""
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


# ── linalg-inverse ────────────────────────────────────────────────────────────

def _gen_linalg_inverse():
    """Entry of the inverse of a 2x2 matrix with nonzero determinant."""
    a, b, c, d, det = _rand_inv2x2()
    # A^{-1} = (1/det) * [[d, -b], [-c, a]]
    # Pick entry and express as fraction
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
    """Determine linear dependence: the scalar c where v2 = c*v1 (dep case)."""
    # Always make them dependent so there's a clean scalar answer
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


# ── linalg-subspaces ──────────────────────────────────────────────────────────

def _gen_linalg_subspaces():
    """Dimension of the column space (= rank) of a simple matrix."""
    # Use a 2x2 or 3x2 matrix with obvious rank
    choice = random.randint(0, 1)
    if choice == 0:
        # rank-2 matrix (columns independent)
        a = random.randint(1, 3); b = 0
        c = 0;                    d = random.randint(1, 3)
        ans = 2
        return {
            "problem_text": (
                f"What is the dimension of the column space of "
                f"\\(A = {_mat2(a,b,c,d)}\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The dimension of the column space equals the rank (number of pivot columns after row reduction)."},
                {"level": 2, "text": "Check whether the columns are linearly independent by computing the determinant."},
                {"level": 3, "text": f"\\(\\det = {a*d} \\neq 0\\), so the columns are independent and \\(\\dim(\\text{{col}}) = 2\\)."},
            ],
        }
    else:
        # rank-1 matrix (second column multiple of first)
        a = random.randint(1, 3); k = random.randint(2, 4)
        b = k * a
        c = random.randint(1, 3); d = k * c
        ans = 1
        return {
            "problem_text": (
                f"What is the dimension of the column space of "
                f"\\(A = {_mat2(a,b,c,d)}\\)?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The dimension of the column space equals the rank of the matrix."},
                {"level": 2, "text": f"Check if the columns are proportional: column 2 = {k} × column 1?"},
                {"level": 3, "text": f"Yes: \\({b}/{a} = {k}\\) and \\({d}/{c} = {k}\\). The columns are linearly dependent, so rank \\(= 1\\)."},
            ],
        }


# ── linalg-rank-nullity ───────────────────────────────────────────────────────

def _gen_linalg_rank_nullity():
    """Rank-nullity theorem: given rank and number of columns, find nullity (or vice versa)."""
    n = random.randint(3, 5)   # number of columns
    rank = random.randint(1, n-1)
    nullity = n - rank
    ask_nullity = random.randint(0, 1)
    if ask_nullity:
        ans = nullity
        return {
            "problem_text": (
                f"A matrix has \\({n}\\) columns and rank \\({rank}\\). "
                f"What is the nullity of the matrix?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Rank-Nullity Theorem: \\(\\text{rank} + \\text{nullity} = n\\) (number of columns)."},
                {"level": 2, "text": f"\\(\\text{{nullity}} = {n} - \\text{{rank}} = {n} - {rank}\\)."},
                {"level": 3, "text": f"\\(\\text{{nullity}} = {n} - {rank} = {ans}\\)."},
            ],
        }
    else:
        ans = rank
        return {
            "problem_text": (
                f"A matrix has \\({n}\\) columns and nullity \\({nullity}\\). "
                f"What is the rank of the matrix?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Rank-Nullity Theorem: \\(\\text{rank} + \\text{nullity} = n\\) (number of columns)."},
                {"level": 2, "text": f"\\(\\text{{rank}} = {n} - \\text{{nullity}} = {n} - {nullity}\\)."},
                {"level": 3, "text": f"\\(\\text{{rank}} = {n} - {nullity} = {ans}\\)."},
            ],
        }


# ── linalg-linear-transforms ─────────────────────────────────────────────────

def _gen_linalg_linear_transforms():
    """Apply T(x) = Ax to a 2D vector; return one component of the result."""
    A = [[random.randint(-3, 3) for _ in range(2)] for _ in range(2)]
    x = [random.randint(-3, 3) for _ in range(2)]
    result = [sum(A[i][k]*x[k] for k in range(2)) for i in range(2)]
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


# ── linalg-change-basis ───────────────────────────────────────────────────────

def _gen_linalg_change_basis():
    """Coordinate of a vector in a new basis {b1, b2} where b1, b2 are standard-like."""
    # Use basis B = {(a,0), (0,d)} (scaled standard basis) for clean coordinates
    a = random.randint(1, 3)
    d = random.randint(1, 3)
    # v = c1*(a,0) + c2*(0,d)  → c1 = v[0]/a, c2 = v[1]/d
    c1 = random.randint(-3, 4)
    c2 = random.randint(-3, 4)
    v = [c1*a, c2*d]
    ask = random.randint(0, 1)
    ans = c1 if ask == 0 else c2
    coord_label = "first" if ask == 0 else "second"
    return {
        "problem_text": (
            f"In the basis \\(\\mathcal{{B}} = \\left\\{{{_vec2(a,0)},\\, {_vec2(0,d)}\\right\\}}\\), "
            f"express \\(\\mathbf{{v}} = {_vec2(*v)}\\) in \\(\\mathcal{{B}}\\)-coordinates. "
            f"What is the {coord_label} coordinate?"
        ),
        "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Find scalars \\(c_1, c_2\\) such that \\(\\mathbf{v} = c_1 \\mathbf{b}_1 + c_2 \\mathbf{b}_2\\)."},
            {"level": 2, "text": f"The basis vectors are \\(({a},0)\\) and \\((0,{d})\\). The {coord_label} coordinate is determined by dividing the {'first' if ask==0 else 'second'} component of \\(\\mathbf{{v}}\\) by {a if ask==0 else d}."},
            {"level": 3, "text": f"\\(c_{ask+1} = {v[ask]} \\div {a if ask==0 else d} = {ans}\\)."},
        ],
    }


# ── linalg-eigenvalues ────────────────────────────────────────────────────────

def _gen_linalg_eigenvalues():
    """Find an eigenvalue of a 2x2 matrix with integer eigenvalues."""
    # Build matrix from eigenvalues: A = P D P^{-1} with simple P
    l1 = random.randint(-3, 4)
    l2 = random.randint(-3, 4)
    while l1 == l2: l2 = random.randint(-3, 4)
    # Use diagonal matrix → eigenvalues are the diagonal entries
    # Perturb slightly: A = [[l1+k, k], [-k, l2-k]] has eigenvalues l1, l2 for any k
    # Simplest: just use diagonal
    choice = random.randint(0, 1)
    if choice == 0:
        a, b, c, d = l1, 0, 0, l2
    else:
        k = random.randint(1, 2)
        a, b, c, d = l1+k, k, -k, l2-k
    # Ask for the larger eigenvalue
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


# ── linalg-diagonalization ────────────────────────────────────────────────────

def _gen_linalg_diagonalization():
    """Given a diagonalizable matrix with known eigenvalues, find A^n entry."""
    # Use diagonal A = diag(l1, l2); A^n = diag(l1^n, l2^n)
    l1 = random.choice([2, 3])
    l2 = random.choice([-1, 0, 1])
    n  = random.randint(2, 4)
    r  = random.randint(0, 1)
    ans = (l1 if r == 0 else l2) ** n
    lams = [l1, l2]
    return {
        "problem_text": (
            f"Let \\(A = {_mat2(l1,0,0,l2)}\\) (a diagonal matrix with eigenvalues \\({l1}\\) and \\({l2}\\)). "
            f"Find the \\(({'1,1' if r==0 else '2,2'})\\) entry of \\(A^{{{n}}}\\)."
        ),
        "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "For a diagonal matrix, \\(A^n\\) is diagonal with each diagonal entry raised to the \\(n\\)-th power."},
            {"level": 2, "text": f"The \\(({'1,1' if r==0 else '2,2'})\\) entry of \\(A\\) is \\({lams[r]}\\). Raise it to the power \\({n}\\)."},
            {"level": 3, "text": f"\\({lams[r]}^{{{n}}} = {ans}\\)."},
        ],
    }


# ── linalg-symmetric-spectral ─────────────────────────────────────────────────

def _gen_linalg_symmetric_spectral():
    """Eigenvalue of a 2x2 symmetric matrix with integer eigenvalues."""
    # Symmetric: A = [[a, b],[b, d]]. Eigenvalues from char poly.
    # Use A = [[p+q, r],[r, p-q]] so eigenvalues = p ± sqrt(q^2 + r^2) — messy.
    # Instead, use A = [[a, 0],[0, d]] (diagonal symmetric) or [[a,b],[b,a]].
    # [[a,b],[b,a]] has eigenvalues a+b, a-b.
    a = random.randint(1, 4)
    b = random.randint(1, 3)
    lam1 = a + b; lam2 = a - b
    ask = random.randint(0, 1)
    ans = lam1 if ask == 0 else lam2
    return {
        "problem_text": (
            f"Find the {'larger' if ask==0 else 'smaller'} eigenvalue of the symmetric matrix "
            f"\\(A = {_mat2(a,b,b,a)}\\)."
        ),
        "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Use the characteristic equation \\(\\det(A - \\lambda I) = 0\\)."},
            {"level": 2, "text": f"\\(({a}-\\lambda)^2 - {b}^2 = 0 \\Rightarrow ({a}-\\lambda) = \\pm {b}\\)."},
            {"level": 3, "text": f"Eigenvalues: \\({a}+{b} = {lam1}\\) and \\({a}-{b} = {lam2}\\). {'Larger' if ask==0 else 'Smaller'}: \\({ans}\\)."},
        ],
    }


# ── linalg-orthogonality ──────────────────────────────────────────────────────

def _gen_linalg_orthogonality():
    """Two vectors are orthogonal iff their dot product is 0; find missing component."""
    # u = (a, b), v = (c, ?) orthogonal → a*c + b*? = 0 → ? = -a*c/b
    a = random.randint(1, 4)
    b = random.choice([-3,-2,-1,1,2,3])
    c_num = random.randint(1, 4)
    # ? = -a*c_num / b — need integer
    # Ensure b divides a*c_num
    prod = a * c_num
    if prod % b != 0:
        # Adjust: set c_num so prod divisible by b
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


# ── linalg-gram-schmidt ───────────────────────────────────────────────────────

def _gen_linalg_gram_schmidt():
    """First step of Gram-Schmidt: find the projection coefficient."""
    # u1 = v1 (already orthogonal base). Projection of v2 onto u1:
    # proj = (v2·u1 / u1·u1) * u1. Ask for the scalar coefficient.
    u1 = [random.randint(1, 3), random.randint(1, 3)]
    # v2 chosen so projection is a clean fraction
    c = random.randint(1, 3)  # projection coefficient numerator
    u1_norm_sq = u1[0]**2 + u1[1]**2
    # v2 = c * u1 + perp component
    perp = [0, 0]
    # Add something orthogonal to u1: (-u1[1], u1[0]) * t
    t = random.randint(1, 2)
    v2 = [c*u1[0] + t*(-u1[1]), c*u1[1] + t*(u1[0])]
    dot = v2[0]*u1[0] + v2[1]*u1[1]
    frac = Fraction(dot, u1_norm_sq)
    ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    return {
        "problem_text": (
            f"In the Gram-Schmidt process, let \\(\\mathbf{{u}}_1 = {_vec2(*u1)}\\). "
            f"Find the projection coefficient \\(\\frac{{\\mathbf{{v}}_2 \\cdot \\mathbf{{u}}_1}}{{\\mathbf{{u}}_1 \\cdot \\mathbf{{u}}_1}}\\) "
            f"for \\(\\mathbf{{v}}_2 = {_vec2(*v2)}\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
        "hints": [
            {"level": 1, "text": "Compute the dot products \\(\\mathbf{v}_2 \\cdot \\mathbf{u}_1\\) and \\(\\mathbf{u}_1 \\cdot \\mathbf{u}_1\\)."},
            {"level": 2, "text": f"\\(\\mathbf{{v}}_2 \\cdot \\mathbf{{u}}_1 = {v2[0]*u1[0]} + {v2[1]*u1[1]} = {dot}\\). \\(\\|\\mathbf{{u}}_1\\|^2 = {u1[0]**2} + {u1[1]**2} = {u1_norm_sq}\\)."},
            {"level": 3, "text": f"Coefficient \\(= \\frac{{{dot}}}{{{u1_norm_sq}}} = {ans}\\)."},
        ],
    }


# ── linalg-orthogonal-projection ──────────────────────────────────────────────

def _gen_linalg_orthogonal_projection():
    """Projection of vector b onto vector a; return one component of the projection."""
    a = [random.randint(1, 3), 0]   # keep simple: a = (k, 0) for clean projection
    k = a[0]
    b = [random.randint(-3, 4), random.randint(-3, 4)]
    # proj_a(b) = (b·a / a·a) * a = (b[0]/k) * (k, 0) = (b[0], 0)
    proj = [b[0], 0]
    r = random.randint(0, 1)
    ans = proj[r]
    comp = "first" if r == 0 else "second"
    return {
        "problem_text": (
            f"Find the {comp} component of the orthogonal projection of "
            f"\\(\\mathbf{{b}} = {_vec2(*b)}\\) onto \\(\\mathbf{{a}} = {_vec2(*a)}\\)."
        ),
        "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "\\(\\text{proj}_{\\mathbf{a}} \\mathbf{b} = \\frac{\\mathbf{b} \\cdot \\mathbf{a}}{\\mathbf{a} \\cdot \\mathbf{a}} \\mathbf{a}\\)."},
            {"level": 2, "text": f"\\(\\mathbf{{b}} \\cdot \\mathbf{{a}} = {b[0]*k}\\). \\(\\mathbf{{a}} \\cdot \\mathbf{{a}} = {k**2}\\). Scalar = \\({b[0]*k}/{k**2} = {b[0]}/{k}\\). Projection = scalar \\(\\times\\, \\mathbf{{a}}\\)."},
            {"level": 3, "text": f"Projection \\(= \\frac{{{b[0]*k}}}{{{k**2}}} \\cdot {_vec2(*a)} = {_vec2(*proj)}\\). The {comp} component is \\({ans}\\)."},
        ],
    }


# ── linalg-least-squares ──────────────────────────────────────────────────────

def _gen_linalg_least_squares():
    """Normal equations: given A^T A x = A^T b, solve for one component."""
    # Over-determined 2-equation, 1-unknown case: fit y = c*x through two points
    # Normal eqn: c = sum(x_i * y_i) / sum(x_i^2)
    x1 = random.randint(1, 3); x2 = random.randint(1, 3)
    while x2 == x1: x2 = random.randint(1, 3)
    c_true = random.randint(1, 4)
    y1 = c_true * x1 + random.choice([-1, 1])
    y2 = c_true * x2 + random.choice([-1, 1])
    # LS estimate: c_hat = (x1*y1 + x2*y2) / (x1^2 + x2^2)
    num = x1*y1 + x2*y2
    denom = x1**2 + x2**2
    frac = Fraction(num, denom)
    ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    return {
        "problem_text": (
            f"Find the least-squares estimate \\(\\hat{{c}}\\) for the model \\(y = cx\\) "
            f"given the data points \\(({x1}, {y1})\\) and \\(({x2}, {y2})\\). "
            f"Use the normal equation \\(\\hat{{c}} = \\frac{{\\sum x_i y_i}}{{\\sum x_i^2}}\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
        "hints": [
            {"level": 1, "text": "The normal equation for \\(y = cx\\) is \\(\\hat{c} = \\frac{\\sum x_i y_i}{\\sum x_i^2}\\)."},
            {"level": 2, "text": f"Numerator: \\({x1} \\cdot {y1} + {x2} \\cdot {y2} = {num}\\). Denominator: \\({x1}^2 + {x2}^2 = {denom}\\)."},
            {"level": 3, "text": f"\\(\\hat{{c}} = \\frac{{{num}}}{{{denom}}} = {ans}\\)."},
        ],
    }


# ── linalg-svd ────────────────────────────────────────────────────────────────

def _gen_linalg_svd():
    """Singular value of a simple diagonal or rank-1 matrix."""
    choice = random.randint(0, 1)
    if choice == 0:
        # Diagonal: singular values are |diagonal entries|
        s1 = random.randint(2, 5); s2 = random.randint(1, s1-1)
        A = [[s1, 0], [0, s2]]
        ans = s1  # largest singular value
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
    else:
        # Rank-1: A = u*v^T, singular value = ||u|| * ||v||
        a = random.randint(2, 4); b = random.randint(2, 4)
        # A = [[a*b, 0],[0, 0]] — singular values: a*b and 0
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
