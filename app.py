import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Procurement Decision Agent",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Procurement Decision Agent")
st.write(
    "AI-assisted supplier allocation based on cost, quality, delivery, capacity and risk."
)

# Load supplier data
df = pd.read_csv("data/suppliers.csv")

st.subheader("Supplier Data")
st.dataframe(df, use_container_width=True)

st.subheader("Purchase Requirement")

quantity = st.number_input(
    "Enter required quantity",
    min_value=1,
    value=8000,
    step=500
)

if st.button("Run Procurement Analysis"):

    st.info("Running Cost, Performance and Risk analysis...")

    # Remove high-risk suppliers
    eligible = df[df["Risk Level"].str.lower() != "high"].copy()

    # Sort by unit price
    eligible = eligible.sort_values("Unit Price")

    remaining = quantity
    allocation = []

    for _, row in eligible.iterrows():

        if remaining <= 0:
            break

        qty = min(remaining, int(row["Capacity"]))
        cost = qty * row["Unit Price"]

        allocation.append({
            "Supplier": row["Supplier"],
            "Units Allocated": qty,
            "Unit Price": row["Unit Price"],
            "Cost": cost,
            "Risk Level": row["Risk Level"]
        })

        remaining -= qty

    result = pd.DataFrame(allocation)

    if remaining > 0:
        st.error(
            f"Not enough eligible supplier capacity. "
            f"Shortfall: {remaining} units."
        )
    else:
        total_cost = result["Cost"].sum()

        st.success("Analysis completed")

        st.subheader("Recommended Allocation")
        st.dataframe(result, use_container_width=True)

        st.metric(
            "Total Procurement Cost",
            f"${total_cost:,.2f}"
        )

        st.subheader("Agent Findings")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 💰 Cost Analyst")
            cheapest = df.loc[df["Unit Price"].idxmin()]
            st.write(
                f"Cheapest supplier: {cheapest['Supplier']} "
                f"at ${cheapest['Unit Price']}"
            )

        with col2:
            st.markdown("### 📊 Performance Analyst")
            best_quality = df.loc[df["Quality Score"].idxmax()]
            st.write(
                f"Highest quality supplier: "
                f"{best_quality['Supplier']} "
                f"({best_quality['Quality Score']})"
            )

        with col3:
            st.markdown("### ⚠️ Risk Analyst")
            high_risk = df[
                df["Risk Level"].str.lower() == "high"
            ]

            if len(high_risk) > 0:
                st.write(
                    "High-risk supplier(s): "
                    + ", ".join(high_risk["Supplier"].tolist())
                )
            else:
                st.write("No high-risk suppliers identified.")

        st.warning(
            "Status: HUMAN APPROVAL REQUIRED"
        )

        st.write(
            "This is an AI-generated recommendation. "
            "The final procurement decision remains with the procurement manager."
        )