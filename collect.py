import requests, csv, os

URL = "https://stats.aipipe.org/usage.json"
FILE = "usage_history.csv"

# load existing rows
rows = {}
if os.path.exists(FILE):
    with open(FILE) as f:
        for r in csv.DictReader(f):
            rows[r["date"]] = r

data = requests.get(URL, timeout=30).json()
for d in data["days"]:
    # only completed days that actually have data (missing != 0)
    if d["complete"] and d["available"] and d["total"]:
        rows[d["date"]] = {
            "date": d["date"],
            "spend_usd": d["total"]["spend_usd"],
            "iitm_users": d["iitm_users"],
        }

with open(FILE, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["date", "spend_usd", "iitm_users"])
    w.writeheader()
    for k in sorted(rows):
        w.writerow(rows[k])
