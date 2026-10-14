from src.storage import CatalogStorage
from src.models import Dataset, Column, Classification, DataDomain

class DataCatalog:
    def __init__(self, storage: CatalogStorage = None):
        self.storage = storage or CatalogStorage()

    def register(self, ds: Dataset):
        self.storage.add(ds)

    def find(self, ds_id):
        return self.storage.get(ds_id)

    def list_all(self):
        return [d.to_dict() for d in self.storage.all()]

    def by_owner(self, owner: str):
        return [d.to_dict() for d in self.storage.all() if d.owner == owner]

    def by_domain(self, domain: str):
        return [d.to_dict() for d in self.storage.all() if d.domain.value == domain]

    def by_classification(self, cls: str):
        return [d.to_dict() for d in self.storage.all() if d.classification.value == cls]

    def pii_datasets(self):
        return [d.to_dict() for d in self.storage.all()
                if any(c.pii for c in d.columns)]
