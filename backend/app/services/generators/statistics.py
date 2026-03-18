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
    """Var(X̄) = σ²/n; find Var(X̄), SD(X̄), or n given Var(X̄)."""
    variant = random.choice([0, 1, 2])
    sig2 = random.choice([4, 9, 16, 25])
    n = random.choice([4, 9, 16, 25, 100])
    if variant == 0:
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
    elif variant == 1:
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
    else:
        # V3: given σ² and target Var(X̄) = σ²/n, find n
        # pick target as sig2 / n so answer is clean integer n
        target = _fr(sig2, n)
        ans = str(n)
        return {
            "problem_text": (
                f"Iid observations with \\(\\sigma^2 = {sig2}\\). "
                f"We want \\(\\text{{Var}}(\\bar{{X}}) = {target}\\). "
                f"Find the required sample size \\(n\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(\\bar{X}) = \\frac{\\sigma^2}{n}\\). Solve for \\(n\\)."},
                {"level": 2, "text": f"\\(n = \\frac{{\\sigma^2}}{{\\text{{Var}}(\\bar{{X}})}} = \\frac{{{sig2}}}{{{target}}}\\)."},
                {"level": 3, "text": f"\\(n = {ans}\\)."},
            ],
        }


# ── stat-estimator-props ──────────────────────────────────────────────────────

def _gen_stat_estimator_props():
    """Bias, MSE, or Var of an estimator."""
    variant = random.choice([0, 1, 2])
    theta = random.randint(2, 8)
    bias = random.choice([-2, -1, 0, 1, 2])
    e_t = theta + bias
    if variant == 0:
        # V1: find bias
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
    elif variant == 1:
        # V2: given Var(T) and Bias, find MSE = Var + Bias²
        var_t = random.choice([1, 4, 9])
        mse = var_t + bias ** 2
        return {
            "problem_text": (
                f"An estimator \\(T\\) has \\(\\text{{Var}}(T) = {var_t}\\) and "
                f"\\(\\text{{Bias}}(T) = {bias}\\). "
                f"Find the MSE: \\(\\text{{MSE}}(T) = \\text{{Var}}(T) + [\\text{{Bias}}(T)]^2\\)."
            ),
            "correct_answer": str(mse), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\text{MSE}(T) = \\text{Var}(T) + [\\text{Bias}(T)]^2\\)."},
                {"level": 2, "text": f"\\(= {var_t} + ({bias})^2 = {var_t} + {bias**2}\\)."},
                {"level": 3, "text": f"\\(\\text{{MSE}}(T) = {mse}\\)."},
            ],
        }
    else:
        # V3: given MSE and Bias, find Var = MSE - Bias²
        var_t = random.choice([1, 4, 9])
        mse = var_t + bias ** 2
        return {
            "problem_text": (
                f"An estimator \\(T\\) has \\(\\text{{MSE}}(T) = {mse}\\) and "
                f"\\(\\text{{Bias}}(T) = {bias}\\). "
                f"Find \\(\\text{{Var}}(T) = \\text{{MSE}}(T) - [\\text{{Bias}}(T)]^2\\)."
            ),
            "correct_answer": str(var_t), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\text{Var}(T) = \\text{MSE}(T) - [\\text{Bias}(T)]^2\\)."},
                {"level": 2, "text": f"\\(= {mse} - ({bias})^2 = {mse} - {bias**2}\\)."},
                {"level": 3, "text": f"\\(\\text{{Var}}(T) = {var_t}\\)."},
            ],
        }


# ── stat-survey-srs ───────────────────────────────────────────────────────────

def _gen_stat_survey_srs():
    """SRS: E[X̄] = μ, Var(X̄) ≈ σ²/n, or SE(X̄) = σ/√n."""
    N = random.randint(50, 200)
    mu = random.randint(10, 50)
    sig2 = random.choice([4, 9, 16, 25])
    n = random.choice([4, 9, 16])
    variant = random.choice([0, 1, 2])
    if variant == 0:
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
    elif variant == 1:
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
    else:
        # V3: find SE(X̄) = σ/√n
        sig = int(sqrt(sig2))
        sqrtn = int(sqrt(n))
        se = _fr(sig, sqrtn)
        return {
            "problem_text": (
                f"An SRS of size \\(n={n}\\) is drawn from a large population with \\(\\sigma^2={sig2}\\). "
                f"Find the standard error \\(\\text{{SE}}(\\bar{{X}}) = \\sigma/\\sqrt{{n}}\\)."
            ),
            "correct_answer": se, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{SE}(\\bar{X}) = \\frac{\\sigma}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(\\sigma = \\sqrt{{{sig2}}} = {sig}\\), \\(\\sqrt{{n}} = {sqrtn}\\)."},
                {"level": 3, "text": f"\\(\\text{{SE}}(\\bar{{X}}) = \\frac{{{sig}}}{{{sqrtn}}} = {se}\\)."},
            ],
        }


# ── stat-mom ──────────────────────────────────────────────────────────────────

def _gen_stat_mom():
    """Method of moments: Uniform(0,θ), Exponential(λ), or Poisson(λ)."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
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
    elif variant == 1:
        # X ~ Exp(λ): E[X] = 1/λ → λ̂ = 1/X̄
        xbar_num = random.randint(2, 6)
        ans = _fr(1, xbar_num)
        return {
            "problem_text": (
                f"\\(X_1, \\ldots, X_n \\sim \\text{{Exponential}}(\\lambda)\\). "
                f"Since \\(E[X] = 1/\\lambda\\), the MOM estimator satisfies \\(1/\\hat{{\\lambda}} = \\bar{{X}}\\). "
                f"If \\(\\bar{{X}} = {xbar_num}\\), find \\(\\hat{{\\lambda}}_{{\\text{{MOM}}}}\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "For Exponential\\((\\lambda)\\), \\(E[X] = 1/\\lambda\\). Set \\(1/\\hat{\\lambda} = \\bar{X}\\)."},
                {"level": 2, "text": f"\\(\\hat{{\\lambda}} = 1/\\bar{{X}} = 1/{xbar_num}\\)."},
                {"level": 3, "text": f"\\(\\hat{{\\lambda}}_{{\\text{{MOM}}}} = {ans}\\)."},
            ],
        }
    else:
        # X ~ Poisson(λ): E[X] = λ → λ̂ = X̄
        xbar_num = random.randint(2, 9)
        return {
            "problem_text": (
                f"\\(X_1, \\ldots, X_n \\sim \\text{{Poisson}}(\\lambda)\\). "
                f"Since \\(E[X] = \\lambda\\), the MOM estimator is \\(\\hat{{\\lambda}}_{{\\text{{MOM}}}} = \\bar{{X}}\\). "
                f"If \\(\\bar{{X}} = {xbar_num}\\), find \\(\\hat{{\\lambda}}_{{\\text{{MOM}}}}\\)."
            ),
            "correct_answer": str(xbar_num), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For Poisson\\((\\lambda)\\), \\(E[X] = \\lambda\\). The MOM estimator is \\(\\hat{\\lambda} = \\bar{X}\\)."},
                {"level": 2, "text": f"\\(\\hat{{\\lambda}} = \\bar{{X}} = {xbar_num}\\)."},
                {"level": 3, "text": f"\\(\\hat{{\\lambda}}_{{\\text{{MOM}}}} = {xbar_num}\\)."},
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
    """Invariance of MLE: g(θ̂) is MLE of g(θ). Three different g functions."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # g(λ) = 1/λ (mean of Exponential)
        lam = random.randint(2, 6)
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
    elif variant == 1:
        # g(μ) = μ² (MLE of squared mean for Normal)
        mu = random.randint(2, 7)
        ans = str(mu ** 2)
        return {
            "problem_text": (
                f"For iid Normal data, the MLE of \\(\\mu\\) is \\(\\hat{{\\mu}} = {mu}\\). "
                f"By the invariance principle, what is the MLE of \\(\\mu^2\\)?"
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "MLE invariance: the MLE of \\(g(\\mu)\\) is \\(g(\\hat{\\mu})\\)."},
                {"level": 2, "text": f"\\(g(\\mu) = \\mu^2\\). Plug in \\(\\hat{{\\mu}} = {mu}\\)."},
                {"level": 3, "text": f"MLE of \\(\\mu^2\\) is \\(({mu})^2 = {mu**2}\\)."},
            ],
        }
    else:
        # g(p) = p(1-p) (variance of Bernoulli, MLE invariance)
        # choose p = a/b so p(1-p) is a clean fraction
        p_num = random.randint(1, 4)
        p_den = random.choice([5, 6])
        q_num = p_den - p_num
        # p(1-p) = p_num*q_num / p_den²
        num = p_num * q_num
        denom = p_den * p_den
        ans = _fr(num, denom)
        return {
            "problem_text": (
                f"For iid Bernoulli data, the MLE of \\(p\\) is \\(\\hat{{p}} = \\frac{{{p_num}}}{{{p_den}}}\\). "
                f"By the invariance principle, what is the MLE of \\(p(1-p)\\)?"
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "MLE invariance: the MLE of \\(g(p)\\) is \\(g(\\hat{p})\\)."},
                {"level": 2, "text": f"\\(g(p) = p(1-p)\\). Plug in \\(\\hat{{p}} = \\frac{{{p_num}}}{{{p_den}}}\\)."},
                {"level": 3, "text": f"\\(\\hat{{p}}(1-\\hat{{p}}) = \\frac{{{p_num}}}{{{p_den}}} \\cdot \\frac{{{q_num}}}{{{p_den}}} = {ans}\\)."},
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
    """Fisher info for Bernoulli, Poisson, or Normal."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # Bernoulli(p): I(p) = 1/(p(1-p))
        den = random.choice([3, 4, 5])
        p_num = random.randint(1, den - 1)
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
    elif variant == 1:
        # Poisson(λ): I(λ) = 1/λ, then total info = n/λ
        lam = random.randint(2, 8)
        n = random.randint(2, 10)
        ans = _fr(n, lam)
        return {
            "problem_text": (
                f"For \\(X \\sim \\text{{Poisson}}(\\lambda)\\), the Fisher information per observation is "
                f"\\(I(\\lambda) = 1/\\lambda\\). "
                f"With \\(n = {n}\\) iid observations and \\(\\lambda = {lam}\\), "
                f"find the total Fisher information \\(n \\cdot I(\\lambda)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Total Fisher information \\(= n \\cdot I(\\lambda) = n/\\lambda\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{n}}}{{{lam}}}\\)."},
                {"level": 3, "text": f"Total info \\(= {ans}\\)."},
            ],
        }
    else:
        # Normal(μ, σ²): I(μ) = 1/σ² (with σ² known)
        sig2 = random.choice([1, 4, 9, 16])
        n = random.randint(2, 10)
        ans = _fr(n, sig2)
        return {
            "problem_text": (
                f"For \\(X \\sim N(\\mu, \\sigma^2={sig2})\\), the Fisher information per observation is "
                f"\\(I(\\mu) = 1/\\sigma^2\\). "
                f"With \\(n = {n}\\) iid observations, find the total Fisher information \\(n \\cdot I(\\mu)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Total Fisher information \\(= n \\cdot I(\\mu) = n/\\sigma^2\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{n}}}{{{sig2}}}\\)."},
                {"level": 3, "text": f"Total info \\(= {ans}\\)."},
            ],
        }


# ── stat-crlb ─────────────────────────────────────────────────────────────────

def _gen_stat_crlb():
    """CRLB = 1/(n·I(θ)): find CRLB, find n·I(θ), or find I(θ) from CRLB."""
    variant = random.choice([0, 1, 2])
    n = random.randint(4, 20)
    i_theta = random.choice([1, 2, 4])
    crlb = _fr(1, n * i_theta)
    if variant == 0:
        # V1: find CRLB
        ans = crlb
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
    elif variant == 1:
        # V2: find total information n·I(θ)
        total = n * i_theta
        return {
            "problem_text": (
                f"The Fisher information per observation is \\(I(\\theta) = {i_theta}\\), "
                f"and there are \\(n = {n}\\) iid observations. "
                f"Find the total Fisher information \\(n \\cdot I(\\theta)\\)."
            ),
            "correct_answer": str(total), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Total Fisher information \\(= n \\cdot I(\\theta)\\)."},
                {"level": 2, "text": f"\\(= {n} \\cdot {i_theta}\\)."},
                {"level": 3, "text": f"Total info \\(= {total}\\)."},
            ],
        }
    else:
        # V3: given CRLB and n, find I(θ)
        # CRLB = 1/(n*i_theta), so I(θ) = 1/(n*CRLB) = i_theta
        return {
            "problem_text": (
                f"An unbiased estimator achieves the Cramér-Rao lower bound of \\({crlb}\\) "
                f"with \\(n = {n}\\) iid observations. "
                f"Find the Fisher information per observation \\(I(\\theta)\\)."
            ),
            "correct_answer": str(i_theta), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "CRLB \\(= \\frac{1}{n \\cdot I(\\theta)}\\). Solve for \\(I(\\theta)\\)."},
                {"level": 2, "text": f"\\(I(\\theta) = \\frac{{1}}{{n \\cdot \\text{{CRLB}}}} = \\frac{{1}}{{{n} \\cdot {crlb}}}\\)."},
                {"level": 3, "text": f"\\(I(\\theta) = {i_theta}\\)."},
            ],
        }

    # fallback (unreachable but satisfies linter)
    return {
        "problem_text": (
            f"The Fisher information per observation is \\(I(\\theta) = {i_theta}\\), "
            f"and there are \\(n = {n}\\) iid observations. "
            f"What is the Cramér-Rao lower bound on the variance of any unbiased estimator?"
        ),
        "correct_answer": crlb, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "CRLB = \\(\\frac{1}{n \\cdot I(\\theta)}\\)."},
            {"level": 2, "text": f"\\(\\frac{{1}}{{{n} \\cdot {i_theta}}} = \\frac{{1}}{{{n*i_theta}}}\\)."},
            {"level": 3, "text": f"CRLB \\(= {crlb}\\)."},
        ],
    }


# ── stat-mvue ─────────────────────────────────────────────────────────────────

def _gen_stat_mvue():
    """MVUE: Var(X̄), CRLB check, or MSE when MVUE is achieved."""
    variant = random.choice([0, 1, 2])
    sig2 = random.choice([1, 4, 9])
    n = random.choice([4, 9, 16, 25])
    if variant == 0:
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
    elif variant == 1:
        # V2: CRLB for Normal(μ, σ²) with n obs = σ²/n; is X̄ efficient?
        # Ask: does Var(X̄) equal the CRLB? Answer is 1 (yes).
        crlb = _fr(sig2, n)
        return {
            "problem_text": (
                f"For \\(X_i \\stackrel{{iid}}{{\\sim}} N(\\mu, \\sigma^2={sig2})\\) with \\(n={n}\\), "
                f"the CRLB for unbiased estimators of \\(\\mu\\) is \\({crlb}\\). "
                f"The variance of \\(\\bar{{X}}\\) is also \\({crlb}\\). "
                f"Does \\(\\bar{{X}}\\) achieve the CRLB? Enter 1 for yes, 0 for no."
            ),
            "correct_answer": "1", "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "An estimator achieves the CRLB if its variance equals the lower bound."},
                {"level": 2, "text": f"\\(\\text{{Var}}(\\bar{{X}}) = {crlb}\\) equals the CRLB \\(= {crlb}\\)."},
                {"level": 3, "text": "Yes, \\(\\bar{X}\\) is efficient. Answer: 1."},
            ],
        }
    else:
        # V3: MSE of an unbiased MVUE equals its variance (bias = 0)
        ans = _fr(sig2, n)
        return {
            "problem_text": (
                f"The MVUE of \\(\\mu\\) for \\(N(\\mu, \\sigma^2={sig2})\\) with \\(n={n}\\) "
                f"is \\(\\bar{{X}}\\), which is unbiased. "
                f"Find the MSE of \\(\\bar{{X}}\\) as an estimator of \\(\\mu\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "For an unbiased estimator, MSE \\(=\\) Var."},
                {"level": 2, "text": f"\\(\\text{{MSE}}(\\bar{{X}}) = \\text{{Var}}(\\bar{{X}}) = \\frac{{{sig2}}}{{{n}}}\\)."},
                {"level": 3, "text": f"MSE \\(= {ans}\\)."},
            ],
        }

    # fallback
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
    """Delta method: Var(g(X̄)) ≈ [g'(μ)]²·σ²/n with g = ax, x², or cx+d."""
    variant = random.choice([0, 1, 2])
    sig2 = random.choice([1, 4, 9])
    n = random.choice([4, 9, 16])
    if variant == 0:
        # g(x) = ax → g'=a; Var = a²σ²/n
        a = random.randint(2, 4)
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
    elif variant == 1:
        # g(x) = cx+d (c constant, d constant) → g'=c; same as variant 0 but ask for g'(μ) first
        c = random.randint(2, 5)
        d = random.randint(1, 4)
        ans = _fr(c**2 * sig2, n)
        return {
            "problem_text": (
                f"By the delta method, if \\(\\text{{Var}}(\\bar{{X}}) = \\frac{{{sig2}}}{{{n}}}\\) "
                f"and \\(g(x) = {c}x + {d}\\), find \\(\\text{{Var}}(g(\\bar{{X}}))\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Delta method: \\(\\text{Var}(g(\\bar{X})) \\approx [g'(\\mu)]^2 \\cdot \\text{Var}(\\bar{X})\\). Constants vanish under differentiation."},
                {"level": 2, "text": f"\\(g'(x) = {c}\\). So \\(\\text{{Var}} = {c}^2 \\cdot \\frac{{{sig2}}}{{{n}}} = \\frac{{{c**2*sig2}}}{{{n}}}\\)."},
                {"level": 3, "text": f"\\(= {ans}\\)."},
            ],
        }
    else:
        # g(x) = ax, but ask for g'(μ) (the derivative at μ) instead of the full variance
        a = random.randint(2, 5)
        mu = random.randint(2, 6)
        # For g(x)=ax², g'(x)=2ax, g'(μ)=2aμ; Var = (2aμ)²·σ²/n
        gprime = 2 * a * mu
        ans = _fr(gprime**2 * sig2, n)
        return {
            "problem_text": (
                f"By the delta method, \\(g(x) = {a}x^2\\) and \\(\\mu = {mu}\\). "
                f"If \\(\\text{{Var}}(\\bar{{X}}) = \\frac{{{sig2}}}{{{n}}}\\), "
                f"find \\(\\text{{Var}}(g(\\bar{{X}})) \\approx [g'(\\mu)]^2 \\cdot \\text{{Var}}(\\bar{{X}})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": f"\\(g'(x) = 2 \\cdot {a} x = {2*a}x\\). At \\(\\mu = {mu}\\): \\(g'({mu}) = {gprime}\\)."},
                {"level": 2, "text": f"\\(\\text{{Var}} \\approx ({gprime})^2 \\cdot \\frac{{{sig2}}}{{{n}}} = {gprime**2} \\cdot \\frac{{{sig2}}}{{{n}}} = \\frac{{{gprime**2*sig2}}}{{{n}}}\\)."},
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
    """Z confidence interval: half-width, SE, or minimum sample size."""
    variant = random.choice([0, 1, 2])
    sig = random.choice([2, 3, 4, 5])
    n = random.choice([4, 9, 16, 25, 100])
    z = random.choice([1, 2])
    label = "68%" if z == 1 else "95%"
    sqrtn = int(sqrt(n))
    if variant == 0:
        # V1: find half-width
        half_width = _fr(z * sig, sqrtn)
        return {
            "problem_text": (
                f"A \\({label}\\) confidence interval uses \\(z^* = {z}\\). "
                f"With \\(\\sigma = {sig}\\) and \\(n = {n}\\), "
                f"find the half-width \\(z^* \\cdot \\sigma/\\sqrt{{n}}\\)."
            ),
            "correct_answer": half_width, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Half-width = \\(z^* \\cdot \\frac{\\sigma}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(= {z} \\cdot \\frac{{{sig}}}{{{sqrtn}}}\\)."},
                {"level": 3, "text": f"\\(= {half_width}\\)."},
            ],
        }
    elif variant == 1:
        # V2: find SE = σ/√n
        se = _fr(sig, sqrtn)
        return {
            "problem_text": (
                f"A z-interval uses \\(\\sigma = {sig}\\) and \\(n = {n}\\). "
                f"Find the standard error \\(\\text{{SE}} = \\sigma/\\sqrt{{n}}\\)."
            ),
            "correct_answer": se, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{SE} = \\frac{\\sigma}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{sig}}}{{\\sqrt{{{n}}}}} = \\frac{{{sig}}}{{{sqrtn}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{SE}} = {se}\\)."},
            ],
        }
    else:
        # V3: find minimum n for desired margin of error E = z*σ/√n
        # choose E to give a clean n
        E = z * sig // sqrtn  # this gives E so that sqrtn = z*sig/E → n = (z*sig/E)²
        if E == 0:
            E = 1
        n_min = (z * sig // E) ** 2
        return {
            "problem_text": (
                f"Using \\(z^* = {z}\\) and \\(\\sigma = {sig}\\), find the minimum sample size "
                f"\\(n = (z^* \\sigma / E)^2\\) to achieve margin of error \\(E = {E}\\)."
            ),
            "correct_answer": str(n_min), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(n = \\left(\\frac{z^* \\sigma}{E}\\right)^2\\)."},
                {"level": 2, "text": f"\\(n = \\left(\\frac{{{z} \\cdot {sig}}}{{{E}}}\\right)^2 = \\left({z*sig//E}\\right)^2\\)."},
                {"level": 3, "text": f"\\(n = {n_min}\\)."},
            ],
        }


# ── stat-ci-t ─────────────────────────────────────────────────────────────────

def _gen_stat_ci_t():
    """t-CI: degrees of freedom, SE = s/√n, or margin of error."""
    variant = random.choice([0, 1, 2])
    n = random.randint(5, 25)
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: find SE = s/√n  (n must be a perfect square for clean answer)
        n2 = random.choice([4, 9, 16, 25])
        s = random.choice([2, 3, 4, 5, 6])
        sqrtn2 = int(sqrt(n2))
        se = _fr(s, sqrtn2)
        return {
            "problem_text": (
                f"A one-sample \\(t\\)-interval uses sample std dev \\(s = {s}\\) and \\(n = {n2}\\). "
                f"Find the standard error \\(\\text{{SE}} = s/\\sqrt{{n}}\\)."
            ),
            "correct_answer": se, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{SE} = \\frac{s}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{s}}}{{\\sqrt{{{n2}}}}} = \\frac{{{s}}}{{{sqrtn2}}}\\)."},
                {"level": 3, "text": f"\\(\\text{{SE}} = {se}\\)."},
            ],
        }
    else:
        # V3: find lower bound of 95% CI: x̄ - t* × SE (use t*=2 as approx)
        n3 = random.choice([4, 9, 16, 25])
        s = random.choice([2, 3, 4])
        sqrtn3 = int(sqrt(n3))
        xbar = random.randint(10, 30)
        t_star = 2
        se_val = s // sqrtn3 if sqrtn3 <= s else 1
        # ensure clean subtraction: pick s divisible by sqrtn3
        s_clean = sqrtn3 * random.randint(1, 3)
        se_clean = s_clean // sqrtn3
        lb = xbar - t_star * se_clean
        return {
            "problem_text": (
                f"A one-sample \\(t\\)-interval: \\(\\bar{{x}} = {xbar}\\), \\(s = {s_clean}\\), "
                f"\\(n = {n3}\\), \\(t^* = {t_star}\\). "
                f"Find the lower bound \\(\\bar{{x}} - t^* \\cdot s/\\sqrt{{n}}\\)."
            ),
            "correct_answer": str(lb), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Lower bound \\(= \\bar{x} - t^* \\cdot \\frac{s}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(= {xbar} - {t_star} \\cdot \\frac{{{s_clean}}}{{{sqrtn3}}} = {xbar} - {t_star} \\cdot {se_clean} = {xbar} - {t_star*se_clean}\\)."},
                {"level": 3, "text": f"Lower bound \\(= {lb}\\)."},
            ],
        }


# ── stat-ci-proportion ────────────────────────────────────────────────────────

def _gen_stat_ci_proportion():
    """CI for proportion: Var(p̂), margin of error, or lower bound."""
    variant = random.choice([0, 1, 2])
    n = random.choice([100, 400, 900])
    p_num = random.randint(1, 9)
    p_den = 10
    # SE² = p(1-p)/n
    se2_num = p_num * (p_den - p_num)
    se2_den = p_den**2 * n
    se2 = _fr(se2_num, se2_den)
    if variant == 0:
        # V1: find Var(p̂)
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
    elif variant == 1:
        # V2: find margin of error E = z* × SE for 95% CI (z*=2)
        # SE = sqrt(p(1-p)/n). Use n=100, p=1/2 so SE=1/20, E=2/20=1/10
        # pick n=100, p_num=5 so p=1/2, SE=1/20, E=2/20=1/10
        n2 = 100
        p_n2 = 5
        p_d2 = 10
        # SE² = 5*5/(100*100) = 25/10000 = 1/400; SE = 1/20
        # E = 2 * 1/20 = 1/10
        z_star = 2
        # represent E as fraction: numerator = z_star * sqrt(p(1-p)/n) numerator
        # For clean answer use p=5/10, n=100: SE=1/20, E=1/10
        se_num = p_n2 * (p_d2 - p_n2)  # 25
        se_den = p_d2 * p_d2 * n2       # 10000
        # SE = sqrt(25/10000) = 5/100 = 1/20
        e_ans = _fr(z_star * 1, 20)  # 2/20 = 1/10
        return {
            "problem_text": (
                f"In a sample of \\(n={n2}\\), \\(\\hat{{p}} = 0.5\\). "
                f"Using \\(z^* = {z_star}\\), find the margin of error "
                f"\\(E = z^* \\cdot \\sqrt{{\\hat{{p}}(1-\\hat{{p}})/n}}\\)."
            ),
            "correct_answer": e_ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(E = z^* \\cdot \\sqrt{\\hat{p}(1-\\hat{p})/n}\\)."},
                {"level": 2, "text": f"\\(\\sqrt{{0.5 \\cdot 0.5 / {n2}}} = \\sqrt{{1/400}} = 1/20\\). Then \\(E = {z_star} \\cdot 1/20\\)."},
                {"level": 3, "text": f"\\(E = {e_ans}\\)."},
            ],
        }
    else:
        # V3: find sample size n for margin of error ≤ E = 1/10 with p̂ = 0.5, z* = 2
        # n = (z*/E)² × p(1-p) = (2/(1/10))² × 1/4 = 400 × 1/4 = 100
        n_ans = 100
        return {
            "problem_text": (
                f"Find the minimum sample size \\(n\\) for a 95% CI (\\(z^*=2\\)) "
                f"on a proportion with \\(\\hat{{p}} = 0.5\\) and margin of error \\(E = 0.1\\). "
                f"Use \\(n = (z^*/E)^2 \\cdot \\hat{{p}}(1-\\hat{{p}})\\)."
            ),
            "correct_answer": str(n_ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(n = \\left(\\frac{z^*}{E}\\right)^2 \\hat{p}(1-\\hat{p})\\)."},
                {"level": 2, "text": "\\(n = (2/0.1)^2 \\cdot 0.5 \\cdot 0.5 = 400 \\cdot 0.25\\)."},
                {"level": 3, "text": f"\\(n = {n_ans}\\)."},
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
    """Power = 1 - β, Type I error = α, or find β given power."""
    variant = random.choice([0, 1, 2])
    alpha = random.choice([5, 10])
    beta = random.choice([10, 20, 30])
    if variant == 0:
        # V1: find power = 1 - β
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
    elif variant == 1:
        # V2: Type I error = α
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
    else:
        # V3: find β given power
        power = 100 - beta
        ans = str(beta)
        return {
            "problem_text": (
                f"A test has power \\(= {power}\\%\\). "
                f"Find the Type II error rate \\(\\beta\\) (in %)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "\\(\\beta = 1 - \\text{Power}\\)."},
                {"level": 2, "text": f"\\(\\beta = 100\\% - {power}\\%\\)."},
                {"level": 3, "text": f"\\(\\beta = {ans}\\%\\)."},
            ],
        }


# ── stat-pvalue ───────────────────────────────────────────────────────────────

def _gen_stat_pvalue():
    """Interpret p-value, compute two-sided from one-sided, or find α boundary."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: reject or not
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
    elif variant == 1:
        # V2: two-sided p = 2 × one-sided p
        # pick a one-sided p that gives a clean two-sided value
        one_sided_pct = random.choice([2, 3, 4, 5])  # in percent
        two_sided_pct = 2 * one_sided_pct
        one_sided = one_sided_pct / 100
        two_sided = two_sided_pct / 100
        return {
            "problem_text": (
                f"A one-sided test yields \\(p_{{\\text{{one-sided}}}} = {one_sided}\\). "
                f"Find the two-sided \\(p\\)-value."
            ),
            "correct_answer": str(two_sided), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Two-sided \\(p\\)-value \\(= 2 \\times\\) one-sided \\(p\\)-value."},
                {"level": 2, "text": f"\\(2 \\times {one_sided}\\)."},
                {"level": 3, "text": f"Two-sided \\(p = {two_sided}\\)."},
            ],
        }
    else:
        # V3: given z statistic, find one-sided p-value (use z-table values)
        # Use simple z values with known tail probabilities
        z_table = {1: "0.16", 2: "0.02", 3: "0.001"}
        z_val = random.choice([1, 2, 3])
        p_ans = z_table[z_val]
        return {
            "problem_text": (
                f"For a one-sided (upper-tail) z-test with \\(z = {z_val}\\), "
                f"the approximate one-sided \\(p\\)-value is \\(P(Z > {z_val})\\). "
                f"Using the standard normal table, select the closest value: "
                f"enter 0.16 if \\(z=1\\), 0.02 if \\(z=2\\), or 0.001 if \\(z=3\\)."
            ),
            "correct_answer": p_ans, "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Use standard normal tail probabilities: \\(P(Z>1)\\approx0.16\\), \\(P(Z>2)\\approx0.02\\), \\(P(Z>3)\\approx0.001\\)."},
                {"level": 2, "text": f"Look up \\(P(Z > {z_val})\\)."},
                {"level": 3, "text": f"\\(p \\approx {p_ans}\\)."},
            ],
        }


# ── stat-neyman-pearson ───────────────────────────────────────────────────────

def _gen_stat_neyman_pearson():
    """NP lemma: reject decision, likelihood ratio, or identify direction."""
    variant = random.choice([0, 1, 2])
    theta0 = random.randint(1, 3)
    theta1 = random.randint(theta0 + 1, theta0 + 3)
    if variant == 0:
        # V1: reject decision (original)
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
    elif variant == 1:
        # V2: compute likelihood ratio for Bernoulli
        # p0, p1, n, x fixed; LR = (p1/p0)^x * ((1-p1)/(1-p0))^(n-x)
        # keep it simple: n=4, x=3, p0=1/2, p1=3/4
        # LR = (3/4 / 1/2)^3 * (1/4 / 1/2)^1 = (3/2)^3 * (1/2)^1 = 27/8 * 1/2 = 27/16
        n_obs = random.choice([2, 3])
        x_obs = n_obs  # all successes for simplicity
        # LR(x) = (p1/p0)^x * ((1-p1)/(1-p0))^(n-x)
        # p0=1/2, p1=3/4, x=n_obs, n-x=0 → LR = (3/2)^n_obs
        p0_num, p0_den = 1, 2
        p1_num, p1_den = 3, 4
        # LR = (p1/p0)^x = (3/2)^n_obs
        lr_num = 3 ** n_obs
        lr_den = 2 ** n_obs
        ans = _fr(lr_num, lr_den)
        return {
            "problem_text": (
                f"Testing \\(H_0: p = 1/2\\) vs \\(H_1: p = 3/4\\) with \\(n={n_obs}\\) iid Bernoulli trials. "
                f"All \\(x = {n_obs}\\) trials are successes. "
                f"Compute the likelihood ratio \\(\\Lambda = L(p_1)/L(p_0)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(L(p) = p^x (1-p)^{n-x}\\). With all successes: \\(L(p) = p^n\\)."},
                {"level": 2, "text": f"\\(\\Lambda = (3/4)^{{{n_obs}}} / (1/2)^{{{n_obs}}} = (3/2)^{{{n_obs}}}\\)."},
                {"level": 3, "text": f"\\(\\Lambda = {ans}\\)."},
            ],
        }
    else:
        # V3: identify rejection direction for Normal test
        # H0: μ=μ0 vs H1: μ=μ1 > μ0 → reject for large X̄
        mu0 = random.randint(10, 20)
        mu1 = mu0 + random.randint(2, 5)
        xbar = mu1 + random.randint(0, 2)
        c = (mu0 + mu1) // 2
        reject = 1 if xbar > c else 0
        return {
            "problem_text": (
                f"Testing \\(H_0: \\mu = {mu0}\\) vs \\(H_1: \\mu = {mu1}\\) for Normal data. "
                f"The NP test rejects \\(H_0\\) for large \\(\\bar{{X}}\\). "
                f"With \\(\\bar{{X}} = {xbar}\\) and critical value \\(c = {c}\\), "
                f"do we reject \\(H_0\\)? Enter 1 for reject, 0 for fail to reject."
            ),
            "correct_answer": str(reject), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Reject \\(H_0\\) when \\(\\bar{X} > c\\)."},
                {"level": 2, "text": f"Compare \\(\\bar{{X}} = {xbar}\\) with \\(c = {c}\\)."},
                {"level": 3, "text": f"\\({xbar}\\) {'>' if reject else 'not >'} \\({c}\\) → {'reject' if reject else 'fail to reject'}. Answer: {reject}."},
            ],
        }


# ── stat-ump ──────────────────────────────────────────────────────────────────

def _gen_stat_ump():
    """UMP test: reject decision, power at alternative, or size of test."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: reject decision based on T vs c
        t_val = random.choice([16, 18, 20, 22])
        c_val = random.choice([14, 15, 17, 19])
        reject = 1 if t_val > c_val else 0
        return {
            "problem_text": (
                f"For a one-parameter exponential family, the UMP test rejects \\(H_0\\) "
                f"when the sufficient statistic \\(T > c\\). "
                f"If \\(T = {t_val}\\) and \\(c = {c_val}\\), "
                f"do we reject \\(H_0\\)? Enter 1 for reject, 0 for fail to reject."
            ),
            "correct_answer": str(reject), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The UMP test rejects \\(H_0\\) when \\(T > c\\)."},
                {"level": 2, "text": f"Compare \\(T = {t_val}\\) with \\(c = {c_val}\\)."},
                {"level": 3, "text": f"\\({t_val}\\) {'>' if reject else 'not >'} \\({c_val}\\) → {'reject' if reject else 'fail to reject'}. Answer: {reject}."},
            ],
        }
    elif variant == 1:
        # V2: power of the UMP test = P(reject | H1) = P(T > c | H1)
        # Use Binomial: T = sum of n Bernoulli(p), reject if T > c
        # Simple: n=4, p1=3/4, c=3; P(T>3)=P(T=4)=(3/4)^4=81/256
        n_obs = 4
        p1_num, p1_den = 3, 4
        c_val = 3
        # P(T=4) = (3/4)^4 = 81/256
        power_num = p1_num ** n_obs
        power_den = p1_den ** n_obs
        ans = _fr(power_num, power_den)
        return {
            "problem_text": (
                f"A UMP test for \\(H_0: p \\leq 1/2\\) vs \\(H_1: p > 1/2\\) "
                f"rejects when \\(T = \\sum_{{i=1}}^{{{n_obs}}} X_i > {c_val}\\) (i.e., \\(T = {n_obs}\\)). "
                f"Find the power at \\(p_1 = {p1_num}/{p1_den}\\): "
                f"\\(P(T = {n_obs} \\mid p = {p1_num}/{p1_den})\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": f"\\(P(T = {n_obs}) = p^{{{n_obs}}}\\) since all trials must succeed."},
                {"level": 2, "text": f"\\(= ({p1_num}/{p1_den})^{{{n_obs}}} = {p1_num**n_obs}/{p1_den**n_obs}\\)."},
                {"level": 3, "text": f"Power \\(= {ans}\\)."},
            ],
        }
    else:
        # V3: size of the test = P(reject | H0) = P(T > c | H0)
        # Same setup: T~Bin(4,1/2), reject if T>3; P(T=4)=(1/2)^4=1/16
        n_obs = 4
        p0_num, p0_den = 1, 2
        c_val = 3
        size_num = p0_num ** n_obs
        size_den = p0_den ** n_obs
        ans = _fr(size_num, size_den)
        return {
            "problem_text": (
                f"A UMP test rejects \\(H_0: p = 1/2\\) when \\(T > {c_val}\\) "
                f"(i.e., \\(T = {n_obs}\\) out of \\(n = {n_obs}\\) Bernoulli trials). "
                f"Find the size of the test \\(P(T = {n_obs} \\mid p = 1/2)\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Size \\(= P(\\text{reject} \\mid H_0)\\)."},
                {"level": 2, "text": f"\\(P(T = {n_obs} \\mid p = 1/2) = (1/2)^{{{n_obs}}}\\)."},
                {"level": 3, "text": f"Size \\(= {ans}\\)."},
            ],
        }


# ── stat-glrt ─────────────────────────────────────────────────────────────────

def _gen_stat_glrt():
    """GLRT statistic: df, reject decision, or compute -2 log Λ."""
    variant = random.choice([0, 1, 2])
    dim_full = random.randint(2, 4)
    dim_null = random.randint(1, dim_full - 1)
    df = dim_full - dim_null
    if variant == 0:
        # V1: find df
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
    elif variant == 1:
        # V2: compute -2 log Λ given log-likelihood values
        ll_null = random.randint(-30, -10)
        ll_full = ll_null + random.randint(2, 6)  # full >= null
        glrt_stat = 2 * (ll_full - ll_null)
        return {
            "problem_text": (
                f"The log-likelihood under \\(H_0\\) is \\(\\hat{{\\ell}}_0 = {ll_null}\\) "
                f"and under the full model is \\(\\hat{{\\ell}} = {ll_full}\\). "
                f"Compute the GLRT statistic \\(-2(\\hat{{\\ell}}_0 - \\hat{{\\ell}})\\)."
            ),
            "correct_answer": str(glrt_stat), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "GLRT statistic \\(= -2(\\hat{\\ell}_0 - \\hat{\\ell}) = 2(\\hat{\\ell} - \\hat{\\ell}_0)\\)."},
                {"level": 2, "text": f"\\(= 2({ll_full} - ({ll_null})) = 2 \\cdot {ll_full - ll_null}\\)."},
                {"level": 3, "text": f"GLRT \\(= {glrt_stat}\\)."},
            ],
        }
    else:
        # V3: reject at α=0.05 given -2 log Λ and df (χ²(df) critical value)
        # Use df=1: χ²(1,0.05)=3.84 ≈ 4; df=2: χ²(2,0.05)=5.99≈6
        df_v3 = random.choice([1, 2])
        crit = 4 if df_v3 == 1 else 6
        stat_val = random.choice([crit - 1, crit + 1])
        reject = 1 if stat_val >= crit else 0
        return {
            "problem_text": (
                f"The GLRT statistic is \\(-2\\log\\Lambda = {stat_val}\\) with \\(df = {df_v3}\\). "
                f"The critical value (\\(\\alpha=0.05\\)) is approximately \\({crit}\\). "
                f"Do we reject \\(H_0\\)? Enter 1 for reject, 0 for fail to reject."
            ),
            "correct_answer": str(reject), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Reject \\(H_0\\) if \\(-2\\log\\Lambda \\geq\\) critical value."},
                {"level": 2, "text": f"Compare {stat_val} with critical value {crit}."},
                {"level": 3, "text": f"{'Reject' if reject else 'Fail to reject'} \\(H_0\\). Answer: {reject}."},
            ],
        }


# ── stat-power-sample-size ────────────────────────────────────────────────────

def _gen_stat_power_sample_size():
    """Sample size planning: find n, find E given n, or find σ given n and E."""
    variant = random.choice([0, 1, 2])
    sig = random.choice([2, 3, 4, 5])
    z = 2  # ≈ 1.96 for 95%
    E = random.choice([1, 2])
    n = (z * sig // E) ** 2
    if variant == 0:
        # V1: find n
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
    elif variant == 1:
        # V2: find E given n and σ (E = z*σ/√n)
        n2 = random.choice([4, 9, 16, 25])
        sig2 = random.choice([2, 3, 4, 5])
        sqrtn2 = int(sqrt(n2))
        E2 = _fr(z * sig2, sqrtn2)
        return {
            "problem_text": (
                f"For a 95% CI (\\(z^*=2\\)), \\(\\sigma={sig2}\\), \\(n={n2}\\). "
                f"Find the margin of error \\(E = z^* \\sigma / \\sqrt{{n}}\\)."
            ),
            "correct_answer": E2, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(E = z^* \\cdot \\frac{\\sigma}{\\sqrt{n}}\\)."},
                {"level": 2, "text": f"\\(= 2 \\cdot \\frac{{{sig2}}}{{{sqrtn2}}}\\)."},
                {"level": 3, "text": f"\\(E = {E2}\\)."},
            ],
        }
    else:
        # V3: find σ given n and E (σ = E*√n/z*)
        n3 = random.choice([4, 9, 16, 25])
        sqrtn3 = int(sqrt(n3))
        # pick E so that E*sqrtn3/z is integer: E = z * k / sqrtn3 for some k
        k = random.randint(1, 3)
        E3 = k  # E3 = k → σ = k*sqrtn3/z; for clean answer need z|k*sqrtn3
        # use z=2: sig = k*sqrtn3//2 if even
        sig3 = k * sqrtn3 // z
        if sig3 < 1:
            sig3 = sqrtn3
            E3 = z * sig3 // sqrtn3
        return {
            "problem_text": (
                f"For a 95% CI (\\(z^*=2\\)), the margin of error is \\(E={E3}\\) "
                f"with \\(n={n3}\\). Find \\(\\sigma\\) from \\(\\sigma = E \\cdot \\sqrt{{n}} / z^*\\)."
            ),
            "correct_answer": str(sig3), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Rearrange \\(E = z^* \\sigma / \\sqrt{n}\\) to get \\(\\sigma = E \\sqrt{n} / z^*\\)."},
                {"level": 2, "text": f"\\(\\sigma = {E3} \\cdot {sqrtn3} / 2 = {E3*sqrtn3}/2\\)."},
                {"level": 3, "text": f"\\(\\sigma = {sig3}\\)."},
            ],
        }


# ── stat-ztest-one ────────────────────────────────────────────────────────────

def _gen_stat_ztest_one():
    """One-sample z-test: compute z, find SE, or find numerator (x̄ - μ0)."""
    variant = random.choice([0, 1, 2])
    mu0 = random.randint(50, 80)
    sig = random.choice([2, 4, 5, 10])
    n = random.choice([4, 16, 25, 100])
    sqrtn = int(sqrt(n))
    diff = random.choice([-2, -1, 1, 2]) * sig // sqrtn
    xbar = mu0 + diff * sqrtn
    z = (xbar - mu0) * sqrtn // sig
    se = sig // sqrtn
    if variant == 0:
        # V1: compute z statistic
        return {
            "problem_text": (
                f"One-sample z-test: \\(\\mu_0 = {mu0}\\), \\(\\sigma = {sig}\\), "
                f"\\(n = {n}\\), \\(\\bar{{x}} = {xbar}\\). "
                f"Compute \\(z = \\frac{{\\bar{{x}} - \\mu_0}}{{\\sigma/\\sqrt{{n}}}}\\)."
            ),
            "correct_answer": str(z), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(z = \\frac{\\bar{x} - \\mu_0}{\\sigma / \\sqrt{n}}\\)."},
                {"level": 2, "text": f"Numerator: \\({xbar} - {mu0} = {xbar-mu0}\\). Denominator: \\({sig}/\\sqrt{{{n}}} = {se}\\)."},
                {"level": 3, "text": f"\\(z = \\frac{{{xbar-mu0}}}{{{se}}} = {z}\\)."},
            ],
        }
    elif variant == 1:
        # V2: find SE = σ/√n
        return {
            "problem_text": (
                f"One-sample z-test with \\(\\sigma = {sig}\\) and \\(n = {n}\\). "
                f"Find the standard error \\(\\text{{SE}} = \\sigma/\\sqrt{{n}}\\)."
            ),
            "correct_answer": str(se), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{SE} = \\sigma / \\sqrt{n}\\)."},
                {"level": 2, "text": f"\\(= {sig} / \\sqrt{{{n}}} = {sig} / {sqrtn}\\)."},
                {"level": 3, "text": f"\\(\\text{{SE}} = {se}\\)."},
            ],
        }
    else:
        # V3: find numerator x̄ - μ0
        num = xbar - mu0
        return {
            "problem_text": (
                f"One-sample z-test: \\(\\mu_0 = {mu0}\\) and \\(\\bar{{x}} = {xbar}\\). "
                f"Find the numerator \\(\\bar{{x}} - \\mu_0\\)."
            ),
            "correct_answer": str(num), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The numerator is \\(\\bar{x} - \\mu_0\\)."},
                {"level": 2, "text": f"\\({xbar} - {mu0}\\)."},
                {"level": 3, "text": f"Numerator \\(= {num}\\)."},
            ],
        }


# ── stat-ttest-one ────────────────────────────────────────────────────────────

def _gen_stat_ttest_one():
    """One-sample t-test: degrees of freedom, t-statistic, or SE."""
    variant = random.choice([0, 1, 2])
    n = random.randint(5, 30)
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: compute t-statistic (n must be perfect square for clean SE)
        n2 = random.choice([4, 9, 16, 25])
        sqrtn2 = int(sqrt(n2))
        s = random.choice([2, 3, 4]) * sqrtn2  # ensure s/√n is integer
        se = s // sqrtn2
        mu0 = random.randint(10, 30)
        # pick xbar so t is a small integer
        t_val = random.choice([-3, -2, -1, 1, 2, 3])
        xbar = mu0 + t_val * se
        return {
            "problem_text": (
                f"One-sample \\(t\\)-test: \\(\\mu_0 = {mu0}\\), \\(s = {s}\\), "
                f"\\(n = {n2}\\), \\(\\bar{{x}} = {xbar}\\). "
                f"Compute \\(t = \\frac{{\\bar{{x}} - \\mu_0}}{{s/\\sqrt{{n}}}}\\)."
            ),
            "correct_answer": str(t_val), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(t = \\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}\\)."},
                {"level": 2, "text": f"Numerator: \\({xbar} - {mu0} = {xbar - mu0}\\). \\(s/\\sqrt{{n}} = {s}/{sqrtn2} = {se}\\)."},
                {"level": 3, "text": f"\\(t = {xbar - mu0}/{se} = {t_val}\\)."},
            ],
        }
    else:
        # V3: find SE = s/√n
        n3 = random.choice([4, 9, 16, 25])
        sqrtn3 = int(sqrt(n3))
        s3 = random.choice([2, 3, 4, 5]) * sqrtn3
        se3 = s3 // sqrtn3
        return {
            "problem_text": (
                f"A one-sample \\(t\\)-test uses \\(s = {s3}\\) and \\(n = {n3}\\). "
                f"Find the standard error \\(\\text{{SE}} = s/\\sqrt{{n}}\\)."
            ),
            "correct_answer": str(se3), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\text{SE} = s / \\sqrt{n}\\)."},
                {"level": 2, "text": f"\\(= {s3} / \\sqrt{{{n3}}} = {s3} / {sqrtn3}\\)."},
                {"level": 3, "text": f"\\(\\text{{SE}} = {se3}\\)."},
            ],
        }

    # fallback
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
    """Two-sample t-test: df, t-statistic numerator, or total N."""
    variant = random.choice([0, 1, 2])
    n1 = random.randint(5, 20)
    n2 = random.randint(5, 20)
    df = n1 + n2 - 2
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: t-statistic numerator = x̄1 - x̄2
        xbar1 = random.randint(20, 40)
        xbar2 = random.randint(10, xbar1 - 1)
        num = xbar1 - xbar2
        return {
            "problem_text": (
                f"A two-sample \\(t\\)-test has \\(\\bar{{x}}_1 = {xbar1}\\) and \\(\\bar{{x}}_2 = {xbar2}\\). "
                f"Find the numerator \\(\\bar{{x}}_1 - \\bar{{x}}_2\\) of the \\(t\\)-statistic."
            ),
            "correct_answer": str(num), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The numerator of the two-sample \\(t\\)-statistic is \\(\\bar{x}_1 - \\bar{x}_2\\)."},
                {"level": 2, "text": f"\\({xbar1} - {xbar2}\\)."},
                {"level": 3, "text": f"Numerator \\(= {num}\\)."},
            ],
        }
    else:
        # V3: total sample size N = n1 + n2
        N = n1 + n2
        return {
            "problem_text": (
                f"A two-sample \\(t\\)-test uses \\(n_1 = {n1}\\) and \\(n_2 = {n2}\\). "
                f"Find the total sample size \\(N = n_1 + n_2\\)."
            ),
            "correct_answer": str(N), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "\\(N = n_1 + n_2\\)."},
                {"level": 2, "text": f"\\({n1} + {n2}\\)."},
                {"level": 3, "text": f"\\(N = {N}\\)."},
            ],
        }


# ── stat-pooled-variance ──────────────────────────────────────────────────────

def _gen_stat_pooled_variance():
    """Pooled variance: Sp², numerator, or denominator."""
    variant = random.choice([0, 1, 2])
    n1 = random.randint(5, 12)
    n2 = random.randint(5, 12)
    s1 = random.randint(1, 4)
    s2 = random.randint(1, 4)
    num = (n1 - 1) * s1**2 + (n2 - 1) * s2**2
    denom = n1 + n2 - 2
    ans = _fr(num, denom)
    if variant == 0:
        # V1: find Sp²
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
    elif variant == 1:
        # V2: find numerator only
        return {
            "problem_text": (
                f"For pooled variance with \\(n_1={n1}\\), \\(s_1^2={s1**2}\\), "
                f"\\(n_2={n2}\\), \\(s_2^2={s2**2}\\), "
                f"find the numerator \\((n_1-1)s_1^2 + (n_2-1)s_2^2\\)."
            ),
            "correct_answer": str(num), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Numerator \\(= (n_1-1)s_1^2 + (n_2-1)s_2^2\\)."},
                {"level": 2, "text": f"\\(= ({n1}-1)\\cdot{s1**2} + ({n2}-1)\\cdot{s2**2} = {(n1-1)*s1**2} + {(n2-1)*s2**2}\\)."},
                {"level": 3, "text": f"Numerator \\(= {num}\\)."},
            ],
        }
    else:
        # V3: find denominator = n1 + n2 - 2
        return {
            "problem_text": (
                f"For a pooled two-sample t-test with \\(n_1={n1}\\) and \\(n_2={n2}\\), "
                f"find the denominator \\(n_1 + n_2 - 2\\) of the pooled variance formula."
            ),
            "correct_answer": str(denom), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Denominator \\(= n_1 + n_2 - 2\\)."},
                {"level": 2, "text": f"\\({n1} + {n2} - 2\\)."},
                {"level": 3, "text": f"Denominator \\(= {denom}\\)."},
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
    """Permutation test: number of permutations, p-value, or test statistic."""
    from math import comb
    variant = random.choice([0, 1, 2])
    n1 = random.randint(2, 4)
    n2 = random.randint(2, 4)
    total_perms = comb(n1 + n2, n1)
    if variant == 0:
        # V1: count permutations
        return {
            "problem_text": (
                f"A permutation test has \\(n_1 = {n1}\\) and \\(n_2 = {n2}\\) observations. "
                f"How many ways can the \\(n_1 + n_2\\) observations be split into groups of size "
                f"\\(n_1\\) and \\(n_2\\)?"
            ),
            "correct_answer": str(total_perms), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Choose \\(n_1\\) items from \\(n_1+n_2\\): \\(\\binom{n_1+n_2}{n_1}\\)."},
                {"level": 2, "text": f"\\(\\binom{{{n1+n2}}}{{{n1}}}\\)."},
                {"level": 3, "text": f"\\(= {total_perms}\\)."},
            ],
        }
    elif variant == 1:
        # V2: p-value = (number of permutations as or more extreme) / total
        # Use n1=n2=2, total=6; say 1 permutation is as extreme or more
        n1v2, n2v2 = 2, 2
        tot = comb(n1v2 + n2v2, n1v2)  # = 6
        extreme = random.randint(1, 3)
        ans = _fr(extreme, tot)
        return {
            "problem_text": (
                f"A permutation test has \\(n_1 = {n1v2}\\) and \\(n_2 = {n2v2}\\) observations "
                f"(\\({tot}\\) total permutations). "
                f"Exactly \\({extreme}\\) permutation(s) produce a test statistic as extreme or more extreme than observed. "
                f"Find the permutation \\(p\\)-value."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(p\\text{-value} = \\frac{\\text{# extreme permutations}}{\\text{total permutations}}\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{extreme}}}{{{tot}}}\\)."},
                {"level": 3, "text": f"\\(p = {ans}\\)."},
            ],
        }
    else:
        # V3: difference in group means as test statistic
        # Group1: [a, b], Group2: [c, d]; test stat = |mean1 - mean2|
        g1 = sorted(random.sample(range(1, 10), 2))
        g2 = sorted(random.sample(range(1, 10), 2))
        while set(g1) & set(g2):
            g2 = sorted(random.sample(range(1, 10), 2))
        mean1_num = sum(g1)
        mean2_num = sum(g2)
        diff_num = abs(mean1_num - mean2_num)
        ans = _fr(diff_num, 2)
        return {
            "problem_text": (
                f"Group 1: \\({', '.join(str(v) for v in g1)}\\). "
                f"Group 2: \\({', '.join(str(v) for v in g2)}\\). "
                f"Find the test statistic \\(|\\bar{{x}}_1 - \\bar{{x}}_2|\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Compute each group mean, then take the absolute difference."},
                {"level": 2, "text": f"\\(\\bar{{x}}_1 = {mean1_num}/2\\), \\(\\bar{{x}}_2 = {mean2_num}/2\\). Difference \\(= {diff_num}/2\\)."},
                {"level": 3, "text": f"\\(|\\bar{{x}}_1 - \\bar{{x}}_2| = {ans}\\)."},
            ],
        }


# ── stat-chi-gof ──────────────────────────────────────────────────────────────

def _gen_stat_chi_gof():
    """Chi-squared GOF: degrees of freedom, expected count, or chi-sq contribution."""
    variant = random.choice([0, 1, 2])
    k = random.randint(3, 6)
    p_est = random.randint(0, 1)
    df = k - 1 - p_est
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: expected count = n × p_i for equal probabilities
        n = random.choice([60, 80, 100, 120])
        k2 = random.choice([3, 4, 5])
        exp_count = n // k2
        return {
            "problem_text": (
                f"A chi-squared GOF test with \\(n = {n}\\) observations and \\(k = {k2}\\) equally likely categories. "
                f"Find the expected count for each category."
            ),
            "correct_answer": str(exp_count), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Expected count \\(= n \\times p_i = n / k\\) when all categories are equally likely."},
                {"level": 2, "text": f"\\(= {n} / {k2}\\)."},
                {"level": 3, "text": f"Expected count \\(= {exp_count}\\)."},
            ],
        }
    else:
        # V3: single chi-squared contribution (O - E)²/E
        O = random.randint(5, 20)
        E = random.choice([5, 10, 15, 20])
        num = (O - E) ** 2
        ans = _fr(num, E)
        return {
            "problem_text": (
                f"In a chi-squared GOF test, one cell has observed count \\(O = {O}\\) "
                f"and expected count \\(E = {E}\\). "
                f"Find the contribution \\((O - E)^2 / E\\) to the chi-squared statistic."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Contribution \\(= (O - E)^2 / E\\)."},
                {"level": 2, "text": f"\\(= ({O} - {E})^2 / {E} = {(O-E)**2} / {E}\\)."},
                {"level": 3, "text": f"\\(= {ans}\\)."},
            ],
        }


# ── stat-chi-indep ────────────────────────────────────────────────────────────

def _gen_stat_chi_indep():
    """Chi-squared independence test: df, expected count, or chi-sq contribution."""
    variant = random.choice([0, 1, 2])
    r = random.randint(2, 4)
    c = random.randint(2, 4)
    df = (r - 1) * (c - 1)
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: expected count E_ij = row_i * col_j / n
        # use clean values: row_total, col_total, n
        n = random.choice([100, 200])
        row_pct = random.choice([40, 50, 60])
        col_pct = random.choice([50, 60])
        row_t = n * row_pct // 100
        col_t = n * col_pct // 100
        exp_num = row_t * col_t
        exp = _fr(exp_num, n)
        return {
            "problem_text": (
                f"In a \\({r} \\times {c}\\) contingency table with \\(n = {n}\\) total observations, "
                f"a row total is \\({row_t}\\) and a column total is \\({col_t}\\). "
                f"Find the expected count \\(E = \\frac{{\\text{{row total}} \\times \\text{{col total}}}}{{n}}\\)."
            ),
            "correct_answer": exp, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(E_{ij} = \\frac{R_i \\cdot C_j}{n}\\)."},
                {"level": 2, "text": f"\\(E = \\frac{{{row_t} \\cdot {col_t}}}{{{n}}} = \\frac{{{exp_num}}}{{{n}}}\\)."},
                {"level": 3, "text": f"\\(E = {exp}\\)."},
            ],
        }
    else:
        # V3: chi-squared contribution (O-E)²/E
        O = random.randint(5, 25)
        E = random.choice([10, 15, 20, 25])
        num = (O - E) ** 2
        ans = _fr(num, E)
        return {
            "problem_text": (
                f"In a chi-squared independence test, one cell has observed \\(O = {O}\\) "
                f"and expected \\(E = {E}\\). "
                f"Compute the contribution \\((O - E)^2 / E\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\((O - E)^2 / E\\)."},
                {"level": 2, "text": f"\\(({O} - {E})^2 / {E} = {(O-E)**2} / {E}\\)."},
                {"level": 3, "text": f"\\(= {ans}\\)."},
            ],
        }


# ── stat-chi-homog ────────────────────────────────────────────────────────────

def _gen_stat_chi_homog():
    """Chi-squared homogeneity: df, expected count, or total cells."""
    variant = random.choice([0, 1, 2])
    r = random.randint(2, 4)
    c = random.randint(2, 4)
    df = (r - 1) * (c - 1)
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: expected count in a cell
        n = random.choice([60, 100, 120, 200])
        r2 = random.choice([2, 3])
        c2 = random.choice([2, 3])
        row_t = n // r2
        col_t = n // c2
        exp_num = row_t * col_t
        exp = _fr(exp_num, n)
        return {
            "problem_text": (
                f"A chi-squared test of homogeneity uses \\(n = {n}\\) total observations "
                f"with \\({r2}\\) categories and \\({c2}\\) groups (equal group sizes). "
                f"A row total is \\({row_t}\\) and a column total is \\({col_t}\\). "
                f"Find the expected count \\(E = \\frac{{\\text{{row}} \\times \\text{{col}}}}{{n}}\\)."
            ),
            "correct_answer": exp, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(E_{ij} = R_i \\cdot C_j / n\\)."},
                {"level": 2, "text": f"\\(E = {row_t} \\cdot {col_t} / {n} = {exp_num}/{n}\\)."},
                {"level": 3, "text": f"\\(E = {exp}\\)."},
            ],
        }
    else:
        # V3: total number of cells in table = r × c
        total_cells = r * c
        return {
            "problem_text": (
                f"A chi-squared test of homogeneity uses a table with \\({r}\\) categories "
                f"and \\({c}\\) groups. How many cells are in the table?"
            ),
            "correct_answer": str(total_cells), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Total cells \\(= r \\times c\\)."},
                {"level": 2, "text": f"\\({r} \\times {c}\\)."},
                {"level": 3, "text": f"Total cells \\(= {total_cells}\\)."},
            ],
        }


# ── stat-anova-one ────────────────────────────────────────────────────────────

def _gen_stat_anova_one():
    """One-way ANOVA: df between, df within, or total N."""
    variant = random.choice([0, 1, 2])
    k = random.randint(3, 5)
    n_per = random.randint(5, 10)
    N = k * n_per
    df_between = k - 1
    df_within = N - k
    if variant == 0:
        # V1: df between
        return {
            "problem_text": (
                f"A one-way ANOVA has \\(k={k}\\) groups of \\(n={n_per}\\) each (\\(N={N}\\) total). "
                f"Find the degrees of freedom between groups (treatment)."
            ),
            "correct_answer": str(df_between), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Between-group \\(df = k - 1\\)."},
                {"level": 2, "text": f"\\({k} - 1\\)."},
                {"level": 3, "text": f"\\(df_{{\\text{{between}}}} = {df_between}\\)."},
            ],
        }
    elif variant == 1:
        # V2: df within
        return {
            "problem_text": (
                f"A one-way ANOVA has \\(k={k}\\) groups of \\(n={n_per}\\) each (\\(N={N}\\) total). "
                f"Find the degrees of freedom within groups (error)."
            ),
            "correct_answer": str(df_within), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Within-group \\(df = N - k\\)."},
                {"level": 2, "text": f"\\({N} - {k}\\)."},
                {"level": 3, "text": f"\\(df_{{\\text{{within}}}} = {df_within}\\)."},
            ],
        }
    else:
        # V3: total sample size N
        return {
            "problem_text": (
                f"A one-way ANOVA has \\(k={k}\\) groups with \\(n={n_per}\\) observations per group. "
                f"Find the total sample size \\(N\\)."
            ),
            "correct_answer": str(N), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "\\(N = k \\times n\\) (when groups are equal-sized)."},
                {"level": 2, "text": f"\\(N = {k} \\times {n_per}\\)."},
                {"level": 3, "text": f"\\(N = {N}\\)."},
            ],
        }


# ── stat-anova-kruskal ────────────────────────────────────────────────────────

def _gen_stat_anova_kruskal():
    """Kruskal-Wallis: df, total N, or sum of ranks check."""
    variant = random.choice([0, 1, 2])
    k = random.randint(3, 5)
    df = k - 1
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: total N and sum of ranks = N(N+1)/2
        n_per = random.randint(3, 6)
        N = k * n_per
        rank_sum = N * (N + 1) // 2
        return {
            "problem_text": (
                f"A Kruskal-Wallis test has \\(k={k}\\) groups of \\(n={n_per}\\) each. "
                f"Find the total sum of all ranks \\(N(N+1)/2\\)."
            ),
            "correct_answer": str(rank_sum), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Total ranks sum \\(= N(N+1)/2\\) where \\(N = kn\\)."},
                {"level": 2, "text": f"\\(N = {k} \\times {n_per} = {N}\\). Sum \\(= {N} \\times {N+1} / 2\\)."},
                {"level": 3, "text": f"Sum of ranks \\(= {rank_sum}\\)."},
            ],
        }
    else:
        # V3: total N = k × n_per
        n_per = random.randint(4, 8)
        N = k * n_per
        return {
            "problem_text": (
                f"A Kruskal-Wallis test compares \\(k={k}\\) groups with \\(n={n_per}\\) observations each. "
                f"Find the total number of observations \\(N\\)."
            ),
            "correct_answer": str(N), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "\\(N = k \\times n\\)."},
                {"level": 2, "text": f"\\({k} \\times {n_per}\\)."},
                {"level": 3, "text": f"\\(N = {N}\\)."},
            ],
        }


# ── stat-multiple-testing ─────────────────────────────────────────────────────

def _gen_stat_multiple_testing():
    """Multiple testing: Bonferroni, expected false rejections, or FDR threshold."""
    variant = random.choice([0, 1, 2])
    m = random.choice([5, 10, 20])
    alpha_pct = random.choice([5, 10])
    alpha_frac = Fraction(alpha_pct, 100)
    corrected = Fraction(alpha_frac.numerator, alpha_frac.denominator * m)
    ans_bonf = _fr(corrected.numerator, corrected.denominator)
    if variant == 0:
        # V1: Bonferroni correction
        return {
            "problem_text": (
                f"You are performing \\(m={m}\\) hypothesis tests at family-wise error rate \\(\\alpha={alpha_pct}\\%\\). "
                f"Using the Bonferroni correction, what is the per-test significance level \\(\\alpha^* = \\alpha/m\\)?"
            ),
            "correct_answer": ans_bonf, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Bonferroni correction: \\(\\alpha^* = \\alpha / m\\)."},
                {"level": 2, "text": f"\\(\\alpha^* = \\frac{{{alpha_pct}\\%}}{{{m}}} = \\frac{{{alpha_pct}}}{{{100*m}}}\\)."},
                {"level": 3, "text": f"\\(\\alpha^* = {ans_bonf}\\)."},
            ],
        }
    elif variant == 1:
        # V2: expected number of false rejections = m0 × α (under H0 for all)
        # use m0 = m (all null), so expected false rejections = m × α
        # keep as integer: choose m and alpha_pct so product is integer
        m2 = random.choice([10, 20])
        alpha2_pct = random.choice([5, 10])
        expected = m2 * alpha2_pct // 100
        return {
            "problem_text": (
                f"You perform \\(m={m2}\\) hypothesis tests, all under \\(H_0\\), "
                f"each at level \\(\\alpha={alpha2_pct}\\%\\). "
                f"How many tests are expected to be falsely rejected?"
            ),
            "correct_answer": str(expected), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Expected false rejections \\(= m \\times \\alpha\\)."},
                {"level": 2, "text": f"\\(= {m2} \\times {alpha2_pct}\\% = {m2} \\times {alpha2_pct}/100\\)."},
                {"level": 3, "text": f"Expected false rejections \\(= {expected}\\)."},
            ],
        }
    else:
        # V3: Bonferroni gives α* = α/m; ask for m given α* and α
        # α* = alpha_frac / m → m = alpha / alpha*
        alpha_top = alpha_pct  # e.g. 10%
        m_ans = m
        # α* = alpha_pct/(100*m); present α* as fraction
        alpha_star_num = alpha_pct
        alpha_star_den = 100 * m
        alpha_star_f = Fraction(alpha_star_num, alpha_star_den)
        alpha_star_str = f"{alpha_star_f.numerator}/{alpha_star_f.denominator}"
        return {
            "problem_text": (
                f"Using Bonferroni correction with \\(\\alpha={alpha_pct}\\%\\), "
                f"the per-test level is \\(\\alpha^* = {alpha_star_str}\\). "
                f"Find the number of tests \\(m = \\alpha/\\alpha^*\\)."
            ),
            "correct_answer": str(m_ans), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(m = \\alpha / \\alpha^*\\)."},
                {"level": 2, "text": f"\\(m = \\frac{{{alpha_pct}\\%}}{{{alpha_star_str}}}\\)."},
                {"level": 3, "text": f"\\(m = {m_ans}\\)."},
            ],
        }


# ── stat-slr ──────────────────────────────────────────────────────────────────

def _gen_stat_slr():
    """SLR: find slope β̂1, predicted value ŷ, or intercept β̂0."""
    variant = random.choice([0, 1, 2])
    b1 = random.randint(1, 4)
    b0 = random.randint(0, 5)
    xs = [1, 2, 3]
    ys = [b0 + b1 * x for x in xs]
    xbar = 2  # mean of 1,2,3
    ybar = sum(ys) / 3
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    sxx = sum((x - xbar)**2 for x in xs)
    if variant == 0:
        # V1: find slope
        ans = _fr(int(sxy), int(sxx))
        return {
            "problem_text": (
                f"Data: \\((x,y)\\) pairs: \\((1,{ys[0]})\\), \\((2,{ys[1]})\\), \\((3,{ys[2]})\\). "
                f"Find the OLS slope \\(\\hat{{\\beta}}_1\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\(\\hat{\\beta}_1 = S_{xy}/S_{xx}\\)."},
                {"level": 2, "text": f"\\(\\bar{{x}}=2\\), \\(\\bar{{y}}={int(ybar)}\\). \\(S_{{xx}} = {int(sxx)}\\), \\(S_{{xy}} = {int(sxy)}\\)."},
                {"level": 3, "text": f"\\(\\hat{{\\beta}}_1 = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: find predicted value ŷ at a new x
        x_new = random.choice([0, 4, 5])
        yhat = b0 + b1 * x_new
        return {
            "problem_text": (
                f"A simple linear regression has \\(\\hat{{\\beta}}_0 = {b0}\\) and \\(\\hat{{\\beta}}_1 = {b1}\\). "
                f"Find the predicted value \\(\\hat{{y}}\\) at \\(x = {x_new}\\)."
            ),
            "correct_answer": str(yhat), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\hat{y} = \\hat{\\beta}_0 + \\hat{\\beta}_1 x\\)."},
                {"level": 2, "text": f"\\(= {b0} + {b1} \\cdot {x_new}\\)."},
                {"level": 3, "text": f"\\(\\hat{{y}} = {yhat}\\)."},
            ],
        }
    else:
        # V3: find intercept β̂0 = ȳ - β̂1 × x̄
        b0_calc = int(ybar) - b1 * int(xbar)
        return {
            "problem_text": (
                f"Simple linear regression on data: \\((1,{ys[0]})\\), \\((2,{ys[1]})\\), \\((3,{ys[2]})\\). "
                f"Given \\(\\hat{{\\beta}}_1 = {b1}\\), find the intercept "
                f"\\(\\hat{{\\beta}}_0 = \\bar{{y}} - \\hat{{\\beta}}_1 \\bar{{x}}\\)."
            ),
            "correct_answer": str(b0_calc), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\hat{\\beta}_0 = \\bar{y} - \\hat{\\beta}_1 \\bar{x}\\)."},
                {"level": 2, "text": f"\\(\\bar{{x}} = 2\\), \\(\\bar{{y}} = {int(ybar)}\\). \\(\\hat{{\\beta}}_0 = {int(ybar)} - {b1} \\cdot 2\\)."},
                {"level": 3, "text": f"\\(\\hat{{\\beta}}_0 = {b0_calc}\\)."},
            ],
        }


# ── stat-slr-matrix ───────────────────────────────────────────────────────────

def _gen_stat_slr_matrix():
    """SLR matrix form: dimensions of X, number of columns of X'X, or rank of X'X."""
    variant = random.choice([0, 1, 2])
    n = random.randint(10, 50)
    if variant == 0:
        # V1: dimensions of X
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
    elif variant == 1:
        # V2: number of rows in β̂ = X'X)^{-1}X'y (= number of parameters = 2)
        return {
            "problem_text": (
                f"In simple linear regression with \\(n={n}\\) observations, "
                f"the OLS estimator is \\(\\hat{{\\boldsymbol{{\\beta}}}} = (\\mathbf{{X}}^\\top \\mathbf{{X}})^{{-1}} \\mathbf{{X}}^\\top \\mathbf{{y}}\\). "
                f"How many elements does \\(\\hat{{\\boldsymbol{{\\beta}}}}\\) have?"
            ),
            "correct_answer": "2", "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\hat{\\boldsymbol{\\beta}}\\) has one element per parameter: intercept and slope."},
                {"level": 2, "text": "SLR has 2 parameters: \\(\\hat{\\beta}_0\\) and \\(\\hat{\\beta}_1\\)."},
                {"level": 3, "text": "\\(\\hat{\\boldsymbol{\\beta}}\\) has 2 elements."},
            ],
        }
    else:
        # V3: rank of X'X (= number of columns of X = 2, assuming full rank)
        return {
            "problem_text": (
                f"In simple linear regression with \\(n={n}\\) observations "
                f"and a full-rank design matrix \\(\\mathbf{{X}}\\) of size \\({n} \\times 2\\), "
                f"what is the rank of \\(\\mathbf{{X}}^\\top \\mathbf{{X}}\\)?"
            ),
            "correct_answer": "2", "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "If \\(\\mathbf{X}\\) has full column rank, then \\(\\text{rank}(\\mathbf{X}^\\top \\mathbf{X}) = \\text{rank}(\\mathbf{X}) = \\) number of columns."},
                {"level": 2, "text": "\\(\\mathbf{X}\\) has 2 columns, so \\(\\mathbf{X}^\\top \\mathbf{X}\\) is \\(2 \\times 2\\)."},
                {"level": 3, "text": "\\(\\text{rank}(\\mathbf{X}^\\top \\mathbf{X}) = 2\\)."},
            ],
        }


# ── stat-slr-inference ────────────────────────────────────────────────────────

def _gen_stat_slr_inference():
    """SLR inference: df, residual = y - ŷ, or SE of slope."""
    variant = random.choice([0, 1, 2])
    n = random.randint(5, 30)
    if variant == 0:
        # V1: degrees of freedom
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
    elif variant == 1:
        # V2: find residual e = y - ŷ
        b0 = random.randint(1, 5)
        b1 = random.randint(2, 4)
        x_val = random.randint(2, 6)
        yhat = b0 + b1 * x_val
        y_obs = yhat + random.choice([-2, -1, 1, 2])
        resid = y_obs - yhat
        return {
            "problem_text": (
                f"An SLR model predicts \\(\\hat{{y}} = {b0} + {b1}x\\). "
                f"For observation \\(x = {x_val}\\), the actual value is \\(y = {y_obs}\\). "
                f"Find the residual \\(e = y - \\hat{{y}}\\)."
            ),
            "correct_answer": str(resid), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "First compute \\(\\hat{y}\\), then \\(e = y - \\hat{y}\\)."},
                {"level": 2, "text": f"\\(\\hat{{y}} = {b0} + {b1} \\cdot {x_val} = {yhat}\\). \\(e = {y_obs} - {yhat}\\)."},
                {"level": 3, "text": f"Residual \\(= {resid}\\)."},
            ],
        }
    else:
        # V3: find number of parameters estimated = 2 (determines df)
        return {
            "problem_text": (
                f"In simple linear regression with \\(n={n}\\) observations, "
                f"how many parameters are estimated (including the intercept)?"
            ),
            "correct_answer": "2", "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "SLR estimates an intercept \\(\\hat{\\beta}_0\\) and a slope \\(\\hat{\\beta}_1\\)."},
                {"level": 2, "text": "That is 2 parameters total."},
                {"level": 3, "text": "Number of parameters \\(= 2\\)."},
            ],
        }


# ── stat-mlr ──────────────────────────────────────────────────────────────────

def _gen_stat_mlr():
    """MLR: residual df, number of parameters, or predicted value."""
    variant = random.choice([0, 1, 2])
    n = random.randint(20, 50)
    p = random.randint(2, 5)
    df = n - p - 1
    if variant == 0:
        # V1: residual df
        return {
            "problem_text": (
                f"Multiple linear regression has \\(n={n}\\) observations and \\(p={p}\\) predictors "
                f"(plus an intercept). Find the residual degrees of freedom \\(n - p - 1\\)."
            ),
            "correct_answer": str(df), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Residual \\(df = n - p - 1\\)."},
                {"level": 2, "text": f"\\({n} - {p} - 1\\)."},
                {"level": 3, "text": f"\\(df = {df}\\)."},
            ],
        }
    elif variant == 1:
        # V2: number of parameters (coefficients) = p + 1
        n_params = p + 1
        return {
            "problem_text": (
                f"Multiple linear regression with \\(p={p}\\) predictors and an intercept. "
                f"How many regression coefficients are estimated in total?"
            ),
            "correct_answer": str(n_params), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "One coefficient per predictor plus one for the intercept."},
                {"level": 2, "text": f"\\(p + 1 = {p} + 1\\)."},
                {"level": 3, "text": f"Total coefficients \\(= {n_params}\\)."},
            ],
        }
    else:
        # V3: predicted value ŷ = β0 + β1*x1 + β2*x2 (p=2)
        b0 = random.randint(1, 5)
        b1 = random.randint(2, 4)
        b2 = random.randint(2, 4)
        x1 = random.randint(1, 5)
        x2 = random.randint(1, 5)
        yhat = b0 + b1 * x1 + b2 * x2
        return {
            "problem_text": (
                f"An MLR model: \\(\\hat{{y}} = {b0} + {b1}x_1 + {b2}x_2\\). "
                f"Find \\(\\hat{{y}}\\) when \\(x_1 = {x1}\\) and \\(x_2 = {x2}\\)."
            ),
            "correct_answer": str(yhat), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Plug in \\(x_1\\) and \\(x_2\\)."},
                {"level": 2, "text": f"\\(= {b0} + {b1} \\cdot {x1} + {b2} \\cdot {x2} = {b0} + {b1*x1} + {b2*x2}\\)."},
                {"level": 3, "text": f"\\(\\hat{{y}} = {yhat}\\)."},
            ],
        }


# ── stat-mlr-inference ────────────────────────────────────────────────────────

def _gen_stat_mlr_inference():
    """F-test in MLR: numerator df, denominator df, or F-test decision."""
    variant = random.choice([0, 1, 2])
    p = random.randint(2, 5)
    n = random.randint(p + 10, 50)
    df_num = p
    df_den = n - p - 1
    if variant == 0:
        # V1: numerator df
        return {
            "problem_text": (
                f"The overall \\(F\\)-test in MLR with \\(p={p}\\) predictors (and an intercept) "
                f"has what numerator degrees of freedom?"
            ),
            "correct_answer": str(df_num), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The \\(F\\)-test numerator \\(df\\) = number of predictors \\(= p\\)."},
                {"level": 2, "text": f"\\(p = {p}\\)."},
                {"level": 3, "text": f"Numerator \\(df = {p}\\)."},
            ],
        }
    elif variant == 1:
        # V2: denominator df = n - p - 1
        return {
            "problem_text": (
                f"The overall \\(F\\)-test in MLR with \\(n={n}\\) observations and \\(p={p}\\) predictors "
                f"has what denominator degrees of freedom?"
            ),
            "correct_answer": str(df_den), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Denominator \\(df = n - p - 1\\)."},
                {"level": 2, "text": f"\\({n} - {p} - 1\\)."},
                {"level": 3, "text": f"Denominator \\(df = {df_den}\\)."},
            ],
        }
    else:
        # V3: reject F-test decision (F vs critical value)
        F_stat = random.choice([3, 5, 8, 12])
        F_crit = random.choice([3, 4, 5])
        reject = 1 if F_stat > F_crit else 0
        return {
            "problem_text": (
                f"An \\(F\\)-test in MLR yields \\(F = {F_stat}\\) with critical value \\(F_{{\\text{{crit}}}} = {F_crit}\\). "
                f"Do we reject \\(H_0\\) (all slopes zero)? Enter 1 for reject, 0 for fail to reject."
            ),
            "correct_answer": str(reject), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Reject \\(H_0\\) if \\(F > F_{\\text{crit}}\\)."},
                {"level": 2, "text": f"Compare \\(F = {F_stat}\\) with \\(F_{{\\text{{crit}}}} = {F_crit}\\)."},
                {"level": 3, "text": f"{'Reject' if reject else 'Fail to reject'} \\(H_0\\). Answer: {reject}."},
            ],
        }


# ── stat-model-comparison ─────────────────────────────────────────────────────

def _gen_stat_model_comparison():
    """AIC = 2k - 2 log L̂: which is better, compute AIC, or ΔAIC."""
    variant = random.choice([0, 1, 2])
    k1 = random.randint(2, 4)
    k2 = k1 + random.randint(1, 2)
    ll1 = random.randint(-50, -20)
    ll2 = ll1 + random.randint(1, 4)
    aic1 = 2 * k1 - 2 * ll1
    aic2 = 2 * k2 - 2 * ll2
    better = 1 if aic1 < aic2 else 2
    if variant == 0:
        # V1: which model is better
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
    elif variant == 1:
        # V2: compute AIC for a single model
        k = random.randint(2, 5)
        ll = random.randint(-40, -10)
        aic = 2 * k - 2 * ll
        return {
            "problem_text": (
                f"A model has \\(k={k}\\) parameters and log-likelihood \\(\\hat{{\\ell}} = {ll}\\). "
                f"Compute the AIC \\(= 2k - 2\\hat{{\\ell}}\\)."
            ),
            "correct_answer": str(aic), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "AIC \\(= 2k - 2\\hat{\\ell}\\)."},
                {"level": 2, "text": f"\\(= 2 \\cdot {k} - 2 \\cdot ({ll}) = {2*k} + {-2*ll}\\)."},
                {"level": 3, "text": f"AIC \\(= {aic}\\)."},
            ],
        }
    else:
        # V3: ΔAIC = AIC2 - AIC1
        delta = abs(aic2 - aic1)
        return {
            "problem_text": (
                f"Model 1 has AIC \\(= {aic1}\\) and Model 2 has AIC \\(= {aic2}\\). "
                f"Find \\(|\\Delta\\text{{AIC}}| = |\\text{{AIC}}_2 - \\text{{AIC}}_1|\\)."
            ),
            "correct_answer": str(delta), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(|\\Delta\\text{AIC}| = |\\text{AIC}_2 - \\text{AIC}_1|\\)."},
                {"level": 2, "text": f"\\(= |{aic2} - {aic1}|\\)."},
                {"level": 3, "text": f"\\(|\\Delta\\text{{AIC}}| = {delta}\\)."},
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
    """Bayesian updating: posterior α, posterior β, or posterior mean."""
    variant = random.choice([0, 1, 2])
    alpha0 = random.randint(1, 3)
    beta0 = random.randint(1, 3)
    x = random.randint(2, 8)   # successes
    n = random.randint(x, x + 5)  # trials
    alpha_post = alpha0 + x
    beta_post = beta0 + n - x
    if variant == 0:
        # V1: posterior α
        ans = str(alpha_post)
        return {
            "problem_text": (
                f"Prior: \\(\\theta \\sim \\text{{Beta}}(\\alpha_0={alpha0}, \\beta_0={beta0})\\). "
                f"Observed \\(x={x}\\) successes in \\(n={n}\\) Bernoulli trials. "
                f"The posterior is \\(\\text{{Beta}}(\\alpha_0+x,\\, \\beta_0+n-x)\\). "
                f"Find the posterior \\(\\alpha\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Posterior \\(\\alpha = \\alpha_0 + x\\)."},
                {"level": 2, "text": f"\\(= {alpha0} + {x}\\)."},
                {"level": 3, "text": f"\\(\\alpha_\\text{{post}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: posterior β
        ans = str(beta_post)
        return {
            "problem_text": (
                f"Prior: \\(\\theta \\sim \\text{{Beta}}(\\alpha_0={alpha0}, \\beta_0={beta0})\\). "
                f"Observed \\(x={x}\\) successes in \\(n={n}\\) Bernoulli trials. "
                f"The posterior is \\(\\text{{Beta}}(\\alpha_0+x,\\, \\beta_0+n-x)\\). "
                f"Find the posterior \\(\\beta\\)."
            ),
            "correct_answer": ans, "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Posterior \\(\\beta = \\beta_0 + n - x\\)."},
                {"level": 2, "text": f"\\(= {beta0} + {n} - {x} = {beta0} + {n-x}\\)."},
                {"level": 3, "text": f"\\(\\beta_\\text{{post}} = {ans}\\)."},
            ],
        }
    else:
        # V3: posterior mean = α_post / (α_post + β_post)
        mean_num = alpha_post
        mean_den = alpha_post + beta_post
        ans = _fr(mean_num, mean_den)
        return {
            "problem_text": (
                f"Prior: \\(\\theta \\sim \\text{{Beta}}({alpha0}, {beta0})\\). "
                f"Observed \\(x={x}\\) successes in \\(n={n}\\) trials. "
                f"The posterior is \\(\\text{{Beta}}({alpha_post}, {beta_post})\\). "
                f"Find the posterior mean \\(E[\\theta | x] = \\frac{{\\alpha}}{{\\alpha + \\beta}}\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Posterior mean of Beta\\((\\alpha, \\beta)\\) is \\(\\frac{\\alpha}{\\alpha + \\beta}\\)."},
                {"level": 2, "text": f"\\(= \\frac{{{alpha_post}}}{{{alpha_post} + {beta_post}}} = \\frac{{{alpha_post}}}{{{mean_den}}}\\)."},
                {"level": 3, "text": f"Posterior mean \\(= {ans}\\)."},
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
    """Monte Carlo: estimate E[g(X)], estimate P(event), or find SE of estimate."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: estimate E[g(X)]
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
    elif variant == 1:
        # V2: estimate P(event) = k/n from n runs with k events
        n = random.choice([100, 200, 400])
        k = random.randint(n // 10, n // 2)
        ans = _fr(k, n)
        return {
            "problem_text": (
                f"In \\(n={n}\\) simulation runs, the event of interest occurred \\(k={k}\\) times. "
                f"Estimate the probability \\(P(\\text{{event}}) = k/n\\)."
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Monte Carlo estimate: \\(\\hat{P}(\\text{event}) = k/n\\)."},
                {"level": 2, "text": f"\\(= {k}/{n}\\)."},
                {"level": 3, "text": f"\\(\\hat{{P}} = {ans}\\)."},
            ],
        }
    else:
        # V3: SE of Monte Carlo estimate = σ/√n
        n = random.choice([4, 9, 16, 25, 100])
        sig = random.choice([2, 3, 4, 5])
        sqrtn = int(sqrt(n))
        se = _fr(sig, sqrtn)
        return {
            "problem_text": (
                f"A Monte Carlo simulation with \\(n={n}\\) runs estimates \\(E[X]\\). "
                f"The true std dev is \\(\\sigma={sig}\\). "
                f"Find the simulation standard error \\(\\text{{SE}} = \\sigma/\\sqrt{{n}}\\)."
            ),
            "correct_answer": se, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Simulation SE \\(= \\sigma / \\sqrt{n}\\)."},
                {"level": 2, "text": f"\\(= {sig} / \\sqrt{{{n}}} = {sig}/{sqrtn}\\)."},
                {"level": 3, "text": f"SE \\(= {se}\\)."},
            ],
        }


# ── stat-confounding ──────────────────────────────────────────────────────────

def _gen_stat_confounding():
    """Confounding: identify confounder, compute adjusted effect, or crude vs adjusted."""
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: identify confounder (original)
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
    elif variant == 1:
        # V2: crude vs adjusted difference (numeric)
        crude = random.randint(5, 15)
        adjusted = random.randint(1, crude - 1)
        confounding_effect = crude - adjusted
        return {
            "problem_text": (
                f"The crude (unadjusted) estimated effect is \\({crude}\\). "
                f"After adjusting for a confounder, the effect is \\({adjusted}\\). "
                f"Find the confounding bias \\(= \\text{{crude}} - \\text{{adjusted}}\\)."
            ),
            "correct_answer": str(confounding_effect), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Confounding bias \\(= \\text{crude estimate} - \\text{adjusted estimate}\\)."},
                {"level": 2, "text": f"\\({crude} - {adjusted}\\)."},
                {"level": 3, "text": f"Confounding bias \\(= {confounding_effect}\\)."},
            ],
        }
    else:
        # V3: identify direction of confounding
        # crude > adjusted → positive confounding → answer 1
        # crude < adjusted → negative confounding → answer 2
        crude = random.randint(4, 10)
        delta = random.choice([-2, -1, 1, 2, 3])
        adjusted = crude + delta
        if adjusted <= 0:
            adjusted = 1
            delta = adjusted - crude
        direction = 1 if crude > adjusted else 2
        return {
            "problem_text": (
                f"Crude estimate: \\({crude}\\). Adjusted estimate: \\({adjusted}\\). "
                f"Is this positive confounding (crude > adjusted, enter 1) "
                f"or negative confounding (crude < adjusted, enter 2)?"
            ),
            "correct_answer": str(direction), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Positive confounding: crude > adjusted. Negative: crude < adjusted."},
                {"level": 2, "text": f"Crude \\(= {crude}\\), adjusted \\(= {adjusted}\\)."},
                {"level": 3, "text": f"{'Positive' if direction==1 else 'Negative'} confounding. Answer: {direction}."},
            ],
        }


# ── stat-causal-intro ─────────────────────────────────────────────────────────

def _gen_stat_causal_intro():
    """Potential outcomes: ATE, ATT, or observed potential outcome."""
    variant = random.choice([0, 1, 2])
    e_y1 = random.randint(5, 12)
    e_y0 = random.randint(2, e_y1 - 1)
    ate = e_y1 - e_y0
    if variant == 0:
        # V1: ATE
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
    elif variant == 1:
        # V2: ATT (Average Treatment Effect on the Treated)
        # Under randomization ATT = ATE; ask to compute it
        e_y1_treated = random.randint(5, 12)
        e_y0_treated = random.randint(2, e_y1_treated - 1)
        att = e_y1_treated - e_y0_treated
        return {
            "problem_text": (
                f"Among treated units, \\(E[Y(1) \\mid D=1] = {e_y1_treated}\\) and "
                f"\\(E[Y(0) \\mid D=1] = {e_y0_treated}\\). "
                f"Find the ATT \\(= E[Y(1) - Y(0) \\mid D=1]\\)."
            ),
            "correct_answer": str(att), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "ATT \\(= E[Y(1) \\mid D=1] - E[Y(0) \\mid D=1]\\)."},
                {"level": 2, "text": f"\\({e_y1_treated} - {e_y0_treated}\\)."},
                {"level": 3, "text": f"ATT \\(= {att}\\)."},
            ],
        }
    else:
        # V3: find observed outcome Y given treatment and potential outcomes
        # Individual: Y(1)=a, Y(0)=b, D=1 → Y_obs = Y(1) = a
        y1 = random.randint(5, 15)
        y0 = random.randint(2, y1 - 1)
        d = random.choice([0, 1])
        y_obs = y1 if d == 1 else y0
        return {
            "problem_text": (
                f"An individual has potential outcomes \\(Y(1) = {y1}\\) and \\(Y(0) = {y0}\\). "
                f"The treatment indicator is \\(D = {d}\\). "
                f"Find the observed outcome \\(Y = D \\cdot Y(1) + (1-D) \\cdot Y(0)\\)."
            ),
            "correct_answer": str(y_obs), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(Y = D \\cdot Y(1) + (1-D) \\cdot Y(0)\\). Only one potential outcome is observed."},
                {"level": 2, "text": f"\\(D = {d}\\), so \\(Y = Y({'1' if d == 1 else '0'}) = {y_obs}\\)."},
                {"level": 3, "text": f"Observed outcome \\(Y = {y_obs}\\)."},
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
