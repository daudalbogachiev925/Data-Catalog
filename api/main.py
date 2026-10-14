from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.catalog import DataCatalog
from src.models import Dataset, Column, Classification, DataDomain
from src.search import CatalogSearch

app = FastAPI(title="Data Catalog API")
catalog = DataCatalog()

class ColumnIn(BaseModel):
    name: str
    dtype: str
    nullable: bool = True
    description: str = ""
    pii: bool = False
    classification: Classification = Classification.INTERNAL

class DatasetIn(BaseModel):
    id: str
    name: str
    domain: DataDomain
    description: str
    owner: str
    steward: str
    source_system: str
    location: str
    classification: Classification
    tags: List[str] = []
    columns: List[ColumnIn] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/datasets")
def list_datasets():
    return catalog.list_all()

@app.post("/datasets")
def create_dataset(ds: DatasetIn):
    dataset = Dataset(
        id=ds.id, name=ds.name, domain=ds.domain, description=ds.description,
        owner=ds.owner, steward=ds.steward, source_system=ds.source_system,
        location=ds.location, classification=ds.classification,
        tags=ds.tags, columns=[Column(**c.dict()) for c in ds.columns])
    catalog.register(dataset)
    return dataset.to_dict()

@app.get("/datasets/{ds_id}")
def get_dataset(ds_id: str):
    d = catalog.find(ds_id)
    if not d:
        raise HTTPException(404, "Dataset not found")
    return d.to_dict()

@app.delete("/datasets/{ds_id}")
def delete_dataset(ds_id: str):
    if not catalog.storage.delete(ds_id):
        raise HTTPException(404, "Dataset not found")
    return {"deleted": ds_id}

@app.get("/search")
def search(q: str, top_k: int = 5):
    searcher = CatalogSearch(catalog.storage.all())
    return searcher.search(q, top_k)

@app.get("/pii")
def pii_datasets():
    return catalog.pii_datasets()
