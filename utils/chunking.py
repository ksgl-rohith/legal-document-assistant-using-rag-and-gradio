import re

def chunk_text(text, size=800, stride=200):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= size: return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text): break
        start += max(size - stride, 1)
    return chunks
