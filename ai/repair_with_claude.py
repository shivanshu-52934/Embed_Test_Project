import ast
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

TEST_FILE = "tests/generated/test_generated.py"

with open(TEST_FILE, "r", encoding="utf-8") as f:
    broken_code = f.read()

# -----------------------------------
# Get syntax error
# -----------------------------------

syntax_error = ""

try:
    ast.parse(broken_code)

    print("No syntax errors detected.")
    exit()

except SyntaxError as e:
    syntax_error = str(e)

# -----------------------------------
# Ask Claude to repair code
# -----------------------------------

prompt = f"""
The following Python pytest file contains syntax errors.

Repair ONLY syntax/structural issues.

Do NOT change test logic.

Return ONLY valid Python code.

Syntax error:
{syntax_error}

Broken code:
{broken_code}
"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2000,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

repaired_code = response.content[0].text

# -----------------------------------
# Remove markdown fences
# -----------------------------------

repaired_code = repaired_code.replace(
    "```python",
    ""
)

repaired_code = repaired_code.replace(
    "```",
    ""
)

# -----------------------------------
# Validate repaired code
# -----------------------------------

try:
    ast.parse(repaired_code)

    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write(repaired_code)

    print("Claude successfully repaired syntax.")

except SyntaxError as e:

    print(f"Claude repair still invalid: {e}")