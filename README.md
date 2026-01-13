Title - Legal Document Assistant

Sub Heading - RAG-Powered Search & Question Answering with Gradio

Introduction - An AI-driven system that helps users upload legal documents, search them intelligently, and ask natural-language questions — powered by Retrieval-Augmented Generation (RAG), FAISS, embeddings, and an interactive Gradio UI.

⸻

Features

✔ Upload PDF, DOCX, or TXT documents

✔ Automatic chunking and vectorization

✔ Semantic search — retrieves relevant clauses beyond keyword matching

✔ RAG-based Q&A answer generation

✔ Plain English explanations of complex legal text

✔ Conflict detection (e.g., contradictory clauses, mismatched values)

✔ Displays source citations for transparency

✔ Gradio UI for seamless interaction

✔ NVIDIA embeddings + fallback to TF-IDF when API disabled

✔ CSV export of extracted corpus

✔ Modular and extensible architecture

⸻

Tech Stack

Component	Technology
Programming Language	Python 3.8+
UI Framework	Gradio
Retrieval	FAISS Vector Search
Embeddings	NVIDIA NV-Embed + TF-IDF fallback
LLM for Q&A	NVIDIA LLaMA-3 or Local Rule-Based
RAG Integration	LangChain / Custom Pipeline
File Support	PDF, DOCX, TXT


⸻

Installation & Setup

1. Clone the repo

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install dependencies

pip install -r requirements.txt

4. Configure NVIDIA API

Create .env or export variable:

export NVIDIA_API_KEY="your key"

Without a key, system automatically switches to TF-IDF embeddings.

⸻

Run the app

python app.py

Then open the local Gradio link in your browser.

⸻

How It Works
	1.	Upload documents
	2.	System extracts and preprocesses text
	3.	Text is split into chunks & converted into embeddings
	4.	Embeddings stored inside FAISS vector DB
	5.	User types a natural question
	6.	The system:
	•	finds semantically similar document clauses
	•	sends them to an LLM
	•	generates grounded responses
	7.	Displays:
	•	answer
	•	retrieved text chunks
	•	conflict warnings

Diagram references — UML and workflow visuals on p. 43-45 show:
	•	Data ingestion
	•	Semantic search pipeline
	•	RAG Q&A sequence
￼

⸻

File Structure

project
 ├─ app.py                  # Main RAG + Gradio interface
 ├─ requirements.txt
 ├─ ingested_corpus.csv     # Auto-generated chunks (optional)
 ├─ README.md
 └─ sample_documents/


⸻

Current Limitations

⚠ Requires OCR for scanned PDFs

⚠ NVIDIA API needs internet + valid key

⚠ Heuristic conflict detection (not legal reasoning)

⚠ May not fully handle jurisdiction-specific nuances

⚠ Privacy concerns for confidential uploads ￼

⸻

Future Enhancements

* Domain-specific legal models (Indian law, US law, etc.)

* Advanced OCR for scanned documents

* Multi-document cross-reference reasoning

* Authentication & role-based privacy controls

* Full cloud deployment templates

⸻

Team

	•	Kandula Sai Gana Laxmi Rohith
  
	•	Anchetti Deekshith
  
	•	Goruganti Sai Khowshik
  

Under guidance of Dr. R. Venkat
St. Peter’s Engineering College, Hyderabad

⸻

References

Includes FAISS, RAG, NVIDIA Developer Docs, Gradio, Python libraries ￼

⸻

If you use this project…

✔ Share feedback or open issues!



