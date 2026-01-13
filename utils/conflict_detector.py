import re

def detect_conflicts(chunks):
    conflicts = []
    combined = " || ".join(chunks).lower()

    if "shall" in combined and "shall not" in combined:
        conflicts.append("Possible contradiction: shall vs shall not")

    amounts = re.findall(r"\$\s*\d+(?:[,\d]*)?", combined)
    if len(set(amounts)) > 1:
        conflicts.append("Multiple monetary values detected")

    return conflicts
