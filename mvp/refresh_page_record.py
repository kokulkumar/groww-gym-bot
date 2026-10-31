"""Refreshes mvp/data/page_record.json from the three public Groww scheme pages (the figures a user sees on each page).
Run from the project root:  python3 mvp/refresh_page_record.py
Source: https://groww.in/mutual-funds/<scheme>  (public page data, read on the date stored in the file)."""
import json, re, sys, time, os
import requests
SCHEMES = {"large-cap": "groww-large-cap-fund-direct-growth", "multicap": "groww-multicap-fund-direct-growth", "elss": "groww-elss-tax-saver-fund-direct-growth"}
UA = {"User-Agent": "Mozilla/5.0 (GrowwGymBot-student-prototype)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "page_record.json")


def num(x):
    return None if x in (None, "", "NA") else float(x)


def fetch(slug):
    url = "https://groww.in/mutual-funds/" + slug
    h = requests.get(url, headers=UA, timeout=30).text
    j = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S).group(1))
    d = j["props"]["pageProps"]["mfServerSideData"]
    mgrs = [m["person_name"] for m in d.get("fund_manager_details", []) if m.get("person_name")]
    li = d.get("lock_in") or {}
    lock = (f"{li['years']} years" if li.get("years") else None)
    rs = (d.get("return_stats") or [{}])[0]
    risk = rs.get("risk")
    return {
        "url": url, "name": d.get("scheme_name") or d.get("fund_name"), "fund_name": d.get("fund_name"),
        "category": f"{d.get('category','')} · {d.get('sub_category','')}".strip(" ·"),
        "nav": num(d.get("nav")), "nav_date": d.get("nav_date"),
        "r1y": num(rs.get("return1y")), "r3y": num(rs.get("return3y")), "r5y": num(rs.get("return5y")), "since": num(rs.get("return_since_created")),
        "expense_ratio": num(d.get("expense_ratio")), "aum_cr": num(d.get("aum")), "exit_load": d.get("exit_load"),
        "min_sip": num(d.get("min_sip_investment")), "min_lump": num(d.get("min_investment_amount")),
        "benchmark": d.get("benchmark_name") or d.get("benchmark"), "risk": (risk + " Risk") if risk and "Risk" not in risk else risk,
        "launch_date": d.get("launch_date"), "managers": mgrs, "lock_in": lock, "fund_house": d.get("fund_house"),
    }


if __name__ == "__main__":
    rec = {"fetched": time.strftime("%Y-%m-%d %H:%M"), "source": "Groww scheme pages (public page data)", "schemes": {}}
    for sid, slug in SCHEMES.items():
        rec["schemes"][sid] = fetch(slug)
        print(sid, rec["schemes"][sid]["nav"], rec["schemes"][sid]["nav_date"], rec["schemes"][sid]["r1y"], rec["schemes"][sid]["r3y"], rec["schemes"][sid]["expense_ratio"], rec["schemes"][sid]["managers"], rec["schemes"][sid]["lock_in"])
    json.dump(rec, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("saved", OUT)
