"""
Statistics problem generators for Fisher App 3.0.
Covers 49 nodes: stat-sampling-dist through stat-causal-intro.

Drop at: backend/app/services/generators/statistics.py
In problem_generator.py add:
    from .generators.statistics import GENERATORS as STAT_GENERATORS
    GENERATORS.update(STAT_GENERATORS)
"""
import random
from fractions import Fraction
from math import sqrt


# ── helpers ───────────────────────────────────────────────────────────────────

def _fr(p, q):
    f = Fraction(p, q)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

def _pm(x):
    """'+x' / '-|x|' / '' string for signed offsets."""
    if x > 0: return f"+ {x}"
    if x < 0: return f"- {abs(x)}"
    return ""


# ── stat-sampling-dist ────────────────────────────────────────────────────────

def _gen_stat_sampling_dist():
    """Var(X̄) = σ²/n; find Var(X̄) or SD(X̄)."""
    sig2 = random.choice([4, 9, 16, 25])
    n = random.choice([4, 9, 16, 25, 100])
    ask = random.randint(0, 1)
    if ask == 0:
        ans = _fr(sig2, n)
        return {
            "problem_text": (
                f"Iid observations with \\(\\sigma^2 = {sig2}\\), sample size \\(n = {n}\\). "
                f"Find \\(\\text{{Var}}(\\bar{{X}})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(\\bar{X}) = \\frac{\\sigma^2}{n}\\)."},
                {"level": 2, "text": f"\\(\\frac{{{sig2}}}{{{n}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(\\bar{{X}}) = {ans}\\)."},
            ],
        }
    else:
        se = _fr(int(sqrt(sig2)), int(sqrt(n)))
        return {
            "problem_text": (
                f"Iid observations with \\(\\sigma^2 = {sig2}\\), sample size \\(n = {n}\\). "
                f"Find the standard error \\(\\text{{SD}}(\\bar{{X}}) = \\sigma/\\sqrt{{n}}\\)."
            ),
            "correct_answer": se, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{SE}(\\bar{X}) = \\frac{\\sigma}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(\\sigma = \\sqrt{{{sig2}}} = {int(sqrt(sig2))}\\), \\(\\sqrt{{n}} = {int(sqrt(n))}\\)."},
                {"level": 3, "text": f"\\(\\text{{SE}} = \\frac{{{int(sqrt(sig2))}}}{{{int(sqrt(n))}}} = {se}\\)."},
            ],
        }


# ── stat-estimator-props ──────────────────────────────────────────────────────

def _gen_stat_estimator_props():
    """Bias of an estimator: E[T] - θ."""
    theta = random.randint(2, 8)
    bias = random.choice([-2, -1, 0, 1, 2])
    e_t = theta + bias
    ans = str(bias)
    return {
        "problem_text": (
            f"An estimator \\(T\\) has \\(E[T] = {e_t}\\) when the true parameter is \\(\\theta = {theta}\\). "
            f"Find the bias \\(\\text{{Bias}}(T) = E[T] - \\theta\\)."
        ),
        "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "\\(\\text{Bias}(T) = E[T] - \\theta\\)."},
            {"level": 2, "text": f"\\({e_t} - {theta}\\)."},
            {"level": 3, "text": f"\\(\\text{{Bias}} = {ans}\\)."},
        ],
    }


# ── stat-survey-srs ───────────────────────────────────────────────────────────

def _gen_stat_survey_srs():
    """SRS: E[X̄] = μ or Var(X̄) ≈ σ²/n (finite population correction optional)."""
    N = random.randint(50, 200)
    mu = random.randint(10, 50)
    sig2 = random.choice([4, 9, 16, 25])
    n = random.choice([4, 9, 16])
    ask = random.randint(0, 1)
    if ask == 0:
        return {
            "problem_text": (
                f"A population of \\(N={N}\\) has mean \\(\\mu={mu}\\). "
                f"An SRS of size \\(n={n}\\) is drawn. What is \\(E[\\bar{{X}}]\\)?"
            ),
            "correct_answer": str(mu), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The sample mean is an unbiased estimator of the population mean."},
                {"level": 2, "text": f"\\(E[\\bar{{X}}] = \\mu = {mu}\\)."},
                {"level": 3, "text": f"\\(E[\\bar{{X}}] = {mu}\\)."},
            ],
        }
    else:
        ans = _fr(sig2, n)
        return {
            "problem_text": (
                f"An SRS of size \\(n={n}\\) is drawn from a large population with \\(\\sigma^2={sig2}\\). "
                f"Approximate \\(\\text{{Var}}(\\bar{{X}})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For large population: \\(\\text{Var}(\\bar{X}) \\approx \\frac{\\sigma^2}{n}\\)."},
                {"level": 2, "text": f"\\(\\frac{{{sig2}}}{{{n}}}\\)."},
                {"level": 3, "text": f"\\(\\approx {ans}\\)."},
            ],
        }


# ── stat-mom ──────────────────────────────────────────────────────────────────

def _gen_stat_mom():
    """Method of moments: equate E[X] = X̄ for Uniform(0,θ)."""
    # X ~ Uniform(0,θ): E[X] = θ/2 → θ̂ = 2X̄
    xbar_num = random.randint(2, 8)
    ans = str(2 * xbar_num)
    return {
        "problem_text": (
            f"\\(X_1, \\ldots, X_n \\sim \\text{{Uniform}}(0, \\theta)\\). "
            f"The method of moments estimator sets \\(E[X] = \\bar{{X}}\\). "
            f"If \\(\\bar{{X}} = {xbar_num}\\), find \\(\\hat{{\\theta}}_{{\\text{{MOM}}}}\\)."
        ),
        "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "For Uniform\\((0,\\theta)\\), \\(E[X] = \\frac{\\theta}{2}\\). Set equal to \\(\\bar{X}\\) and solve."},
            {"level": 2, "text": f"\\(\\frac{{\\hat{{\\theta}}}}{{2}} = {xbar_num} \\Rightarrow \\hat{{\\theta}} = 2 \\cdot {xbar_num}\\)."},
            {"level": 3, "text": f"\\(\\hat{{\\theta}}_{{\\text{{MOM}}}} = {ans}\\)."},
        ],
    }


# ── stat-mle-univariate ───────────────────────────────────────────────────────

def _gen_stat_mle_univariate():
    """MLE for Exponential(λ): λ̂ = 1/X̄."""
    n = random.randint(2, 5)
    vals = [random.randint(1, 5) for _ in range(n)]
    xbar_num = sum(vals)
    # λ̂ = n / Σxi = 1/X̄
    ans = _fr(n, xbar_num)
    return {
        "problem_text": (
            f"Observations \\(x_1={vals[0]}, " +
            ", ".join(f"x_{i+2}={v}" for i,v in enumerate(vals[1:])) +
            f"\\) are iid \\(\\text{{Exponential}}(\\lambda)\\). "
            f"The MLE is \\(\\hat{{\\lambda}} = 1/\\bar{{x}}\\). Find \\(\\hat{{\\lambda}}\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "MLE for Exponential: \\(\\hat{\\lambda} = \\frac{1}{\\bar{x}}\\)."},
            {"level": 2, "text": f"\\(\\bar{{x}} = \\frac{{{xbar_num}}}{{{n}}}\\). So \\(\\hat{{\\lambda}} = \\frac{{{n}}}{{{xbar_num}}}\\)."},
            {"level": 3, "text": f"\\(\\hat{{\\lambda}} = {ans}\\)."},
        ],
    }


# ── stat-mle-multiparameter ───────────────────────────────────────────────────

def _gen_stat_mle_multiparameter():
    """MLE for Normal(μ,σ²): μ̂ = X̄."""
    n = random.randint(3, 5)
    vals = [random.randint(1, 8) for _ in range(n)]
    mu_hat_num = sum(vals)
    ans = _fr(mu_hat_num, n)
    return {
        "problem_text": (
            f"Observations \\(" + ", ".join(str(v) for v in vals) +
            f"\\) are iid \\(N(\\mu, \\sigma^2)\\). "
            f"Find the MLE \\(\\hat{{\\mu}}\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "The MLE for \\(\\mu\\) in a normal model is the sample mean."},
            {"level": 2, "text": f"\\(\\hat{{\\mu}} = \\bar{{x}} = \\frac{{{mu_hat_num}}}{{{n}}}\\)."},
            {"level": 3, "text": f"\\(\\hat{{\\mu}} = {ans}\\)."},
        ],
    }


# ── stat-mle-properties ───────────────────────────────────────────────────────

def _gen_stat_mle_properties():
    """Invariance of MLE: if θ̂ is MLE of θ, then g(θ̂) is MLE of g(θ)."""
    lam = random.randint(2, 6)
    # MLE of E[X] = 1/λ given λ̂
    ans = _fr(1, lam)
    return {
        "problem_text": (
            f"For iid Exponential data, the MLE of \\(\\lambda\\) is \\(\\hat{{\\lambda}} = {lam}\\). "
            f"By the invariance principle, what is the MLE of \\(E[X] = 1/\\lambda\\)?"
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "MLE invariance: if \\(\\hat{\\lambda}\\) is the MLE of \\(\\lambda\\), then \\(g(\\hat{\\lambda})\\) is the MLE of \\(g(\\lambda)\\)."},
            {"level": 2, "text": f"\\(g(\\lambda) = 1/\\lambda\\). Plug in \\(\\hat{{\\lambda}} = {lam}\\)."},
            {"level": 3, "text": f"MLE of \\(E[X]\\) is \\(1/{lam} = {ans}\\)."},
        ],
    }


# ── stat-sufficiency ──────────────────────────────────────────────────────────

def _gen_stat_sufficiency():
    """Sufficient statistic: identify T = ΣXi for Bernoulli or Exponential."""
    choice = random.randint(0, 1)
    if choice == 0:
        n = random.randint(3, 6)
        vals = [random.randint(0, 1) for _ in range(n)]
        t = sum(vals)
        return {
            "problem_text": (
                f"\\(X_1, \\ldots, X_{n} \\stackrel{{iid}}{{\\sim}} \\text{{Bernoulli}}(p)\\) "
                f"with observations \\({', '.join(str(v) for v in vals)}\\). "
                f"The sufficient statistic is \\(T = \\sum X_i\\). Find \\(T\\)."
            ),
            "correct_answer": str(t), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For Bernoulli, the sufficient statistic is the total count of successes."},
                {"level": 2, "text": f"Add all observations: \\({' + '.join(str(v) for v in vals)}\\)."},
                {"level": 3, "text": f"\\(T = {t}\\)."},
            ],
        }
    else:
        n = random.randint(3, 5)
        vals = [random.randint(1, 5) for _ in range(n)]
        t = sum(vals)
        return {
            "problem_text": (
                f"\\(X_1, \\ldots, X_{n} \\stackrel{{iid}}{{\\sim}} \\text{{Exponential}}(\\lambda)\\) "
                f"with observations \\({', '.join(str(v) for v in vals)}\\). "
                f"The sufficient statistic is \\(T = \\sum X_i\\). Find \\(T\\)."
            ),
            "correct_answer": str(t), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For Exponential, the sufficient statistic is the sum of observations."},
                {"level": 2, "text": f"\\({' + '.join(str(v) for v in vals)}\\)."},
                {"level": 3, "text": f"\\(T = {t}\\)."},
            ],
        }


# ── stat-fisher-info ──────────────────────────────────────────────────────────

def _gen_stat_fisher_info():
    """Fisher info for Bernoulli(p): I(p) = 1/(p(1-p))."""
    den = random.choice([3, 4, 5])
    p_num = random.randint(1, den - 1)
    # I(p) = 1 / (p(1-p)) = den² / (p_num * (den - p_num))
    num = den * den
    denom = p_num * (den - p_num)
    ans = _fr(num, denom)
    return {
        "problem_text": (
            f"For \\(X \\sim \\text{{Bernoulli}}(p)\\), the Fisher information is "
            f"\\(I(p) = \\frac{{1}}{{p(1-p)}}\\). "
            f"Evaluate \\(I(p)\\) at \\(p = \\frac{{{p_num}}}{{{den}}}\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Plug \\(p\\) into \\(I(p) = \\frac{1}{p(1-p)}\\)."},
            {"level": 2, "text": f"\\(p(1-p) = \\frac{{{p_num}}}{{{den}}} \\cdot \\frac{{{den-p_num}}}{{{den}}} = \\frac{{{p_num*(den-p_num)}}}{{{den**2}}}\\)."},
            {"level": 3, "text": f"\\(I(p) = \\frac{{{den**2}}}{{{p_num*(den-p_num)}}} = {ans}\\)."},
        ],
    }


# ── stat-crlb ─────────────────────────────────────────────────────────────────

def _gen_stat_crlb():
    """CRLB = 1/(n·I(θ)): lower bound on variance of unbiased estimator."""
    n = random.randint(4, 20)
    i_theta = random.choice([1, 2, 4])
    ans = _fr(1, n * i_theta)
    return {
        "problem_text": (
            f"The Fisher information per observation is \\(I(\\theta) = {i_theta}\\), "
            f"and there are \\(n = {n}\\) iid observations. "
            f"What is the Cramér-Rao lower bound on the variance of any unbiased estimator?"
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "CRLB = \\(\\frac{1}{n \\cdot I(\\theta)}\\)."},
            {"level": 2, "text": f"\\(\\frac{{1}}{{{n} \\cdot {i_theta}}} = \\frac{{1}}{{{n*i_theta}}}\\)."},
            {"level": 3, "text": f"CRLB \\(= {ans}\\)."},
        ],
    }


# ── stat-mvue ─────────────────────────────────────────────────────────────────

def _gen_stat_mvue():
    """MVUE: identify that the sample mean achieves CRLB for Normal."""
    mu = random.randint(2, 8)
    sig2 = random.choice([1, 4, 9])
    n = random.choice([4, 9, 16, 25])
    ans = _fr(sig2, n)
    return {
        "problem_text": (
            f"\\(X_1,\\ldots,X_n \\stackrel{{iid}}{{\\sim}} N(\\mu, \\sigma^2={sig2})\\), \\(n={n}\\). "
            f"The MVUE of \\(\\mu\\) is \\(\\bar{{X}}\\). What is \\(\\text{{Var}}(\\bar{{X}})\\)?"
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "The variance of the sample mean is \\(\\sigma^2/n\\), which equals the CRLB here."},
            {"level": 2, "text": f"\\(\\text{{Var}}(\\bar{{X}}) = \\frac{{{sig2}}}{{{n}}}\\)."},
            {"level": 3, "text": f"\\(= {ans}\\)."},
        ],
    }


# ── stat-delta-method ─────────────────────────────────────────────────────────

def _gen_stat_delta_method():
    """Delta method: Var(g(X̄)) ≈ [g'(μ)]²·σ²/n."""
    # g(x) = ax+b → g'=a; Var = a²σ²/n
    a = random.randint(2, 4)
    sig2 = random.choice([1, 4, 9])
    n = random.choice([4, 9, 16])
    ans = _fr(a**2 * sig2, n)
    return {
        "problem_text": (
            f"By the delta method, if \\(\\text{{Var}}(\\bar{{X}}) = \\frac{{\\sigma^2}}{{n}} = \\frac{{{sig2}}}{{{n}}}\\) "
            f"and \\(g(x) = {a}x\\), find \\(\\text{{Var}}(g(\\bar{{X}}))\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Delta method: \\(\\text{Var}(g(\\bar{X})) \\approx [g'(\\mu)]^2 \\cdot \\text{Var}(\\bar{X})\\)."},
            {"level": 2, "text": f"\\(g'(x) = {a}\\). So \\(\\text{{Var}} = {a}^2 \\cdot \\frac{{{sig2}}}{{{n}}} = \\frac{{{a**2*sig2}}}{{{n}}}\\)."},
            {"level": 3, "text": f"\\(= {ans}\\)."},
        ],
    }


# ── stat-bootstrap ────────────────────────────────────────────────────────────

def _gen_stat_bootstrap():
    """Bootstrap SE: concept question — what does bootstrap estimate?"""
    stat_names = ["sample mean", "sample median", "sample variance", "sample correlation"]
    stat = random.choice(stat_names)
    return {
        "problem_text": (
            f"The bootstrap is used to estimate the standard error of the {stat}. "
            f"In each bootstrap replicate, \\(n\\) observations are drawn with replacement "
            f"from the original sample of size \\(n\\). "
            f"If the original sample size is \\(n=25\\), how many observations are in each bootstrap sample?"
        ),
        "correct_answer": "25", "answer_type": "numeric", "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "Bootstrap samples are the same size as the original sample."},
            {"level": 2, "text": "Each bootstrap sample has \\(n\\) observations drawn with replacement."},
            {"level": 3, "text": "Bootstrap sample size = \\(n = 25\\)."},
        ],
    }


# ── stat-ci-z ─────────────────────────────────────────────────────────────────

def _gen_stat_ci_z():
    """Z confidence interval: width or half-width."""
    # 95% CI: X̄ ± 1.96 σ/√n; ask for half-width
    sig = random.choice([2, 3, 4, 5])
    n = random.choice([4, 9, 16, 25, 100])
    z = random.choice([1, 2])   # 1 for 68%, 2 for 95% (approx)
    se = Fraction(sig, int(sqrt(n)))
    half_width = _fr(z * sig, int(sqrt(n)))
    label = "68%" if z == 1 else "95%"
    return {
        "problem_text": (
            f"A \\({label}\\) confidence interval uses \\(z^* = {z}\\). "
            f"With \\(\\sigma = {sig}\\) and \\(n = {n}\\), "
            f"find the half-width \\(z^* \\cdot \\sigma/\\sqrt{{n}}\\)."
        ),
        "correct_answer": half_width, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Half-width = \\(z^* \\cdot \\frac{\\sigma}{\\sqrt{n}}\\)."},
            {"level": 2, "text": f"\\(= {z} \\cdot \\frac{{{sig}}}{{\\sqrt{{{n}}}}} = {z} \\cdot \\frac{{{sig}}}{{{int(sqrt(n))}}}\\)."},
            {"level": 3, "text": f"\\(= \\frac{{{z*sig}}}{{{int(sqrt(n))}}} = {half_width}\\)."},
        ],
    }


# ── stat-ci-t ─────────────────────────────────────────────────────────────────

def _gen_stat_ci_t():
    """t-CI: degrees of freedom for a one-sample t-interval."""
    n = random.randint(5, 25)
    ans = str(n - 1)
    return {
        "problem_text": (
            f"A one-sample \\(t\\)-interval is constructed from \\(n = {n}\\) observations. "
            f"How many degrees of freedom does the \\(t\\)-distribution have?"
        ),
        "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "The degrees of freedom for a one-sample \\(t\\)-interval is \\(n - 1\\)."},
            {"level": 2, "text": f"\\(df = {n} - 1\\)."},
            {"level": 3, "text": f"\\(df = {ans}\\)."},
        ],
    }


# ── stat-ci-proportion ────────────────────────────────────────────────────────

def _gen_stat_ci_proportion():
    """CI for proportion: SE = sqrt(p̂(1-p̂)/n)."""
    n = random.choice([100, 400, 900])
    p_num = random.randint(1, 9)
    p_den = 10
    p = Fraction(p_num, p_den)
    # SE² = p(1-p)/n
    se2_num = p_num * (p_den - p_num)
    se2_den = p_den**2 * n
    se2 = _fr(se2_num, se2_den)
    return {
        "problem_text": (
            f"In a sample of \\(n={n}\\), the sample proportion is \\(\\hat{{p}} = \\frac{{{p_num}}}{{{p_den}}}\\). "
            f"Find \\(\\widehat{{\\text{{Var}}}}(\\hat{{p}}) = \\hat{{p}}(1-\\hat{{p}})/n\\)."
        ),
        "correct_answer": se2, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "\\(\\widehat{\\text{Var}}(\\hat{p}) = \\frac{\\hat{p}(1-\\hat{p})}{n}\\)."},
            {"level": 2, "text": f"\\(= \\frac{{\\frac{{{p_num}}}{{{p_den}}} \\cdot \\frac{{{p_den-p_num}}}{{{p_den}}}}}{{{n}}}\\)."},
            {"level": 3, "text": f"\\(= \\frac{{{se2_num}}}{{{se2_den}}} = {se2}\\)."},
        ],
    }


# ── stat-hyp-setup ────────────────────────────────────────────────────────────

def _gen_stat_hyp_setup():
    """Identify H0/H1 direction: one-sided vs two-sided."""
    mu0 = random.randint(50, 100)
    direction = random.choice(["greater", "less", "not equal"])
    symbol = {"greater": ">", "less": "<", "not equal": "\\neq"}[direction]
    sides = {"greater": 1, "less": 1, "not equal": 2}[direction]
    return {
        "problem_text": (
            f"A researcher tests \\(H_0: \\mu = {mu0}\\) vs \\(H_1: \\mu {symbol} {mu0}\\). "
            f"How many sides does this test have?"
        ),
        "correct_answer": str(sides), "answer_type": "numeric", "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "A test is one-sided if \\(H_1\\) uses \\(>\\) or \\(<\\), and two-sided if it uses \\(\\neq\\)."},
            {"level": 2, "text": f"\\(H_1: \\mu {symbol} {mu0}\\)."},
            {"level": 3, "text": f"This is a {'one' if sides==1 else 'two'}-sided test: {sides} side(s)."},
        ],
    }


# ── stat-errors-power ─────────────────────────────────────────────────────────

def _gen_stat_errors_power():
    """Power = 1 - β, or identify Type I / Type II error rate."""
    alpha = random.choice([5, 10])
    beta = random.choice([10, 20, 30])
    ask = random.randint(0, 1)
    if ask == 0:
        ans = str(100 - beta)
        return {
            "problem_text": (
                f"A test has Type II error rate \\(\\beta = {beta}\\%\\). "
                f"What is the power of the test (in %)?"
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Power \\(= 1 - \\beta\\)."},
                {"level": 2, "text": f"\\(100\\% - {beta}\\%\\)."},
                {"level": 3, "text": f"Power \\(= {ans}\\%\\)."},
            ],
        }
    else:
        ans = str(alpha)
        return {
            "problem_text": (
                f"A test is conducted at significance level \\(\\alpha = {alpha}\\%\\). "
                f"What is the probability of a Type I error (in %)?"
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The Type I error rate equals the significance level \\(\\alpha\\)."},
                {"level": 2, "text": f"\\(\\alpha = {alpha}\\%\\)."},
                {"level": 3, "text": f"Type I error rate \\(= {ans}\\%\\)."},
            ],
        }


# ── stat-pvalue ───────────────────────────────────────────────────────────────

def _gen_stat_pvalue():
    """Interpret p-value: reject H0 if p ≤ α."""
    alpha = random.choice([0.01, 0.05, 0.10])
    reject = random.randint(0, 1)
    if reject:
        p = round(alpha * random.uniform(0.1, 0.9), 4)
        conclusion = "Reject"
    else:
        p = round(alpha + random.uniform(0.01, 0.10), 4)
        conclusion = "Fail to reject"
    return {
        "problem_text": (
            f"A hypothesis test yields \\(p\\)-value \\(= {p}\\). "
            f"The significance level is \\(\\alpha = {alpha}\\). "
            f"Enter 1 if you reject \\(H_0\\), or 0 if you fail to reject \\(H_0\\)."
        ),
        "correct_answer": "1" if reject else "0", "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "Reject \\(H_0\\) if the \\(p\\)-value \\(\\leq \\alpha\\)."},
            {"level": 2, "text": f"Compare \\(p = {p}\\) with \\(\\alpha = {alpha}\\)."},
            {"level": 3, "text": f"\\({p} " + ("\\leq" if reject else ">") + f" {alpha}\\) → {conclusion} \\(H_0\\). Answer: " + ("1" if reject else "0") + "."},
        ],
    }


# ── stat-neyman-pearson ───────────────────────────────────────────────────────

def _gen_stat_neyman_pearson():
    """NP lemma: likelihood ratio test statistic for simple hypotheses."""
    theta0 = random.randint(1, 3)
    theta1 = random.randint(theta0 + 1, theta0 + 3)
    # For Exponential: LR = (θ0/θ1)^n * exp(-(1/θ0 - 1/θ1)Σx)
    # Reject when Σx > c ↔ X̄ > c'
    # Ask: for Exp(λ), the NP test rejects for large or small X̄?
    # λ0 < λ1 → reject H0:λ=λ0 when x̄ is SMALL (high λ1 means smaller mean)
    return {
        "problem_text": (
            f"Testing \\(H_0: \\lambda = {theta0}\\) vs \\(H_1: \\lambda = {theta1}\\) "
            f"for iid Exponential(\\(\\lambda\\)) data. "
            f"The NP most powerful test rejects \\(H_0\\) for small values of \\(\\bar{{X}}\\). "
            f"If \\(\\bar{{X}} = {theta0}\\) and the critical value is \\(c = {theta0 - 1}\\), "
            f"do we reject \\(H_0\\)? Enter 1 for reject, 0 for fail to reject."
        ),
        "correct_answer": "0", "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Reject when \\(\\bar{X} < c\\)."},
            {"level": 2, "text": f"Compare \\(\\bar{{X}} = {theta0}\\) with \\(c = {theta0-1}\\)."},
            {"level": 3, "text": f"\\({theta0} \\not< {theta0-1}\\) → fail to reject. Answer: 0."},
        ],
    }


# ── stat-ump ──────────────────────────────────────────────────────────────────

def _gen_stat_ump():
    """UMP test: for exponential family, identify rejection region direction."""
    return {
        "problem_text": (
            "For a one-parameter exponential family with natural parameter \\(\\eta(\\theta)\\) "
            "increasing in \\(\\theta\\), and testing \\(H_0: \\theta \\leq \\theta_0\\) vs "
            "\\(H_1: \\theta > \\theta_0\\), the UMP test rejects for large values of the "
            "sufficient statistic \\(T\\). "
            "If \\(T = 18\\) and the critical value is \\(c = 15\\), "
            "do we reject \\(H_0\\)? Enter 1 for reject, 0 for fail to reject."
        ),
        "correct_answer": "1", "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "The UMP test rejects \\(H_0\\) when \\(T > c\\)."},
            {"level": 2, "text": "Compare \\(T = 18\\) with \\(c = 15\\)."},
            {"level": 3, "text": "\\(18 > 15\\) → reject \\(H_0\\). Answer: 1."},
        ],
    }


# ── stat-glrt ─────────────────────────────────────────────────────────────────

def _gen_stat_glrt():
    """GLRT statistic: -2 log Λ is asymptotically χ² with df = dim(Θ) - dim(Θ0)."""
    dim_full = random.randint(2, 4)
    dim_null = random.randint(1, dim_full - 1)
    df = dim_full - dim_null
    return {
        "problem_text": (
            f"The full model has \\({dim_full}\\) free parameters; "
            f"the null model (nested) has \\({dim_null}\\) free parameters. "
            f"Under \\(H_0\\), the GLRT statistic \\(-2\\log\\Lambda\\) is asymptotically "
            f"\\(\\chi^2\\) with how many degrees of freedom?"
        ),
        "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "The degrees of freedom for the GLRT = (parameters in full model) - (parameters in null model)."},
            {"level": 2, "text": f"\\({dim_full} - {dim_null}\\)."},
            {"level": 3, "text": f"\\(df = {df}\\)."},
        ],
    }


# ── stat-power-sample-size ────────────────────────────────────────────────────

def _gen_stat_power_sample_size():
    """Sample size to achieve desired margin of error: n = (z·σ/E)²."""
    sig = random.choice([2, 3, 4, 5])
    z = 2  # ≈ 1.96 for 95%
    E = random.choice([1, 2])
    n = (z * sig // E) ** 2
    return {
        "problem_text": (
            f"For a 95% CI (using \\(z^*=2\\)), \\(\\sigma={sig}\\), desired margin of error \\(E={E}\\). "
            f"Find the minimum sample size \\(n = \\left(\\frac{{z^* \\sigma}}{{E}}\\right)^2\\)."
        ),
        "correct_answer": str(n), "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "\\(n = \\left(\\frac{z^* \\sigma}{E}\\right)^2\\)."},
            {"level": 2, "text": f"\\(= \\left(\\frac{{{z} \\cdot {sig}}}{{{E}}}\\right)^2 = \\left({z*sig//E}\\right)^2\\)."},
            {"level": 3, "text": f"\\(n = {n}\\)."},
        ],
    }


# ── stat-ztest-one ────────────────────────────────────────────────────────────

def _gen_stat_ztest_one():
    """One-sample z-test statistic: z = (X̄ - μ0) / (σ/√n)."""
    mu0 = random.randint(50, 80)
    sig = random.choice([2, 4, 5, 10])
    n = random.choice([4, 16, 25, 100])
    diff = random.choice([-2, -1, 1, 2]) * sig // int(sqrt(n))
    xbar = mu0 + diff * int(sqrt(n))
    z = (xbar - mu0) * int(sqrt(n)) // sig
    return {
        "problem_text": (
            f"One-sample z-test: \\(\\mu_0 = {mu0}\\), \\(\\sigma = {sig}\\), "
            f"\\(n = {n}\\), \\(\\bar{{x}} = {xbar}\\). "
            f"Compute \\(z = \\frac{{\\bar{{x}} - \\mu_0}}{{\\sigma/\\sqrt{{n}}}}\\)."
        ),
        "correct_answer": str(z), "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "\\(z = \\frac{\\bar{x} - \\mu_0}{\\sigma / \\sqrt{n}}\\)."},
            {"level": 2, "text": f"Numerator: \\({xbar} - {mu0} = {xbar-mu0}\\). Denominator: \\({sig}/\\sqrt{{{n}}} = {sig//int(sqrt(n))}\\)."},
            {"level": 3, "text": f"\\(z = \\frac{{{xbar-mu0}}}{{{sig//int(sqrt(n))}}} = {z}\\)."},
        ],
    }


# ── stat-ttest-one ────────────────────────────────────────────────────────────

def _gen_stat_ttest_one():
    """One-sample t-test: degrees of freedom."""
    n = random.randint(5, 30)
    return {
        "problem_text": (
            f"A one-sample \\(t\\)-test uses \\(n = {n}\\) observations. "
            f"What are the degrees of freedom?"
        ),
        "correct_answer": str(n - 1), "answer_type": "numeric", "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "Degrees of freedom for a one-sample \\(t\\)-test: \\(df = n - 1\\)."},
            {"level": 2, "text": f"\\(df = {n} - 1\\)."},
            {"level": 3, "text": f"\\(df = {n-1}\\)."},
        ],
    }


# ── stat-ttest-two ────────────────────────────────────────────────────────────

def _gen_stat_ttest_two():
    """Two-sample t-test (equal variances): df = n1 + n2 - 2."""
    n1 = random.randint(5, 20)
    n2 = random.randint(5, 20)
    df = n1 + n2 - 2
    return {
        "problem_text": (
            f"A two-sample \\(t\\)-test (equal variances) compares groups of size "
            f"\\(n_1 = {n1}\\) and \\(n_2 = {n2}\\). "
            f"What are the degrees of freedom?"
        ),
        "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "For a two-sample pooled \\(t\\)-test: \\(df = n_1 + n_2 - 2\\)."},
            {"level": 2, "text": f"\\(df = {n1} + {n2} - 2\\)."},
            {"level": 3, "text": f"\\(df = {df}\\)."},
        ],
    }


# ── stat-pooled-variance ──────────────────────────────────────────────────────

def _gen_stat_pooled_variance():
    """Pooled variance: Sp² = ((n1-1)s1² + (n2-1)s2²) / (n1+n2-2)."""
    n1 = random.randint(5, 12)
    n2 = random.randint(5, 12)
    s1 = random.randint(1, 4)
    s2 = random.randint(1, 4)
    num = (n1 - 1) * s1**2 + (n2 - 1) * s2**2
    denom = n1 + n2 - 2
    ans = _fr(num, denom)
    return {
        "problem_text": (
            f"\\(n_1={n1}\\), \\(s_1^2={s1**2}\\), \\(n_2={n2}\\), \\(s_2^2={s2**2}\\). "
            f"Find the pooled variance "
            f"\\(S_p^2 = \\frac{{(n_1-1)s_1^2 + (n_2-1)s_2^2}}{{n_1+n_2-2}}\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Plug values into the formula."},
            {"level": 2, "text": f"Numerator: \\(({n1}-1)\\cdot{s1**2} + ({n2}-1)\\cdot{s2**2} = {(n1-1)*s1**2} + {(n2-1)*s2**2} = {num}\\)."},
            {"level": 3, "text": f"\\(S_p^2 = \\frac{{{num}}}{{{denom}}} = {ans}\\)."},
        ],
    }


# ── stat-ttest-paired ─────────────────────────────────────────────────────────

def _gen_stat_ttest_paired():
    """Paired t-test: d̄ = mean of differences."""
    n = random.randint(3, 6)
    diffs = [random.randint(-3, 4) for _ in range(n)]
    dbar_num = sum(diffs)
    ans = _fr(dbar_num, n)
    return {
        "problem_text": (
            f"Paired differences are: \\({', '.join(str(d) for d in diffs)}\\). "
            f"Compute \\(\\bar{{d}}\\), the mean of the differences."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "\\(\\bar{d} = \\frac{1}{n}\\sum d_i\\)."},
            {"level": 2, "text": f"Sum = \\({' + '.join(str(d) for d in diffs)} = {dbar_num}\\). Divide by \\({n}\\)."},
            {"level": 3, "text": f"\\(\\bar{{d}} = \\frac{{{dbar_num}}}{{{n}}} = {ans}\\)."},
        ],
    }


# ── stat-mannwhitney ──────────────────────────────────────────────────────────

def _gen_stat_mannwhitney():
    """Mann-Whitney U: count U statistic for small samples."""
    # Small example: compare two groups
    n1 = random.randint(2, 3)
    n2 = random.randint(2, 3)
    # Generate distinct values
    all_vals = random.sample(range(1, 12), n1 + n2)
    g1 = sorted(all_vals[:n1])
    g2 = sorted(all_vals[n1:])
    # U1 = number of (g1[i], g2[j]) pairs where g1[i] > g2[j]
    u1 = sum(1 for x in g1 for y in g2 if x > y)
    return {
        "problem_text": (
            f"Group 1: \\({', '.join(str(v) for v in g1)}\\). "
            f"Group 2: \\({', '.join(str(v) for v in g2)}\\). "
            f"Compute \\(U_1\\) = number of times a Group 1 value exceeds a Group 2 value."
        ),
        "correct_answer": str(u1), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Compare every pair \\((x_i, y_j)\\) where \\(x_i \\in\\) Group 1 and \\(y_j \\in\\) Group 2. Count pairs where \\(x_i > y_j\\)."},
            {"level": 2, "text": f"Total pairs to check: \\({n1} \\times {n2} = {n1*n2}\\)."},
            {"level": 3, "text": f"\\(U_1 = {u1}\\)."},
        ],
    }


# ── stat-wilcoxon-signed ──────────────────────────────────────────────────────

def _gen_stat_wilcoxon_signed():
    """Wilcoxon signed rank: sum of ranks of positive differences."""
    n = random.randint(3, 5)
    diffs = random.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], n)
    abs_diffs = sorted(abs(d) for d in diffs)
    # Assign ranks (1 to n)
    ranks = {v: i+1 for i, v in enumerate(abs_diffs)}
    w_plus = sum(ranks[abs(d)] for d in diffs if d > 0)
    return {
        "problem_text": (
            f"Signed differences: \\({', '.join(str(d) for d in diffs)}\\). "
            f"Rank the absolute values (rank 1 = smallest). "
            f"Compute \\(W^+\\) = sum of ranks for positive differences."
        ),
        "correct_answer": str(w_plus), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Rank \\(|d_i|\\) from smallest to largest. \\(W^+\\) = sum of ranks for positive \\(d_i\\)."},
            {"level": 2, "text": f"Absolute values: \\({', '.join(str(abs(d)) for d in diffs)}\\). Ranks: \\({', '.join(str(ranks[abs(d)]) for d in diffs)}\\)."},
            {"level": 3, "text": f"Positive differences: \\({', '.join(str(d) for d in diffs if d>0)}\\) have ranks \\({', '.join(str(ranks[abs(d)]) for d in diffs if d>0)}\\). Sum = \\({w_plus}\\)."},
        ],
    }


# ── stat-permutation ──────────────────────────────────────────────────────────

def _gen_stat_permutation():
    """Permutation test: number of possible permutations of n1+n2 items."""
    n1 = random.randint(2, 4)
    n2 = random.randint(2, 4)
    from math import comb
    ans = comb(n1 + n2, n1)
    return {
        "problem_text": (
            f"A permutation test has \\(n_1 = {n1}\\) and \\(n_2 = {n2}\\) observations. "
            f"How many ways can the \\(n_1 + n_2\\) observations be split into groups of size "
            f"\\(n_1\\) and \\(n_2\\)?"
        ),
        "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Choose \\(n_1\\) items from \\(n_1+n_2\\): \\(\\binom{n_1+n_2}{n_1}\\)."},
            {"level": 2, "text": f"\\(\\binom{{{n1+n2}}}{{{n1}}}\\)."},
            {"level": 3, "text": f"\\(= {ans}\\)."},
        ],
    }


# ── stat-chi-gof ──────────────────────────────────────────────────────────────

def _gen_stat_chi_gof():
    """Chi-squared GOF: degrees of freedom = k - 1 (or k - 1 - p)."""
    k = random.randint(3, 6)
    p_est = random.randint(0, 1)
    df = k - 1 - p_est
    label = f"(estimating {p_est} parameter{'s' if p_est>1 else ''})" if p_est else ""
    return {
        "problem_text": (
            f"A chi-squared goodness-of-fit test has \\(k = {k}\\) categories "
            f"{'and requires estimating ' + str(p_est) + ' parameter from the data ' if p_est else ''}(all parameters known if not stated). "
            f"What are the degrees of freedom?"
        ),
        "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "\\(df = k - 1 - \\text{(number of estimated parameters)}\\)."},
            {"level": 2, "text": f"\\(df = {k} - 1 - {p_est}\\)."},
            {"level": 3, "text": f"\\(df = {df}\\)."},
        ],
    }


# ── stat-chi-indep ────────────────────────────────────────────────────────────

def _gen_stat_chi_indep():
    """Chi-squared independence test: df = (r-1)(c-1)."""
    r = random.randint(2, 4)
    c = random.randint(2, 4)
    df = (r - 1) * (c - 1)
    return {
        "problem_text": (
            f"A chi-squared test of independence uses a \\({r} \\times {c}\\) contingency table. "
            f"What are the degrees of freedom?"
        ),
        "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "\\(df = (r-1)(c-1)\\) for an \\(r \\times c\\) contingency table."},
            {"level": 2, "text": f"\\(df = ({r}-1)({c}-1) = {r-1} \\cdot {c-1}\\)."},
            {"level": 3, "text": f"\\(df = {df}\\)."},
        ],
    }


# ── stat-chi-homog ────────────────────────────────────────────────────────────

def _gen_stat_chi_homog():
    """Chi-squared homogeneity: df = (r-1)(c-1) same formula."""
    r = random.randint(2, 4)
    c = random.randint(2, 4)
    df = (r - 1) * (c - 1)
    return {
        "problem_text": (
            f"A chi-squared test of homogeneity compares \\({c}\\) groups across \\({r}\\) categories. "
            f"What are the degrees of freedom?"
        ),
        "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "The test of homogeneity uses the same \\(df\\) formula as independence: \\((r-1)(c-1)\\)."},
            {"level": 2, "text": f"\\(({r}-1)({c}-1) = {r-1} \\cdot {c-1}\\)."},
            {"level": 3, "text": f"\\(df = {df}\\)."},
        ],
    }


# ── stat-anova-one ────────────────────────────────────────────────────────────

def _gen_stat_anova_one():
    """One-way ANOVA: df between = k-1, df within = N-k."""
    k = random.randint(3, 5)
    n_per = random.randint(5, 10)
    N = k * n_per
    df_between = k - 1
    df_within = N - k
    ask = random.randint(0, 1)
    if ask == 0:
        ans = str(df_between)
        label = "between groups (treatment)"
    else:
        ans = str(df_within)
        label = "within groups (error)"
    return {
        "problem_text": (
            f"A one-way ANOVA has \\(k={k}\\) groups of \\(n={n_per}\\) each (\\(N={N}\\) total). "
            f"Find the degrees of freedom {label}."
        ),
        "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "Between: \\(df = k - 1\\). Within: \\(df = N - k\\)."},
            {"level": 2, "text": f"Between: \\({k}-1={df_between}\\). Within: \\({N}-{k}={df_within}\\)."},
            {"level": 3, "text": f"Answer: \\({ans}\\)."},
        ],
    }


# ── stat-anova-kruskal ────────────────────────────────────────────────────────

def _gen_stat_anova_kruskal():
    """Kruskal-Wallis: df for chi-squared approximation = k-1."""
    k = random.randint(3, 5)
    df = k - 1
    return {
        "problem_text": (
            f"A Kruskal-Wallis test compares \\(k={k}\\) independent groups. "
            f"Under \\(H_0\\), the test statistic is approximately \\(\\chi^2\\). "
            f"What are the degrees of freedom?"
        ),
        "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "The Kruskal-Wallis statistic is approximately \\(\\chi^2_{k-1}\\)."},
            {"level": 2, "text": f"\\(df = k - 1 = {k} - 1\\)."},
            {"level": 3, "text": f"\\(df = {df}\\)."},
        ],
    }


# ── stat-multiple-testing ─────────────────────────────────────────────────────

def _gen_stat_multiple_testing():
    """Bonferroni correction: α* = α/m."""
    m = random.choice([5, 10, 20])
    alpha_pct = random.choice([5, 10])
    alpha_frac = Fraction(alpha_pct, 100)
    corrected = Fraction(alpha_frac.numerator, alpha_frac.denominator * m)
    ans = _fr(corrected.numerator, corrected.denominator)
    return {
        "problem_text": (
            f"You are performing \\(m={m}\\) hypothesis tests at family-wise error rate \\(\\alpha={alpha_pct}\\%\\). "
            f"Using the Bonferroni correction, what is the per-test significance level \\(\\alpha^* = \\alpha/m\\)?"
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "Bonferroni correction: \\(\\alpha^* = \\alpha / m\\)."},
            {"level": 2, "text": f"\\(\\alpha^* = \\frac{{{alpha_pct}\\%}}{{{m}}} = \\frac{{{alpha_pct}}}{{{100*m}}}\\)."},
            {"level": 3, "text": f"\\(\\alpha^* = {ans}\\)."},
        ],
    }


# ── stat-slr ──────────────────────────────────────────────────────────────────

def _gen_stat_slr():
    """SLR: β̂1 = Σ(xi-x̄)(yi-ȳ) / Σ(xi-x̄)²."""
    # Simple: 3 points with integer slope
    b1 = random.randint(1, 4)
    b0 = random.randint(0, 5)
    xs = [1, 2, 3]
    ys = [b0 + b1 * x + random.choice([0]) for x in xs]
    xbar = 2  # mean of 1,2,3
    ybar = sum(ys) / 3
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    sxx = sum((x - xbar)**2 for x in xs)
    ans = _fr(int(sxy), int(sxx))
    return {
        "problem_text": (
            f"Data: \\((x,y)\\) pairs: \\((1,{ys[0]})\\), \\((2,{ys[1]})\\), \\((3,{ys[2]})\\). "
            f"Find the OLS slope \\(\\hat{{\\beta}}_1 = \\frac{{\\sum(x_i-\\bar{{x}})(y_i-\\bar{{y}})}}{{\\sum(x_i-\\bar{{x}})^2}}\\)."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Compute \\(S_{xy} = \\sum(x_i - \\bar{x})(y_i - \\bar{y})\\) and \\(S_{xx} = \\sum(x_i - \\bar{x})^2\\)."},
            {"level": 2, "text": f"\\(\\bar{{x}}=2\\), \\(\\bar{{y}}={int(ybar)}\\). \\(S_{{xx}} = {int(sxx)}\\), \\(S_{{xy}} = {int(sxy)}\\)."},
            {"level": 3, "text": f"\\(\\hat{{\\beta}}_1 = {int(sxy)}/{int(sxx)} = {ans}\\)."},
        ],
    }


# ── stat-slr-matrix ───────────────────────────────────────────────────────────

def _gen_stat_slr_matrix():
    """SLR in matrix form: dimension of X matrix."""
    n = random.randint(10, 50)
    return {
        "problem_text": (
            f"In simple linear regression with \\(n={n}\\) observations, "
            f"the design matrix \\(\\mathbf{{X}}\\) includes an intercept column and one predictor. "
            f"What are the dimensions of \\(\\mathbf{{X}}\\)?"
        ),
        "correct_answer": f"{n}x2", "answer_type": "symbolic", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "The design matrix has one row per observation and one column per parameter (intercept + slope)."},
            {"level": 2, "text": f"\\(n = {n}\\) rows, 2 columns (intercept and one predictor)."},
            {"level": 3, "text": f"\\(\\mathbf{{X}}\\) is \\({n} \\times 2\\). Enter as {n}x2."},
        ],
    }


# ── stat-slr-inference ────────────────────────────────────────────────────────

def _gen_stat_slr_inference():
    """SLR inference: df for t-test on slope = n-2."""
    n = random.randint(5, 30)
    return {
        "problem_text": (
            f"In simple linear regression with \\(n={n}\\) observations, "
            f"a \\(t\\)-test on the slope uses how many degrees of freedom?"
        ),
        "correct_answer": str(n - 2), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "SLR estimates 2 parameters (intercept and slope), so residual df \\(= n - 2\\)."},
            {"level": 2, "text": f"\\(df = {n} - 2\\)."},
            {"level": 3, "text": f"\\(df = {n-2}\\)."},
        ],
    }


# ── stat-mlr ──────────────────────────────────────────────────────────────────

def _gen_stat_mlr():
    """MLR: residual df = n - p - 1."""
    n = random.randint(20, 50)
    p = random.randint(2, 5)
    df = n - p - 1
    return {
        "problem_text": (
            f"Multiple linear regression has \\(n={n}\\) observations and \\(p={p}\\) predictors "
            f"(plus an intercept). Find the residual degrees of freedom \\(n - p - 1\\)."
        ),
        "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "Residual \\(df = n - p - 1\\) (subtract one for each estimated coefficient including intercept)."},
            {"level": 2, "text": f"\\({n} - {p} - 1\\)."},
            {"level": 3, "text": f"\\(df = {df}\\)."},
        ],
    }


# ── stat-mlr-inference ────────────────────────────────────────────────────────

def _gen_stat_mlr_inference():
    """F-test numerator df = p (number of predictors)."""
    p = random.randint(2, 5)
    n = random.randint(p + 10, 50)
    return {
        "problem_text": (
            f"The overall \\(F\\)-test in MLR with \\(p={p}\\) predictors (and an intercept) "
            f"has what numerator degrees of freedom?"
        ),
        "correct_answer": str(p), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "The \\(F\\)-test numerator \\(df\\) = number of predictors \\(= p\\)."},
            {"level": 2, "text": f"\\(p = {p}\\)."},
            {"level": 3, "text": f"Numerator \\(df = {p}\\)."},
        ],
    }


# ── stat-model-comparison ─────────────────────────────────────────────────────

def _gen_stat_model_comparison():
    """AIC = 2k - 2 log L̂; compare two models."""
    k1 = random.randint(2, 4)
    k2 = k1 + random.randint(1, 2)
    # log-likelihoods
    ll1 = random.randint(-50, -20)
    ll2 = ll1 + random.randint(1, 4)   # larger model fits better
    aic1 = 2 * k1 - 2 * ll1
    aic2 = 2 * k2 - 2 * ll2
    better = 1 if aic1 < aic2 else 2
    return {
        "problem_text": (
            f"Model 1: \\(k={k1}\\) parameters, \\(\\hat{{\\ell}}={ll1}\\). "
            f"Model 2: \\(k={k2}\\) parameters, \\(\\hat{{\\ell}}={ll2}\\). "
            f"AIC \\(= 2k - 2\\hat{{\\ell}}\\). "
            f"Which model has the lower AIC? Enter 1 or 2."
        ),
        "correct_answer": str(better), "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "AIC = \\(2k - 2\\hat{\\ell}\\). Lower AIC is preferred."},
            {"level": 2, "text": f"AIC\\(_1\\) = \\(2\\cdot{k1} - 2\\cdot({ll1}) = {aic1}\\). AIC\\(_2\\) = \\(2\\cdot{k2} - 2\\cdot({ll2}) = {aic2}\\)."},
            {"level": 3, "text": f"Lower AIC = Model {better}. Answer: {better}."},
        ],
    }


# ── stat-regression-checks ───────────────────────────────────────────────────

def _gen_stat_regression_checks():
    """Regression diagnostics: residual sum of squares."""
    n = random.randint(3, 5)
    resids = [random.randint(-3, 3) for _ in range(n)]
    rss = sum(r**2 for r in resids)
    return {
        "problem_text": (
            f"Residuals from a regression: \\({', '.join(str(r) for r in resids)}\\). "
            f"Compute the residual sum of squares (RSS)."
        ),
        "correct_answer": str(rss), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "RSS \\(= \\sum e_i^2\\) (sum of squared residuals)."},
            {"level": 2, "text": f"Square each: \\({', '.join(str(r**2) for r in resids)}\\)."},
            {"level": 3, "text": f"RSS \\(= {' + '.join(str(r**2) for r in resids)} = {rss}\\)."},
        ],
    }


# ── stat-bayes-posterior ──────────────────────────────────────────────────────

def _gen_stat_bayes_posterior():
    """Bayesian updating: Beta-Binomial conjugate — posterior parameters."""
    alpha0 = random.randint(1, 3)
    beta0 = random.randint(1, 3)
    x = random.randint(2, 8)   # successes
    n = random.randint(x, x + 5)  # trials
    alpha_post = alpha0 + x
    beta_post = beta0 + n - x
    ask = random.randint(0, 1)
    ans = str(alpha_post) if ask == 0 else str(beta_post)
    param = "\\alpha" if ask == 0 else "\\beta"
    return {
        "problem_text": (
            f"Prior: \\(\\theta \\sim \\text{{Beta}}(\\alpha_0={alpha0}, \\beta_0={beta0})\\). "
            f"Observed \\(x={x}\\) successes in \\(n={n}\\) Bernoulli trials. "
            f"The posterior is \\(\\text{{Beta}}(\\alpha_0+x,\\, \\beta_0+n-x)\\). "
            f"Find the posterior parameter \\({param}\\)."
        ),
        "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Beta-Binomial conjugate: posterior is \\(\\text{Beta}(\\alpha_0 + x,\\, \\beta_0 + n - x)\\)."},
            {"level": 2, "text": f"\\(\\alpha_\\text{{post}} = {alpha0} + {x} = {alpha_post}\\). \\(\\beta_\\text{{post}} = {beta0} + {n-x} = {beta_post}\\)."},
            {"level": 3, "text": f"\\({param}_\\text{{post}} = {ans}\\)."},
        ],
    }


# ── stat-order-statistics ─────────────────────────────────────────────────────

def _gen_stat_order_statistics():
    """Order statistics: find the k-th order statistic from a small sample."""
    n = random.randint(4, 7)
    sample = random.sample(range(1, 15), n)
    k = random.randint(1, n)
    ans = str(sorted(sample)[k - 1])
    return {
        "problem_text": (
            f"Sample: \\({', '.join(str(v) for v in sample)}\\). "
            f"Find \\(X_{{({k})}}\\), the \\({k}\\)-th order statistic (\\({k}\\)-th smallest value)."
        ),
        "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "Sort the sample from smallest to largest."},
            {"level": 2, "text": f"Sorted: \\({', '.join(str(v) for v in sorted(sample))}\\)."},
            {"level": 3, "text": f"The {k}-th value is \\({ans}\\)."},
        ],
    }


# ── stat-simulation ───────────────────────────────────────────────────────────

def _gen_stat_simulation():
    """Monte Carlo: estimate of E[g(X)] using sample mean of g(Xi)."""
    n = random.choice([100, 1000])
    total = random.randint(n, 5 * n)
    ans = _fr(total, n)
    return {
        "problem_text": (
            f"A Monte Carlo simulation generates \\(n={n}\\) samples and computes "
            f"\\(g(X_i)\\) for each. The sum is \\(\\sum_{{i=1}}^{{{n}}} g(X_i) = {total}\\). "
            f"Estimate \\(E[g(X)]\\) using the sample mean."
        ),
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "Monte Carlo estimate: \\(\\hat{E}[g(X)] = \\frac{1}{n}\\sum g(X_i)\\)."},
            {"level": 2, "text": f"\\(\\frac{{{total}}}{{{n}}}\\)."},
            {"level": 3, "text": f"\\(= {ans}\\)."},
        ],
    }


# ── stat-confounding ──────────────────────────────────────────────────────────

def _gen_stat_confounding():
    """Confounding: identify the confounding variable in a scenario."""
    return {
        "problem_text": (
            "A study finds that cities with more hospitals have higher death rates. "
            "A researcher claims hospitals cause deaths. "
            "Identify the likely confounder: enter 1 for 'city population size', "
            "or 2 for 'number of doctors'."
        ),
        "correct_answer": "1", "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "A confounder is associated with both the exposure (hospitals) and the outcome (death rate)."},
            {"level": 2, "text": "Larger cities have more hospitals AND more people (who can die). Population size drives both."},
            {"level": 3, "text": "The confounder is city population size. Answer: 1."},
        ],
    }


# ── stat-causal-intro ─────────────────────────────────────────────────────────

def _gen_stat_causal_intro():
    """Potential outcomes: ATE = E[Y(1) - Y(0)]."""
    e_y1 = random.randint(5, 12)
    e_y0 = random.randint(2, e_y1 - 1)
    ate = e_y1 - e_y0
    return {
        "problem_text": (
            f"In the potential outcomes framework, \\(E[Y(1)] = {e_y1}\\) and \\(E[Y(0)] = {e_y0}\\). "
            f"Find the Average Treatment Effect (ATE) \\(= E[Y(1)] - E[Y(0)]\\)."
        ),
        "correct_answer": str(ate), "answer_type": "numeric", "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "ATE \\(= E[Y(1)] - E[Y(0)]\\)."},
            {"level": 2, "text": f"\\({e_y1} - {e_y0}\\)."},
            {"level": 3, "text": f"ATE \\(= {ate}\\)."},
        ],
    }


# ── GENERATORS dict ───────────────────────────────────────────────────────────

GENERATORS = {
    "stat-sampling-dist":      _gen_stat_sampling_dist,
    "stat-estimator-props":    _gen_stat_estimator_props,
    "stat-survey-srs":         _gen_stat_survey_srs,
    "stat-mom":                _gen_stat_mom,
    "stat-mle-univariate":     _gen_stat_mle_univariate,
    "stat-mle-multiparameter": _gen_stat_mle_multiparameter,
    "stat-mle-properties":     _gen_stat_mle_properties,
    "stat-sufficiency":        _gen_stat_sufficiency,
    "stat-fisher-info":        _gen_stat_fisher_info,
    "stat-crlb":               _gen_stat_crlb,
    "stat-mvue":               _gen_stat_mvue,
    "stat-delta-method":       _gen_stat_delta_method,
    "stat-bootstrap":          _gen_stat_bootstrap,
    "stat-ci-z":               _gen_stat_ci_z,
    "stat-ci-t":               _gen_stat_ci_t,
    "stat-ci-proportion":      _gen_stat_ci_proportion,
    "stat-hyp-setup":          _gen_stat_hyp_setup,
    "stat-errors-power":       _gen_stat_errors_power,
    "stat-pvalue":             _gen_stat_pvalue,
    "stat-neyman-pearson":     _gen_stat_neyman_pearson,
    "stat-ump":                _gen_stat_ump,
    "stat-glrt":               _gen_stat_glrt,
    "stat-power-sample-size":  _gen_stat_power_sample_size,
    "stat-ztest-one":          _gen_stat_ztest_one,
    "stat-ttest-one":          _gen_stat_ttest_one,
    "stat-ttest-two":          _gen_stat_ttest_two,
    "stat-pooled-variance":    _gen_stat_pooled_variance,
    "stat-ttest-paired":       _gen_stat_ttest_paired,
    "stat-mannwhitney":        _gen_stat_mannwhitney,
    "stat-wilcoxon-signed":    _gen_stat_wilcoxon_signed,
    "stat-permutation":        _gen_stat_permutation,
    "stat-chi-gof":            _gen_stat_chi_gof,
    "stat-chi-indep":          _gen_stat_chi_indep,
    "stat-chi-homog":          _gen_stat_chi_homog,
    "stat-anova-one":          _gen_stat_anova_one,
    "stat-anova-kruskal":      _gen_stat_anova_kruskal,
    "stat-multiple-testing":   _gen_stat_multiple_testing,
    "stat-slr":                _gen_stat_slr,
    "stat-slr-matrix":         _gen_stat_slr_matrix,
    "stat-slr-inference":      _gen_stat_slr_inference,
    "stat-mlr":                _gen_stat_mlr,
    "stat-mlr-inference":      _gen_stat_mlr_inference,
    "stat-model-comparison":   _gen_stat_model_comparison,
    "stat-regression-checks":  _gen_stat_regression_checks,
    "stat-bayes-posterior":    _gen_stat_bayes_posterior,
    "stat-order-statistics":   _gen_stat_order_statistics,
    "stat-simulation":         _gen_stat_simulation,
    "stat-confounding":        _gen_stat_confounding,
    "stat-causal-intro":       _gen_stat_causal_intro,
}
