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
    """Size of union/intersection using given counts."""
    total = random.randint(10, 20)
    a = random.randint(3, total - 2)
    b = random.randint(3, total - 2)
    inter = random.randint(1, min(a, b) - 1)
    union = a + b - inter
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
        # Give union and one set, find intersection
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


# ── prob-axioms ───────────────────────────────────────────────────────────────

def _gen_prob_axioms():
    """Complement rule or basic axiom."""
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


# ── prob-inclusion-excl ───────────────────────────────────────────────────────

def _gen_prob_inclusion_excl():
    """P(A∪B) via inclusion-exclusion with given probabilities."""
    den = random.choice([6, 8, 10, 12])
    a = random.randint(2, den - 2)
    b = random.randint(2, den - 2)
    inter = random.randint(1, min(a, b) - 1)
    union_num = a + b - inter
    # Ensure ≤ 1
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


# ── prob-area-probability ─────────────────────────────────────────────────────

def _gen_prob_area_probability():
    """Geometric probability: inner region / outer region."""
    outer = random.randint(3, 6)  # side of outer square
    inner = random.randint(1, outer - 1)  # side of inner square
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


# ── prob-conditional ──────────────────────────────────────────────────────────

def _gen_prob_conditional():
    """P(A|B) = P(A∩B) / P(B)."""
    den = random.choice([6, 8, 10, 12])
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


# ── prob-independence ─────────────────────────────────────────────────────────

def _gen_prob_independence():
    """P(A∩B) = P(A)·P(B) for independent events."""
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


# ── prob-total-prob ───────────────────────────────────────────────────────────

def _gen_prob_total_prob():
    """Law of total probability with 2 partitions."""
    # P(B) = P(B|A)P(A) + P(B|A^c)P(A^c)
    den = random.choice([4, 5, 6])
    pa = random.randint(1, den - 1)
    pac = den - pa
    # P(B|A) = p1/den2, P(B|A^c) = p2/den2
    den2 = random.choice([4, 5])
    p1 = random.randint(1, den2 - 1)
    p2 = random.randint(1, den2 - 1)
    # P(B) = (pa*p1 + pac*p2) / (den * den2)
    num = pa * p1 + pac * p2
    denom = den * den2
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


# ── prob-bayes ────────────────────────────────────────────────────────────────

def _gen_prob_bayes():
    """Bayes' theorem: P(A|B) with 2-partition setup."""
    den = random.choice([4, 5])
    pa = random.randint(1, den - 1)
    pac = den - pa
    den2 = random.choice([4, 5])
    p_ba = random.randint(1, den2 - 1)
    p_bac = random.randint(1, den2 - 1)
    # P(A|B) = P(B|A)P(A) / [P(B|A)P(A) + P(B|A^c)P(A^c)]
    num = pa * p_ba
    denom_total = pa * p_ba + pac * p_bac
    ans = _fr(num, denom_total)
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
            {"level": 3, "text": f"\\(P(A|B) = \\frac{{\\frac{{{pa*p_ba}}}{{{den*den2}}}}}{{\\frac{{{denom_total}}}{{{den*den2}}}}} = \\frac{{{num}}}{{{denom_total}}} = {ans}\\)."},
        ],
    }


# ── prob-discrete-rv ──────────────────────────────────────────────────────────

def _gen_prob_discrete_rv():
    """PMF of a simple discrete RV; find P(X = k) from a table."""
    # 3-value RV: P(0)=a, P(1)=b, P(2)=c with a+b+c=1
    den = random.choice([4, 5, 6, 8])
    a = random.randint(1, den - 2)
    b = random.randint(1, den - a - 1)
    c = den - a - b
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


# ── prob-expected-value ───────────────────────────────────────────────────────

def _gen_prob_expected_value():
    """E[X] for a simple discrete RV."""
    den = random.choice([4, 6, 8])
    a = random.randint(1, den - 2)
    b = random.randint(1, den - a - 1)
    c = den - a - b
    # Values 0, 1, 2 for simplicity
    # E[X] = 0*(a/den) + 1*(b/den) + 2*(c/den) = (b + 2c)/den
    num = b + 2*c
    ans = _fr(num, den)
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
            {"level": 3, "text": f"\\(= \\frac{{{b} + 2 \\cdot {c}}}{{{den}}} = \\frac{{{num}}}{{{den}}} = {ans}\\)."},
        ],
    }


# ── prob-indicators ───────────────────────────────────────────────────────────

def _gen_prob_indicators():
    """E[I_A] = P(A); find expected value of an indicator."""
    den = random.choice([4, 5, 6, 8, 10])
    k = random.randint(1, den - 1)
    ans = _fr(k, den)
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


# ── prob-variance ─────────────────────────────────────────────────────────────

def _gen_prob_variance():
    """Var(X) = E[X²] - (E[X])² for a two-value RV."""
    # X takes values 0 and v with P(X=v) = p/q
    q = random.choice([3, 4, 5])
    p = random.randint(1, q - 1)
    v = random.randint(2, 5)
    # E[X] = v*p/q, E[X²] = v²*p/q
    # Var = v²*p/q - v²*p²/q² = v²*p*(q-p)/q²
    num = v*v * p * (q - p)
    denom = q*q
    ans = _fr(num, denom)
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
            {"level": 3, "text": f"\\(\\text{{Var}} = \\frac{{{v*v*p}}}{{{q}}} - \\frac{{{v*p}^2}}{{{q}^2}} = \\frac{{{num}}}{{{denom}}} = {ans}\\)."},
        ],
    }


# ── prob-bernoulli-binom ──────────────────────────────────────────────────────

def _gen_prob_bernoulli_binom():
    """Binomial distribution: E[X] or Var[X]."""
    n = random.randint(4, 10)
    p_den = random.choice([2, 3, 4, 5])
    p_num = random.randint(1, p_den - 1)
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
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


# ── prob-hypergeometric ───────────────────────────────────────────────────────

def _gen_prob_hypergeometric():
    """Hypergeometric E[X] = n*K/N."""
    N = random.randint(8, 15)
    K = random.randint(2, N - 2)
    n = random.randint(2, min(K + 2, N - 2))
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


# ── prob-geometric-dist ───────────────────────────────────────────────────────

def _gen_prob_geometric_dist():
    """Geometric distribution: E[X] = 1/p or P(X=1) = p."""
    p_den = random.choice([2, 3, 4, 5])
    p_num = random.randint(1, p_den - 1)
    ask = random.randint(0, 1)
    if ask == 0:
        # E[X] = 1/p (number of trials until first success)
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
    else:
        # P(X=k) = (1-p)^{k-1} * p for k=1 → just p
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


# ── prob-poisson ──────────────────────────────────────────────────────────────

def _gen_prob_poisson():
    """Poisson distribution: E[X] or Var[X] = λ."""
    lam = random.randint(1, 8)
    ask = random.randint(0, 1)
    quantity = "E[X]" if ask == 0 else "\\text{Var}(X)"
    return {
        "problem_text": (
            f"\\(X \\sim \\text{{Poisson}}(\\lambda={lam})\\). "
            f"Find \\({quantity}\\)."
        ),
        "correct_answer": str(lam), "answer_type": "numeric", "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "For a Poisson RV with rate \\(\\lambda\\), both the mean and variance equal \\(\\lambda\\)."},
            {"level": 2, "text": f"\\(E[X] = \\text{{Var}}(X) = \\lambda = {lam}\\)."},
            {"level": 3, "text": f"\\({quantity} = {lam}\\)."},
        ],
    }


# ── prob-poisson-approx ───────────────────────────────────────────────────────

def _gen_prob_poisson_approx():
    """Poisson approximation to binomial: λ = np."""
    n = random.randint(50, 200)
    p_den = random.choice([100, 50, 200])
    p_num = random.randint(1, 4)
    lam = n * p_num // p_den
    # Ensure lam is integer and positive
    while lam == 0:
        p_num += 1
        lam = n * p_num // p_den
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


# ── prob-continuous-rv ────────────────────────────────────────────────────────

def _gen_prob_continuous_rv():
    """Uniform distribution: P(X < t) or E[X]."""
    a = 0
    b = random.randint(2, 8)
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
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


# ── prob-normal ───────────────────────────────────────────────────────────────

def _gen_prob_normal():
    """Standard normal: find z-score or use 68-95-99.7 rule."""
    mu = random.randint(-2, 4)
    sigma = random.randint(1, 3)
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
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


# ── prob-exponential-dist ─────────────────────────────────────────────────────

def _gen_prob_exponential_dist():
    """Exponential distribution: E[X] = 1/λ or Var[X] = 1/λ²."""
    lam = random.randint(1, 5)
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
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


# ── prob-memoryless ───────────────────────────────────────────────────────────

def _gen_prob_memoryless():
    """Memoryless property: P(X > s+t | X > s) = P(X > t)."""
    lam = random.randint(1, 4)
    s = random.randint(1, 4)
    t = random.randint(1, 4)
    # P(X > t) = e^{-λt} — express answer symbolically
    # Ask: what does memoryless give us? = P(X > t)
    # Ask for t only (the answer is the value of t, identifying the correct simplified form)
    # Better: ask for the rate that makes P(X>t)=e^{-2} → lam=2, t=1 etc.
    # Cleanest: ask for P(X > s+t | X > s) numerically where lam*(s+t) is small
    # Use lam=1, t chosen so e^{-t} is recognizable — skip; ask conceptually
    # Ask: if X is memoryless Exp(λ), what does P(X>s+t|X>s) simplify to?
    # Answer = P(X > t) represented as "P(X > t)" — but that's not a number.
    # Instead: ask for E[X | X > s] = s + 1/lam (memoryless: remaining life = fresh)
    ans = str(s) + "+" + _fr(1, lam)
    # Actually compute numerically: E[X|X>s] = s + 1/lam
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


# ── prob-gamma-dist ───────────────────────────────────────────────────────────

def _gen_prob_gamma_dist():
    """Gamma distribution: E[X] = α/β or Var[X] = α/β²."""
    alpha = random.randint(2, 6)
    beta = random.randint(1, 4)
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
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


# ── prob-normal-approx ────────────────────────────────────────────────────────

def _gen_prob_normal_approx():
    """CLT/normal approx: find μ or σ of the approximating normal."""
    n = random.randint(20, 100)
    p_den = random.choice([2, 4, 5])
    p_num = random.randint(1, p_den - 1)
    ask = random.randint(0, 1)
    if ask == 0:
        mu = n * p_num
        ans = _fr(mu, p_den)
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
    else:
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


# ── prob-cdf-method ───────────────────────────────────────────────────────────

def _gen_prob_cdf_method():
    """CDF method: F_Y(y) for Y = aX + b where X ~ Uniform(0,1)."""
    a = random.randint(2, 5)
    b = random.randint(0, 3)
    # Y = aX + b ~ Uniform(b, a+b)
    # F_Y(y) = (y - b)/a for b ≤ y ≤ a+b
    t = random.randint(b + 1, a + b - 1)
    ans = _fr(t - b, a)
    return {
        "problem_text": (
            f"Let \\(X \\sim \\text{{Uniform}}(0, 1)\\) and \\(Y = {a}X + {b}\\). "
            f"Find \\(F_Y({t}) = P(Y \\leq {t})\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "\\(P(Y \\leq t) = P(aX + b \\leq t) = P\\!\\left(X \\leq \\frac{t-b}{a}\\right)\\)."},
            {"level": 2, "text": f"Since \\(X \\sim \\text{{Uniform}}(0,1)\\), \\(P(X \\leq u) = u\\) for \\(0 \\leq u \\leq 1\\)."},
            {"level": 3, "text": f"\\(F_Y({t}) = \\frac{{{t}-{b}}}{{{a}}} = \\frac{{{t-b}}}{{{a}}} = {ans}\\)."},
        ],
    }


# ── prob-transformations ──────────────────────────────────────────────────────

def _gen_prob_transformations():
    """E[aX + b] or Var(aX + b) using linearity."""
    mu = random.randint(1, 6)
    sig2 = random.randint(1, 5)
    a = random.randint(2, 4)
    b = random.randint(1, 6)
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
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


# ── prob-inverse-cdf ──────────────────────────────────────────────────────────

def _gen_prob_inverse_cdf():
    """Quantile of Uniform(a, b): F^{-1}(p) = a + p(b-a)."""
    a = 0
    b = random.randint(2, 8)
    # p = k/b for clean answer
    k = random.randint(1, b - 1)
    p_num = k; p_den = b
    ans = str(k)   # a + (k/b)*(b-0) = k
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


# ── prob-joint-discrete ───────────────────────────────────────────────────────

def _gen_prob_joint_discrete():
    """Joint PMF: find P(X=i, Y=j) or P(X=i) from a 2x2 table."""
    den = random.choice([8, 10, 12])
    a = random.randint(1, den//2 - 1)
    b = random.randint(1, den//2 - 1)
    c = random.randint(1, den - a - b - 1)
    d = den - a - b - c
    # Table: (0,0)=a, (0,1)=b, (1,0)=c, (1,1)=d
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


# ── prob-joint-continuous ─────────────────────────────────────────────────────

def _gen_prob_joint_continuous():
    """Joint Uniform on [0,a]x[0,b]: P(X<s, Y<t) = (s/a)(t/b)."""
    a = random.randint(2, 4)
    b = random.randint(2, 4)
    s = random.randint(1, a - 1)
    t = random.randint(1, b - 1)
    # P = (s*t) / (a*b)
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


# ── prob-marginal ─────────────────────────────────────────────────────────────

def _gen_prob_marginal():
    """Marginal PMF from a joint discrete table."""
    den = random.choice([8, 10, 12])
    a = random.randint(1, den//2 - 1)
    b = random.randint(1, den - a - 2)
    c = random.randint(1, den - a - b - 1)
    d = den - a - b - c
    # P_X(0) = a+b, P_X(1) = c+d
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


# ── prob-conditional-dist ─────────────────────────────────────────────────────

def _gen_prob_conditional_dist():
    """Conditional PMF P(X=x | Y=y)."""
    den = random.choice([8, 10, 12])
    a = random.randint(1, den//2 - 1)
    b = random.randint(1, den - a - 2)
    c = random.randint(1, den - a - b - 1)
    d = den - a - b - c
    # P(X=0|Y=0) = a / (a+c), P(X=1|Y=0) = c / (a+c)
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


# ── prob-covariance ───────────────────────────────────────────────────────────

def _gen_prob_covariance():
    """Cov(X,Y) = E[XY] - E[X]E[Y]; Cov(aX, bY) = ab·Cov(X,Y)."""
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
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


# ── prob-conditional-expect ───────────────────────────────────────────────────

def _gen_prob_conditional_expect():
    """E[X|Y=y] from a simple conditional distribution."""
    den = random.choice([6, 8, 10])
    a = random.randint(1, den - 2)
    b = den - a
    # P(X=0|Y=0) = a/den, P(X=1|Y=0) = b/den
    # E[X|Y=0] = 0*(a/den) + 1*(b/den) = b/den
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


# ── prob-bivariate-normal ─────────────────────────────────────────────────────

def _gen_prob_bivariate_normal():
    """Bivariate normal: E[X|Y=y] = μ_X + ρ(σ_X/σ_Y)(y - μ_Y)."""
    mu_x = random.randint(0, 4)
    mu_y = random.randint(0, 4)
    sig_x = random.randint(1, 3)
    sig_y = random.randint(1, 3)
    rho_num = 0  # use ρ=0 → E[X|Y] = μ_X (independent)
    # Simplify: ask for E[X|Y=y] when ρ=0
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


# ── prob-mgf ──────────────────────────────────────────────────────────────────

def _gen_prob_mgf():
    """MGF: M'(0) = E[X] or M(0) = 1."""
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
        # Bernoulli(p) MGF: M(t) = (1-p) + p*e^t; M'(0) = p
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


# ── prob-poisson-process ──────────────────────────────────────────────────────

def _gen_prob_poisson_process():
    """Poisson process: E[N(t)] = λt or number of events in interval."""
    lam = random.randint(1, 5)
    t = random.randint(1, 6)
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
        # Interarrival time ~ Exp(λ); E = 1/λ
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


# ── prob-order-stats ──────────────────────────────────────────────────────────

def _gen_prob_order_stats():
    """Order statistics: E[X_{(1)}] or E[X_{(n)}] for Uniform(0,1)."""
    n = random.randint(2, 5)
    ask = random.randint(0, 1)
    if ask == 0:
        # E[X_{(1)}] = 1/(n+1)
        ans = _fr(1, n + 1)
        k = 1
    else:
        # E[X_{(n)}] = n/(n+1)
        ans = _fr(n, n + 1)
        k = n
    k_label = f"X_{{({k})}}"
    return {
        "problem_text": (
            f"Let \\(X_1, \\ldots, X_{{{n}}}\\) be iid \\(\\text{{Uniform}}(0,1)\\). "
            f"Find \\(E[{k_label}]\\) (the expected value of the \\({'min' if k==1 else 'max'}\\))."
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
    """LLN: sample mean converges to μ; find μ."""
    mu = random.randint(2, 10)
    sig2 = random.randint(1, 5)
    n = random.choice([100, 500, 1000])
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


# ── prob-clt ──────────────────────────────────────────────────────────────────

def _gen_prob_clt():
    """CLT: find the variance of √n(X̄ - μ) limiting distribution."""
    mu = random.randint(1, 6)
    sig2 = random.randint(1, 5)
    n = random.choice([30, 50, 100])
    ask = random.randint(0, 1)
    if ask == 0:
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
    else:
        # CLT: √n(X̄ - μ)/σ → N(0,1). Ask for the limiting variance of √n(X̄-μ) = σ²
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
