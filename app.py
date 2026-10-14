import streamlit as st
import pandas as pd
from src.catalog import DataCatalog
from src.models import Dataset, Column, Classification, DataDomain
from src.search import CatalogSearch
from src.metadata import detect_pii_columns

st.set_page_config(page_title="Data Catalog", layout="wide")
st.title("📚 Data Catalog")

catalog = DataCatalog()

# Seed
if not catalog.storage.all():
    catalog.register(Dataset(
        id="ds1", name="customers", domain=DataDomain.CUSTOMER,
        description="Клиентская база", owner="data-team", steward="alice",
        source_system="PostgreSQL", location="prod.public.customers",
        classification=Classification.CONFIDENTIAL,
        tags=["pii", "core"],
        columns=[
            Column("id", "int", False, "ID клиента"),
            Column("email", "str", False, "Email", pii=True, classification=Classification.CONFIDENTIAL),
            Column("name", "str", True, "Имя", pii=True, classification=Classification.CONFIDENTIAL),
            Column("created_at", "datetime", False, "Дата регистрации"),
        ]))

st.sidebar.header("Фильтры")
data = catalog.list_all()
domains = ["All"] + sorted({d["domain"] for d in data})
domain_filter = st.sidebar.selectbox("Domain", domains)

filtered = data if domain_filter == "All" else [d for d in data if d["domain"] == domain_filter]

c1, c2, c3 = st.columns(3)
c1.metric("Datasets", len(filtered))
c2.metric("PII Datasets", len([d for d in filtered if any(c.get("pii") for c in d["columns"])]))
c3.metric("Domains", len({d["domain"] for d in filtered}))

st.subheader("Все датасеты")
st.dataframe(pd.DataFrame([{
    "ID": d["id"], "Name": d["name"], "Domain": d["domain"],
    "Owner": d["owner"], "Classification": d["classification"],
    "Tags": ", ".join(d["tags"]),
} for d in filtered]))

st.subheader("🔍 Поиск")
query = st.text_input("Запрос:")
if query:
    searcher = CatalogSearch(catalog.storage.all())
    results = searcher.search(query)
    for r in results:
        st.write(f"**{r['dataset']['name']}** — score: {r['score']:.3f}")
        st.caption(r["dataset"]["description"])

st.subheader("Детали датасета")
if filtered:
    selected = st.selectbox("Выберите", [d["id"] for d in filtered])
    ds = catalog.find(selected)
    st.json(ds.to_dict())
