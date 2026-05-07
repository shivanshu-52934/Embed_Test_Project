import json
import re

C_FILE = "c_modules/sensor_parser.c"

with open(C_FILE, "r", encoding="utf-8") as f:
    c_code = f.read()

analysis = {}

# -----------------------------------
# Detect checksum algorithm
# -----------------------------------

if "^=" in c_code or "^" in c_code:
    analysis["checksum_algorithm"] = "xor"

elif "+" in c_code:
    analysis["checksum_algorithm"] = "sum"

else:
    analysis["checksum_algorithm"] = "unknown"

# -----------------------------------
# Detect null checks
# -----------------------------------

if "NULL" in c_code:
    analysis["handles_null"] = True
else:
    analysis["handles_null"] = False

# -----------------------------------
# Detect loops
# -----------------------------------

loop_count = len(re.findall(r"\bfor\b|\bwhile\b", c_code))

analysis["loop_count"] = loop_count

# -----------------------------------
# Save analysis
# -----------------------------------

output_path = "ai/c_analysis.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(analysis, f, indent=4)

print("\n=== C CODE ANALYSIS ===\n")

print(json.dumps(analysis, indent=4))