import os
from glob import glob

# ← adjust these to match your structure
INPUT_DIR  = os.path.join(os.getcwd(), "inputs")
TARGET_DIR = os.path.join(os.getcwd(), "targets")
OUTPUT     = "grant_edits_all_versions.jsonl"

def main():
    # find all your *.input.docx under inputs/
    input_paths  = sorted(glob(os.path.join(INPUT_DIR,  "*.input.docx")))
    target_paths = sorted(glob(os.path.join(TARGET_DIR, "*.target*.docx")))

    print("Found inputs:", len(input_paths), "files")
    # map inputs → their matching targets by name
    pairs = []
    for inp in input_paths:
        stem = os.path.basename(inp).replace(".input.docx","")
        # collect all matching targets for that stem
        targs = sorted(glob(os.path.join(TARGET_DIR, f"{stem}.target*.docx")))
        if not targs:
            print(" ⚠️ no target for", stem)
            continue
        pairs.append((inp, targs))

    # now write your JSONL
    with open(OUTPUT, "w", encoding="utf-8") as out:
        for inp, targs in pairs:
            # load each .docx, extract text, and for each version emit a line
            input_text = load_docx_text(inp)
            for targ in targs:
                target_text = load_docx_text(targ)
                rec = {
                  "instruction": "Improve this grant proposal answer",
                  "input": input_text,
                  "output": target_text
                }
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Wrote {len(pairs)} stems × their versions to {OUTPUT}")
