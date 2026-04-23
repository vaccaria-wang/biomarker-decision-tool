import streamlit as st
from openai import OpenAI
import os

# --- LOAD API KEY FROM STREAMLIT SECRETS ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are a translational biomarker decision system.

Convert user input into a structured, decision-ready biomarker strategy dashboard.

CRITICAL RULES:
- No long paragraphs
- Use headers, tables, bullet points
- Preserve biological detail
- Do not remove biology due to feasibility
- Separate: Biology truth, Measurement reality, Decision role
- Use conditional decisions (GO / CONDITIONAL / NO-GO)
- Always include failure analog

OUTPUT FORMAT:

### 🔴 Decision Summary
- Recommendation:
- Primary driver:
- Key risk:

### 🧠 Biological Context
- Bullet points only

### 🟥 Decision Core
(Table with columns:
Biomarker | Biology Truth | Measurement Reality | Decision Role | Go/No-Go Rule | Risk)

### 🚦 Go / No-Go Logic
- GO:
- CONDITIONAL:
- NO-GO:

### ⚠️ Top Risks (max 3)
1.
2.
3.

### 🧠 Decision Confidence
- Biology:
- Measurement:
- Decision:

### 💥 Failure Analog
- Study / program:
- Link:
- Insight:

### 🟢 Minimal Viable Strategy
- Primary:
- Secondary:
- Supporting:
- Ignore for now:

### 🔁 Alternative Path
- If:
- Then:

### 🔁 Fallback Strategy
- Bullet points
"""

# --- PAGE CONFIG ---
st.set_page_config(page_title="Biomarker Decision Tool", layout="wide")

# --- TITLE ---
st.title("🧬 Translational Biomarker Decision Tool")

# --- INPUT ---
user_input = st.text_input(
    "Enter disease, gene, or program:",
    placeholder="e.g. SYNGAP1, Alzheimer's tau therapy Phase 2"
)

# --- RUN BUTTON ---
if st.button("Run Analysis") and user_input:

    with st.spinner("Analyzing..."):
        try:
            response = client.chat.completions.create(
                model="gpt-5.3",
                temperature=0.3,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
            )

            output = response.choices[0].message.content

            # --- DISPLAY RESULT ---
            st.markdown(output)

        except Exception as e:
            st.error(f"Error: {e}")