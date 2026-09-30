from __future__ import annotations

import re
from decimal import Decimal

MONEY_RE = re.compile(r"R\$\s*([\d.]+,\d{2})")
CNPJ_RE = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")

def parse_nfse_text(text: str) -> dict:
    """Extract a compact set of fields from already-extracted NFSe text.

    PDF rendering/OCR layers are intentionally left outside this public example.
    """
    normalized = "\n".join(line.strip() for line in (text or "").splitlines() if line.strip())
    cnpjs = CNPJ_RE.findall(normalized)
    money_values = MONEY_RE.findall(normalized)

    amount = None
    if money_values:
        amount = str(Decimal(money_values[-1].replace(".", "").replace(",", ".")))

    return {
        "provider_cnpj": cnpjs[0] if cnpjs else None,
        "customer_cnpj": cnpjs[1] if len(cnpjs) > 1 else None,
        "amount": amount,
        "raw_length": len(normalized),
    }

if __name__ == "__main__":
    sample = """
    Prestador 00.000.000/0001-00
    Tomador 11.111.111/0001-11
    Valor do serviço R$ 1.234,56
    """
    print(parse_nfse_text(sample))
