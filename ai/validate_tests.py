import ast
import json
import re

TEST_FILE = "tests/generated/test_generated.py"
ANALYSIS_FILE = "ai/c_analysis.json"

with open(TEST_FILE, "r", encoding="utf-8") as f:
    content = f.read()

with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
    analysis = json.load(f)

issues = []

# -----------------------------------
# Syntax validation
# -----------------------------------

try:
    ast.parse(content)

except SyntaxError as e:
    issues.append(
        f"Syntax error detected: {e}"
    )

# -----------------------------------
# Structural checks
# -----------------------------------

if "```" in content:
    issues.append("Markdown fences detected.")

forbidden_imports = [
    "subprocess",
    "os.system",
    "shutil"
]

for imp in forbidden_imports:
    if imp in content:
        issues.append(f"Forbidden usage detected: {imp}")

if "ctypes.CDLL" not in content:
    issues.append("Missing ctypes.CDLL usage.")

expected_functions = [
    "compute_checksum",
    "validate_checksum"
]

for func in expected_functions:
    if func not in content:
        issues.append(f"Expected function missing: {func}")

if "libsensor.so" not in content:
    issues.append("Incorrect shared library reference.")

# -----------------------------------
# Semantic validation
# -----------------------------------

checksum_algorithm = analysis.get(
    "checksum_algorithm",
    "unknown"
)

if checksum_algorithm == "xor":

    suspicious_patterns = [
    r"&\s*0xFF",
    r"\bsum\s*\("
]

    for pattern in suspicious_patterns:
        if re.search(pattern, content):
            issues.append(
                "Generated tests may assume SUM checksum logic instead of XOR."
            )
            break

# -----------------------------------
# Final report
# -----------------------------------

print("\n=== VALIDATION REPORT ===\n")

if not issues:
    print("No obvious issues detected.")

else:
    for issue in issues:
        print(f"[WARNING] {issue}")