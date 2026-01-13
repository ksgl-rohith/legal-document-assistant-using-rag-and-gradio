import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_MODEL = "nvidia/nv-embed-v1"

def nvidia_embeddings(texts):
    if not NVIDIA_API_KEY:
        raise RuntimeError("NVIDIA key missing")
    url = "https://integrate.api.nvidia.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}"}
    payload = {"model": NVIDIA_MODEL, "input": texts}
    resp = requests.post(url, headers=headers, json=payload)
    embs = [item["embedding"] for item in resp.json()["data"]]
    return np.array(embs, dtype=np.float32)

def tfidf_fit(texts):
    vec = TfidfVectorizer(max_features=2048)
    X = normalize(vec.fit_transform(texts))
    return X.toarray().astype(np.float32), vec

def tfidf_transform(vec, texts):
    X = normalize(vec.transform(texts))
    return X.toarray().astype(np.float32)
