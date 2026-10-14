import json
import os
from typing import List, Optional
from src.models import Dataset

class CatalogStorage:
    def __init__(self, path="data/seed.json"):
        self.path = path
        self._ensure()
        self.datasets: List[Dataset] = self._load()

    def _ensure(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self):
        with open(self.path, encoding="utf-8") as f:
            return [Dataset(**d) for d in json.load(f)]

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([d.to_dict() for d in self.datasets], f,
                      ensure_ascii=False, indent=2)

    def add(self, ds: Dataset):
        self.datasets.append(ds)
        self.save()

    def get(self, ds_id: str) -> Optional[Dataset]:
        return next((d for d in self.datasets if d.id == ds_id), None)

    def delete(self, ds_id: str) -> bool:
        before = len(self.datasets)
        self.datasets = [d for d in self.datasets if d.id != ds_id]
        self.save()
        return len(self.datasets) < before

    def all(self) -> List[Dataset]:
        return self.datasets
