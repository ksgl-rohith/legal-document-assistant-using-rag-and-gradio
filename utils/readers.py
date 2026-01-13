import io, os, tempfile
import PyPDF2, docx

def read_pdf_bytes(raw):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(raw))
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    except:
        return ""

def read_docx_bytes(raw):
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=".docx") as tmp:
            tmp.write(raw)
            tmp.flush()
            doc = docx.Document(tmp.name)
            os.unlink(tmp.name)
        return "\n".join([p.text for p in doc.paragraphs])
    except:
        return ""

def read_text_bytes(raw):
    try: return raw.decode("utf-8", errors="ignore")
    except: return ""

def extract_text_from_upload(file_obj):
    fname = file_obj.name
    raw = file_obj.read()

    if fname.lower().endswith(".pdf") or raw[:4] == b"%PDF":
        return read_pdf_bytes(raw)
    if fname.lower().endswith(".docx"):
        return read_docx_bytes(raw)
    return read_text_bytes(raw)
