#!/usr/bin/env python3
"""
Build a mixed LiveBench dataset from multiple topics and save to data/ directory.

This script extracts specific fields from LiveBench datasets on Hugging Face:
- category
- turns
- ground_truth
- question_id

Usage:
    python src/data_prep.py
"""

from pathlib import Path
from typing import List, Tuple

import pandas as pd
from datasets import load_dataset 

# -----------------------------
# CONFIG
# -----------------------------

# (Hugging Face dataset name, topic label)
DATASETS: List[Tuple[str, str]] = [
    ("livebench/math", "math"),
    ("livebench/coding", "coding"),
    ("livebench/reasoning", "reasoning"),
    ("livebench/data_analysis", "data_analysis"),
    ("livebench/language", "language"),
]

# Number of examples to sample per topic (None = use full test split)
SAMPLES_PER_TOPIC: int = 200  # adjust as needed

# Get the project root directory (parent of src/)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "data"
OUTPUT_JSONL = OUTPUT_DIR / "livebench_mixed.jsonl"


# -----------------------------
# MAIN
# -----------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_dfs: List[pd.DataFrame] = []

    for ds_name, topic in DATASETS:
        print(f"Loading dataset: {ds_name} (topic={topic})")
        ds = load_dataset(ds_name, split="test")

        # Shuffle for randomness
        ds = ds.shuffle(seed=42)

        # Subsample if requested
        if SAMPLES_PER_TOPIC is not None and SAMPLES_PER_TOPIC < len(ds):
            ds = ds.select(range(SAMPLES_PER_TOPIC))

        rows = []
        for ex in ds:
            # Extract ONLY the requested fields
            # category, turns, ground_truth, question_id
            
            category = ex.get("category", topic) # Fallback to topic if category missing
            turns = ex.get("turns", [])
            ground_truth = ex.get("ground_truth", "")
            question_id = ex.get("question_id", "")
            
            # Additional check for missing question_id fallback
            if not question_id:
                 for key in ("id", "sample_id", "task_id", "raw_id"):
                     if key in ex and ex[key] is not None:
                         question_id = str(ex[key])
                         break
            
            rows.append(
                {
                    "question_id": question_id,
                    "category": category,
                    "turns": turns,
                    "ground_truth": ground_truth,
                }
            )

        df_topic = pd.DataFrame(rows)
        print(f"  -> collected {len(df_topic)} examples")
        all_dfs.append(df_topic)

    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"Total combined examples: {len(combined)}")

    # Save to JSONL (standard format for NLP datasets)
    combined.to_json(OUTPUT_JSONL, orient="records", lines=True)

    print(f"Saved JSONL to: {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()
