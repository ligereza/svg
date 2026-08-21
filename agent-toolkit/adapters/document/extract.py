import json
import sys
from pathlib import Path


def extract(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".docx":
        from docx import Document
        document = Document(path)
        return "\n\n".join(p.text for p in document.paragraphs if p.text.strip())
    if suffix == ".pdf":
        try:
            import pdfplumber
            pages = [page.extract_text() or "" for page in pdfplumber.open(path).pages]
        except Exception:
            from pypdf import PdfReader
            pages = [page.extract_text() or "" for page in PdfReader(path).pages]
        return {"text": "\n\n".join(f"[[PAGE {index + 1}]]\n{page}" for index, page in enumerate(pages)), "pages": len(pages)}
    raise ValueError(f"Unsupported document format: {suffix}")


if __name__ == "__main__":
    value = extract(sys.argv[1])
    print(json.dumps(value if isinstance(value, dict) else {"text": value}, ensure_ascii=False))
