from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CatalogSearch:
    def __init__(self, datasets):
        self.datasets = datasets
        self.vectorizer = TfidfVectorizer()
        corpus = [self._text(d) for d in datasets]
        self.matrix = self.vectorizer.fit_transform(corpus) if corpus else None

    def _text(self, d):
        cols = " ".join(c.name for c in d.columns)
        return f"{d.name} {d.description} {d.domain.value} {d.owner} {' '.join(d.tags)} {cols}"

    def search(self, query, top_k=5):
        if self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        sims = cosine_similarity(q, self.matrix)[0]
        idx = sims.argsort()[::-1][:top_k]
        return [{"dataset": self.datasets[i].to_dict(), "score": float(sims[i])}
                for i in idx if sims[i] > 0]
