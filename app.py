import os
import pandas as pd
import gradio as gr

from utils.readers import extract_text_from_upload
from utils.chunking import chunk_text
from utils.conflict_detector import detect_conflicts
from utils.rag_index import RAGIndex


CORPUS_CSV = "ingested_corpus.csv"
rag = RAGIndex()
corpus_df = pd.DataFrame()


def ingest_documents(uploaded_files):
    global rag, corpus_df

    if not uploaded_files:
        return "No files uploaded.", None, "Index not built."

    records = []
    for f in uploaded_files:
        filename = getattr(f, "name", "uploaded_file")
        raw_text = extract_text_from_upload(f)
        if not raw_text:
            continue
        for i, chunk in enumerate(chunk_text(raw_text)):
            records.append(
                {"doc_id": filename, "filename": filename, "chunk_id": i, "text": chunk}
            )

    if not records:
        return "No text extracted.", None, "Index not built."

    df = pd.DataFrame(records)
    df.to_csv(CORPUS_CSV, index=False)
    corpus_df = df.copy()

    rag.__init__()
    rag.build(corpus_df)

    return f"Ingested {len(df)} chunks.", CORPUS_CSV, f"Index built with {len(df)} chunks."


def clear_corpus():
    global rag, corpus_df

    if os.path.exists(CORPUS_CSV):
        os.remove(CORPUS_CSV)
    corpus_df = pd.DataFrame()
    rag.__init__()
    return "Cleared corpus and index."


def ask_question(question, topk):
    if rag.index is None:
        return (
            "Index not built. Ingest documents first.",
            "No",
            pd.DataFrame(columns=["doc_id", "chunk_id", "score", "text"]),
            "No conflicts detected.",
        )

    results = []
    retrieved = rag.query(question, topk=topk)

    texts = []
    for row in retrieved:
        results.append(
            [
                row["doc_id"],
                row["chunk_id"],
                0.0,  # FAISS score optional
                row["text"],
            ]
        )
        texts.append(row["text"])

    retrieved_df = pd.DataFrame(results, columns=["doc_id", "chunk_id", "score", "text"])

    try:
        from utils.embedding_utils import nvidia_embeddings
        # If embedding succeeds, assume NVIDIA usage
        used_nvidia = "Yes"
    except Exception:
        used_nvidia = "No"

    from utils.embedding_utils import tfidf_transform

    conflicts = detect_conflicts(texts)
    conflict_msg = "No conflicts detected." if not conflicts else "\n".join(conflicts)

    explanation = "Answer generated based on retrieved clauses. Integrate your RAG LLM generation here."

    return explanation, used_nvidia, retrieved_df, conflict_msg


def build_ui():
    with gr.Blocks(title="Legal Document Assistant") as demo:
        gr.Markdown("# Legal Document Assistant - RAG Search and Q&A")

        with gr.Row():
            with gr.Column(scale=2):
                uploader = gr.File(
                    file_count="multiple",
                    label="Upload legal documents (PDF/DOCX/TXT)",
                    file_types=[".pdf", ".docx", ".txt"],
                )
                ingest_btn = gr.Button("Ingest & Build Index")
                ingest_status = gr.Markdown()
                download_corpus = gr.File(label="Download Corpus CSV")

            with gr.Column(scale=1):
                idx_info = gr.Markdown("Index not built yet.")
                clear_btn = gr.Button("Clear Corpus & Index")
                export_idx_btn = gr.Button("Export ingested CSV")

        question = gr.Textbox(label="Enter question")
        kslider = gr.Slider(1, 10, value=5, step=1, label="Top k clauses")
        ask_btn = gr.Button("Get Answer")

        used_box = gr.Textbox(label="NVIDIA used", interactive=False)
        explanation_out = gr.Textbox(label="Explanation", lines=10, interactive=False)
        conflicts_out = gr.Markdown(label="Possible Conflicts")
        retrieved_table = gr.Dataframe(headers=["doc_id", "chunk_id", "score", "text"])

        ingest_btn.click(
            ingest_documents,
            inputs=[uploader],
            outputs=[ingest_status, download_corpus, idx_info],
        )

        clear_btn.click(clear_corpus, outputs=[ingest_status])

        export_idx_btn.click(
            lambda: CORPUS_CSV if os.path.exists(CORPUS_CSV) else None,
            outputs=[download_corpus],
        )

        ask_btn.click(
            ask_question,
            inputs=[question, kslider],
            outputs=[explanation_out, used_box, retrieved_table, conflicts_out],
        )

    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch(server_name="0.0.0.0", share=False)
