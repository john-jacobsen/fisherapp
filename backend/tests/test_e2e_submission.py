"""
End-to-end HTTP submission test for the MathLive fraction fix (FIXES-4).

Run inside Docker: python tests/test_e2e_submission.py
"""
import sys
import json
import urllib.request
import urllib.error

BASE = "http://localhost:8000"


def post(path, data, token=None):
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        BASE + path, data=body, headers={"Content-Type": "application/json"}
    )
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "detail": e.read().decode()}


def login_or_register():
    """Return a valid auth token, registering first if needed."""
    login = post("/api/auth/login", {"email": "fixes4test@test.com", "password": "Test1234!"})
    token = login.get("token") or login.get("access_token")
    if token:
        return token
    # Register then login
    post("/api/auth/register", {
        "email": "fixes4test@test.com",
        "name": "Fixes4 Test",
        "password": "Test1234!",
    })
    login = post("/api/auth/login", {"email": "fixes4test@test.com", "password": "Test1234!"})
    token = login.get("token") or login.get("access_token")
    if not token:
        print("AUTH FAILED:", login)
        sys.exit(1)
    return token


def test_submit(token, node_id, answer_str, label):
    """Start a session and submit answer_str; return is_correct."""
    s = post(f"/api/practice/{node_id}/start", {}, token)
    if "_error" in s:
        print(f"  Start failed for {label}: {s}")
        return None
    result = post(f"/api/practice/{node_id}/submit", {
        "session_id": s["session_id"],
        "problem_id": s["problem"]["id"],
        "answer": answer_str,
        "mode": "test",
    }, token)
    return result


def main():
    print("=" * 60)
    print("FIXES-4 End-to-End Submission Test")
    print("=" * 60)

    token = login_or_register()
    print("Auth: OK")

    # Test cases: MathLive shorthand fractions submitted via HTTP
    # These are Python string literals — no shell escaping involved
    test_cases = [
        ("\\frac12",     "frac-simplify", "\\frac12 (1/2 shorthand)"),
        ("\\frac56",     "frac-simplify", "\\frac56 (5/6 shorthand)"),
        ("\\frac23",     "frac-simplify", "\\frac23 (2/3 shorthand)"),
        ("\\frac{5}{6}", "frac-simplify", "\\frac{5}{6} (braces)"),
    ]

    print()
    all_pass = True
    for answer_str, node_id, label in test_cases:
        result = test_submit(token, node_id, answer_str, label)
        if result is None:
            all_pass = False
            continue
        is_correct = result.get("is_correct")
        correct_ans = result.get("correct_answer", "?")
        # Note: the submitted answer may not match the node's generated problem answer.
        # What we verify is that the answer is PARSED correctly (not rejected due to
        # \frac12 format) — i.e. the checker did not return False due to a parse error.
        # If the submitted fraction doesn't equal the problem's correct answer, that's
        # a wrong-answer (expected), not a parse failure.
        # To truly verify the fix, we check the answer_checker directly below.
        status = "SUBMITTED" if is_correct is not None else "ERROR"
        print(f"  [{status}] {label}")
        print(f"           correct_answer={correct_ans!r}, is_correct={is_correct}")
        if result.get("error"):
            print(f"           PARSE ERROR: {result.get('message')}")
            all_pass = False

    # Direct checker verification (no HTTP escaping concerns)
    print()
    print("=== Direct answer_checker verification ===")
    sys.path.insert(0, "/app")
    from app.services.answer_checker import check_answer

    checker_cases = [
        ("\\frac12",      "1/2",           True,  "\\frac12 == 1/2"),
        ("\\frac56",      "5/6",           True,  "\\frac56 == 5/6"),
        ("\\frac23",      "2/3",           True,  "\\frac23 == 2/3"),
        ("\\frac{1}{2}",  "1/2",           True,  "\\frac{1}{2} == 1/2"),
        ("\\frac{5}{6}",  "5/6",           True,  "\\frac{5}{6} == 5/6"),
        ("\\frac12",      "\\frac{1}{2}",  True,  "\\frac12 == \\frac{1}{2}"),
        ("\\frac{1}{2}",  "\\frac12",      True,  "\\frac{1}{2} == \\frac12"),
        ("1/2",           "1/2",           True,  "1/2 == 1/2 (plain)"),
        ("5/6",           "\\frac{5}{6}",  True,  "5/6 == \\frac{5}{6}"),
        ("\\frac{15}{24}", "5/8",          True,  "\\frac{15}{24} == 5/8 (multi-digit)"),
        ("\\frac{10}{18}", "5/9",          True,  "\\frac{10}{18} == 5/9 (multi-digit)"),
    ]

    for student, correct, expected, label in checker_cases:
        result = check_answer(student, correct, "symbolic")
        ok = result == expected
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}")
        if not ok:
            print(f"           expected={expected}, got={result}")
            all_pass = False

    print()
    if all_pass:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
