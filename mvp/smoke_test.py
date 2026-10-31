"""HTTP smoke test of every endpoint, run against a running server:  python3 mvp/smoke_test.py http://localhost:8700
Catches errors that direct function tests miss (routing, rate limiter, JSON)."""
import sys, json, requests
B = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8700").rstrip("/")
def post(path, body): return requests.post(B + path, json=body, timeout=70)
checks = []
def ok(name, cond, extra=""): checks.append(cond); print(("PASS " if cond else "FAIL ") + name, extra)
r = requests.get(B + "/api/health", timeout=20); ok("health", r.status_code == 200 and r.json().get("ok"))
r = requests.get(B + "/api/schemes", timeout=20); ok("schemes", r.status_code == 200 and len(r.json().get("schemes", {})) == 3)
r = requests.get(B + "/", timeout=20); ok("home page", r.status_code == 200 and "Groww Gym Bot" in r.text)
r = requests.get(B + "/api/news", timeout=90); j = r.json(); ok("news", r.status_code == 200 and len(j.get("stories", [])) >= 3 and len(j.get("snapshot", [])) >= 1, f"{len(j.get('stories', []))} stories, {len(j.get('snapshot', []))} quotes")
r = post("/api/fund-chat", {"scheme": "large-cap", "message": "What is the exit load?"}); ok("fund chat fact", r.status_code == 200 and r.json()["kind"] == "answer")
r = post("/api/fund-chat", {"scheme": "large-cap", "message": "Is this better than HDFC Mid Cap?"}); ok("fund chat decline", r.status_code == 200 and r.json()["kind"] == "decline")
r = post("/api/coach", {"message": "What is a SIP?"}); ok("coach concept", r.status_code == 200 and r.json()["basis"] in ("lessons", "general"))
r = post("/api/coach", {"message": "Should I buy more now?"}); ok("coach decline", r.status_code == 200 and r.json()["basis"] == "declined")
r = post("/api/quiz-reword", {"chapter": 1, "stems": ["What is a unit?"]}); ok("quiz reword", r.status_code == 200 and "stems" in r.json())
print(f"\n{sum(checks)} of {len(checks)} passed"); sys.exit(0 if all(checks) else 1)
