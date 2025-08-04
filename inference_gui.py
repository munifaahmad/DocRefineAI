import json
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModelForSeq2SeqLM

VAL_FILE = "val.jsonl"
BASE = "google/flan-t5-small"
ADAPTER = "lora_grant_editor"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(BASE)
    base = AutoModelForSeq2SeqLM.from_pretrained(BASE)
    model = PeftModelForSeq2SeqLM.from_pretrained(base, ADAPTER)
    model.eval()
    return tokenizer, model

def run_inference(text_widget):
    text_widget.insert(tk.END, "Loading model…\n")
    tok, model = load_model()
    text_widget.insert(tk.END, "Model loaded. Running inference on validation set:\n\n")
    with open(VAL_FILE, encoding="utf-8") as f:
        examples = [json.loads(l) for l in f]

    for i, rec in enumerate(examples, start=1):
        inp, gold = rec["input"], rec["output"]
        prompt = rec["instruction"] + "\n\n" + inp
        inputs = tok(prompt, return_tensors="pt", truncation=True, max_length=512)
        out = model.generate(**inputs, max_new_tokens=256)
        pred = tok.decode(out[0], skip_special_tokens=True)

        text_widget.insert(tk.END, f"--- RECORD {i} ---\n")
        text_widget.insert(tk.END, f"INPUT:\n{inp}\n\n")
        text_widget.insert(tk.END, f"GOLD EDIT:\n{gold}\n\n")
        text_widget.insert(tk.END, f"MODEL EDIT:\n{pred}\n")
        text_widget.insert(tk.END, "\n" + ("—"*50) + "\n\n")
        text_widget.see(tk.END)

    text_widget.insert(tk.END, "✅ Done.\n")

def main():
    root = tk.Tk()
    root.title("Grant‐Edit Inference Monitor")
    root.geometry("800x600")

    lbl = tk.Label(root, text="Inference log:", font=("Courier", 12))
    lbl.pack(anchor="nw")

    txt = ScrolledText(root, font=("Courier", 10), wrap="word")
    txt.pack(fill="both", expand=True)

    # run inference in another thread so GUI stays responsive
    threading.Thread(target=run_inference, args=(txt,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
