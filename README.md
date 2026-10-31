# Groww Gym Bot (concept prototype)

A mobile-first web prototype that helps first-time mutual fund investors keep their SIP going: an 18-month course (lesson + quick check each month), streak, XP and levels, plus two AI helpers: **Ask the Coach** (market news in plain words, learning questions) and **Fund chat** (facts from public scheme pages for three Groww schemes).

**This is a student concept prototype. It is not the real Groww app and no real money moves. It gives information, not investment advice.**

## What is live and what is simulated
- Live: market news (public RSS feeds), index and commodity quotes, Coach and Fund chat answers (Gemini), quick-check question wording.
- Simulated: sign-in, payments, SIP, AutoPay, notifications, leaderboard.
- Safeguards: rules in code run before the model (personal data, prompt injection, advice and forecast requests, distress), numbers in replies are checked against the live data and dated page record, and replies that sound like advice are blocked.

## Run locally
```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your-key   # never commit this
python3 -m uvicorn mvp.server:app --port 8700
```
Open http://localhost:8700 (add `?nosplash=1` to skip the splash screen).

## Deploy on Render
Create a new Blueprint from this repo (`render.yaml`). In the service's Environment settings add `GEMINI_API_KEY`. The key is read only on the server and never sent to the browser. The free plan sleeps when idle, so the first load can take about a minute.

## Quality checks (in `mvp/`)
`golden_run.py` (30 Fund chat + 16 Coach questions), `redteam_run.py` (36 hostile prompts), `smoke_test.py` (endpoints).
