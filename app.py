import streamlit as st
import subprocess
from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------

st.set_page_config(
    page_title="Procurement Decision Agent",
    page_icon="📦",
    layout="wide"
)

PROJECT_DIR = Path(__file__).parent
DATA_FILE = PROJECT_DIR / "data" / "suppliers.csv"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "recommendation" not in st.session_state:
    st.session_state.recommendation = None

if "output_file" not in st.session_state:
    st.session_state.output_file = None

if "claude_details" not in st.session_state:
    st.session_state.claude_details = None

if "decision" not in st.session_state:
    st.session_state.decision = "Pending Review"


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("📦 Procurement Decision Agent")

st.caption(
    "Multi-Agent Supplier Allocation using Claude Code"
)

st.write(
    "This agent analyses supplier data using Cost, Performance "
    "and Risk subagents and recommends how a procurement order "
    "can be allocated across suppliers."
)

st.divider()


# ---------------------------------------------------
# LOAD SUPPLIER DATA
# ---------------------------------------------------

try:

    suppliers = pd.read_csv(DATA_FILE)

except Exception as e:

    st.error(f"Could not load supplier data: {e}")
    st.stop()


st.subheader("Supplier Data")

st.dataframe(
    suppliers,
    width="stretch",
    hide_index=True
)

st.divider()


# ---------------------------------------------------
# PURCHASE REQUIREMENT
# ---------------------------------------------------

st.subheader("Purchase Requirement")

quantity = st.number_input(
    "Enter required quantity",
    min_value=1,
    value=8000,
    step=500
)


# ---------------------------------------------------
# GET LATEST OUTPUT
# ---------------------------------------------------

def get_latest_output():

    files = list(
        OUTPUT_DIR.glob("recommendation_*.md")
    )

    if not files:
        return None

    return max(
        files,
        key=lambda f: f.stat().st_mtime
    )


# ---------------------------------------------------
# RUN AGENT BUTTON
# ---------------------------------------------------

if st.button(
    "🚀 Run Procurement Agent",
    type="primary"
):

    prompt = f"""
Run the Procurement Decision Agent for {quantity} units.

Use the existing Cost Analyst, Performance Analyst and Risk Analyst.

Use only data/suppliers.csv.

Return:

- Cost Analyst findings
- Performance Analyst findings
- Risk Analyst findings
- Recommended supplier allocation
- Quantity allocated to each supplier
- Total procurement cost
- Key risks
- Short reasoning

Save the recommendation as a new markdown file inside output/.

Do not finalize the procurement decision.

Keep:

Status: HUMAN APPROVAL REQUIRED

Be concise.
"""

    with st.spinner(
        "Claude multi-agent analysis is running. "
        "This may take 1–4 minutes..."
    ):

        try:

            result = subprocess.run(
                ["claude.cmd", "-p"],
                cwd=str(PROJECT_DIR),
                input=prompt,
                capture_output=True,
                text=True,
                timeout=240
            )

        except subprocess.TimeoutExpired:

            st.error(
                "The agent took more than 4 minutes."
            )

            st.stop()

        except Exception as e:

            st.error(
                f"Error while running agent: {e}"
            )

            st.stop()


    # ---------------------------------------------------
    # CHECK RESULT
    # ---------------------------------------------------

    if result.returncode != 0:

        st.error("Agent execution failed.")

        st.code(
            result.stderr
        )

    else:

        latest_file = get_latest_output()

        if latest_file is None:

            st.warning(
                "Claude completed but no output file was created."
            )

            st.session_state.claude_details = result.stdout

        else:

            recommendation = latest_file.read_text(
                encoding="utf-8"
            )

            # SAVE RESULT IN SESSION STATE
            st.session_state.recommendation = recommendation
            st.session_state.output_file = latest_file.name
            st.session_state.claude_details = result.stdout

            st.session_state.decision = "Pending Review"

            st.success(
                "✅ Multi-agent analysis completed"
            )


# ---------------------------------------------------
# DISPLAY SAVED RESULT
# ---------------------------------------------------

if st.session_state.recommendation:

    st.divider()

    st.subheader(
        "📋 Procurement Recommendation"
    )

    st.markdown(
        st.session_state.recommendation
    )

    st.info(
        f"Saved as: {st.session_state.output_file}"
    )

    st.divider()


    # ---------------------------------------------------
    # HUMAN REVIEW
    # ---------------------------------------------------

    st.subheader(
        "👤 Human Review"
    )

    st.warning(
        "Status: HUMAN APPROVAL REQUIRED"
    )

    st.write(
        "This is an AI-generated recommendation only. "
        "The final procurement decision remains with "
        "the human procurement manager."
    )

    decision = st.radio(
        "Review decision",
        [
            "Pending Review",
            "Approve Recommendation",
            "Request Changes",
            "Reject Recommendation"
        ],
        key="decision"
    )


    # ---------------------------------------------------
    # APPROVE
    # ---------------------------------------------------

    if decision == "Approve Recommendation":

        st.success(
            "✅ Human approval indicated."
        )

        st.write(
            "The recommendation has been reviewed by the human user."
        )

        st.info(
            "Formal procurement sign-off remains the responsibility "
            "of the procurement manager."
        )


    # ---------------------------------------------------
    # REQUEST CHANGES
    # ---------------------------------------------------

    elif decision == "Request Changes":

        st.warning(
            "Human reviewer has requested changes."
        )

        changes = st.text_area(
            "Describe the changes required",
            key="change_request"
        )

        if st.button(
            "Record Change Request"
        ):

            if changes.strip():

                st.success(
                    "Change request recorded."
                )

                st.write(
                    changes
                )

            else:

                st.warning(
                    "Please describe the requested changes."
                )


    # ---------------------------------------------------
    # REJECT
    # ---------------------------------------------------

    elif decision == "Reject Recommendation":

        st.error(
            "❌ Recommendation rejected by human reviewer."
        )

        st.write(
            "The recommendation will not be treated as a final procurement decision."
        )


    # ---------------------------------------------------
    # TECHNICAL DETAILS
    # ---------------------------------------------------

    if st.session_state.claude_details:

        with st.expander(
            "🔍 Technical execution details"
        ):

            st.text(
                st.session_state.claude_details
            )


# ---------------------------------------------------
# RESET BUTTON
# ---------------------------------------------------

if st.session_state.recommendation:

    st.divider()

    if st.button(
        "🔄 Start New Analysis"
    ):

        st.session_state.recommendation = None
        st.session_state.output_file = None
        st.session_state.claude_details = None
        st.session_state.decision = "Pending Review"

        st.rerun()


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Built using Claude Code | "
    "Cost Analyst + Performance Analyst + Risk Analyst"
)