import re
import sys

print(f"Python version: {sys.version}")

# Sample text to test regex behavior
text = '"H"ello" world"'

# Dictionary of patterns using different quantifier modes
patterns = {
    # Greedy quantifier: .* tries to match as much text as possible, then backtracks
    "Greedy      (.*)":   r'"(.*)"',

    # Lazy quantifier: .*? tries to match as little text as possible, expands if needed
    "Lazy        (.*?)":  r'"(.*?)"',

    # Possessive quantifier: .*+ tries to match as much text as possible and refuses to backtrack
    # Note: Supported in Python 3.11+ only
    "Possessive  (.*+)":  r'"(.*+)"',
}

# Loop through each pattern and apply it to the sample text
for desc, pat in patterns.items():
    print(f"\nPattern: {desc} -> {pat}")
    try:
        regex = re.compile(pat)
        m = regex.search(text)
        # Show the matched group or None if no match
        print("  Match:", m.group(1) if m else None)
    except re.error as err:
        # If the regex syntax is invalid (e.g., unsupported possessive), show error
        print("  Error:", err)



import re
import sys

print(f"Python version: {sys.version}")

text = '"Hello" world"'
patterns = {
    "Greedy      ([a-z|\s]+)":   r'"([a-z|\s]+)"',
    "Lazy        ([a-z|\s]+?)":  r'"([a-z|\s]+?)"',
    "Possessive  ([a-z|\s]++)":  r'"([a-z|\s]++)"',
}

for desc, pat in patterns.items():
    print(f"\nPattern: {desc} -> {pat}")
    try:
        regex = re.compile(pat)
        m = regex.search(text)
        print("  Match:", m.group(1) if m else None)
    except re.error as err:
        print("  Error:", err)