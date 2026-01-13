import pandas as pd
from .embedding_utils import *
from .faiss_utils import build_index, search

class RAGIndex:
    def __init__(self):
        self.df = pd.DataFrame()
        self.index = None
        self.vec = None
        self.vectors = None

    def build(self, df):
        texts = df["text"].tolist()
        try:
            emb = nvidia_embeddings(texts)
            self.vectors = emb
            self.vec = None
        except:
            emb, vec = tfidf_fit(texts)
            self.vec = vec
            self.vectors = emb

        self.index = build_index(self.vectors)
        self.df = df.reset_index(drop=True)

    def query(self, q, topk=5):
        if self.vec:
            qv = tfidf_transform(self.vec, [q])
        else:
            qv = nvidia_embeddings([q])
        D, I = search(self.index, qv, topk)
        return [self.df.iloc[i] for i in I]
