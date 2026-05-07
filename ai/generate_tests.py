import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Read header file
with open("c_modules/sensor_parser.h", "r") as f:
    header_content = f.read()

prompt = f"""
You are generating pytest test cases for embedded C code.

Given this C header file:

{header_content}

Generate ONLY valid Python pytest code using ctypes.

Requirements:
- Load shared library: c_modules/libsensor.so
- Use ctypes correctly
- Include:
    - normal test cases
    - boundary cases
    - invalid input cases
- Output ONLY executable Python code
- No markdown
- No explanations
"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1200,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

generated_code = response.content[0].text

output_path = "tests/generated/test_generated.py"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(generated_code)

print(f"Generated test file saved to: {output_path}")