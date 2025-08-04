# inference_openai_full.py

import os
import json
import openai

# 1) Load your OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

# 2) Point this at your full 15‐example JSONL
VAL_FILE = "val_full.jsonl"

SYSTEM_PROMPT = (
    "You are a grant‐writing assistant. "
    "Rewrite or improve the following snippet of a grant proposal "
    "for clarity, conciseness, and impact."
)

def generate_edit(text: str) -> str:
    """Call the v1 OpenAI chat completions endpoint."""
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",  "content": SYSTEM_PROMPT},
            {"role": "user",    "content": text},
        ],
        temperature=0.7,
        top_p=0.9,
        n=1,
    )
    return resp.choices[0].message.content.strip()

def main():
    # 3) Read _all_ examples
    with open(VAL_FILE, encoding="utf-8") as f:
        examples = [json.loads(line) for line in f]

    print(f"\nRunning validation on {len(examples)} examples")
    print("=" * 60)

    # 4) Loop through every record (1–15) and print INPUT / GOLD / MODEL
    for i, ex in enumerate(examples, start=1):
        inp  = ex["input"]
        gold = ex["output"]
        out  = generate_edit(inp)

        print(f"\n--- RECORD {i} ---")
        print("INPUT:\n", inp, "\n")
        print("GOLD EDIT:\n", gold, "\n")
        print("MODEL EDIT:\n", out, "\n")
        print("-" * 60)

if __name__ == "__main__":
    main()
