"""
Seed basic stub problems for each knowledge node.
These are minimal problems to make the placement test functional.
Run after seed_knowledge_graph.py.

Usage (from project root):
    docker compose run --rm backend python scripts/seed_problems.py
"""
from app.database import SessionLocal
from app.models.content import Problem, Hint
from app.models.knowledge import KnowledgeNode
from app.models.progress import ResponseLog
import app.models  # noqa

PROBLEMS = [
    # Fractions
    {
        "node_id": "frac-simplify",
        "problems": [
            {"text": "Simplify: \\frac{12}{18}", "answer": "2/3", "hints": [
                "Find the GCD of 12 and 18.",
                "GCD(12, 18) = 6. Divide both numerator and denominator by 6.",
                "12 ÷ 6 = 2 and 18 ÷ 6 = 3, so the answer is \\frac{2}{3}."
            ]},
            {"text": "Simplify: \\frac{15}{25}", "answer": "3/5", "hints": [
                "Find what number divides both 15 and 25.",
                "GCD(15, 25) = 5. Divide both by 5.",
                "15 ÷ 5 = 3 and 25 ÷ 5 = 5, so the answer is \\frac{3}{5}."
            ]},
            {"text": "Simplify: \\frac{24}{36}", "answer": "2/3", "hints": [
                "Find the GCD of 24 and 36.",
                "GCD(24, 36) = 12.",
                "24 ÷ 12 = 2 and 36 ÷ 12 = 3, so the answer is \\frac{2}{3}."
            ]},
        ]
    },
    {
        "node_id": "frac-add-like",
        "problems": [
            {"text": "Add: \\frac{3}{7} + \\frac{2}{7}", "answer": "5/7", "hints": [
                "The denominators are the same, so add the numerators.",
                "3 + 2 = 5, keep the denominator 7.",
                "\\frac{3}{7} + \\frac{2}{7} = \\frac{5}{7}"
            ]},
            {"text": "Subtract: \\frac{5}{9} - \\frac{2}{9}", "answer": "1/3", "hints": [
                "The denominators are the same, subtract the numerators.",
                "5 - 2 = 3, keep the denominator 9.",
                "\\frac{3}{9} simplifies to \\frac{1}{3}."
            ]},
        ]
    },
    {
        "node_id": "frac-common-denom",
        "problems": [
            {"text": "Find the LCD of \\frac{1}{4} and \\frac{1}{6}.", "answer": "12", "type": "numeric", "hints": [
                "List multiples of 4: 4, 8, 12, 16...",
                "List multiples of 6: 6, 12, 18...",
                "The smallest common multiple is 12."
            ]},
            {"text": "Find the LCD of \\frac{1}{3} and \\frac{1}{5}.", "answer": "15", "type": "numeric", "hints": [
                "Since 3 and 5 share no common factors, LCD = 3 × 5.",
                "LCD = 15.",
                "The answer is 15."
            ]},
        ]
    },
    {
        "node_id": "frac-add-unlike",
        "problems": [
            {"text": "Add: \\frac{1}{4} + \\frac{1}{6}", "answer": "5/12", "hints": [
                "Find the LCD of 4 and 6. LCD = 12.",
                "Convert: \\frac{1}{4} = \\frac{3}{12} and \\frac{1}{6} = \\frac{2}{12}.",
                "\\frac{3}{12} + \\frac{2}{12} = \\frac{5}{12}."
            ]},
            {"text": "Add: \\frac{2}{3} + \\frac{1}{4}", "answer": "11/12", "hints": [
                "LCD of 3 and 4 is 12.",
                "\\frac{2}{3} = \\frac{8}{12} and \\frac{1}{4} = \\frac{3}{12}.",
                "\\frac{8}{12} + \\frac{3}{12} = \\frac{11}{12}."
            ]},
            {"text": "Subtract: \\frac{3}{4} - \\frac{1}{3}", "answer": "5/12", "hints": [
                "LCD of 4 and 3 is 12.",
                "\\frac{3}{4} = \\frac{9}{12} and \\frac{1}{3} = \\frac{4}{12}.",
                "\\frac{9}{12} - \\frac{4}{12} = \\frac{5}{12}."
            ]},
        ]
    },
    {
        "node_id": "frac-multiply",
        "problems": [
            {"text": "Multiply: \\frac{2}{3} \\times \\frac{3}{4}", "answer": "1/2", "hints": [
                "Multiply numerators: 2 × 3 = 6. Multiply denominators: 3 × 4 = 12.",
                "\\frac{6}{12} — now simplify.",
                "GCD(6,12) = 6, so \\frac{6}{12} = \\frac{1}{2}."
            ]},
            {"text": "Multiply: \\frac{5}{6} \\times \\frac{3}{10}", "answer": "1/4", "hints": [
                "Multiply: \\frac{5 \\times 3}{6 \\times 10} = \\frac{15}{60}.",
                "Simplify \\frac{15}{60}.",
                "GCD(15, 60) = 15, so \\frac{15}{60} = \\frac{1}{4}."
            ]},
        ]
    },
    {
        "node_id": "frac-divide",
        "problems": [
            {"text": "Divide: \\frac{3}{4} \\div \\frac{1}{2}", "answer": "3/2", "hints": [
                "Dividing by a fraction means multiplying by its reciprocal.",
                "\\frac{3}{4} \\times \\frac{2}{1} = \\frac{6}{4}.",
                "Simplify: \\frac{6}{4} = \\frac{3}{2}."
            ]},
            {"text": "Divide: \\frac{2}{5} \\div \\frac{4}{15}", "answer": "3/2", "hints": [
                "Flip the second fraction: reciprocal of \\frac{4}{15} is \\frac{15}{4}.",
                "\\frac{2}{5} \\times \\frac{15}{4} = \\frac{30}{20}.",
                "\\frac{30}{20} = \\frac{3}{2}."
            ]},
        ]
    },
    # Order of Operations
    {
        "node_id": "order-pemdas",
        "problems": [
            {"text": "Evaluate: 3 + 4 \\times 2", "answer": "11", "type": "numeric", "hints": [
                "Remember PEMDAS: multiplication before addition.",
                "Do 4 × 2 = 8 first.",
                "Then 3 + 8 = 11."
            ]},
            {"text": "Evaluate: 12 \\div 4 - 1", "answer": "2", "type": "numeric", "hints": [
                "Division before subtraction.",
                "12 ÷ 4 = 3.",
                "3 - 1 = 2."
            ]},
            {"text": "Evaluate: 2^3 + 5 \\times 2 - 4", "answer": "14", "type": "numeric", "hints": [
                "PEMDAS: Exponents first, then multiplication.",
                "2^3 = 8, then 5 × 2 = 10.",
                "8 + 10 - 4 = 14."
            ]},
        ]
    },
    {
        "node_id": "order-nested",
        "problems": [
            {"text": "Evaluate: 2 \\times (3 + (4 - 1))", "answer": "12", "type": "numeric", "hints": [
                "Work from the innermost parentheses out.",
                "Innermost: 4 - 1 = 3. Then 3 + 3 = 6.",
                "2 × 6 = 12."
            ]},
            {"text": "Evaluate: [(2 + 3) \\times 4] - 6 \\div 2", "answer": "17", "type": "numeric", "hints": [
                "Start with the bracket: (2 + 3) = 5.",
                "5 × 4 = 20, and 6 ÷ 2 = 3.",
                "20 - 3 = 17."
            ]},
        ]
    },
    # Exponents
    {
        "node_id": "exp-product",
        "problems": [
            {"text": "Simplify: x^3 \\cdot x^4", "answer": "x**7", "hints": [
                "When multiplying same base, add the exponents.",
                "x^3 · x^4 = x^(3+4).",
                "= x^7."
            ]},
            {"text": "Simplify: 2^3 \\cdot 2^5", "answer": "256", "type": "numeric", "hints": [
                "Add the exponents: 2^(3+5) = 2^8.",
                "2^8 = 256.",
                "The answer is 256."
            ]},
        ]
    },
    {
        "node_id": "exp-power",
        "problems": [
            {"text": "Simplify: (x^2)^4", "answer": "x**8", "hints": [
                "Power rule: (x^a)^b = x^(a·b).",
                "(x^2)^4 = x^(2·4).",
                "= x^8."
            ]},
            {"text": "Simplify: (2^3)^2", "answer": "64", "type": "numeric", "hints": [
                "(2^3)^2 = 2^(3·2) = 2^6.",
                "2^6 = 64.",
                "The answer is 64."
            ]},
        ]
    },
    {
        "node_id": "exp-negative",
        "problems": [
            {"text": "Evaluate: 2^{-3}", "answer": "1/8", "hints": [
                "Negative exponent means reciprocal: x^(-n) = 1/x^n.",
                "2^(-3) = 1/(2^3).",
                "= 1/8."
            ]},
            {"text": "Evaluate: 5^0", "answer": "1", "type": "numeric", "hints": [
                "Any nonzero number to the 0 power equals 1.",
                "x^0 = 1 for x ≠ 0.",
                "5^0 = 1."
            ]},
        ]
    },
    {
        "node_id": "exp-combined",
        "problems": [
            {"text": "Simplify: \\frac{x^5 \\cdot x^{-2}}{x^0}", "answer": "x**3", "hints": [
                "Apply product rule in numerator: x^5 · x^(-2) = x^(5-2) = x^3.",
                "x^0 = 1.",
                "x^3 / 1 = x^3."
            ]},
            {"text": "Simplify: \\frac{(x^2)^3}{x^4}", "answer": "x**2", "hints": [
                "Power rule: (x^2)^3 = x^6.",
                "Quotient rule: x^6 / x^4 = x^(6-4).",
                "= x^2."
            ]},
        ]
    },
    # Equations
    {
        "node_id": "eq-one-step",
        "problems": [
            {"text": "Solve for x: x + 7 = 12", "answer": "5", "type": "numeric", "hints": [
                "Isolate x by subtracting 7 from both sides.",
                "x + 7 - 7 = 12 - 7.",
                "x = 5."
            ]},
            {"text": "Solve for x: 3x = 21", "answer": "7", "type": "numeric", "hints": [
                "Isolate x by dividing both sides by 3.",
                "3x/3 = 21/3.",
                "x = 7."
            ]},
            {"text": "Solve for x: x - 4 = 9", "answer": "13", "type": "numeric", "hints": [
                "Add 4 to both sides.",
                "x - 4 + 4 = 9 + 4.",
                "x = 13."
            ]},
        ]
    },
    {
        "node_id": "eq-two-step",
        "problems": [
            {"text": "Solve for x: 2x + 3 = 11", "answer": "4", "type": "numeric", "hints": [
                "First subtract 3 from both sides: 2x = 8.",
                "Then divide by 2.",
                "x = 4."
            ]},
            {"text": "Solve for x: 3x - 5 = 16", "answer": "7", "type": "numeric", "hints": [
                "Add 5 to both sides: 3x = 21.",
                "Divide by 3.",
                "x = 7."
            ]},
            {"text": "Solve for x: \\frac{x}{4} + 2 = 5", "answer": "12", "type": "numeric", "hints": [
                "Subtract 2 from both sides: x/4 = 3.",
                "Multiply both sides by 4.",
                "x = 12."
            ]},
        ]
    },
    {
        "node_id": "eq-fractions",
        "problems": [
            {"text": "Solve for x: \\frac{x}{3} + \\frac{x}{6} = 5", "answer": "10", "type": "numeric", "hints": [
                "Multiply through by the LCD of 3 and 6, which is 6.",
                "2x + x = 30, so 3x = 30.",
                "x = 10."
            ]},
            {"text": "Solve for x: \\frac{2x}{5} = 4", "answer": "10", "type": "numeric", "hints": [
                "Multiply both sides by 5.",
                "2x = 20.",
                "x = 10."
            ]},
        ]
    },
    {
        "node_id": "eq-distribution",
        "problems": [
            {"text": "Solve for x: 2(x + 3) = 14", "answer": "4", "type": "numeric", "hints": [
                "Distribute: 2x + 6 = 14.",
                "Subtract 6: 2x = 8.",
                "x = 4."
            ]},
            {"text": "Solve for x: 3(2x - 1) = 15", "answer": "3", "type": "numeric", "hints": [
                "Distribute: 6x - 3 = 15.",
                "Add 3: 6x = 18.",
                "x = 3."
            ]},
            {"text": "Solve for x: 4(x + 2) - 3x = 11", "answer": "3", "type": "numeric", "hints": [
                "Distribute: 4x + 8 - 3x = 11.",
                "Combine like terms: x + 8 = 11.",
                "x = 3."
            ]},
        ]
    },
    {
        "node_id": "eq-quadratic",
        "problems": [
            {"text": "Solve: x^2 - 5x + 6 = 0", "answer": "2,3", "type": "multiple_choice", "hints": [
                "Factor: look for two numbers that multiply to 6 and add to -5.",
                "Those numbers are -2 and -3: (x-2)(x-3) = 0.",
                "x = 2 or x = 3."
            ]},
            {"text": "Solve: x^2 + x - 6 = 0", "answer": "2,-3", "type": "multiple_choice", "hints": [
                "Factor: two numbers that multiply to -6 and add to 1.",
                "Those are 3 and -2: (x+3)(x-2) = 0.",
                "x = -3 or x = 2."
            ]},
        ]
    },
    # Logarithms
    {
        "node_id": "log-exponential",
        "problems": [
            {"text": "Evaluate: 2^4", "answer": "16", "type": "numeric", "hints": [
                "2^4 means 2 multiplied by itself 4 times.",
                "2 × 2 × 2 × 2 = 16.",
                "The answer is 16."
            ]},
            {"text": "If f(x) = 3^x, find f(2).", "answer": "9", "type": "numeric", "hints": [
                "Substitute x = 2 into f(x) = 3^x.",
                "f(2) = 3^2.",
                "= 9."
            ]},
        ]
    },
    {
        "node_id": "log-definition",
        "problems": [
            {"text": "Evaluate: \\log_2(8)", "answer": "3", "type": "numeric", "hints": [
                "log_2(8) asks: 2 to what power gives 8?",
                "2^3 = 8.",
                "\\log_2(8) = 3."
            ]},
            {"text": "Evaluate: \\log_{10}(1000)", "answer": "3", "type": "numeric", "hints": [
                "10 to what power gives 1000?",
                "10^3 = 1000.",
                "\\log_{10}(1000) = 3."
            ]},
        ]
    },
    {
        "node_id": "log-rules",
        "problems": [
            {"text": "Simplify: \\log_2(4) + \\log_2(8)", "answer": "5", "type": "numeric", "hints": [
                "Product rule: log(a) + log(b) = log(ab).",
                "\\log_2(4 × 8) = \\log_2(32).",
                "2^5 = 32, so the answer is 5."
            ]},
            {"text": "Simplify: \\log_3(27) - \\log_3(3)", "answer": "2", "type": "numeric", "hints": [
                "Quotient rule: log(a) - log(b) = log(a/b).",
                "\\log_3(27/3) = \\log_3(9).",
                "3^2 = 9, so the answer is 2."
            ]},
        ]
    },
    {
        "node_id": "log-equations",
        "problems": [
            {"text": "Solve: \\log_2(x) = 4", "answer": "16", "type": "numeric", "hints": [
                "Convert to exponential form: 2^4 = x.",
                "2^4 = 16.",
                "x = 16."
            ]},
            {"text": "Solve: \\log_3(x+1) = 2", "answer": "8", "type": "numeric", "hints": [
                "Convert: 3^2 = x + 1.",
                "9 = x + 1.",
                "x = 8."
            ]},
        ]
    },
    # Summation
    {
        "node_id": "sum-sigma",
        "problems": [
            {"text": "Evaluate: \\sum_{i=1}^{4} i", "answer": "10", "type": "numeric", "hints": [
                "Expand the sum: 1 + 2 + 3 + 4.",
                "Add them up.",
                "= 10."
            ]},
            {"text": "Evaluate: \\sum_{k=1}^{3} 2k", "answer": "12", "type": "numeric", "hints": [
                "Substitute k = 1, 2, 3: 2(1) + 2(2) + 2(3).",
                "= 2 + 4 + 6.",
                "= 12."
            ]},
        ]
    },
    {
        "node_id": "sum-arithmetic",
        "problems": [
            {"text": "Find the sum of the first 10 natural numbers: 1 + 2 + ... + 10", "answer": "55", "type": "numeric", "hints": [
                "Use the formula S_n = n(n+1)/2.",
                "S_10 = 10 × 11 / 2.",
                "= 55."
            ]},
            {"text": "Evaluate: \\sum_{i=1}^{5} (2i - 1)", "answer": "25", "type": "numeric", "hints": [
                "This is the sum of odd numbers: 1 + 3 + 5 + 7 + 9.",
                "Or use n^2: 5^2.",
                "= 25."
            ]},
        ]
    },
    {
        "node_id": "sum-nested",
        "problems": [
            {"text": "Evaluate: \\sum_{i=1}^{2} \\sum_{j=1}^{2} i \\cdot j", "answer": "9", "type": "numeric", "hints": [
                "Expand the inner sum for each i.",
                "i=1: 1·1 + 1·2 = 3. i=2: 2·1 + 2·2 = 6.",
                "3 + 6 = 9."
            ]},
        ]
    },
    # Combinatorics
    {
        "node_id": "comb-counting",
        "problems": [
            {"text": "A restaurant has 3 appetizers and 4 main courses. How many different meals (one appetizer + one main) are possible?", "answer": "12", "type": "numeric", "hints": [
                "Use the multiplication principle.",
                "3 choices × 4 choices = ?",
                "= 12 different meals."
            ]},
            {"text": "A coin is flipped 3 times. How many different outcome sequences are possible?", "answer": "8", "type": "numeric", "hints": [
                "Each flip has 2 outcomes (H or T).",
                "Total = 2 × 2 × 2.",
                "= 8."
            ]},
        ]
    },
    {
        "node_id": "comb-permutations",
        "problems": [
            {"text": "How many ways can 4 people be arranged in a line?", "answer": "24", "type": "numeric", "hints": [
                "This is 4! (4 factorial).",
                "4! = 4 × 3 × 2 × 1.",
                "= 24."
            ]},
            {"text": "How many 3-letter arrangements can be made from 5 distinct letters (no repetition)?", "answer": "60", "type": "numeric", "hints": [
                "Use P(5,3) = 5!/(5-3)! = 5!/2!",
                "= 5 × 4 × 3.",
                "= 60."
            ]},
        ]
    },
    {
        "node_id": "comb-combinations",
        "problems": [
            {"text": "How many ways can you choose 2 items from 5 (order doesn't matter)?", "answer": "10", "type": "numeric", "hints": [
                "Use C(5,2) = 5!/(2! × 3!).",
                "= (5 × 4)/(2 × 1).",
                "= 10."
            ]},
            {"text": "How many 3-person committees can be formed from 6 people?", "answer": "20", "type": "numeric", "hints": [
                "Use C(6,3) = 6!/(3! × 3!).",
                "= (6 × 5 × 4)/(3 × 2 × 1).",
                "= 20."
            ]},
        ]
    },
    # Geometric Series
    {
        "node_id": "geo-sequences",
        "problems": [
            {"text": "Find the next term: 2, 6, 18, 54, ___", "answer": "162", "type": "numeric", "hints": [
                "Find the common ratio: 6/2 = 3.",
                "Multiply the last term by 3.",
                "54 × 3 = 162."
            ]},
            {"text": "In a geometric sequence with first term 5 and ratio 2, what is the 4th term?", "answer": "40", "type": "numeric", "hints": [
                "Formula: a_n = a_1 × r^(n-1).",
                "a_4 = 5 × 2^3.",
                "= 5 × 8 = 40."
            ]},
        ]
    },
    {
        "node_id": "geo-finite",
        "problems": [
            {"text": "Find the sum: 1 + 2 + 4 + 8 + 16", "answer": "31", "type": "numeric", "hints": [
                "This is a geometric series with a=1, r=2, n=5.",
                "S_n = a(r^n - 1)/(r - 1) = 1(2^5 - 1)/(2-1).",
                "= 31."
            ]},
            {"text": "Find the sum of the first 4 terms of a geometric series: a=3, r=2.", "answer": "45", "type": "numeric", "hints": [
                "S_4 = 3(2^4 - 1)/(2 - 1).",
                "= 3 × 15.",
                "= 45."
            ]},
        ]
    },
    {
        "node_id": "geo-infinite",
        "problems": [
            {"text": "Find the sum of the infinite geometric series: 1 + \\frac{1}{2} + \\frac{1}{4} + \\frac{1}{8} + ...", "answer": "2", "type": "numeric", "hints": [
                "S = a/(1-r) when |r| < 1. Here a=1, r=1/2.",
                "S = 1/(1 - 1/2) = 1/(1/2).",
                "= 2."
            ]},
            {"text": "A geometric series has a=6 and r=1/3. Find the infinite sum.", "answer": "9", "type": "numeric", "hints": [
                "S = a/(1-r) = 6/(1 - 1/3).",
                "= 6/(2/3) = 6 × 3/2.",
                "= 9."
            ]},
        ]
    },
]


def seed():
    db = SessionLocal()
    try:
        # Get all nodes
        nodes = {n.id: n for n in db.query(KnowledgeNode).all()}
        if not nodes:
            print("No nodes found. Run seed_knowledge_graph.py first.")
            return

        total_problems = 0
        total_hints = 0

        for node_data in PROBLEMS:
            node_id = node_data["node_id"]
            if node_id not in nodes:
                print(f"Warning: node {node_id} not found in DB, skipping.")
                continue

            # Remove existing problems for this node
            existing = db.query(Problem).filter(Problem.node_id == node_id).all()
            for p in existing:
                db.query(ResponseLog).filter(ResponseLog.problem_id == p.id).delete()
                db.query(Hint).filter(Hint.problem_id == p.id).delete()
                db.delete(p)
            db.flush()

            for prob_data in node_data["problems"]:
                problem = Problem(
                    node_id=node_id,
                    problem_text=prob_data["text"],
                    correct_answer=prob_data["answer"],
                    answer_type=prob_data.get("type", "symbolic"),
                    difficulty=0.5,
                    source="manual",
                )
                db.add(problem)
                db.flush()

                for i, hint_text in enumerate(prob_data.get("hints", []), start=1):
                    hint = Hint(
                        problem_id=problem.id,
                        level=i,
                        hint_text=hint_text,
                    )
                    db.add(hint)

                total_problems += 1
                total_hints += len(prob_data.get("hints", []))

        db.commit()
        print(f"Seeded {total_problems} problems and {total_hints} hints.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
