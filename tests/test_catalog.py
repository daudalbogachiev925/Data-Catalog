from src.catalog import DataCatalog
from src.storage import CatalogStorage
from src.models import Dataset, Column, Classification, DataDomain
import tempfile, os

def test_register_and_find():
    tmp = tempfile.mktemp(suffix=".json")
    storage = CatalogStorage(tmp)
    catalog = DataCatalog(storage)
    ds = Dataset(id="t1", name="test", domain=DataDomain.PRODUCT,
                 description="t", owner="o", steward="s",
                 source_system="db", location="t",
                 classification=Classification.INTERNAL)
    catalog.register(ds)
    assert catalog.find("t1") is not None
    os.remove(tmp)

def test_pii_detection():
    from src.metadata import detect_pii_columns
    cols = [{"name": "email"}, {"name": "id"}, {"name": "phone_number"}]
    result = detect_pii_columns(cols)
    assert "email" in result and "phone_number" in result
