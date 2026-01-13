import faiss
import numpy as np

def build_index(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(vectors)
    index.add(vectors)
    return index

def search(index, qvec, topk=5):
    faiss.normalize_L2(qvec)
    D, I = index.search(qvec, topk)
    return D[0], I[0]
