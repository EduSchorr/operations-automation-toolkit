from __future__ import annotations

from pathlib import Path

ALLOWED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".csv", ".docx", ".png", ".jpg", ".jpeg"}

def validate_attachments(paths: list[str], max_size_mb: int = 15) -> list[dict]:
    result = []
    limit = max_size_mb * 1024 * 1024
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f"Attachment not found: {path.name}")
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Attachment type is not allowed: {path.suffix}")
        size = path.stat().st_size
        if size > limit:
            raise ValueError(f"Attachment is larger than {max_size_mb} MB: {path.name}")
        result.append({"name": path.name, "path": str(path), "size": size})
    return result
