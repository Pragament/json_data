import requests
import json
import hashlib
import re 
import os

TOPICS_URL = "https://staticapis.pragament.com/textbooks/page_attributes/66a75c91853f0633ba01ec73.json"

# Extract 24-char hex ID from URL
match = re.search(r'/([a-f0-9]{24})\.json$', TOPICS_URL)
if match:
    file_id = match.group(1)
else:
    file_id = "output"

# Use last 6 digits of file_id (converted from hex to int) as base formula ID
base_formula_id = int(file_id[-6:], 16)

OUTPUT_DIR = "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, f"{file_id}-formulas.json")

# Add or extend known formulas related to chapters
FORMULA_MAP = {
    "Real Numbers": "a^m * a^n = a^(m+n)",
    "Linear Equations": "y = mx + b",
    "Triangles": "Area = (1/2) * base * height",
    "Surface Areas and Volumes": "Volume of cube = a^3",
    "Statistics": "Mean = Sum of observations / Number of observations",
    "Probability": "P(E) = Number of favorable outcomes / Total outcomes"
}

def hash_id(text):
    return abs(int(hashlib.md5(text.encode()).hexdigest(), 16)) % 10**6

def fetch_chapter_formulas():
    response = requests.get(TOPICS_URL)
    response.raise_for_status()
    pages = response.json()

    formulas = []
    found_chapters = []
    formula_counter = 0

    for page in pages:
        if page.get("type") == "chapter":
            chapter_name = page.get("text", "").strip()
            if chapter_name:
                found_chapters.append(chapter_name)
                if chapter_name in FORMULA_MAP:
                    formula_id = base_formula_id + formula_counter
                    formula_counter += 1
                    formulas.append({
                        "formula_id": formula_id,
                        "formula_text": FORMULA_MAP[chapter_name],
                        "topic_id": hash_id(chapter_name),
                        "chapter": chapter_name
                    })

    # Print all chapter names to terminal
    print("📚 Chapters found in textbook:")
    for ch in found_chapters:
        print("-", ch)

    # Save formulas to JSON
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(formulas, f, indent=4, ensure_ascii=False)

    print(f"\n✅ {len(formulas)} formulas saved to '{OUTPUT_PATH}'")

if __name__ == "__main__":
    fetch_chapter_formulas()
