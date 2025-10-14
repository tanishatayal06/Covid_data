import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("COVID-19 Dataset Storytelling Dashboard 🦠")

try:
    df = pd.read_csv("country_wise_latest.csv")
except FileNotFoundError:
    st.error("Error: 'country_wise_latest.csv' not found. Make sure the CSV file is in the same folder as your script.")
    st.stop()

st.sidebar.header("Filter Data")


country_filter = st.sidebar.multiselect(
    "Select Countries",
    options=df['Country/Region'].unique(),
    default=df['Country/Region'].unique()[:5]  # first 5 by default
)

filtered_df = df[df['Country/Region'].isin(country_filter)]

st.write("### Filtered COVID-19 Dataset")
st.dataframe(filtered_df)

st.write("### Summary Statistics")
st.write(filtered_df.describe())

if not filtered_df.empty:
    st.header("1️⃣ Basic Visualizations")


    st.subheader("Confirmed Cases by Country")
    fig1, ax1 = plt.subplots()
    sns.barplot(data=filtered_df, x="Country/Region", y="Confirmed", ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.subheader("Confirmed vs Deaths")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=filtered_df, x="Confirmed", y="Deaths", hue="Country/Region", ax=ax2)
    st.pyplot(fig2)

    st.subheader("Confirmed vs Recovered")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=filtered_df, x="Confirmed", y="Recovered", hue="Country/Region", ax=ax3)
    st.pyplot(fig3)

    if "Deaths" in filtered_df.columns and "Confirmed" in filtered_df.columns:
        st.subheader("Death Rate Distribution")
        filtered_df["DeathRate"] = (filtered_df["Deaths"] / filtered_df["Confirmed"].replace(0, 1)) * 100
        fig4, ax4 = plt.subplots()
        sns.boxplot(data=filtered_df, y="DeathRate", ax=ax4)
        ax4.set_ylabel("Death Rate (%)")
        st.pyplot(fig4)

    st.header("2️⃣ Misleading Visualization")

    st.subheader("Deaths by Country (Truncated Y-axis ❌)")
    fig5, ax5 = plt.subplots()
    sns.barplot(data=filtered_df, x="Country/Region", y="Deaths", ax=ax5)
    ax5.set_ylim(filtered_df["Deaths"].min() - 100, filtered_df["Deaths"].min() + 500)  # Misleading zoom-in
    plt.xticks(rotation=45)
    st.pyplot(fig5)
    st.caption("⚠️ Wrong: Truncated Y-axis exaggerates small differences.")


    st.header("3️⃣ Corrected Visualization")

    st.subheader("Deaths by Country (Proper Scale ✅)")
    fig6, ax6 = plt.subplots()
    sns.barplot(data=filtered_df.sort_values("Deaths", ascending=False),
                x="Country/Region", y="Deaths", ax=ax6, palette="Reds")
    plt.xticks(rotation=45)
    st.pyplot(fig6)
    st.caption("✅ Correct: Full Y-axis shows the true scale of differences.")

else:
    st.warning("No data available for selected countries.")