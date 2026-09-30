from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

def export_messages(messages: list[dict], output_zip: str | Path) -> Path:
    """Export already-selected message metadata/content into a portable ZIP.

    The Outlook-specific selection layer is intentionally omitted from the public
    portfolio; this function demonstrates the sanitized export format.
    """
    target = Path(output_zip).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(target, "w", ZIP_DEFLATED) as archive:
        manifest = []
        for index, message in enumerate(messages, start=1):
            safe = {
                "id": str(message.get("id") or index),
                "subject": str(message.get("subject") or ""),
                "sender": str(message.get("sender") or ""),
                "received_at": str(message.get("received_at") or ""),
                "body": str(message.get("body") or ""),
            }
            name = f"messages/{index:04d}.json"
            archive.writestr(name, json.dumps(safe, ensure_ascii=False, indent=2))
            manifest.append({"file": name, "subject": safe["subject"]})
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    return target
