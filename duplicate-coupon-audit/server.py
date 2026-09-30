from fastapi import FastAPI

from coupons import find_duplicates

app = FastAPI(title="Duplicate Coupon Audit", version="portfolio")

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/audit")
def audit(payload: dict):
    rows = payload.get("rows") or []
    duplicates = find_duplicates(rows)
    return {"duplicates": duplicates, "count": len(duplicates)}
