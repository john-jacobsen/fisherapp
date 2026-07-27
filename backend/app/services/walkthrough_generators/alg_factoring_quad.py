"""
Generator for the alg-factoring-quad walkthrough.

Factor a MONIC quadratic  x^2 + bx + c  into  (x + p)(x + q)  where
    p + q = b   (the two numbers add to the middle coefficient)
    p * q = c   (the two numbers multiply to the constant term)

Constraints:
  - p, q are small distinct nonzero integers in [-6, 6]
  - p < q for a stable display order
  - b = p + q != 0  (keeps a real middle term; excludes difference-of-squares
    so the "add to b" step is non-trivial and the display never shows "+ 0x")
  - q - p != 1  (so the step-3 "right sum, wrong product" distractor genuinely
    has the wrong product and stays distinct)
  - all three step-3 option pairs are distinct

Sign-aware display strings are built here so prompts read naturally
(e.g. "x^2 - 5x + 6" and "(x - 2)(x - 3)") with no "+ -" or bare "1x" artifacts.

Returned variables:
  p, q              the two numbers with p + q = b and p * q = c
  b                 middle coefficient (sum p + q)
  c                 constant term (product p * q)
  abs_b, abs_c      magnitudes, for prose
  neg_b             -b  (sum of the sign-flipped distractor pair)
  quadratic         full display string of the quadratic, e.g. "x^2 - 5x + 6"
  factor_p          sign-aware factor "(x - 2)" / "(x + 2)"
  factor_q          sign-aware factor for q
  factored          factor_p + factor_q, e.g. "(x - 2)(x - 3)" (the step-4 answer)
  d1p, d1q          step-3 distractor 1 (-p, -q): right product, wrong sum
  d2p, d2q          step-3 distractor 2 (p+1, q-1): right sum, wrong product
  d2_prod           product of distractor 2, (p+1)*(q-1)  (!= c)
"""
import random


def _factor(v: int) -> str:
    """Sign-aware factor string for (x + v)."""
    if v >= 0:
        return f"(x + {v})"
    return f"(x - {abs(v)})"


def _build(p: int, q: int) -> dict:
    b = p + q
    c = p * q
    abs_b, abs_c = abs(b), abs(c)

    # middle term (b is never 0; show plain "x" when |b| == 1)
    if b > 0:
        mid = "+ x" if b == 1 else f"+ {b}x"
    else:
        mid = "- x" if abs_b == 1 else f"- {abs_b}x"
    # constant term (c is never 0)
    const = f"+ {c}" if c > 0 else f"- {abs_c}"
    quadratic = f"x^2 {mid} {const}"

    factor_p = _factor(p)
    factor_q = _factor(q)

    d1p, d1q = -p, -q          # right product, wrong sum
    d2p, d2q = p + 1, q - 1    # right sum, wrong product

    return {
        "p": p, "q": q,
        "b": b, "c": c,
        "abs_b": abs_b, "abs_c": abs_c,
        "neg_b": -b,
        "quadratic": quadratic,
        "factor_p": factor_p,
        "factor_q": factor_q,
        "factored": factor_p + factor_q,
        "d1p": d1p, "d1q": d1q,
        "d2p": d2p, "d2q": d2q,
        "d2_prod": d2p * d2q,
    }


def generate() -> dict:
    for _ in range(5000):
        p = random.randint(-6, 6)
        q = random.randint(-6, 6)
        if p == 0 or q == 0 or p >= q:
            continue
        if p + q == 0:            # need a real middle term
            continue
        if q - p == 1:            # keep the "wrong product" distractor honest
            continue

        v = _build(p, q)

        # All three step-3 option pairs must be distinct.
        pairs = {(p, q), (v["d1p"], v["d1q"]), (v["d2p"], v["d2q"])}
        if len(pairs) != 3:
            continue
        # The wrong-product distractor must actually have the wrong product.
        if v["d2_prod"] == v["c"]:
            continue

        return v

    # Fallback: x^2 - 5x + 6 = (x - 2)(x - 3)
    return _build(-3, -2)
