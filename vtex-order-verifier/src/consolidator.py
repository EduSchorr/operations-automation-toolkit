from __future__ import annotations

def normalize_order(value) -> str:
    return "".join(ch for ch in str(value or "").strip().upper() if ch.isalnum())

def consolidate(rows: list[dict]) -> list[dict]:
    """Consolidate repeated unresolved-order rows before verification."""
    grouped = {}
    for row in rows:
        order_id = normalize_order(row.get("order_id"))
        if not order_id:
            continue
        current = grouped.setdefault(order_id, {
            "order_id": order_id,
            "sources": set(),
            "references": set(),
            "occurrences": 0,
        })
        current["occurrences"] += 1
        if row.get("source"):
            current["sources"].add(str(row["source"]))
        if row.get("reference"):
            current["references"].add(str(row["reference"]))

    result = []
    for item in grouped.values():
        result.append({
            **item,
            "sources": sorted(item["sources"]),
            "references": sorted(item["references"]),
        })
    return sorted(result, key=lambda item: (-item["occurrences"], item["order_id"]))
