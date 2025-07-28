import fitz  # PyMuPDF
import re
import json

def extract_title(doc):
    # Tries to find a good title from the first page
    title_candidates = doc[0].get_text("text").split("\n")
    for line in title_candidates:
        if "Red Hat Enterprise Agreement" in line:
            return line.strip()
    return "Extracted PDF Title"

def is_heading(line):
    """
    Match headings like:
    - "1. Term"
    - "10. Confidentiality"
    - "PRODUCT APPENDIX 2A TRAINING AND TRAINING UNITS"
    """
    line = line.strip()
    if re.match(r"^\d{1,2}\.\s+[A-Z]", line):
        return True
    if re.match(r"^PRODUCT APPENDIX.*", line, re.IGNORECASE):
        return True
    return False

def extract_headings(doc):
    outline = []
    for page_num, page in enumerate(doc):
        lines = page.get_text("text").split("\n")
        for line in lines:
            clean = line.strip()
            if is_heading(clean):
                outline.append({
                    "level": "H1",
                    "text": clean,
                    "page": page_num + 1
                })
    return outline

def main():
    input_pdf = "sample.pdf.pdf"  # Change this to your PDF filename
    output_json = "output.json"

    doc = fitz.open(input_pdf)

    result = {
        "title": extract_title(doc),
        "outline": extract_headings(doc)
    }

    # Save JSON
    with open(output_json, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Extracted {len(result['outline'])} headings.")
    print(f"📄 Output saved to {output_json}\n")

    # Optional: Print headings to terminal
    for h in result["outline"]:
        print(f"[Page {h['page']}] {h['text']}")

if __name__ == "__main__":
    main()
