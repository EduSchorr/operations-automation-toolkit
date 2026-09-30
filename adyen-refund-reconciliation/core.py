from __future__ import annotations

from decimal import Decimal, InvalidOperation

def money(value) -> Decimal:
    try:
        return Decimal(str(value).replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return Decimal("0.00")

def normalize_reference(value) -> str:
    return "".join(ch for ch in str(value or "").upper() if ch.isalnum())

def reconcile(refunds: list[dict], controls: list[dict]) -> dict:
    index = {normalize_reference(row.get("reference")): row for row in refunds if normalize_reference(row.get("reference"))}
    matched, pending, differences = [], [], []
    for row in controls:
        reference = normalize_reference(row.get("reference"))
        refund = index.get(reference)
        if not refund:
            pending.append({**row, "reason": "refund_not_found"})
            continue
        expected, actual = money(row.get("amount")), money(refund.get("amount"))
        item = {"reference": reference, "expected": str(expected), "actual": str(actual)}
        (matched if expected == actual else differences).append(item)
    return {"matched": matched, "pending": pending, "differences": differences}
