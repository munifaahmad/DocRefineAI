from typing import List
from docx import Document

# load_doc_text.py

from docx import Document

def load_doc_text(path: str) -> str:
    """Return all non-empty paragraphs joined by newlines."""
    doc = Document(path)
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paras)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} path/to/file.docx")
        sys.exit(1)
    path = sys.argv[1]
    print(load_doc_text(path))
