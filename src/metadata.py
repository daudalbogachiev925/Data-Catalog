def extract_schema(sample_rows):
    """sample_rows: list[dict]"""
    if not sample_rows:
        return []
    keys = set()
    for r in sample_rows:
        keys.update(r.keys())
    cols = []
    for k in sorted(keys):
        values = [r.get(k) for r in sample_rows if r.get(k) is not None]
        dtype = type(values[0]).__name__ if values else "unknown"
        cols.append({"name": k, "dtype": dtype, "nullable": len(values) < len(sample_rows)})
    return cols

def detect_pii_columns(columns):
    """Эвристика: PII по имени колонки."""
    pii_patterns = ["email", "phone", "ssn", "passport", "name",
                    "address", "birth", "ip", "card", "iban", "login"]
    result = []
    for c in columns:
        name = c["name"].lower()
        if any(p in name for p in pii_patterns):
            result.append(c["name"])
    return result
