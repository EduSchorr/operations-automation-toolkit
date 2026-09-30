from __future__ import annotations

from collections import defaultdict

def normalize_coupon(value) -> str:
    return "".join(ch for ch in str(value or "").upper() if ch.isalnum())

def find_duplicates(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        coupon = normalize_coupon(row.get("coupon"))
        if coupon:
            groups[coupon].append(row)

    result = []
    for coupon, items in groups.items():
        if len(items) < 2:
            continue
        result.append({
            "coupon": coupon,
            "occurrences": len(items),
            "orders": [str(item.get("order_id") or "") for item in items],
            "rows": items,
        })
    return sorted(result, key=lambda item: (-item["occurrences"], item["coupon"]))
