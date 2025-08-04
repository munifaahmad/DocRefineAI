import os, glob, json
from docx import Document

INPUT_DIR  = "inputs"
TARGET_DIR = "targets"
OUT_FILE   = "val_full.jsonl"

def read_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

if __name__ == "__main__":
    inputs  = sorted(glob.glob(os.path.join(INPUT_DIR,  "*.input.docx")))
    examples = []
    for inp_path in inputs:
        base = os.path.basename(inp_path).replace(".input.docx","")
        tgt_path = os.path.join(TARGET_DIR, base + ".target.docx")
        if not os.path.exists(tgt_path):
            print(f"⚠️  skipping {base}: no target found")
            continue

        inp_txt = read_docx(inp_path)
        tgt_txt = read_docx(tgt_path)
        examples.append({"input": inp_txt, "output": tgt_txt})

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Wrote {len(examples)} examples to {OUT_FILE}")
