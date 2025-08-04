# DocRefineAI

DocRefineAI is an AI-powered in-place document refinement system built for nonprofits. It ingests client-submitted `.docx` templates and, using a fine-tuned T5 model trained on real before/after edits, rewrites each paragraph for clarity, active voice, consistent metrics, and clean formatting—while preserving the original template structure. Known finalized documents are returned instantly via exact-match lookup.

## Key Features

- Fine-tuned T5 model on real .docx before/after pairs  
- Preserves Word template structure (headings, tables, layout)  
- Paragraph-by-paragraph edits: active voice, punctuation, number standardization (e.g., “twenty-five”), placeholder removal  
- Bullet formatting for program descriptions: “• Program Title – Description”  
- Duplicate suppression and prompt leakage filtering  
- Exact-match hash lookup to instantly serve previously approved final documents  
- Simple upload API via FastAPI for seamless integration

## Quick Start

1. Place original and target `.docx` pairs in `known_inputs/` and `known_targets/`.  
2. Fine-tune the model with your before/after examples (`python finetune_t5.py`).  
3. Run the server:  
   ```bash
   uvicorn app:app --reload
