# Data-Catalog
Каталог данных: реестр датасетов, метаданные, теги, поиск, владельцы, классификация.
# Data Catalog

Реестр датасетов с метаданными, владельцами, классификацией, PII-детекцией и поиском.

## Запуск
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload   # API
streamlit run app.py            # UI
```
