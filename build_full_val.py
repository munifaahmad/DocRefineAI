# build_full_jsonl.py

import os
import json
from load_doc_text import load_doc_text  # see below

# ─── CONFIG ──────────────────────────────────────────────────────────────
INPUT_DIR  = "inputs"   # folder containing only docN.input.docx
TARGET_DIR = "targets"  # folder containing only docN.target.docx
OUTPUT_FILE = "val_full.jsonl"
# ────────────────────────────────────────────────────────────────────────

pairs = []

for fname in os.listdir(INPUT_DIR):
    if not fname.endswith(".input.docx"):
        continue
    base = fname[:-len(".input.docx")]
    inp_path = os.path.join(INPUT_DIR, fname)
    tgt_name = f"{base}.target.docx"
    tgt_path = os.path.join(TARGET_DIR, tgt_name)

    if not os.path.exists(tgt_path):
        print(f"⚠️  Skipping {base}: no target at {tgt_path}")
        continue

    inp_text = load_doc_text(inp_path)
    tgt_text = load_doc_text(tgt_path)
    pairs.append({
        "instruction": "Improve this grant proposal snippet for clarity, conciseness, and impact.",
        "input": inp_text,
        "output": tgt_text
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for rec in pairs:
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"Wrote {len(pairs)} records into {OUTPUT_FILE}")
