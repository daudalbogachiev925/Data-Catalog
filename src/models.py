from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class Classification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class DataDomain(str, Enum):
    CUSTOMER = "customer"
    PRODUCT = "product"
    FINANCE = "finance"
    HR = "hr"
    MARKETING = "marketing"
    OPERATIONS = "operations"

@dataclass
class Column:
    name: str
    dtype: str
    nullable: bool = True
    description: str = ""
    pii: bool = False
    classification: Classification = Classification.INTERNAL

@dataclass
class Dataset:
    id: str
    name: str
    domain: DataDomain
    description: str
    owner: str
    steward: str
    source_system: str
    location: str
    classification: Classification
    tags: List[str] = field(default_factory=list)
    columns: List[Column] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    row_count: int = 0
    quality_score: float = 0.0

    def to_dict(self):
        d = asdict(self)
        d["classification"] = self.classification.value
        d["domain"] = self.domain.value
        for c in d["columns"]:
            c["classification"] = c["classification"].value if hasattr(c["classification"], "value") else c["classification"]
        return d
