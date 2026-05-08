import json
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="EmbedTest Dashboard",
    layout="wide"
)

st.title("EmbedTest AI Testing Dashboard")

st.markdown("---")

# =========================
# Semantic Analysis Section
# =========================

st.header("C Code Semantic Analysis")

analysis_path = Path("ai/c_analysis.json")

if analysis_path.exists():

    with open(analysis_path, "r") as f:
        analysis = json.load(f)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Checksum Algorithm",
        analysis.get("checksum_algorithm", "Unknown")
    )

    col2.metric(
        "Handles NULL Buffers",
        str(analysis.get("handles_null", False))
    )

    col3.metric(
        "Loop Count",
        analysis.get("loop_count", 0)
    )

else:
    st.warning("No semantic analysis found.")

st.markdown("---")

# =========================
# Test Metrics
# =========================

st.header(" Generated Test Metrics")

generated_test_file = Path("tests/generated/test_generated.py")

if generated_test_file.exists():

    content = generated_test_file.read_text()

    test_count = content.count("def test_")

    st.metric(
        "Generated Tests",
        test_count
    )

else:
    st.warning("Generated test file not found.")

st.markdown("---")

# =========================
# Coverage Metrics
# =========================

st.header("Coverage Summary")

coverage_info = Path("coverage_reports/coverage.info")

if coverage_info.exists():

    coverage_text = coverage_info.read_text()

    lines_hit = 0
    lines_found = 0

    for line in coverage_text.splitlines():

        if line.startswith("LF:"):
            lines_found += int(line.split(":")[1])

        if line.startswith("LH:"):
            lines_hit += int(line.split(":")[1])

    if lines_found > 0:

        coverage_percent = round(
            (lines_hit / lines_found) * 100,
            2
        )

        st.metric(
            "Line Coverage %",
            f"{coverage_percent}%"
        )

        st.progress(coverage_percent / 100)

else:
    st.warning("Coverage report not found.")

st.markdown("---")

st.success("EmbedTest pipeline operational.")