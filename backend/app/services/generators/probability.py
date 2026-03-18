"""
Probability problem generators for Fisher App 3.0.
Covers 39 nodes: prob-sample-space through prob-clt.

Drop at: backend/app/services/generators/probability.py
In problem_generator.py add:
    from .generators.probability import GENERATORS as PROB_GENERATORS
    GENERATORS.update(PROB_GENERATORS)
"""
import random
from fractions import Fraction
from math import factorial, comb, gcd


# ── helpers ───────────────────────────────────────────────────────────────────

def _fr(p, q):
    """Reduced fraction as string; int string if denominator 1."""
    f = Fraction(p, q)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

def _pct(p, q):
    """Percentage string from fraction p/q (integer %)."""
    return str(100 * p // q)


# ── prob-sample-space ─────────────────────────────────────────────────────────

def _gen_prob_sample_space():
    """Count outcomes in a uniform sample space."""
    choice = random.randint(0, 2)
    if choice == 0:
        n = random.randint(2, 3)  # n fair dice
        ans = 6**n
        label = "two" if n == 2 else "three"
        return {
            "problem_text": f"A fair die is rolled {label} times. How many outcomes are in the sample space?",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Each roll has 6 outcomes. Use the multiplication principle."},
                {"level": 2, "text": f"\\({n}\\) independent rolls: \\(6^{{{n}}}\\)."},
                {"level": 3, "text": f"\\(6^{{{n}}} = {ans}\\)."},
            ],
        }
    elif choice == 1:
        n = random.randint(2, 4)  # n coin flips
        ans = 2**n
        return {
            "problem_text": f"A fair coin is flipped {n} times. How many outcomes are in the sample space?",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Each flip has 2 outcomes. Use the multiplication principle."},
                {"level": 2, "text": f"\\({n}\\) independent flips: \\(2^{{{n}}}\\)."},
                {"level": 3, "text": f"\\(2^{{{n}}} = {ans}\\)."},
            ],
        }
    else:
        n = random.randint(3, 6)  # choose r from n
        r = random.randint(2, n)
        ans = comb(n, r)
        return {
            "problem_text": (
                f"A committee of {r} is chosen from {n} people. "
                f"How many equally likely outcomes are in the sample space?"
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The order of selection doesn't matter — use combinations."},
                {"level": 2, "text": f"\\(\\binom{{{n}}}{{{r}}} = \\frac{{{n}!}}{{{r}!({n}-{r})!}}\\)."},
                {"level": 3, "text": f"\\(\\binom{{{n}}}{{{r}}} = {ans}\\)."},
            ],
        }


# ── prob-set-ops ──────────────────────────────────────────────────────────────

def _gen_prob_set_ops():
    """Size of union, intersection, or complement of union."""
    total = random.randint(10, 20)
    a = random.randint(3, total - 2)
    b = random.randint(3, total - 2)
    inter = random.randint(1, min(a, b) - 1)
    union = a + b - inter
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Find union
        ans = union
        return {
            "problem_text": (
                f"In a group of students, \\(|A| = {a}\\), \\(|B| = {b}\\), and \\(|A \\cap B| = {inter}\\). "
                f"Find \\(|A \\cup B|\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Inclusion-exclusion: \\(|A \\cup B| = |A| + |B| - |A \\cap B|\\)."},
                {"level": 2, "text": f"\\({a} + {b} - {inter}\\)."},
                {"level": 3, "text": f"\\({a} + {b} - {inter} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Find intersection
        ans = inter
        return {
            "problem_text": (
                f"\\(|A| = {a}\\), \\(|B| = {b}\\), and \\(|A \\cup B| = {union}\\). "
                f"Find \\(|A \\cap B|\\)."
            ),
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Rearrange inclusion-exclusion: \\(|A \\cap B| = |A| + |B| - |A \\cup B|\\)."},
                {"level": 2, "text": f"\\({a} + {b} - {union}\\)."},
                {"level": 3, "text": f"\\({ans}\\)."},
            ],
        }
    else:
        # Find |A only| = |A| - |A∩B| (elements in A but not B)
        a_only = a - inter
        return {
            "problem_text": (
                f"A survey finds \\(|A| = {a}\\), \\(|B| = {b}\\), and \\(|A \\cap B| = {inter}\\). "
                f"How many elements are in \\(A\\) but not in \\(B\\)?"
            ),
            "correct_answer": str(a_only), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Elements only in \\(A\\) (not in \\(B\\)) = \\(|A| - |A \\cap B|\\)."},
                {"level": 2, "text": f"\\({a} - {inter}\\)."},
                {"level": 3, "text": f"\\({a} - {inter} = {a_only}\\)."},
            ],
        }


# ── prob-axioms ───────────────────────────────────────────────────────────────

def _gen_prob_axioms():
    """Complement rule, independence union, or De Morgan."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # P(A^c) = 1 - P(A)
        p_num = random.randint(1, 5)
        p_den = random.randint(p_num + 1, 8)
        comp_num = p_den - p_num
        ans = _fr(comp_num, p_den)
        return {
            "problem_text": (
                f"If \\(P(A) = \\frac{{{p_num}}}{{{p_den}}}\\), what is \\(P(A^c)\\)?"
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Complement rule: \\(P(A^c) = 1 - P(A)\\)."},
                {"level": 2, "text": f"\\(1 - \\frac{{{p_num}}}{{{p_den}}} = \\frac{{{p_den} - {p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(P(A^c) = \\frac{{{comp_num}}}{{{p_den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # P(A∪B) for independent A, B: P(A)+P(B)-P(A)P(B)
        den_a = random.choice([2, 3, 4])
        den_b = random.choice([2, 3, 4])
        a = random.randint(1, den_a - 1)
        b = random.randint(1, den_b - 1)
        # P(A∪B) = a/den_a + b/den_b - ab/(den_a*den_b)
        num = a * den_b + b * den_a - a * b
        denom = den_a * den_b
        ans = _fr(num, denom)
        return {
            "problem_text": (
                f"Independent events \\(A\\) and \\(B\\) satisfy \\(P(A) = \\frac{{{a}}}{{{den_a}}}\\) "
                f"and \\(P(B) = \\frac{{{b}}}{{{den_b}}}\\). Find \\(P(A \\cup B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\\). For independent events, \\(P(A \\cap B) = P(A)P(B)\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{a}}}{{{den_a}}} + \\frac{{{b}}}{{{den_b}}} - \\frac{{{a}}}{{{den_a}}} \\cdot \\frac{{{b}}}{{{den_b}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{a*den_b} + {b*den_a} - {a*b}}}{{{denom}}} = {ans}\\)."},
            ],
        }
    else:
        # Given P(A∪B) and P(A), P(B) independent, find P(A^c ∩ B^c) = 1 - P(A∪B)
        den_a = random.choice([2, 3, 4])
        den_b = random.choice([2, 3, 4])
        a = random.randint(1, den_a - 1)
        b = random.randint(1, den_b - 1)
        num_union = a * den_b + b * den_a - a * b
        denom = den_a * den_b
        # P(A^c ∩ B^c) = 1 - P(A∪B)
        comp_num = denom - num_union
        ans = _fr(comp_num, denom)
        return {
            "problem_text": (
                f"Independent events \\(A\\) and \\(B\\) satisfy \\(P(A) = \\frac{{{a}}}{{{den_a}}}\\) "
                f"and \\(P(B) = \\frac{{{b}}}{{{den_b}}}\\). "
                f"Find \\(P(A^c \\cap B^c)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "By De Morgan's law: \\(P(A^c \\cap B^c) = P((A \\cup B)^c) = 1 - P(A \\cup B)\\)."},
                {"level": 2, "text": f"First find \\(P(A \\cup B) = \\frac{{{a}}}{{{den_a}}} + \\frac{{{b}}}{{{den_b}}} - \\frac{{{a*b}}}{{{denom}}} = \\frac{{{num_union}}}{{{denom}}}\\)."},
                {"level": 3, "text": f"\\(P(A^c \\cap B^c) = 1 - \\frac{{{num_union}}}{{{denom}}} = \\frac{{{comp_num}}}{{{denom}}} = {ans}\\)."},
            ],
        }


# ── prob-inclusion-excl ───────────────────────────────────────────────────────

def _gen_prob_inclusion_excl():
    """P(A∪B) via inclusion-exclusion, or find P(A∩B), or three-event."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Find P(A∪B)
        den = random.choice([6, 8, 10, 12])
        a = random.randint(2, den - 2)
        b = random.randint(2, den - 2)
        inter = random.randint(1, min(a, b) - 1)
        union_num = a + b - inter
        while union_num > den:
            inter += 1
            union_num = a + b - inter
        ans = _fr(union_num, den)
        return {
            "problem_text": (
                f"\\(P(A) = \\frac{{{a}}}{{{den}}}\\), \\(P(B) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(A \\cap B) = \\frac{{{inter}}}{{{den}}}\\). Find \\(P(A \\cup B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\\)."},
                {"level": 2, "text": f"\\(\\frac{{{a}}}{{{den}}} + \\frac{{{b}}}{{{den}}} - \\frac{{{inter}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{union_num}}}{{{den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Find P(A∩B) given P(A∪B)
        den = random.choice([6, 8, 10, 12])
        a = random.randint(2, den - 2)
        b = random.randint(2, den - 2)
        inter = random.randint(1, min(a, b) - 1)
        union_num = a + b - inter
        while union_num > den:
            inter += 1
            union_num = a + b - inter
        ans = _fr(inter, den)
        return {
            "problem_text": (
                f"\\(P(A) = \\frac{{{a}}}{{{den}}}\\), \\(P(B) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(A \\cup B) = \\frac{{{union_num}}}{{{den}}}\\). Find \\(P(A \\cap B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Rearrange inclusion-exclusion: \\(P(A \\cap B) = P(A) + P(B) - P(A \\cup B)\\)."},
                {"level": 2, "text": f"\\(\\frac{{{a}}}{{{den}}} + \\frac{{{b}}}{{{den}}} - \\frac{{{union_num}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{inter}}}{{{den}}} = {ans}\\)."},
            ],
        }
    else:
        # Three events: how many are in exactly one, given |A|, |B|, |C|, |A∩B|, |A∩C|, |B∩C|, |A∩B∩C|
        total = random.randint(20, 40)
        ab = random.randint(2, 5)
        ac = random.randint(2, 5)
        bc = random.randint(2, 5)
        abc = random.randint(1, min(ab, ac, bc) - 1)
        a_only_part = random.randint(3, 8)
        b_only_part = random.randint(3, 8)
        c_only_part = random.randint(3, 8)
        exactly_one = a_only_part + b_only_part + c_only_part
        return {
            "problem_text": (
                f"In a class, \\(|A \\cap B| = {ab}\\), \\(|A \\cap C| = {ac}\\), \\(|B \\cap C| = {bc}\\), "
                f"\\(|A \\cap B \\cap C| = {abc}\\). "
                f"The number of students in exactly one of \\(A\\), \\(B\\), \\(C\\) alone (not shared) is "
                f"\\({a_only_part}\\), \\({b_only_part}\\), and \\({c_only_part}\\) respectively. "
                f"How many students are in exactly one event?"
            ),
            "correct_answer": str(exactly_one), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Students in exactly one event are those in only \\(A\\), only \\(B\\), or only \\(C\\)."},
                {"level": 2, "text": f"Sum the three 'only' counts: \\({a_only_part} + {b_only_part} + {c_only_part}\\)."},
                {"level": 3, "text": f"\\({a_only_part} + {b_only_part} + {c_only_part} = {exactly_one}\\)."},
            ],
        }


# ── prob-area-probability ─────────────────────────────────────────────────────

def _gen_prob_area_probability():
    """Geometric probability: area-based uniform probability."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # inner square inside outer square
        outer = random.randint(3, 6)
        inner = random.randint(1, outer - 1)
        ans = _fr(inner**2, outer**2)
        return {
            "problem_text": (
                f"A point is chosen uniformly at random inside a \\({outer} \\times {outer}\\) square. "
                f"What is the probability it falls inside a centered \\({inner} \\times {inner}\\) square?"
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For a uniform distribution on a region, probability = favorable area / total area."},
                {"level": 2, "text": f"Favorable area = \\({inner}^2 = {inner**2}\\). Total area = \\({outer}^2 = {outer**2}\\)."},
                {"level": 3, "text": f"\\(P = \\frac{{{inner**2}}}{{{outer**2}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # circle inside rectangle: P = pi*r^2 / (W*H) — but pi is irrational
        # Use rectangle strip: P(X in [0,a] where X~Uniform(0,W)) = a/W
        W = random.randint(4, 8)
        H = random.randint(4, 8)
        strip_w = random.randint(1, W - 1)
        strip_h = random.randint(1, H - 1)
        ans = _fr(strip_w * strip_h, W * H)
        return {
            "problem_text": (
                f"A point is chosen uniformly at random in a \\({W} \\times {H}\\) rectangle. "
                f"What is the probability it lands in the lower-left \\({strip_w} \\times {strip_h}\\) corner region?"
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Probability equals favorable area divided by total area."},
                {"level": 2, "text": f"Favorable area = \\({strip_w} \\times {strip_h} = {strip_w*strip_h}\\). Total area = \\({W} \\times {H} = {W*H}\\)."},
                {"level": 3, "text": f"\\(P = \\frac{{{strip_w*strip_h}}}{{{W*H}}} = {ans}\\)."},
            ],
        }
    else:
        # Triangle inside rectangle: P = (1/2 * b * h) / (W * H)
        W = random.choice([4, 6, 8])
        H = random.choice([4, 6, 8])
        # triangle with base W and height H/2 (or some clean fraction)
        tri_base = W
        tri_height = H // 2
        tri_area = tri_base * tri_height  # = W*H/2, divided by 2 = W*H/4
        # P = (1/2 * tri_base * tri_height) / (W*H)
        ans = _fr(tri_base * tri_height, 2 * W * H)
        return {
            "problem_text": (
                f"A point is chosen uniformly in a \\({W} \\times {H}\\) rectangle. "
                f"What is the probability it lies inside a triangle with base \\({tri_base}\\) and height \\({tri_height}\\) "
                f"in the corner of the rectangle?"
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Probability = triangle area / rectangle area. Triangle area = \\(\\frac{1}{2} \\cdot \\text{base} \\cdot \\text{height}\\)."},
                {"level": 2, "text": f"Triangle area = \\(\\frac{{1}}{{2}} \\cdot {tri_base} \\cdot {tri_height} = {tri_base*tri_height//2}\\). Rectangle area = \\({W*H}\\)."},
                {"level": 3, "text": f"\\(P = \\frac{{{tri_base*tri_height}}}{{{2*W*H}}} = {ans}\\)."},
            ],
        }


# ── prob-conditional ──────────────────────────────────────────────────────────

def _gen_prob_conditional():
    """P(A|B), P(B|A), or find P(A∩B) given conditional probability."""
    variant = random.choice([0, 1, 2])
    den = random.choice([6, 8, 10, 12])
    if variant == 0:
        # Find P(A|B)
        b = random.randint(2, den - 1)
        inter = random.randint(1, b - 1)
        ans = _fr(inter, b)
        return {
            "problem_text": (
                f"\\(P(B) = \\frac{{{b}}}{{{den}}}\\) and \\(P(A \\cap B) = \\frac{{{inter}}}{{{den}}}\\). "
                f"Find \\(P(A \\mid B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}\\)."},
                {"level": 2, "text": f"\\(\\frac{{{inter}/{den}}}{{{b}/{den}}} = \\frac{{{inter}}}{{{b}}}\\)."},
                {"level": 3, "text": f"\\(P(A \\mid B) = \\frac{{{inter}}}{{{b}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Find P(B|A) — swap roles
        a = random.randint(2, den - 1)
        inter = random.randint(1, a - 1)
        ans = _fr(inter, a)
        return {
            "problem_text": (
                f"\\(P(A) = \\frac{{{a}}}{{{den}}}\\) and \\(P(A \\cap B) = \\frac{{{inter}}}{{{den}}}\\). "
                f"Find \\(P(B \\mid A)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(P(B \\mid A) = \\frac{P(A \\cap B)}{P(A)}\\)."},
                {"level": 2, "text": f"\\(\\frac{{{inter}/{den}}}{{{a}/{den}}} = \\frac{{{inter}}}{{{a}}}\\)."},
                {"level": 3, "text": f"\\(P(B \\mid A) = \\frac{{{inter}}}{{{a}}} = {ans}\\)."},
            ],
        }
    else:
        # Find P(A∩B) given P(A|B) and P(B)
        b = random.randint(2, den - 1)
        inter = random.randint(1, b - 1)
        cond_ans = _fr(inter, b)
        ans = _fr(inter, den)
        return {
            "problem_text": (
                f"\\(P(B) = \\frac{{{b}}}{{{den}}}\\) and \\(P(A \\mid B) = \\frac{{{inter}}}{{{b}}}\\). "
                f"Find \\(P(A \\cap B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Rearrange: \\(P(A \\cap B) = P(A \\mid B) \\cdot P(B)\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{inter}}}{{{b}}} \\cdot \\frac{{{b}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(P(A \\cap B) = \\frac{{{inter}}}{{{den}}} = {ans}\\)."},
            ],
        }


# ── prob-independence ─────────────────────────────────────────────────────────

def _gen_prob_independence():
    """P(A∩B), P(A∪B) for independent events, or find P(A) given independence."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Find P(A∩B) = P(A)*P(B)
        den_a = random.choice([2, 3, 4])
        den_b = random.choice([2, 3, 4])
        a = random.randint(1, den_a - 1)
        b = random.randint(1, den_b - 1)
        ans = _fr(a * b, den_a * den_b)
        return {
            "problem_text": (
                f"Events \\(A\\) and \\(B\\) are independent with \\(P(A) = \\frac{{{a}}}{{{den_a}}}\\) "
                f"and \\(P(B) = \\frac{{{b}}}{{{den_b}}}\\). Find \\(P(A \\cap B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For independent events: \\(P(A \\cap B) = P(A) \\cdot P(B)\\)."},
                {"level": 2, "text": f"\\(\\frac{{{a}}}{{{den_a}}} \\cdot \\frac{{{b}}}{{{den_b}}} = \\frac{{{a*b}}}{{{den_a*den_b}}}\\)."},
                {"level": 3, "text": f"\\(P(A \\cap B) = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Find P(A) given P(A∩B) and independence: P(A) = P(A∩B)/P(B)
        den_a = random.choice([2, 3, 4])
        den_b = random.choice([2, 3, 4])
        a = random.randint(1, den_a - 1)
        b = random.randint(1, den_b - 1)
        inter_num = a * b
        inter_den = den_a * den_b
        ans = _fr(a, den_a)
        return {
            "problem_text": (
                f"Events \\(A\\) and \\(B\\) are independent. \\(P(B) = \\frac{{{b}}}{{{den_b}}}\\) "
                f"and \\(P(A \\cap B) = \\frac{{{inter_num}}}{{{inter_den}}}\\). Find \\(P(A)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For independent events: \\(P(A \\cap B) = P(A) \\cdot P(B)\\), so \\(P(A) = \\frac{P(A \\cap B)}{P(B)}\\)."},
                {"level": 2, "text": f"\\(P(A) = \\frac{{{inter_num}/{inter_den}}}{{{b}/{den_b}}} = \\frac{{{inter_num}}}{{{inter_den}}} \\cdot \\frac{{{den_b}}}{{{b}}}\\)."},
                {"level": 3, "text": f"\\(P(A) = \\frac{{{a}}}{{{den_a}}} = {ans}\\)."},
            ],
        }
    else:
        # Find P(A^c ∩ B^c) = P(A^c)*P(B^c) for independent events
        den_a = random.choice([2, 3, 4])
        den_b = random.choice([2, 3, 4])
        a = random.randint(1, den_a - 1)
        b = random.randint(1, den_b - 1)
        comp_a = den_a - a
        comp_b = den_b - b
        ans = _fr(comp_a * comp_b, den_a * den_b)
        return {
            "problem_text": (
                f"Events \\(A\\) and \\(B\\) are independent with \\(P(A) = \\frac{{{a}}}{{{den_a}}}\\) "
                f"and \\(P(B) = \\frac{{{b}}}{{{den_b}}}\\). Find \\(P(A^c \\cap B^c)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Since \\(A\\) and \\(B\\) are independent, so are \\(A^c\\) and \\(B^c\\). Use \\(P(A^c \\cap B^c) = P(A^c) P(B^c)\\)."},
                {"level": 2, "text": f"\\(P(A^c) = 1 - \\frac{{{a}}}{{{den_a}}} = \\frac{{{comp_a}}}{{{den_a}}}\\). \\(P(B^c) = \\frac{{{comp_b}}}{{{den_b}}}\\)."},
                {"level": 3, "text": f"\\(P(A^c \\cap B^c) = \\frac{{{comp_a}}}{{{den_a}}} \\cdot \\frac{{{comp_b}}}{{{den_b}}} = {ans}\\)."},
            ],
        }


# ── prob-total-prob ───────────────────────────────────────────────────────────

def _gen_prob_total_prob():
    """Law of total probability: find P(B), P(B^c), or a prior probability."""
    variant = random.choice([0, 1, 2])
    den = random.choice([4, 5, 6])
    pa = random.randint(1, den - 1)
    pac = den - pa
    den2 = random.choice([4, 5])
    p1 = random.randint(1, den2 - 1)
    p2 = random.randint(1, den2 - 1)
    num = pa * p1 + pac * p2
    denom = den * den2
    if variant == 0:
        # Find P(B)
        ans = _fr(num, denom)
        return {
            "problem_text": (
                f"\\(P(A) = \\frac{{{pa}}}{{{den}}}\\), "
                f"\\(P(B \\mid A) = \\frac{{{p1}}}{{{den2}}}\\), "
                f"\\(P(B \\mid A^c) = \\frac{{{p2}}}{{{den2}}}\\). "
                f"Find \\(P(B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Law of total probability: \\(P(B) = P(B|A)P(A) + P(B|A^c)P(A^c)\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{p1}}}{{{den2}}} \\cdot \\frac{{{pa}}}{{{den}}} + \\frac{{{p2}}}{{{den2}}} \\cdot \\frac{{{pac}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{pa*p1} + {pac*p2}}}{{{denom}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Find P(B^c) = 1 - P(B)
        comp_num = denom - num
        ans = _fr(comp_num, denom)
        return {
            "problem_text": (
                f"\\(P(A) = \\frac{{{pa}}}{{{den}}}\\), "
                f"\\(P(B \\mid A) = \\frac{{{p1}}}{{{den2}}}\\), "
                f"\\(P(B \\mid A^c) = \\frac{{{p2}}}{{{den2}}}\\). "
                f"Find \\(P(B^c)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "First use total probability to find \\(P(B)\\), then apply the complement rule."},
                {"level": 2, "text": f"\\(P(B) = \\frac{{{p1}}}{{{den2}}} \\cdot \\frac{{{pa}}}{{{den}}} + \\frac{{{p2}}}{{{den2}}} \\cdot \\frac{{{pac}}}{{{den}}} = \\frac{{{num}}}{{{denom}}}\\)."},
                {"level": 3, "text": f"\\(P(B^c) = 1 - \\frac{{{num}}}{{{denom}}} = \\frac{{{comp_num}}}{{{denom}}} = {ans}\\)."},
            ],
        }
    else:
        # Three-partition total probability
        den3 = random.choice([3, 4])
        p_a1 = random.randint(1, den3 - 2)
        p_a2 = random.randint(1, den3 - p_a1 - 1)
        p_a3 = den3 - p_a1 - p_a2
        den4 = random.choice([4, 5])
        pb_a1 = random.randint(1, den4 - 1)
        pb_a2 = random.randint(1, den4 - 1)
        pb_a3 = random.randint(1, den4 - 1)
        num_b = p_a1 * pb_a1 + p_a2 * pb_a2 + p_a3 * pb_a3
        denom_b = den3 * den4
        ans = _fr(num_b, denom_b)
        return {
            "problem_text": (
                f"Three mutually exclusive and exhaustive events satisfy "
                f"\\(P(A_1) = \\frac{{{p_a1}}}{{{den3}}}\\), \\(P(A_2) = \\frac{{{p_a2}}}{{{den3}}}\\), \\(P(A_3) = \\frac{{{p_a3}}}{{{den3}}}\\). "
                f"Also \\(P(B \\mid A_1) = \\frac{{{pb_a1}}}{{{den4}}}\\), \\(P(B \\mid A_2) = \\frac{{{pb_a2}}}{{{den4}}}\\), "
                f"\\(P(B \\mid A_3) = \\frac{{{pb_a3}}}{{{den4}}}\\). Find \\(P(B)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Total probability: \\(P(B) = \\sum_{i} P(B \\mid A_i) P(A_i)\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{pb_a1}}}{{{den4}}} \\cdot \\frac{{{p_a1}}}{{{den3}}} + \\frac{{{pb_a2}}}{{{den4}}} \\cdot \\frac{{{p_a2}}}{{{den3}}} + \\frac{{{pb_a3}}}{{{den4}}} \\cdot \\frac{{{p_a3}}}{{{den3}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{p_a1*pb_a1} + {p_a2*pb_a2} + {p_a3*pb_a3}}}{{{denom_b}}} = {ans}\\)."},
            ],
        }


# ── prob-bayes ────────────────────────────────────────────────────────────────

def _gen_prob_bayes():
    """Bayes' theorem: P(A|B), P(A^c|B), or real-world context."""
    variant = random.choice([0, 1, 2])
    den = random.choice([4, 5])
    pa = random.randint(1, den - 1)
    pac = den - pa
    den2 = random.choice([4, 5])
    p_ba = random.randint(1, den2 - 1)
    p_bac = random.randint(1, den2 - 1)
    num_ab = pa * p_ba
    num_acb = pac * p_bac
    denom_total = num_ab + num_acb
    if variant == 0:
        # Find P(A|B)
        ans = _fr(num_ab, denom_total)
        return {
            "problem_text": (
                f"\\(P(A) = \\frac{{{pa}}}{{{den}}}\\), "
                f"\\(P(B \\mid A) = \\frac{{{p_ba}}}{{{den2}}}\\), "
                f"\\(P(B \\mid A^c) = \\frac{{{p_bac}}}{{{den2}}}\\). "
                f"Find \\(P(A \\mid B)\\) using Bayes' theorem."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Bayes' theorem: \\(P(A|B) = \\frac{P(B|A)P(A)}{P(B)}\\). First find \\(P(B)\\) via total probability."},
                {"level": 2, "text": f"\\(P(B) = \\frac{{{p_ba}}}{{{den2}}} \\cdot \\frac{{{pa}}}{{{den}}} + \\frac{{{p_bac}}}{{{den2}}} \\cdot \\frac{{{pac}}}{{{den}}} = \\frac{{{denom_total}}}{{{den*den2}}}\\)."},
                {"level": 3, "text": f"\\(P(A|B) = \\frac{{{num_ab}}}{{{denom_total}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Find P(A^c|B) — posterior for complement
        ans = _fr(num_acb, denom_total)
        return {
            "problem_text": (
                f"\\(P(A) = \\frac{{{pa}}}{{{den}}}\\), "
                f"\\(P(B \\mid A) = \\frac{{{p_ba}}}{{{den2}}}\\), "
                f"\\(P(B \\mid A^c) = \\frac{{{p_bac}}}{{{den2}}}\\). "
                f"Find \\(P(A^c \\mid B)\\) using Bayes' theorem."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "By Bayes' theorem: \\(P(A^c|B) = \\frac{P(B|A^c)P(A^c)}{P(B)}\\)."},
                {"level": 2, "text": f"\\(P(B) = \\frac{{{denom_total}}}{{{den*den2}}}\\). Numerator: \\(\\frac{{{p_bac}}}{{{den2}}} \\cdot \\frac{{{pac}}}{{{den}}} = \\frac{{{num_acb}}}{{{den*den2}}}\\)."},
                {"level": 3, "text": f"\\(P(A^c|B) = \\frac{{{num_acb}}}{{{denom_total}}} = {ans}\\)."},
            ],
        }
    else:
        # Medical test context: disease prevalence, sensitivity, specificity
        prev_den = random.choice([10, 20, 100])
        prev_num = random.randint(1, prev_den // 5)
        sens_den = random.choice([10, 20])
        sens_num = random.randint(sens_den * 3 // 4, sens_den - 1)
        spec_den = random.choice([10, 20])
        spec_num = random.randint(spec_den * 3 // 4, spec_den - 1)
        # P(disease) = prev_num/prev_den, P(+|disease) = sens_num/sens_den, P(+|no disease) = (spec_den-spec_num)/spec_den
        fp_num = spec_den - spec_num
        # P(disease|+) = P(+|D)*P(D) / [P(+|D)*P(D) + P(+|D^c)*P(D^c)]
        tp = prev_num * sens_num * spec_den
        fp_part = (prev_den - prev_num) * fp_num * sens_den
        total_pos = tp + fp_part
        ans = _fr(tp, total_pos)
        return {
            "problem_text": (
                f"A disease affects \\(\\frac{{{prev_num}}}{{{prev_den}}}\\) of the population. "
                f"A test has sensitivity \\(P(+|\\text{{disease}}) = \\frac{{{sens_num}}}{{{sens_den}}}\\) "
                f"and false-positive rate \\(P(+|\\text{{no disease}}) = \\frac{{{fp_num}}}{{{spec_den}}}\\). "
                f"Given a positive test, find \\(P(\\text{{disease}} \\mid +)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.8,
            "hints": [
                {"level": 1, "text": "Apply Bayes' theorem: \\(P(D|+) = \\frac{P(+|D)P(D)}{P(+|D)P(D) + P(+|D^c)P(D^c)}\\)."},
                {"level": 2, "text": f"Numerator: \\(\\frac{{{sens_num}}}{{{sens_den}}} \\cdot \\frac{{{prev_num}}}{{{prev_den}}}\\). Denominator adds \\(\\frac{{{fp_num}}}{{{spec_den}}} \\cdot \\frac{{{prev_den-prev_num}}}{{{prev_den}}}\\)."},
                {"level": 3, "text": f"\\(P(\\text{{disease}}|+) = \\frac{{{tp}}}{{{total_pos}}} = {ans}\\)."},
            ],
        }


# ── prob-discrete-rv ──────────────────────────────────────────────────────────

def _gen_prob_discrete_rv():
    """PMF of a simple discrete RV: find P(X=k), E[X], or mode."""
    den = random.choice([4, 5, 6, 8])
    a = random.randint(1, den - 2)
    b = random.randint(1, den - a - 1)
    c = den - a - b
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Find P(X=k)
        vals = [(0, a), (1, b), (2, c)]
        k, pk = random.choice(vals)
        ans = _fr(pk, den)
        return {
            "problem_text": (
                f"A discrete random variable \\(X\\) has PMF: "
                f"\\(P(X=0) = \\frac{{{a}}}{{{den}}}\\), "
                f"\\(P(X=1) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(X=2) = \\frac{{{c}}}{{{den}}}\\). "
                f"Find \\(P(X = {k})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Read the probability directly from the PMF table."},
                {"level": 2, "text": f"\\(P(X={k})\\) is given as \\(\\frac{{{pk}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(P(X={k}) = \\frac{{{pk}}}{{{den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Find E[X] = (0*a + 1*b + 2*c)/den
        num = b + 2 * c
        ans = _fr(num, den)
        return {
            "problem_text": (
                f"A discrete random variable \\(X\\) has PMF: "
                f"\\(P(X=0) = \\frac{{{a}}}{{{den}}}\\), "
                f"\\(P(X=1) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(X=2) = \\frac{{{c}}}{{{den}}}\\). "
                f"Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(E[X] = \\sum_k k \\cdot P(X=k)\\)."},
                {"level": 2, "text": f"\\(= 0 \\cdot \\frac{{{a}}}{{{den}}} + 1 \\cdot \\frac{{{b}}}{{{den}}} + 2 \\cdot \\frac{{{c}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{b} + 2 \\cdot {c}}}{{{den}}} = {ans}\\)."},
            ],
        }
    else:
        # Find mode (value with highest probability)
        probs = [a, b, c]
        mode_val = probs.index(max(probs))
        ans = str(mode_val)
        return {
            "problem_text": (
                f"A discrete random variable \\(X\\) has PMF: "
                f"\\(P(X=0) = \\frac{{{a}}}{{{den}}}\\), "
                f"\\(P(X=1) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(X=2) = \\frac{{{c}}}{{{den}}}\\). "
                f"Find the mode of \\(X\\) (the most likely value)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The mode is the value of \\(X\\) that has the highest probability."},
                {"level": 2, "text": f"Compare \\(\\frac{{{a}}}{{{den}}}\\), \\(\\frac{{{b}}}{{{den}}}\\), \\(\\frac{{{c}}}{{{den}}}\\) — the largest numerator wins."},
                {"level": 3, "text": f"The largest probability is \\(\\frac{{{max(probs)}}}{{{den}}}\\), so the mode is \\(X = {mode_val}\\)."},
            ],
        }


# ── prob-expected-value ───────────────────────────────────────────────────────

def _gen_prob_expected_value():
    """E[X], E[2X+3], or E[X²] for a simple discrete RV."""
    den = random.choice([4, 6, 8])
    a = random.randint(1, den - 2)
    b = random.randint(1, den - a - 1)
    c = den - a - b
    num = b + 2 * c
    ex = _fr(num, den)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X]
        ans = ex
        return {
            "problem_text": (
                f"A random variable \\(X\\) has PMF: "
                f"\\(P(X=0) = \\frac{{{a}}}{{{den}}}\\), "
                f"\\(P(X=1) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(X=2) = \\frac{{{c}}}{{{den}}}\\). "
                f"Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(E[X] = \\sum_k k \\cdot P(X=k)\\)."},
                {"level": 2, "text": f"\\(= 0 \\cdot \\frac{{{a}}}{{{den}}} + 1 \\cdot \\frac{{{b}}}{{{den}}} + 2 \\cdot \\frac{{{c}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{num}}}{{{den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # E[aX + b_const] using linearity
        a_coeff = random.randint(2, 4)
        b_const = random.randint(1, 5)
        # E[aX+b] = a*E[X] + b = a*(num/den) + b = (a*num + b*den)/den
        ans_num = a_coeff * num + b_const * den
        ans = _fr(ans_num, den)
        return {
            "problem_text": (
                f"A random variable \\(X\\) has PMF: "
                f"\\(P(X=0) = \\frac{{{a}}}{{{den}}}\\), "
                f"\\(P(X=1) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(X=2) = \\frac{{{c}}}{{{den}}}\\). "
                f"Find \\(E[{a_coeff}X + {b_const}]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "By linearity: \\(E[aX + b] = aE[X] + b\\)."},
                {"level": 2, "text": f"First find \\(E[X] = \\frac{{{num}}}{{{den}}}\\). Then \\({a_coeff} \\cdot \\frac{{{num}}}{{{den}}} + {b_const}\\)."},
                {"level": 3, "text": f"\\(E[{a_coeff}X + {b_const}] = \\frac{{{ans_num}}}{{{den}}} = {ans}\\)."},
            ],
        }
    else:
        # E[X²] = 0²*(a/den) + 1²*(b/den) + 2²*(c/den) = (b + 4c)/den
        ex2_num = b + 4 * c
        ans = _fr(ex2_num, den)
        return {
            "problem_text": (
                f"A random variable \\(X\\) has PMF: "
                f"\\(P(X=0) = \\frac{{{a}}}{{{den}}}\\), "
                f"\\(P(X=1) = \\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(X=2) = \\frac{{{c}}}{{{den}}}\\). "
                f"Find \\(E[X^2]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(E[X^2] = \\sum_k k^2 \\cdot P(X=k)\\)."},
                {"level": 2, "text": f"\\(= 0^2 \\cdot \\frac{{{a}}}{{{den}}} + 1^2 \\cdot \\frac{{{b}}}{{{den}}} + 2^2 \\cdot \\frac{{{c}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{b} + 4 \\cdot {c}}}{{{den}}} = {ans}\\)."},
            ],
        }


# ── prob-indicators ───────────────────────────────────────────────────────────

def _gen_prob_indicators():
    """Indicator random variables: E[I_A], Var(I_A), or sum of indicators."""
    variant = random.choice([0, 1, 2])
    den = random.choice([4, 5, 6, 8, 10])
    k = random.randint(1, den - 1)
    p = _fr(k, den)
    if variant == 0:
        # E[I_A] = P(A)
        ans = p
        return {
            "problem_text": (
                f"Let \\(I_A\\) be the indicator random variable for event \\(A\\), "
                f"where \\(P(A) = \\frac{{{k}}}{{{den}}}\\). "
                f"Find \\(E[I_A]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "An indicator variable \\(I_A\\) equals 1 if \\(A\\) occurs, 0 otherwise."},
                {"level": 2, "text": "\\(E[I_A] = 1 \\cdot P(A) + 0 \\cdot P(A^c) = P(A)\\)."},
                {"level": 3, "text": f"\\(E[I_A] = P(A) = \\frac{{{k}}}{{{den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Var(I_A) = P(A)(1-P(A)) = p(1-p)
        comp = den - k
        var_num = k * comp
        var_den = den * den
        ans = _fr(var_num, var_den)
        return {
            "problem_text": (
                f"Let \\(I_A\\) be the indicator for event \\(A\\) with \\(P(A) = \\frac{{{k}}}{{{den}}}\\). "
                f"Find \\(\\text{{Var}}(I_A)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For a Bernoulli random variable: \\(\\text{Var}(I_A) = P(A)(1 - P(A))\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{k}}}{{{den}}} \\cdot \\frac{{{comp}}}{{{den}}} = \\frac{{{var_num}}}{{{var_den}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(I_A) = {ans}\\)."},
            ],
        }
    else:
        # Sum of indicators: E[I_A + I_B] = P(A) + P(B) (linearity)
        den2 = random.choice([4, 5, 6, 8, 10])
        k2 = random.randint(1, den2 - 1)
        # E[I_A + I_B] = k/den + k2/den2 = (k*den2 + k2*den) / (den*den2)
        sum_num = k * den2 + k2 * den
        sum_den = den * den2
        ans = _fr(sum_num, sum_den)
        return {
            "problem_text": (
                f"Events \\(A\\) and \\(B\\) have \\(P(A) = \\frac{{{k}}}{{{den}}}\\) and \\(P(B) = \\frac{{{k2}}}{{{den2}}}\\). "
                f"Using indicator variables, find \\(E[I_A + I_B]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "By linearity of expectation: \\(E[I_A + I_B] = E[I_A] + E[I_B] = P(A) + P(B)\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{k}}}{{{den}}} + \\frac{{{k2}}}{{{den2}}} = \\frac{{{k*den2} + {k2*den}}}{{{sum_den}}}\\)."},
                {"level": 3, "text": f"\\(E[I_A + I_B] = {ans}\\)."},
            ],
        }


# ── prob-variance ─────────────────────────────────────────────────────────────

def _gen_prob_variance():
    """Var(X), SD(X), or Var(aX+b) for a two-value RV."""
    q = random.choice([3, 4, 5])
    p = random.randint(1, q - 1)
    v = random.randint(2, 5)
    # Var(X) = v²*p*(q-p)/q²
    var_num = v * v * p * (q - p)
    var_den = q * q
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Var(X)
        ans = _fr(var_num, var_den)
        return {
            "problem_text": (
                f"\\(X\\) takes value \\(0\\) with probability \\(\\frac{{{q-p}}}{{{q}}}\\) "
                f"and value \\({v}\\) with probability \\(\\frac{{{p}}}{{{q}}}\\). "
                f"Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(X) = E[X^2] - (E[X])^2\\)."},
                {"level": 2, "text": f"\\(E[X] = {v} \\cdot \\frac{{{p}}}{{{q}}} = \\frac{{{v*p}}}{{{q}}}\\). \\(E[X^2] = {v}^2 \\cdot \\frac{{{p}}}{{{q}}} = \\frac{{{v*v*p}}}{{{q}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = \\frac{{{var_num}}}{{{var_den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Var(aX + b) = a²Var(X)
        a_coeff = random.randint(2, 4)
        b_const = random.randint(1, 5)
        new_var_num = a_coeff * a_coeff * var_num
        ans = _fr(new_var_num, var_den)
        return {
            "problem_text": (
                f"\\(X\\) takes value \\(0\\) with probability \\(\\frac{{{q-p}}}{{{q}}}\\) "
                f"and value \\({v}\\) with probability \\(\\frac{{{p}}}{{{q}}}\\). "
                f"Find \\(\\text{{Var}}({a_coeff}X + {b_const})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(aX + b) = a^2 \\text{Var}(X)\\). The constant \\(b\\) does not affect variance."},
                {"level": 2, "text": f"First find \\(\\text{{Var}}(X) = \\frac{{{var_num}}}{{{var_den}}}\\). Then multiply by \\({a_coeff}^2 = {a_coeff**2}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}({a_coeff}X + {b_const}) = {a_coeff**2} \\cdot \\frac{{{var_num}}}{{{var_den}}} = {ans}\\)."},
            ],
        }
    else:
        # Three-value RV: Var via E[X²] - (E[X])²
        den3 = random.choice([4, 6, 8])
        aa = random.randint(1, den3 - 2)
        bb = random.randint(1, den3 - aa - 1)
        cc = den3 - aa - bb
        # E[X] = (bb + 2*cc)/den3, E[X²] = (bb + 4*cc)/den3
        ex_num = bb + 2 * cc
        ex2_num = bb + 4 * cc
        # Var = E[X²] - (E[X])² = ex2_num/den3 - ex_num²/den3²
        var_n = ex2_num * den3 - ex_num * ex_num
        var_d = den3 * den3
        ans = _fr(var_n, var_d)
        return {
            "problem_text": (
                f"A random variable \\(X\\) has PMF: "
                f"\\(P(X=0) = \\frac{{{aa}}}{{{den3}}}\\), "
                f"\\(P(X=1) = \\frac{{{bb}}}{{{den3}}}\\), "
                f"\\(P(X=2) = \\frac{{{cc}}}{{{den3}}}\\). "
                f"Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(X) = E[X^2] - (E[X])^2\\)."},
                {"level": 2, "text": f"\\(E[X] = \\frac{{{ex_num}}}{{{den3}}}\\), \\(E[X^2] = \\frac{{{ex2_num}}}{{{den3}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = \\frac{{{ex2_num}}}{{{den3}}} - \\frac{{{ex_num}^2}}{{{den3}^2}} = \\frac{{{var_n}}}{{{var_d}}} = {ans}\\)."},
            ],
        }


# ── prob-bernoulli-binom ──────────────────────────────────────────────────────

def _gen_prob_bernoulli_binom():
    """Binomial distribution: E[X], Var[X], or P(X=k) for small k."""
    n = random.randint(4, 10)
    p_den = random.choice([2, 3, 4, 5])
    p_num = random.randint(1, p_den - 1)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X] = np
        num = n * p_num
        ans = _fr(num, p_den)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Binomial}}(n={n}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For \\(X \\sim \\text{Binomial}(n, p)\\), \\(E[X] = np\\)."},
                {"level": 2, "text": f"\\(E[X] = {n} \\cdot \\frac{{{p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(E[X] = \\frac{{{num}}}{{{p_den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Var(X) = np(1-p)
        num = n * p_num * (p_den - p_num)
        ans = _fr(num, p_den**2)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Binomial}}(n={n}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For \\(X \\sim \\text{Binomial}(n, p)\\), \\(\\text{Var}(X) = np(1-p)\\)."},
                {"level": 2, "text": f"\\(\\text{{Var}} = {n} \\cdot \\frac{{{p_num}}}{{{p_den}}} \\cdot \\frac{{{p_den-p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{num}}}{{{p_den**2}}} = {ans}\\)."},
            ],
        }
    else:
        # P(X = 0) = (1-p)^n  or  P(X = n) = p^n — keep n small for clean fractions
        n_small = random.randint(2, 3)
        k = random.choice([0, n_small])
        if k == 0:
            # P(X=0) = (1-p)^n = ((p_den-p_num)/p_den)^n
            comp_num = p_den - p_num
            ans_num = comp_num ** n_small
            ans_den = p_den ** n_small
            ans = _fr(ans_num, ans_den)
            return {
                "problem_text": (
                    f"\\(X \\sim \\text{{Binomial}}(n={n_small}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                    f"Find \\(P(X = 0)\\)."
                ),
                "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
                "hints": [
                    {"level": 1, "text": "\\(P(X=0) = \\binom{n}{0} p^0 (1-p)^n = (1-p)^n\\)."},
                    {"level": 2, "text": f"\\(= \\left(\\frac{{{comp_num}}}{{{p_den}}}\\right)^{{{n_small}}}\\)."},
                    {"level": 3, "text": f"\\(= \\frac{{{ans_num}}}{{{ans_den}}} = {ans}\\)."},
                ],
            }
        else:
            # P(X = n_small) = p^n
            ans_num = p_num ** n_small
            ans_den = p_den ** n_small
            ans = _fr(ans_num, ans_den)
            return {
                "problem_text": (
                    f"\\(X \\sim \\text{{Binomial}}(n={n_small}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                    f"Find \\(P(X = {n_small})\\)."
                ),
                "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
                "hints": [
                    {"level": 1, "text": f"\\(P(X={n_small}) = \\binom{{{n_small}}}{{{n_small}}} p^{{{n_small}}} (1-p)^0 = p^{{{n_small}}}\\)."},
                    {"level": 2, "text": f"\\(= \\left(\\frac{{{p_num}}}{{{p_den}}}\\right)^{{{n_small}}}\\)."},
                    {"level": 3, "text": f"\\(= \\frac{{{ans_num}}}{{{ans_den}}} = {ans}\\)."},
                ],
            }


# ── prob-hypergeometric ───────────────────────────────────────────────────────

def _gen_prob_hypergeometric():
    """Hypergeometric distribution: E[X], Var[X], or P(X=0)."""
    N = random.randint(8, 15)
    K = random.randint(2, N - 2)
    n = random.randint(2, min(K + 2, N - 2))
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X] = nK/N
        ans = _fr(n * K, N)
        return {
            "problem_text": (
                f"A box has \\(N={N}\\) balls, \\(K={K}\\) of which are red. "
                f"\\({n}\\) balls are drawn without replacement. "
                f"Let \\(X\\) = number of red balls drawn. Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For a Hypergeometric RV, \\(E[X] = \\frac{nK}{N}\\)."},
                {"level": 2, "text": f"\\(E[X] = \\frac{{{n} \\cdot {K}}}{{{N}}}\\)."},
                {"level": 3, "text": f"\\(E[X] = \\frac{{{n*K}}}{{{N}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Var(X) = n * K/N * (N-K)/N * (N-n)/(N-1)
        # Compute numerically; keep N, K, n small enough for clean fractions
        N2 = random.choice([6, 8, 10])
        K2 = random.randint(2, N2 - 2)
        n2 = random.randint(2, min(K2, N2 - K2))
        # Var = n * K*(N-K)*n*(N-n) / (N^2 * (N-1)) — complex; just compute
        var_num = n2 * K2 * (N2 - K2) * (N2 - n2)
        var_den = N2 * N2 * (N2 - 1)
        ans = _fr(var_num, var_den)
        return {
            "problem_text": (
                f"A box has \\(N={N2}\\) balls, \\(K={K2}\\) red. "
                f"\\({n2}\\) balls are drawn without replacement (\\(X\\) = red drawn). "
                f"Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "For Hypergeometric: \\(\\text{Var}(X) = n \\cdot \\frac{K}{N} \\cdot \\frac{N-K}{N} \\cdot \\frac{N-n}{N-1}\\)."},
                {"level": 2, "text": f"\\(= {n2} \\cdot \\frac{{{K2}}}{{{N2}}} \\cdot \\frac{{{N2-K2}}}{{{N2}}} \\cdot \\frac{{{N2-n2}}}{{{N2-1}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{var_num}}}{{{var_den}}} = {ans}\\)."},
            ],
        }
    else:
        # P(X=0) = C(N-K, n) / C(N, n) — probability of drawing no red balls
        N3 = random.choice([6, 8, 10])
        K3 = random.randint(2, N3 - 3)
        n3 = random.randint(1, N3 - K3 - 1)
        p_num = comb(N3 - K3, n3)
        p_den = comb(N3, n3)
        ans = _fr(p_num, p_den)
        return {
            "problem_text": (
                f"An urn has \\({N3}\\) balls, \\({K3}\\) red and \\({N3-K3}\\) blue. "
                f"\\({n3}\\) balls are drawn without replacement. "
                f"Find the probability of drawing no red balls."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(P(X=0) = \\frac{\\binom{N-K}{n}}{\\binom{N}{n}}\\) — choose all \\(n\\) from the non-red balls."},
                {"level": 2, "text": f"\\(= \\frac{{\\binom{{{N3-K3}}}{{{n3}}}}}{{\\binom{{{N3}}}{{{n3}}}}} = \\frac{{{p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(P(X=0) = {ans}\\)."},
            ],
        }


# ── prob-geometric-dist ───────────────────────────────────────────────────────

def _gen_prob_geometric_dist():
    """Geometric distribution: E[X], P(X=1), Var(X), or P(X=2)."""
    p_den = random.choice([2, 3, 4, 5])
    p_num = random.randint(1, p_den - 1)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X] = 1/p
        ans = _fr(p_den, p_num)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Geometric}}(p=\\frac{{{p_num}}}{{{p_den}}})\\) "
                f"(number of trials until first success). Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For a Geometric RV (trials until first success), \\(E[X] = \\frac{1}{p}\\)."},
                {"level": 2, "text": f"\\(E[X] = \\frac{{1}}{{{p_num}/{p_den}}} = \\frac{{{p_den}}}{{{p_num}}}\\)."},
                {"level": 3, "text": f"\\(E[X] = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # P(X=1) = p
        ans = _fr(p_num, p_den)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Geometric}}(p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"Find \\(P(X = 1)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "\\(P(X=k) = (1-p)^{k-1} p\\)."},
                {"level": 2, "text": f"\\(P(X=1) = (1-p)^0 \\cdot p = p\\)."},
                {"level": 3, "text": f"\\(P(X=1) = \\frac{{{p_num}}}{{{p_den}}} = {ans}\\)."},
            ],
        }
    else:
        # Var(X) = (1-p)/p² = (p_den - p_num)*p_den² / p_num²  — but this may not simplify cleanly
        # Use Var(X) = (1-p)/p²
        var_num = (p_den - p_num) * p_den * p_den
        var_den = p_num * p_num * p_den
        ans = _fr((p_den - p_num) * p_den, p_num * p_num)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Geometric}}(p=\\frac{{{p_num}}}{{{p_den}}})\\) "
                f"(number of trials until first success). Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For a Geometric RV, \\(\\text{Var}(X) = \\frac{1-p}{p^2}\\)."},
                {"level": 2, "text": f"\\(1-p = \\frac{{{p_den-p_num}}}{{{p_den}}}\\), \\(p^2 = \\frac{{{p_num**2}}}{{{p_den**2}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = \\frac{{{p_den-p_num}}}{{{p_den}}} \\cdot \\frac{{{p_den**2}}}{{{p_num**2}}} = {ans}\\)."},
            ],
        }


# ── prob-poisson ──────────────────────────────────────────────────────────────

def _gen_prob_poisson():
    """Poisson distribution: E[X], Var[X], or SD(X) (when integer)."""
    lam = random.randint(1, 8)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X] = lambda
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Poisson}}(\\lambda={lam})\\). "
                f"Find \\(E[X]\\)."
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "For a Poisson RV, \\(E[X] = \\lambda\\)."},
                {"level": 2, "text": f"\\(E[X] = \\lambda = {lam}\\)."},
                {"level": 3, "text": f"\\(E[X] = {lam}\\)."},
            ],
        }
    elif variant == 1:
        # Var(X) = lambda — ask differently (find rate given variance)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Poisson}}(\\lambda={lam})\\). "
                f"Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "For a Poisson RV, \\(\\text{Var}(X) = \\lambda\\)."},
                {"level": 2, "text": f"\\(\\text{{Var}}(X) = \\lambda = {lam}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = {lam}\\)."},
            ],
        }
    else:
        # P(X=0) = e^{-lambda} — not a nice scalar; instead ask for E[X²] = Var(X) + (E[X])² = lambda + lambda²
        ex2 = lam + lam * lam
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Poisson}}(\\lambda={lam})\\). "
                f"Find \\(E[X^2]\\)."
            ),
            "correct_answer": str(ex2), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Use \\(E[X^2] = \\text{Var}(X) + (E[X])^2\\)."},
                {"level": 2, "text": f"For Poisson: \\(\\text{{Var}}(X) = \\lambda = {lam}\\) and \\(E[X] = \\lambda = {lam}\\)."},
                {"level": 3, "text": f"\\(E[X^2] = {lam} + {lam}^2 = {lam} + {lam*lam} = {ex2}\\)."},
            ],
        }


# ── prob-poisson-approx ───────────────────────────────────────────────────────

def _gen_prob_poisson_approx():
    """Poisson approximation to binomial: find λ, E[X], or Var(X)."""
    n = random.randint(50, 200)
    p_den = random.choice([100, 50, 200])
    p_num = random.randint(1, 4)
    lam = n * p_num // p_den
    while lam == 0:
        p_num += 1
        lam = n * p_num // p_den
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Find lambda
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Binomial}}(n={n}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"Approximate \\(X\\) with a Poisson distribution. What is the Poisson rate parameter \\(\\lambda\\)?"
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The Poisson approximation uses \\(\\lambda = np\\)."},
                {"level": 2, "text": f"\\(\\lambda = {n} \\cdot \\frac{{{p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(\\lambda = {lam}\\)."},
            ],
        }
    elif variant == 1:
        # Under the Poisson approximation, E[X] = lambda
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Binomial}}(n={n}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"Using the Poisson approximation \\(X \\approx \\text{{Poisson}}(\\lambda)\\), "
                f"find the approximate expected value \\(E[X]\\)."
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For the Poisson approximation, \\(\\lambda = np\\) and \\(E[X] = \\lambda\\)."},
                {"level": 2, "text": f"\\(\\lambda = {n} \\cdot \\frac{{{p_num}}}{{{p_den}}} = {lam}\\)."},
                {"level": 3, "text": f"\\(E[X] \\approx {lam}\\)."},
            ],
        }
    else:
        # Given lambda, find what n and p must satisfy for the approximation to hold; reverse: given lambda and p find n
        lam2 = random.randint(2, 8)
        p2_den = random.choice([100, 200])
        p2_num = random.randint(1, 3)
        n2 = lam2 * p2_den // p2_num
        return {
            "problem_text": (
                f"A rare event has probability \\(p = \\frac{{{p2_num}}}{{{p2_den}}}\\) per trial. "
                f"Using the Poisson approximation with \\(\\lambda = {lam2}\\), how many trials \\(n\\) are needed?"
            ),
            "correct_answer": str(n2), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The Poisson approximation sets \\(\\lambda = np\\), so \\(n = \\frac{\\lambda}{p}\\)."},
                {"level": 2, "text": f"\\(n = \\frac{{{lam2}}}{{{p2_num}/{p2_den}}} = {lam2} \\cdot \\frac{{{p2_den}}}{{{p2_num}}}\\)."},
                {"level": 3, "text": f"\\(n = {n2}\\)."},
            ],
        }


# ── prob-continuous-rv ────────────────────────────────────────────────────────

def _gen_prob_continuous_rv():
    """Uniform distribution: E[X], P(X < t), or Var(X)."""
    a = 0
    b = random.randint(2, 8)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X] = (a+b)/2
        num = a + b
        ans = _fr(num, 2)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Uniform}}({a}, {b})\\). Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For \\(X \\sim \\text{Uniform}(a, b)\\), \\(E[X] = \\frac{a+b}{2}\\)."},
                {"level": 2, "text": f"\\(E[X] = \\frac{{{a}+{b}}}{{2}} = \\frac{{{a+b}}}{{2}}\\)."},
                {"level": 3, "text": f"\\(E[X] = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # P(X < t) = (t - a) / (b - a)
        t = random.randint(1, b - 1)
        ans = _fr(t - a, b - a)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Uniform}}({a}, {b})\\). Find \\(P(X < {t})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For Uniform\\((a,b)\\), \\(P(X < t) = \\frac{t - a}{b - a}\\)."},
                {"level": 2, "text": f"\\(P(X < {t}) = \\frac{{{t} - {a}}}{{{b} - {a}}} = \\frac{{{t-a}}}{{{b-a}}}\\)."},
                {"level": 3, "text": f"\\(P(X < {t}) = {ans}\\)."},
            ],
        }
    else:
        # Var(X) = (b-a)²/12
        length = b - a
        var_num = length * length
        ans = _fr(var_num, 12)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Uniform}}({a}, {b})\\). Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Uniform\\((a,b)\\), \\(\\text{Var}(X) = \\frac{(b-a)^2}{12}\\)."},
                {"level": 2, "text": f"\\(b - a = {length}\\), so \\(\\text{{Var}}(X) = \\frac{{{length}^2}}{{12}} = \\frac{{{var_num}}}{{12}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = {ans}\\)."},
            ],
        }


# ── prob-normal ───────────────────────────────────────────────────────────────

def _gen_prob_normal():
    """Normal distribution: z-score, E[X], Var(X), or standardize a sum."""
    mu = random.randint(-2, 4)
    sigma = random.randint(1, 3)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # z-score
        x = mu + random.choice([-2, -1, 1, 2]) * sigma
        ans = str((x - mu) // sigma)
        return {
            "problem_text": (
                f"\\(X \\sim N(\\mu={mu}, \\sigma^2={sigma**2})\\). "
                f"Find the \\(z\\)-score for \\(x = {x}\\): \\(z = \\frac{{x - \\mu}}{{\\sigma}}\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The z-score standardizes \\(x\\): \\(z = \\frac{x - \\mu}{\\sigma}\\)."},
                {"level": 2, "text": f"\\(z = \\frac{{{x} - {mu}}}{{{sigma}}}\\)."},
                {"level": 3, "text": f"\\(z = \\frac{{{x-mu}}}{{{sigma}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # E[X] = mu
        return {
            "problem_text": (
                f"\\(X \\sim N(\\mu={mu}, \\sigma^2={sigma**2})\\). Find \\(E[X]\\)."
            ),
            "correct_answer": str(mu), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "For a normal distribution, \\(E[X] = \\mu\\)."},
                {"level": 2, "text": f"\\(E[X] = \\mu = {mu}\\)."},
                {"level": 3, "text": f"\\(E[X] = {mu}\\)."},
            ],
        }
    else:
        # Var(X) = sigma²
        return {
            "problem_text": (
                f"\\(X \\sim N(\\mu={mu}, \\sigma^2={sigma**2})\\). Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": str(sigma**2), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "For a normal distribution, \\(\\text{Var}(X) = \\sigma^2\\)."},
                {"level": 2, "text": f"The distribution is \\(N({mu}, {sigma**2})\\), so \\(\\sigma^2 = {sigma**2}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = {sigma**2}\\)."},
            ],
        }


# ── prob-exponential-dist ─────────────────────────────────────────────────────

def _gen_prob_exponential_dist():
    """Exponential distribution: E[X], Var[X], or find rate λ given mean."""
    lam = random.randint(1, 5)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        ans = _fr(1, lam)
        return {
            "problem_text": f"\\(X \\sim \\text{{Exponential}}(\\lambda={lam})\\). Find \\(E[X]\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For an Exponential RV with rate \\(\\lambda\\), \\(E[X] = \\frac{1}{\\lambda}\\)."},
                {"level": 2, "text": f"\\(E[X] = \\frac{{1}}{{{lam}}}\\)."},
                {"level": 3, "text": f"\\(E[X] = {ans}\\)."},
            ],
        }
    elif variant == 1:
        ans = _fr(1, lam**2)
        return {
            "problem_text": f"\\(X \\sim \\text{{Exponential}}(\\lambda={lam})\\). Find \\(\\text{{Var}}(X)\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Exponential\\((\\lambda)\\), \\(\\text{Var}(X) = \\frac{1}{\\lambda^2}\\)."},
                {"level": 2, "text": f"\\(\\text{{Var}}(X) = \\frac{{1}}{{{lam}^2}} = \\frac{{1}}{{{lam**2}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = {ans}\\)."},
            ],
        }
    else:
        # Given E[X] = 1/lambda, find lambda (reverse)
        mean_val = lam  # mean = lam, so actual lambda = 1/lam_val... use integer mean for clarity
        mean = random.randint(2, 6)
        rate = mean  # E[X] = 1/rate → rate = 1/mean... let E[X] = 1/mean so rate = mean?
        # Actually: if E[X] = 1/lambda, and we give E[X] = 1/mean_given, lambda = mean_given
        mean_given = random.randint(2, 6)
        # E[X] = 1/lambda → lambda = 1/E[X] = mean_given (when E[X] = 1/mean_given)
        # Let's say E[X] = mean_given (integer), then lambda = 1/mean_given
        ans = _fr(1, mean_given)
        return {
            "problem_text": (
                f"The lifetime of a device follows an Exponential distribution "
                f"with mean \\(E[X] = {mean_given}\\) years. Find the rate parameter \\(\\lambda\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For an Exponential RV: \\(E[X] = \\frac{1}{\\lambda}\\), so \\(\\lambda = \\frac{1}{E[X]}\\)."},
                {"level": 2, "text": f"\\(\\lambda = \\frac{{1}}{{{mean_given}}}\\)."},
                {"level": 3, "text": f"\\(\\lambda = {ans}\\)."},
            ],
        }


# ── prob-memoryless ───────────────────────────────────────────────────────────

def _gen_prob_memoryless():
    """Memoryless property: E[X|X>s] for Exponential, or Geometric P(X>m+n|X>m)."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X|X>s] = s + 1/lam for Exponential
        lam = random.randint(1, 4)
        s = random.randint(1, 4)
        val = _fr(s * lam + 1, lam)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Exponential}}(\\lambda={lam})\\). "
                f"By the memoryless property, find \\(E[X \\mid X > {s}]\\)."
            ),
            "correct_answer": val, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "The memoryless property says: given \\(X > s\\), the remaining lifetime has the same Exponential\\((\\lambda)\\) distribution."},
                {"level": 2, "text": f"So \\(E[X \\mid X > {s}] = {s} + E[X] = {s} + \\frac{{1}}{{{lam}}}\\)."},
                {"level": 3, "text": f"\\(= {s} + \\frac{{1}}{{{lam}}} = \\frac{{{s*lam+1}}}{{{lam}}} = {val}\\)."},
            ],
        }
    elif variant == 1:
        # Geometric memoryless: P(X > m+n | X > m) = P(X > n) = (1-p)^n
        p_den = random.choice([2, 3, 4])
        p_num = random.randint(1, p_den - 1)
        n = random.randint(1, 3)
        # P(X > n) = (1-p)^n = ((p_den - p_num)/p_den)^n
        comp = p_den - p_num
        ans_num = comp ** n
        ans_den = p_den ** n
        ans = _fr(ans_num, ans_den)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Geometric}}(p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"By the memoryless property, \\(P(X > m+{n} \\mid X > m)\\) equals \\(P(X > {n})\\). "
                f"Find \\(P(X > {n})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "The Geometric distribution is memoryless: \\(P(X > m+n \\mid X > m) = P(X > n)\\)."},
                {"level": 2, "text": f"\\(P(X > n) = (1-p)^n = \\left(\\frac{{{comp}}}{{{p_den}}}\\right)^{{{n}}}\\)."},
                {"level": 3, "text": f"\\(P(X > {n}) = \\frac{{{ans_num}}}{{{ans_den}}} = {ans}\\)."},
            ],
        }
    else:
        # Exponential memoryless: P(X > a+b | X > a) = P(X > b), ask for E[X | X > s] with different framing
        lam = random.randint(1, 4)
        s = random.randint(1, 3)
        t = random.randint(1, 3)
        val = _fr(s * lam + 1, lam)
        return {
            "problem_text": (
                f"A machine has been running for \\({s}\\) hours without failure. "
                f"Its lifetime \\(X \\sim \\text{{Exponential}}(\\lambda={lam})\\). "
                f"What is the expected total lifetime \\(E[X \\mid X > {s}]\\)?"
            ),
            "correct_answer": val, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Due to the memoryless property of the Exponential distribution, \\(E[X \\mid X > s] = s + \\frac{1}{\\lambda}\\)."},
                {"level": 2, "text": f"\\(E[X \\mid X > {s}] = {s} + \\frac{{1}}{{{lam}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{s*lam+1}}}{{{lam}}} = {val}\\)."},
            ],
        }


# ── prob-gamma-dist ───────────────────────────────────────────────────────────

def _gen_prob_gamma_dist():
    """Gamma distribution: E[X], Var[X], or shape parameter from mean/variance."""
    alpha = random.randint(2, 6)
    beta = random.randint(1, 4)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        ans = _fr(alpha, beta)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Gamma}}(\\alpha={alpha}, \\beta={beta})\\) "
                f"(rate parameterization). Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Gamma\\((\\alpha, \\beta)\\) with rate \\(\\beta\\), \\(E[X] = \\frac{\\alpha}{\\beta}\\)."},
                {"level": 2, "text": f"\\(E[X] = \\frac{{{alpha}}}{{{beta}}}\\)."},
                {"level": 3, "text": f"\\(E[X] = {ans}\\)."},
            ],
        }
    elif variant == 1:
        ans = _fr(alpha, beta**2)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Gamma}}(\\alpha={alpha}, \\beta={beta})\\) "
                f"(rate parameterization). Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Gamma\\((\\alpha, \\beta)\\) with rate \\(\\beta\\), \\(\\text{Var}(X) = \\frac{\\alpha}{\\beta^2}\\)."},
                {"level": 2, "text": f"\\(\\text{{Var}}(X) = \\frac{{{alpha}}}{{{beta}^2}} = \\frac{{{alpha}}}{{{beta**2}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = {ans}\\)."},
            ],
        }
    else:
        # Find shape α given E[X] and Var(X): α = E[X]²/Var(X)... may not be integer always
        # Use: α = E[X]*beta, Var = alpha/beta² → give E[X] and rate β, find α
        # E[X] = alpha/beta, so alpha = E[X]*beta
        mean_num = alpha  # E[X] = alpha/beta as a fraction
        mean_den = beta
        ans = str(alpha)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Gamma}}(\\alpha, \\beta={beta})\\) (rate parameterization) "
                f"with \\(E[X] = \\frac{{{mean_num}}}{{{mean_den}}}\\). Find \\(\\alpha\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Gamma\\((\\alpha, \\beta)\\) with rate \\(\\beta\\): \\(E[X] = \\frac{\\alpha}{\\beta}\\), so \\(\\alpha = E[X] \\cdot \\beta\\)."},
                {"level": 2, "text": f"\\(\\alpha = \\frac{{{mean_num}}}{{{mean_den}}} \\cdot {beta}\\)."},
                {"level": 3, "text": f"\\(\\alpha = {alpha}\\)."},
            ],
        }


# ── prob-normal-approx ────────────────────────────────────────────────────────

def _gen_prob_normal_approx():
    """CLT/normal approx: find μ, σ², or the standardized z-value."""
    n = random.randint(20, 100)
    p_den = random.choice([2, 4, 5])
    p_num = random.randint(1, p_den - 1)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # μ = np
        mu_num = n * p_num
        ans = _fr(mu_num, p_den)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Binomial}}(n={n}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"For the normal approximation \\(X \\approx N(\\mu, \\sigma^2)\\), find \\(\\mu\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Normal approximation to binomial: \\(\\mu = np\\)."},
                {"level": 2, "text": f"\\(\\mu = {n} \\cdot \\frac{{{p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(\\mu = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # σ² = np(1-p)
        num = n * p_num * (p_den - p_num)
        ans = _fr(num, p_den**2)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Binomial}}(n={n}, p=\\frac{{{p_num}}}{{{p_den}}})\\). "
                f"For the normal approximation, find \\(\\sigma^2\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Normal approximation: \\(\\sigma^2 = np(1-p)\\)."},
                {"level": 2, "text": f"\\(\\sigma^2 = {n} \\cdot \\frac{{{p_num}}}{{{p_den}}} \\cdot \\frac{{{p_den-p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(\\sigma^2 = \\frac{{{num}}}{{{p_den**2}}} = {ans}\\)."},
            ],
        }
    else:
        # Find n so that E[X] = target integer (reverse: given mu and p, find n)
        n2 = random.randint(20, 100)
        p2_den = random.choice([4, 5, 10])
        p2_num = random.randint(1, p2_den - 1)
        mu_target_num = n2 * p2_num
        mu_target = _fr(mu_target_num, p2_den)
        # Ask: if X~Bin(n, p) and mu = target, find n
        ans = str(n2)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Binomial}}(n, p=\\frac{{{p2_num}}}{{{p2_den}}})\\) and the normal approximation "
                f"has mean \\(\\mu = {mu_target}\\). Find \\(n\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The approximating normal has \\(\\mu = np\\), so \\(n = \\mu / p\\)."},
                {"level": 2, "text": f"\\(n = {mu_target} \\div \\frac{{{p2_num}}}{{{p2_den}}} = {mu_target} \\cdot \\frac{{{p2_den}}}{{{p2_num}}}\\)."},
                {"level": 3, "text": f"\\(n = {n2}\\)."},
            ],
        }


# ── prob-cdf-method ───────────────────────────────────────────────────────────

def _gen_prob_cdf_method():
    """CDF method: F_Y(y) for linear transform of Uniform, or CDF of min/max."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Y = aX + b, X ~ Uniform(0,1)
        a = random.randint(2, 5)
        b = random.randint(0, 3)
        t = random.randint(b + 1, a + b - 1)
        ans = _fr(t - b, a)
        b_part = f" + {b}" if b > 0 else ""
        return {
            "problem_text": (
                f"Let \\(X \\sim \\text{{Uniform}}(0, 1)\\) and \\(Y = {a}X{b_part}\\). "
                f"Find \\(F_Y({t}) = P(Y \\leq {t})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(P(Y \\leq t) = P(aX + b \\leq t) = P\\!\\left(X \\leq \\frac{t-b}{a}\\right)\\)."},
                {"level": 2, "text": f"Since \\(X \\sim \\text{{Uniform}}(0,1)\\), \\(P(X \\leq u) = u\\) for \\(0 \\leq u \\leq 1\\)."},
                {"level": 3, "text": f"\\(F_Y({t}) = \\frac{{{t}-{b}}}{{{a}}} = \\frac{{{t-b}}}{{{a}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # CDF of Y = X², X ~ Uniform(0,1): F_Y(y) = sqrt(y) — not clean scalar
        # Instead: Y = aX, find the CDF at a fraction
        a = random.randint(2, 6)
        # F_Y(t) = t/a; choose t as multiple of a for clean answer? No—choose arbitrary t in (0,a)
        # Ask: find P(Y > t) = 1 - t/a for integer t in 1..a-1
        t = random.randint(1, a - 1)
        ans = _fr(a - t, a)
        return {
            "problem_text": (
                f"Let \\(X \\sim \\text{{Uniform}}(0, 1)\\) and \\(Y = {a}X\\). "
                f"Find \\(P(Y > {t})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(P(Y > t) = P({a}X > t) = P\\!\\left(X > \\frac{{t}}{{{a}}}\\right) = 1 - \\frac{{t}}{{{a}}}\\)."},
                {"level": 2, "text": f"\\(= 1 - \\frac{{{t}}}{{{a}}} = \\frac{{{a} - {t}}}{{{a}}}\\)."},
                {"level": 3, "text": f"\\(P(Y > {t}) = \\frac{{{a-t}}}{{{a}}} = {ans}\\)."},
            ],
        }
    else:
        # CDF of max of n iid Uniform(0,1): F_{X_(n)}(t) = t^n for t in [0,1]
        # Evaluated at a fraction k/m
        n = random.randint(2, 3)
        m = random.choice([2, 3, 4])
        k = random.randint(1, m - 1)
        # t = k/m; F = (k/m)^n
        ans = _fr(k ** n, m ** n)
        return {
            "problem_text": (
                f"Let \\(X_1, \\ldots, X_{{{n}}}\\) be iid \\(\\text{{Uniform}}(0,1)\\) and \\(M = \\max(X_1, \\ldots, X_{{{n}}})\\). "
                f"Find the CDF \\(F_M\\!\\left(\\frac{{{k}}}{{{m}}}\\right) = P\\!\\left(M \\leq \\frac{{{k}}}{{{m}}}\\right)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "\\(P(M \\leq t) = P(X_1 \\leq t, \\ldots, X_n \\leq t) = t^n\\) (by independence and Uniform CDF)."},
                {"level": 2, "text": f"\\(= \\left(\\frac{{{k}}}{{{m}}}\\right)^{{{n}}} = \\frac{{{k}^{{{n}}}}}{{{m}^{{{n}}}}}\\)."},
                {"level": 3, "text": f"\\(F_M\\!\\left(\\frac{{{k}}}{{{m}}}\\right) = \\frac{{{k**n}}}{{{m**n}}} = {ans}\\)."},
            ],
        }


# ── prob-transformations ──────────────────────────────────────────────────────

def _gen_prob_transformations():
    """E[aX + b], Var(aX + b), or E[X+Y] using linearity."""
    mu = random.randint(1, 6)
    sig2 = random.randint(1, 5)
    a = random.randint(2, 4)
    b = random.randint(1, 6)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        ans = str(a * mu + b)
        return {
            "problem_text": (
                f"\\(E[X] = {mu}\\). Find \\(E[{a}X + {b}]\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Linearity of expectation: \\(E[aX + b] = aE[X] + b\\)."},
                {"level": 2, "text": f"\\({a} \\cdot {mu} + {b}\\)."},
                {"level": 3, "text": f"\\(= {a*mu} + {b} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        ans = str(a**2 * sig2)
        return {
            "problem_text": (
                f"\\(\\text{{Var}}(X) = {sig2}\\). Find \\(\\text{{Var}}({a}X + {b})\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(aX + b) = a^2 \\text{Var}(X)\\). Constants shift don't affect variance."},
                {"level": 2, "text": f"\\({a}^2 \\cdot {sig2} = {a**2} \\cdot {sig2}\\)."},
                {"level": 3, "text": f"\\(= {ans}\\)."},
            ],
        }
    else:
        # E[X + Y] = E[X] + E[Y] (no independence needed)
        mu_y = random.randint(1, 6)
        ans = str(mu + mu_y)
        return {
            "problem_text": (
                f"\\(E[X] = {mu}\\) and \\(E[Y] = {mu_y}\\). "
                f"Find \\(E[X + Y]\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "By linearity of expectation: \\(E[X + Y] = E[X] + E[Y]\\) (always, regardless of dependence)."},
                {"level": 2, "text": f"\\(E[X + Y] = {mu} + {mu_y}\\)."},
                {"level": 3, "text": f"\\(E[X + Y] = {ans}\\)."},
            ],
        }


# ── prob-inverse-cdf ──────────────────────────────────────────────────────────

def _gen_prob_inverse_cdf():
    """Quantile (inverse CDF): Uniform quantile, median of Uniform, or Exponential quantile."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Uniform(0, b) quantile
        a = 0
        b = random.randint(2, 8)
        k = random.randint(1, b - 1)
        p_num = k; p_den = b
        ans = str(k)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Uniform}}({a}, {b})\\). "
                f"Find the \\(\\frac{{{p_num}}}{{{p_den}}}\\)-quantile: "
                f"the value \\(x\\) such that \\(P(X \\leq x) = \\frac{{{p_num}}}{{{p_den}}}\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Uniform\\((a,b)\\), \\(F^{-1}(p) = a + p(b-a)\\)."},
                {"level": 2, "text": f"\\(F^{{-1}}\\!\\left(\\frac{{{p_num}}}{{{p_den}}}\\right) = {a} + \\frac{{{p_num}}}{{{p_den}}} \\cdot ({b} - {a})\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{p_num}}}{{{p_den}}} \\cdot {b} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Median of Uniform(a, b): (a+b)/2
        a = random.randint(0, 3)
        b = random.randint(a + 2, a + 8)
        ans = _fr(a + b, 2)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Uniform}}({a}, {b})\\). "
                f"Find the median (the value \\(m\\) such that \\(P(X \\leq m) = \\frac{{1}}{{2}}\\))."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For Uniform\\((a,b)\\), \\(F^{-1}(1/2) = \\frac{a+b}{2}\\)."},
                {"level": 2, "text": f"Median \\(= \\frac{{{a}+{b}}}{{2}} = \\frac{{{a+b}}}{{2}}\\)."},
                {"level": 3, "text": f"Median \\(= {ans}\\)."},
            ],
        }
    else:
        # Uniform(0, b): find x such that P(X > x) = k/b
        a = 0
        b = random.randint(3, 8)
        k = random.randint(1, b - 1)
        # P(X > x) = (b-x)/b = k/b → x = b - k
        ans = str(b - k)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Uniform}}({a}, {b})\\). "
                f"Find the value \\(x\\) such that \\(P(X > x) = \\frac{{{k}}}{{{b}}}\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Uniform\\((0,b)\\): \\(P(X > x) = \\frac{b-x}{b}\\). Set this equal to \\(\\frac{k}{b}\\) and solve."},
                {"level": 2, "text": f"\\(\\frac{{b - x}}{{{b}}} = \\frac{{{k}}}{{{b}}} \\Rightarrow b - x = {k} \\Rightarrow x = b - {k}\\)."},
                {"level": 3, "text": f"\\(x = {b} - {k} = {b-k}\\)."},
            ],
        }


# ── prob-joint-discrete ───────────────────────────────────────────────────────

def _gen_prob_joint_discrete():
    """Joint PMF: find joint probability, marginal, or check independence."""
    den = random.choice([8, 10, 12])
    a = random.randint(1, den//2 - 1)
    b = random.randint(1, den//2 - 1)
    c = random.randint(1, den - a - b - 1)
    d = den - a - b - c
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Joint or marginal probability
        choices = [("P(X=0, Y=0)", _fr(a, den)),
                   ("P(X=0, Y=1)", _fr(b, den)),
                   ("P(X=1, Y=0)", _fr(c, den)),
                   ("P(X=1, Y=1)", _fr(d, den)),
                   ("P(X=0)", _fr(a+b, den)),
                   ("P(X=1)", _fr(c+d, den))]
        label, ans = random.choice(choices)
        return {
            "problem_text": (
                f"The joint PMF of \\((X, Y)\\) is: "
                f"\\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find \\({label}\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Read off the joint probability directly, or sum across the relevant row/column for a marginal."},
                {"level": 2, "text": f"Identify the cell(s) corresponding to \\({label}\\)."},
                {"level": 3, "text": f"\\({label} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # P(Y=1) (marginal of Y)
        ans = _fr(b + d, den)
        return {
            "problem_text": (
                f"The joint PMF of \\((X, Y)\\) is: "
                f"\\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find the marginal probability \\(P(Y=1)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The marginal of \\(Y\\) is obtained by summing over all values of \\(X\\)."},
                {"level": 2, "text": f"\\(P(Y=1) = P(X=0, Y=1) + P(X=1, Y=1) = \\frac{{{b}}}{{{den}}} + \\frac{{{d}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(P(Y=1) = \\frac{{{b+d}}}{{{den}}} = {ans}\\)."},
            ],
        }
    else:
        # E[XY] = 0*0*P(0,0) + 0*1*P(0,1) + 1*0*P(1,0) + 1*1*P(1,1) = d/den
        ans = _fr(d, den)
        return {
            "problem_text": (
                f"The joint PMF of \\((X, Y)\\) is: "
                f"\\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find \\(E[XY]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(E[XY] = \\sum_{x,y} xy \\cdot P(X=x, Y=y)\\)."},
                {"level": 2, "text": f"Only the term \\(x=1, y=1\\) contributes (since \\(xy=0\\) otherwise): \\(1 \\cdot 1 \\cdot P(1,1)\\)."},
                {"level": 3, "text": f"\\(E[XY] = \\frac{{{d}}}{{{den}}} = {ans}\\)."},
            ],
        }


# ── prob-joint-continuous ─────────────────────────────────────────────────────

def _gen_prob_joint_continuous():
    """Joint Uniform on rectangle: P(X<s,Y<t), P(X+Y<c), or E[X]."""
    a = random.randint(2, 4)
    b = random.randint(2, 4)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # P(X < s, Y < t)
        s = random.randint(1, a - 1)
        t = random.randint(1, b - 1)
        ans = _fr(s * t, a * b)
        return {
            "problem_text": (
                f"\\((X, Y)\\) is uniformly distributed on \\([0,{a}] \\times [0,{b}]\\). "
                f"Find \\(P(X < {s},\\, Y < {t})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For a uniform distribution on a rectangle, probability = favorable area / total area."},
                {"level": 2, "text": f"Favorable area = \\({s} \\times {t} = {s*t}\\). Total area = \\({a} \\times {b} = {a*b}\\)."},
                {"level": 3, "text": f"\\(P = \\frac{{{s*t}}}{{{a*b}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # E[X] for joint uniform on [0,a]x[0,b]: marginal of X is Uniform(0,a), so E[X] = a/2
        ans = _fr(a, 2)
        return {
            "problem_text": (
                f"\\((X, Y)\\) is uniformly distributed on \\([0,{a}] \\times [0,{b}]\\). "
                f"Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The marginal of \\(X\\) is \\(\\text{Uniform}(0, {a})\\), so \\(E[X] = \\frac{a}{2}\\)."},
                {"level": 2, "text": f"\\(E[X] = \\frac{{{a}}}{{2}}\\)."},
                {"level": 3, "text": f"\\(E[X] = {ans}\\)."},
            ],
        }
    else:
        # P(X < s) alone (marginal)
        s = random.randint(1, a - 1)
        ans = _fr(s, a)
        return {
            "problem_text": (
                f"\\((X, Y)\\) is uniformly distributed on \\([0,{a}] \\times [0,{b}]\\). "
                f"Find \\(P(X < {s})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The marginal distribution of \\(X\\) is \\(\\text{Uniform}(0,{a})\\)."},
                {"level": 2, "text": f"\\(P(X < {s}) = \\frac{{{s}}}{{{a}}}\\) (area of the favorable strip divided by total area)."},
                {"level": 3, "text": f"\\(P(X < {s}) = {ans}\\)."},
            ],
        }


# ── prob-marginal ─────────────────────────────────────────────────────────────

def _gen_prob_marginal():
    """Marginal PMF from a joint table: P_X, P_Y, or E[X] via marginal."""
    den = random.choice([8, 10, 12])
    a = random.randint(1, den//2 - 1)
    b = random.randint(1, den - a - 2)
    c = random.randint(1, den - a - b - 1)
    d = den - a - b - c
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # P_X(0) or P_X(1)
        ask = random.randint(0, 1)
        if ask == 0:
            ans = _fr(a + b, den)
            label = "\\(P_X(0)\\)"
            formula = f"\\frac{{{a}+{b}}}{{{den}}}"
        else:
            ans = _fr(c + d, den)
            label = "\\(P_X(1)\\)"
            formula = f"\\frac{{{c}+{d}}}{{{den}}}"
        return {
            "problem_text": (
                f"Joint PMF: \\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find the marginal {label}."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The marginal PMF of \\(X\\) is obtained by summing over all values of \\(Y\\)."},
                {"level": 2, "text": f"Sum the joint probabilities in the row for the relevant \\(X\\) value."},
                {"level": 3, "text": f"{label} \\(= {formula} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # P_Y(0) or P_Y(1)
        ask = random.randint(0, 1)
        if ask == 0:
            ans = _fr(a + c, den)
            label = "\\(P_Y(0)\\)"
            formula = f"\\frac{{{a}+{c}}}{{{den}}}"
        else:
            ans = _fr(b + d, den)
            label = "\\(P_Y(1)\\)"
            formula = f"\\frac{{{b}+{d}}}{{{den}}}"
        return {
            "problem_text": (
                f"Joint PMF: \\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find the marginal {label}."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The marginal PMF of \\(Y\\) is obtained by summing over all values of \\(X\\)."},
                {"level": 2, "text": f"Sum the joint probabilities in the column for the relevant \\(Y\\) value."},
                {"level": 3, "text": f"{label} \\(= {formula} = {ans}\\)."},
            ],
        }
    else:
        # E[X] using marginal: E[X] = 0*P_X(0) + 1*P_X(1) = (c+d)/den
        ex_num = c + d
        ans = _fr(ex_num, den)
        return {
            "problem_text": (
                f"Joint PMF: \\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find \\(E[X]\\) using the marginal distribution of \\(X\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "First find the marginal PMF of \\(X\\): \\(P_X(0) = P(X=0)\\), \\(P_X(1) = P(X=1)\\). Then compute \\(E[X]\\)."},
                {"level": 2, "text": f"\\(P_X(1) = \\frac{{{c}+{d}}}{{{den}}}\\). \\(E[X] = 0 \\cdot P_X(0) + 1 \\cdot P_X(1)\\)."},
                {"level": 3, "text": f"\\(E[X] = \\frac{{{ex_num}}}{{{den}}} = {ans}\\)."},
            ],
        }


# ── prob-conditional-dist ─────────────────────────────────────────────────────

def _gen_prob_conditional_dist():
    """Conditional PMF P(X|Y=0), P(X|Y=1), or P(Y|X=0)."""
    den = random.choice([8, 10, 12])
    a = random.randint(1, den//2 - 1)
    b = random.randint(1, den - a - 2)
    c = random.randint(1, den - a - b - 1)
    d = den - a - b - c
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # P(X=0|Y=0) or P(X=1|Y=0)
        ask = random.randint(0, 1)
        if ask == 0:
            ans = _fr(a, a + c)
            label = "\\(P(X=0 \\mid Y=0)\\)"
            expr = f"\\frac{{{a}}}{{{a+c}}}"
        else:
            ans = _fr(c, a + c)
            label = "\\(P(X=1 \\mid Y=0)\\)"
            expr = f"\\frac{{{c}}}{{{a+c}}}"
        return {
            "problem_text": (
                f"Joint PMF: \\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find {label}."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(P(X=x \\mid Y=y) = \\frac{P(X=x, Y=y)}{P(Y=y)}\\)."},
                {"level": 2, "text": f"\\(P(Y=0) = \\frac{{{a}+{c}}}{{{den}}}\\). Divide the relevant joint probability by \\(P(Y=0)\\)."},
                {"level": 3, "text": f"{label} \\(= {expr} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # E[X|Y=1] using conditional distribution (binary X, so E[X|Y=1] = P(X=1|Y=1) = d/(b+d))
        ans = _fr(d, b + d)
        return {
            "problem_text": (
                f"Joint PMF: \\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find \\(E[X \\mid Y=1]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "First find the conditional distribution of \\(X\\) given \\(Y=1\\), then compute its expectation."},
                {"level": 2, "text": f"\\(P(Y=1) = \\frac{{{b}+{d}}}{{{den}}}\\). \\(P(X=1 \\mid Y=1) = \\frac{{{d}}}{{{b+d}}}\\). Since \\(X \\in \\{{0,1\\}}\\): \\(E[X \\mid Y=1] = P(X=1 \\mid Y=1)\\)."},
                {"level": 3, "text": f"\\(E[X \\mid Y=1] = \\frac{{{d}}}{{{b+d}}} = {ans}\\)."},
            ],
        }
    else:
        # P(Y=0|X=1) or P(Y=1|X=1) — given X=1
        ask = random.randint(0, 1)
        if ask == 0:
            ans = _fr(c, c + d)
            label = "\\(P(Y=0 \\mid X=1)\\)"
            expr = f"\\frac{{{c}}}{{{c+d}}}"
        else:
            ans = _fr(d, c + d)
            label = "\\(P(Y=1 \\mid X=1)\\)"
            expr = f"\\frac{{{d}}}{{{c+d}}}"
        return {
            "problem_text": (
                f"Joint PMF: \\(P(0,0)=\\frac{{{a}}}{{{den}}}\\), \\(P(0,1)=\\frac{{{b}}}{{{den}}}\\), "
                f"\\(P(1,0)=\\frac{{{c}}}{{{den}}}\\), \\(P(1,1)=\\frac{{{d}}}{{{den}}}\\). "
                f"Find {label}."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(P(Y=y \\mid X=1) = \\frac{P(X=1, Y=y)}{P(X=1)}\\)."},
                {"level": 2, "text": f"\\(P(X=1) = \\frac{{{c}+{d}}}{{{den}}}\\)."},
                {"level": 3, "text": f"{label} \\(= {expr} = {ans}\\)."},
            ],
        }


# ── prob-covariance ───────────────────────────────────────────────────────────

def _gen_prob_covariance():
    """Cov(X,Y), Var(X+Y), or Cov(aX, bY) = ab·Cov(X,Y)."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Given E[XY], E[X], E[Y], find Cov
        ex = random.randint(1, 4)
        ey = random.randint(1, 4)
        cov = random.randint(-3, 4)
        exy = ex * ey + cov
        return {
            "problem_text": (
                f"\\(E[X] = {ex}\\), \\(E[Y] = {ey}\\), \\(E[XY] = {exy}\\). "
                f"Find \\(\\text{{Cov}}(X, Y)\\)."
            ),
            "correct_answer": str(cov), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\text{Cov}(X,Y) = E[XY] - E[X]E[Y]\\)."},
                {"level": 2, "text": f"\\(E[X]E[Y] = {ex} \\cdot {ey} = {ex*ey}\\)."},
                {"level": 3, "text": f"\\(\\text{{Cov}} = {exy} - {ex*ey} = {cov}\\)."},
            ],
        }
    elif variant == 1:
        # Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y)
        vx = random.randint(1, 4)
        vy = random.randint(1, 4)
        cov = random.randint(-2, 3)
        v_sum = vx + vy + 2 * cov
        return {
            "problem_text": (
                f"\\(\\text{{Var}}(X) = {vx}\\), \\(\\text{{Var}}(Y) = {vy}\\), \\(\\text{{Cov}}(X,Y) = {cov}\\). "
                f"Find \\(\\text{{Var}}(X + Y)\\)."
            ),
            "correct_answer": str(v_sum), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(X+Y) = \\text{Var}(X) + \\text{Var}(Y) + 2\\text{Cov}(X,Y)\\)."},
                {"level": 2, "text": f"\\({vx} + {vy} + 2({cov})\\)."},
                {"level": 3, "text": f"\\(= {vx} + {vy} + {2*cov} = {v_sum}\\)."},
            ],
        }
    else:
        # Cov(aX, bY) = ab * Cov(X, Y)
        cov = random.randint(1, 5)
        a_scale = random.randint(2, 4)
        b_scale = random.randint(2, 4)
        new_cov = a_scale * b_scale * cov
        return {
            "problem_text": (
                f"\\(\\text{{Cov}}(X, Y) = {cov}\\). Find \\(\\text{{Cov}}({a_scale}X,\\, {b_scale}Y)\\)."
            ),
            "correct_answer": str(new_cov), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For constants \\(a, b\\): \\(\\text{Cov}(aX, bY) = ab \\cdot \\text{Cov}(X, Y)\\)."},
                {"level": 2, "text": f"\\(\\text{{Cov}}({a_scale}X, {b_scale}Y) = {a_scale} \\cdot {b_scale} \\cdot \\text{{Cov}}(X,Y) = {a_scale*b_scale} \\cdot {cov}\\)."},
                {"level": 3, "text": f"\\(\\text{{Cov}}({a_scale}X, {b_scale}Y) = {new_cov}\\)."},
            ],
        }


# ── prob-conditional-expect ───────────────────────────────────────────────────

def _gen_prob_conditional_expect():
    """E[X|Y=y] from joint table: E[X|Y=0], E[X|Y=1], or iterated E[E[X|Y]]."""
    den = random.choice([6, 8, 10])
    a = random.randint(1, den - 2)
    b = den - a
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X|Y=0] with 2-valued X
        ans = _fr(b, den)
        return {
            "problem_text": (
                f"Given \\(Y=0\\), the conditional distribution of \\(X\\) is: "
                f"\\(P(X=0 \\mid Y=0) = \\frac{{{a}}}{{{den}}}\\) and "
                f"\\(P(X=1 \\mid Y=0) = \\frac{{{b}}}{{{den}}}\\). "
                f"Find \\(E[X \\mid Y=0]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(E[X \\mid Y=0] = \\sum_x x \\cdot P(X=x \\mid Y=0)\\)."},
                {"level": 2, "text": f"\\(= 0 \\cdot \\frac{{{a}}}{{{den}}} + 1 \\cdot \\frac{{{b}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{b}}}{{{den}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # E[Y|X=0]: given X=0, the conditional distribution of Y (binary Y)
        c = random.randint(1, den - 2)
        d = den - c
        ans = _fr(d, den)
        return {
            "problem_text": (
                f"Given \\(X=0\\), the conditional distribution of \\(Y\\) is: "
                f"\\(P(Y=0 \\mid X=0) = \\frac{{{c}}}{{{den}}}\\) and "
                f"\\(P(Y=1 \\mid X=0) = \\frac{{{d}}}{{{den}}}\\). "
                f"Find \\(E[Y \\mid X=0]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(E[Y \\mid X=0] = \\sum_y y \\cdot P(Y=y \\mid X=0)\\)."},
                {"level": 2, "text": f"\\(= 0 \\cdot \\frac{{{c}}}{{{den}}} + 1 \\cdot \\frac{{{d}}}{{{den}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{d}}}{{{den}}} = {ans}\\)."},
            ],
        }
    else:
        # E[X|Y=0] for a 3-valued X: values 0, 1, 2
        den2 = random.choice([4, 6, 8])
        p0 = random.randint(1, den2 - 2)
        p1 = random.randint(1, den2 - p0 - 1)
        p2 = den2 - p0 - p1
        # E[X|Y=0] = (0*p0 + 1*p1 + 2*p2)/den2
        num = p1 + 2 * p2
        ans = _fr(num, den2)
        return {
            "problem_text": (
                f"Given \\(Y=0\\), the conditional distribution of \\(X\\) is: "
                f"\\(P(X=0 \\mid Y=0) = \\frac{{{p0}}}{{{den2}}}\\), "
                f"\\(P(X=1 \\mid Y=0) = \\frac{{{p1}}}{{{den2}}}\\), "
                f"\\(P(X=2 \\mid Y=0) = \\frac{{{p2}}}{{{den2}}}\\). "
                f"Find \\(E[X \\mid Y=0]\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(E[X \\mid Y=0] = \\sum_x x \\cdot P(X=x \\mid Y=0)\\)."},
                {"level": 2, "text": f"\\(= 0 \\cdot \\frac{{{p0}}}{{{den2}}} + 1 \\cdot \\frac{{{p1}}}{{{den2}}} + 2 \\cdot \\frac{{{p2}}}{{{den2}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{p1} + 2 \\cdot {p2}}}{{{den2}}} = {ans}\\)."},
            ],
        }


# ── prob-bivariate-normal ─────────────────────────────────────────────────────

def _gen_prob_bivariate_normal():
    """Bivariate normal: E[X|Y=y] (rho=0), E[X], or Var(X)."""
    mu_x = random.randint(0, 4)
    mu_y = random.randint(0, 4)
    sig_x = random.randint(1, 3)
    sig_y = random.randint(1, 3)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X|Y=y] when ρ=0
        y = random.randint(0, 6)
        ans = str(mu_x)
        return {
            "problem_text": (
                f"\\((X,Y)\\) follows a bivariate normal with \\(\\mu_X={mu_x}\\), "
                f"\\(\\mu_Y={mu_y}\\), \\(\\sigma_X={sig_x}\\), \\(\\sigma_Y={sig_y}\\), "
                f"and correlation \\(\\rho=0\\). Find \\(E[X \\mid Y={y}]\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For bivariate normal: \\(E[X|Y=y] = \\mu_X + \\rho \\frac{\\sigma_X}{\\sigma_Y}(y - \\mu_Y)\\)."},
                {"level": 2, "text": "When \\(\\rho = 0\\), the second term vanishes."},
                {"level": 3, "text": f"\\(E[X \\mid Y={y}] = \\mu_X + 0 = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # E[X] = mu_X (marginal mean)
        ans = str(mu_x)
        return {
            "problem_text": (
                f"\\((X,Y)\\) follows a bivariate normal with \\(\\mu_X={mu_x}\\), "
                f"\\(\\mu_Y={mu_y}\\), \\(\\sigma_X={sig_x}\\), \\(\\sigma_Y={sig_y}\\). "
                f"Find \\(E[X]\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The marginal distribution of \\(X\\) in a bivariate normal is \\(N(\\mu_X, \\sigma_X^2)\\)."},
                {"level": 2, "text": f"\\(E[X] = \\mu_X\\)."},
                {"level": 3, "text": f"\\(E[X] = {mu_x}\\)."},
            ],
        }
    else:
        # Var(X) = sig_x²
        ans = str(sig_x**2)
        return {
            "problem_text": (
                f"\\((X,Y)\\) follows a bivariate normal with \\(\\mu_X={mu_x}\\), "
                f"\\(\\mu_Y={mu_y}\\), \\(\\sigma_X={sig_x}\\), \\(\\sigma_Y={sig_y}\\). "
                f"Find \\(\\text{{Var}}(X)\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The marginal distribution of \\(X\\) is \\(N(\\mu_X, \\sigma_X^2)\\), so \\(\\text{Var}(X) = \\sigma_X^2\\)."},
                {"level": 2, "text": f"\\(\\sigma_X = {sig_x}\\), so \\(\\sigma_X^2 = {sig_x**2}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(X) = {ans}\\)."},
            ],
        }


# ── prob-mgf ──────────────────────────────────────────────────────────────────

def _gen_prob_mgf():
    """MGF: M(0)=1, M'(0)=E[X] for Bernoulli, or M''(0)=E[X²] for Bernoulli."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # M(0) = 1 for any valid MGF
        return {
            "problem_text": "For any random variable \\(X\\) with MGF \\(M_X(t) = E[e^{tX}]\\), what is \\(M_X(0)\\)?",
            "correct_answer": "1", "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Substitute \\(t=0\\) into the definition \\(M_X(t) = E[e^{tX}]\\)."},
                {"level": 2, "text": "\\(M_X(0) = E[e^{0 \\cdot X}] = E[1]\\)."},
                {"level": 3, "text": "\\(E[1] = 1\\). So \\(M_X(0) = 1\\)."},
            ],
        }
    elif variant == 1:
        # Bernoulli(p): M'(0) = E[X] = p
        den = random.choice([3, 4, 5])
        p_num = random.randint(1, den - 1)
        ans = _fr(p_num, den)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Bernoulli}}(p=\\frac{{{p_num}}}{{{den}}})\\) has MGF "
                f"\\(M_X(t) = (1-p) + pe^t\\). "
                f"Find \\(M_X'(0)\\) (which equals \\(E[X]\\))."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Differentiate \\(M_X(t)\\) with respect to \\(t\\) and evaluate at \\(t=0\\)."},
                {"level": 2, "text": f"\\(M_X'(t) = pe^t\\). At \\(t=0\\): \\(M_X'(0) = p \\cdot e^0 = p\\)."},
                {"level": 3, "text": f"\\(M_X'(0) = p = \\frac{{{p_num}}}{{{den}}} = {ans}\\)."},
            ],
        }
    else:
        # Geometric MGF evaluated: use Poisson MGF M_X(t) = exp(lambda*(e^t - 1))
        # M_X(0) = exp(lambda*0) = 1. Instead: Poisson M'(0) = lambda
        lam = random.randint(1, 6)
        return {
            "problem_text": (
                f"\\(X \\sim \\text{{Poisson}}(\\lambda={lam})\\) has MGF "
                f"\\(M_X(t) = e^{{\\lambda(e^t - 1)}}\\). "
                f"Find \\(M_X'(0)\\) (which equals \\(E[X]\\))."
            ),
            "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Differentiate \\(M_X(t) = e^{\\lambda(e^t - 1)}\\) and evaluate at \\(t=0\\)."},
                {"level": 2, "text": f"\\(M_X'(t) = \\lambda e^t \\cdot e^{{\\lambda(e^t - 1)}}\\). At \\(t=0\\): \\(M_X'(0) = \\lambda e^0 \\cdot e^0 = \\lambda\\)."},
                {"level": 3, "text": f"\\(M_X'(0) = \\lambda = {lam}\\)."},
            ],
        }


# ── prob-poisson-process ──────────────────────────────────────────────────────

def _gen_prob_poisson_process():
    """Poisson process: E[N(t)], interarrival time, or Var[N(t)]."""
    lam = random.randint(1, 5)
    t = random.randint(1, 6)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[N(t)] = lambda * t
        ans = str(lam * t)
        return {
            "problem_text": (
                f"Events arrive at rate \\(\\lambda={lam}\\) per unit time (Poisson process). "
                f"Find \\(E[N({t})]\\), the expected number of arrivals in \\([0,{t}]\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For a Poisson process with rate \\(\\lambda\\), \\(N(t) \\sim \\text{Poisson}(\\lambda t)\\)."},
                {"level": 2, "text": f"\\(E[N({t})] = \\lambda t = {lam} \\cdot {t}\\)."},
                {"level": 3, "text": f"\\(E[N({t})] = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # Interarrival time E = 1/lambda
        ans = _fr(1, lam)
        return {
            "problem_text": (
                f"A Poisson process has rate \\(\\lambda={lam}\\). "
                f"What is the expected interarrival time?"
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Interarrival times in a Poisson process are \\(\\text{Exponential}(\\lambda)\\)."},
                {"level": 2, "text": f"\\(E[T] = \\frac{{1}}{{\\lambda}} = \\frac{{1}}{{{lam}}}\\)."},
                {"level": 3, "text": f"\\(E[T] = {ans}\\)."},
            ],
        }
    else:
        # Var[N(t)] = lambda * t (Poisson variance = mean)
        ans = str(lam * t)
        return {
            "problem_text": (
                f"Events arrive at rate \\(\\lambda={lam}\\) per unit time (Poisson process). "
                f"Find \\(\\text{{Var}}[N({t})]\\), the variance of arrivals in \\([0,{t}]\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(N(t) \\sim \\text{Poisson}(\\lambda t)\\). For a Poisson RV, variance equals its rate."},
                {"level": 2, "text": f"\\(\\text{{Var}}[N({t})] = \\lambda t = {lam} \\cdot {t}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}[N({t})] = {ans}\\)."},
            ],
        }


# ── prob-order-stats ──────────────────────────────────────────────────────────

def _gen_prob_order_stats():
    """Order statistics: E[X_{(k)}] for Uniform(0,1), any k."""
    n = random.randint(2, 5)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # E[X_{(1)}] = 1/(n+1)
        k = 1
        ans = _fr(1, n + 1)
    elif variant == 1:
        # E[X_{(n)}] = n/(n+1)
        k = n
        ans = _fr(n, n + 1)
    else:
        # E[X_{(k)}] for middle k
        k = random.randint(1, n)
        ans = _fr(k, n + 1)
    k_label = f"X_{{({k})}}"
    label_desc = "min" if k == 1 else ("max" if k == n else f"{k}-th smallest")
    return {
        "problem_text": (
            f"Let \\(X_1, \\ldots, X_{{{n}}}\\) be iid \\(\\text{{Uniform}}(0,1)\\). "
            f"Find \\(E[{k_label}]\\) (the expected value of the {label_desc})."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": f"For iid Uniform(0,1), \\(E[X_{{(k)}}] = \\frac{{k}}{{n+1}}\\)."},
            {"level": 2, "text": f"Here \\(k={k}\\), \\(n={n}\\)."},
            {"level": 3, "text": f"\\(E[{k_label}] = \\frac{{{k}}}{{{n+1}}} = {ans}\\)."},
        ],
    }


# ── prob-lln ──────────────────────────────────────────────────────────────────

def _gen_prob_lln():
    """LLN: find convergence limit, SE = σ/√n, or n for SE < ε."""
    mu = random.randint(2, 10)
    sig2 = random.randint(1, 5)
    n = random.choice([100, 400, 900])  # perfect squares for SE calculations
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # What does X̄_n converge to?
        return {
            "problem_text": (
                f"Observations \\(X_1, X_2, \\ldots\\) are iid with \\(E[X_i] = {mu}\\) and "
                f"\\(\\text{{Var}}(X_i) = {sig2}\\). "
                f"By the Law of Large Numbers, what value does \\(\\bar{{X}}_n\\) converge to in probability?"
            ),
            "correct_answer": str(mu), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The LLN states: \\(\\bar{X}_n \\xrightarrow{p} E[X]\\) as \\(n \\to \\infty\\)."},
                {"level": 2, "text": f"The population mean is \\(\\mu = {mu}\\)."},
                {"level": 3, "text": f"\\(\\bar{{X}}_n \\xrightarrow{{p}} {mu}\\)."},
            ],
        }
    elif variant == 1:
        # SE(X̄_n) = σ/√n — use perfect square n so SE is rational
        import math
        sqrt_n = int(math.isqrt(n))
        # SE = sqrt(sig2)/sqrt_n — only clean if sig2 is a perfect square
        sig2_sq = random.choice([1, 4, 9])
        sig = int(sig2_sq ** 0.5)
        se = _fr(sig, sqrt_n)
        return {
            "problem_text": (
                f"Observations are iid with \\(\\text{{Var}}(X_i) = {sig2_sq}\\). "
                f"Find the standard error of the sample mean \\(\\bar{{X}}_n\\) for \\(n = {n}\\)."
            ),
            "correct_answer": se, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The standard error (SE) is \\(\\text{SE}(\\bar{X}_n) = \\frac{\\sigma}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(\\sigma = \\sqrt{{{sig2_sq}}} = {sig}\\). \\(\\sqrt{{n}} = \\sqrt{{{n}}} = {sqrt_n}\\)."},
                {"level": 3, "text": f"\\(\\text{{SE}} = \\frac{{{sig}}}{{{sqrt_n}}} = {se}\\)."},
            ],
        }
    else:
        # By LLN, find what (1/n)*(X₁² + ... + Xₙ²) converges to = E[X²]
        ex = mu
        ex2 = ex * ex + sig2  # E[X²] = Var(X) + (E[X])²
        return {
            "problem_text": (
                f"Observations \\(X_1, X_2, \\ldots\\) are iid with \\(E[X_i] = {mu}\\) and "
                f"\\(\\text{{Var}}(X_i) = {sig2}\\). "
                f"By the LLN, what does \\(\\frac{{1}}{{n}} \\sum_{{i=1}}^n X_i^2\\) converge to in probability?"
            ),
            "correct_answer": str(ex2), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "By the LLN, \\(\\frac{1}{n}\\sum X_i^2 \\xrightarrow{p} E[X^2]\\)."},
                {"level": 2, "text": f"\\(E[X^2] = \\text{{Var}}(X) + (E[X])^2 = {sig2} + {mu}^2 = {sig2} + {mu*mu}\\)."},
                {"level": 3, "text": f"\\(E[X^2] = {ex2}\\)."},
            ],
        }


# ── prob-clt ──────────────────────────────────────────────────────────────────

def _gen_prob_clt():
    """CLT: Var(X̄), limiting σ², or E[X̄] = μ."""
    mu = random.randint(1, 6)
    sig2 = random.randint(1, 5)
    n = random.choice([30, 50, 100])
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Var(X̄_n) = σ²/n
        ans = _fr(sig2, n)
        return {
            "problem_text": (
                f"Iid observations with \\(E[X] = {mu}\\), \\(\\text{{Var}}(X) = {sig2}\\). "
                f"Find \\(\\text{{Var}}(\\bar{{X}}_n)\\) for \\(n={n}\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(\\bar{X}_n) = \\frac{\\sigma^2}{n}\\)."},
                {"level": 2, "text": f"\\(\\frac{{{sig2}}}{{{n}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(\\bar{{X}}_n) = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # CLT: limiting variance of √n(X̄-μ)
        return {
            "problem_text": (
                f"Iid observations with \\(\\text{{Var}}(X) = {sig2}\\). "
                f"By the CLT, \\(\\sqrt{{n}}(\\bar{{X}}_n - \\mu) \\xrightarrow{{d}} N(0, \\sigma^2)\\). "
                f"What is \\(\\sigma^2\\) in this limiting distribution?"
            ),
            "correct_answer": str(sig2), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The CLT says \\(\\sqrt{n}(\\bar{X}_n - \\mu) \\to N(0, \\text{Var}(X))\\)."},
                {"level": 2, "text": f"The limiting variance is \\(\\text{{Var}}(X) = \\sigma^2\\)."},
                {"level": 3, "text": f"\\(\\sigma^2 = {sig2}\\)."},
            ],
        }
    else:
        # E[X̄_n] = μ (sample mean is unbiased)
        return {
            "problem_text": (
                f"Iid observations with \\(E[X] = {mu}\\) and \\(\\text{{Var}}(X) = {sig2}\\). "
                f"Find \\(E[\\bar{{X}}_n]\\) for any \\(n\\)."
            ),
            "correct_answer": str(mu), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "By linearity of expectation: \\(E[\\bar{X}_n] = E\\left[\\frac{1}{n}\\sum_{i=1}^n X_i\\right] = \\frac{1}{n} \\sum_{i=1}^n E[X_i]\\)."},
                {"level": 2, "text": f"\\(= \\frac{{1}}{{n}} \\cdot n \\cdot E[X] = E[X] = {mu}\\)."},
                {"level": 3, "text": f"\\(E[\\bar{{X}}_n] = {mu}\\)."},
            ],
        }


# ── GENERATORS dict ───────────────────────────────────────────────────────────

GENERATORS = {
    "prob-sample-space":       _gen_prob_sample_space,
    "prob-set-ops":            _gen_prob_set_ops,
    "prob-axioms":             _gen_prob_axioms,
    "prob-inclusion-excl":     _gen_prob_inclusion_excl,
    "prob-area-probability":   _gen_prob_area_probability,
    "prob-conditional":        _gen_prob_conditional,
    "prob-independence":       _gen_prob_independence,
    "prob-total-prob":         _gen_prob_total_prob,
    "prob-bayes":              _gen_prob_bayes,
    "prob-discrete-rv":        _gen_prob_discrete_rv,
    "prob-expected-value":     _gen_prob_expected_value,
    "prob-indicators":         _gen_prob_indicators,
    "prob-variance":           _gen_prob_variance,
    "prob-bernoulli-binom":    _gen_prob_bernoulli_binom,
    "prob-hypergeometric":     _gen_prob_hypergeometric,
    "prob-geometric-dist":     _gen_prob_geometric_dist,
    "prob-poisson":            _gen_prob_poisson,
    "prob-poisson-approx":     _gen_prob_poisson_approx,
    "prob-continuous-rv":      _gen_prob_continuous_rv,
    "prob-normal":             _gen_prob_normal,
    "prob-exponential-dist":   _gen_prob_exponential_dist,
    "prob-memoryless":         _gen_prob_memoryless,
    "prob-gamma-dist":         _gen_prob_gamma_dist,
    "prob-normal-approx":      _gen_prob_normal_approx,
    "prob-cdf-method":         _gen_prob_cdf_method,
    "prob-transformations":    _gen_prob_transformations,
    "prob-inverse-cdf":        _gen_prob_inverse_cdf,
    "prob-joint-discrete":     _gen_prob_joint_discrete,
    "prob-joint-continuous":   _gen_prob_joint_continuous,
    "prob-marginal":           _gen_prob_marginal,
    "prob-conditional-dist":   _gen_prob_conditional_dist,
    "prob-covariance":         _gen_prob_covariance,
    "prob-conditional-expect": _gen_prob_conditional_expect,
    "prob-bivariate-normal":   _gen_prob_bivariate_normal,
    "prob-mgf":                _gen_prob_mgf,
    "prob-poisson-process":    _gen_prob_poisson_process,
    "prob-order-stats":        _gen_prob_order_stats,
    "prob-lln":                _gen_prob_lln,
    "prob-clt":                _gen_prob_clt,
}
