import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App setup
st.set_page_config(page_title="Census Data Analysis Dashboard", layout="wide")
st.title("📊 Census Data Analysis Dashboard - by Prem Kumar")

# File upload
uploaded_file = st.file_uploader("📂 Upload your Census CSV file", type="csv")

if uploaded_file is not None:
    column_names = [
        'Age', 'Education', 'Marital_Status', 'Gender',
        'Occupation', 'Income', 'Parents_Present',
        'Country', 'Native', 'Weeks_Worked'
    ]

    data = pd.read_csv(uploaded_file, names=column_names, header=None)

    # Convert numeric columns
    data['Income'] = pd.to_numeric(data['Income'], errors='coerce')
    data['Weeks_Worked'] = pd.to_numeric(data['Weeks_Worked'], errors='coerce')
    data['Age'] = pd.to_numeric(data['Age'], errors='coerce')

    st.success("✅ File uploaded successfully!")
    st.subheader("🔍 Data Preview")
    st.dataframe(data.head())

    # Sidebar operations
    st.sidebar.header("📊 Choose an Analysis")
    options = st.sidebar.multiselect(
        "Select analyses:",
        [
            "Education Distribution",           # Graph ✅
            "Gender-wise Total Income",         # Graph ✅
            "Tax Estimation by Gender",         # Graph ✅
            "Average Income by Education",      # Graph ✅
            "Income by Country",                # Graph ✅
            "Employable Widows & Divorced",
            "Senior Citizens (55–60)",
            "Citizens Above 60",
            "Working Population %",
            "Non-Citizens Working %",
            "Citizens Age >23 Unemployed",
            "Education vs Gender Count",
            "Orphans by Parents & Gender",
            "Parents Presence Distribution"
        ]
    )

    # Helper for bar chart
    def plot_bar(data_series, title, xlabel="", ylabel="Value"):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=data_series.index, y=data_series.values, palette="viridis", ax=ax)
        plt.xticks(rotation=45, ha='right')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        st.pyplot(fig)

    # === Only 5 Graphs ===
    if "Education Distribution" in options:
        st.subheader("🎓 Education Distribution")
        edu_counts = data['Education'].value_counts()
        plot_bar(edu_counts, "Education Distribution", "Education Level")

    if "Gender-wise Total Income" in options:
        st.subheader("💵 Gender-wise Total Income")
        gender_income = data.groupby('Gender')['Income'].sum()
        fig, ax = plt.subplots()
        ax.pie(gender_income, labels=gender_income.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig)

    if "Tax Estimation by Gender" in options:
        st.subheader("💸 Estimated Tax by Gender (10%)")
        tax = data.groupby('Gender')['Income'].sum() * 0.10
        plot_bar(tax, "Tax Estimation by Gender", "Gender", "Tax Amount")

    if "Average Income by Education" in options:
        st.subheader("📈 Average Income by Education Level")
        avg_income = data.groupby('Education')['Income'].mean().sort_values(ascending=False)
        plot_bar(avg_income, "Average Income by Education", "Education", "Avg Income")

    if "Income by Country" in options:
        st.subheader("🌍 Income Distribution by Country")
        country_income = data.groupby('Country')['Income'].sum().sort_values(ascending=False)
        plot_bar(country_income, "Total Income by Country", "Country", "Total Income")

    # === Other analyses (no graphs) ===
    if "Employable Widows & Divorced" in options:
        st.subheader("👩 Employable Widows & Divorced")
        emp = data[
            (data['Marital_Status'].isin(['Widowed', 'Divorced'])) &
            (data['Occupation'] != 'Unemployed')
        ]
        st.write(f"Count: {emp.shape[0]}")
        st.dataframe(emp)

    if "Senior Citizens (55–60)" in options:
        st.subheader("👴 Senior Citizens (55–60)")
        senior = data[(data['Age'] >= 55) & (data['Age'] < 60)]
        st.write(f"Count: {senior.shape[0]}")
        st.dataframe(senior)

    if "Citizens Above 60" in options:
        st.subheader("👵 Citizens Above 60")
        old = data[(data['Age'] > 60) & (data['Country'] == 'Citizen')]
        st.write(f"Count: {old.shape[0]}")
        st.dataframe(old)

    if "Working Population %" in options:
        st.subheader("⚙️ Working Population Percentage")
        working = data[data['Occupation'] != 'Unemployed']
        percent = (len(working) / len(data)) * 100
        st.write(f"Working Population: {percent:.2f}%")

    if "Non-Citizens Working %" in options:
        st.subheader("🌎 Non-Citizens Working Percentage")
        non_cit = data[data['Country'] != 'Citizen']
        working_nc = non_cit[non_cit['Occupation'] != 'Unemployed']
        percent = (len(working_nc) / len(non_cit) * 100) if len(non_cit) > 0 else 0
        st.write(f"{percent:.2f}% of Non-Citizens are Employed")

    if "Citizens Age >23 Unemployed" in options:
        st.subheader("🙍 Citizens Age >23 Without Employment")
        unemployed = data[
            (data['Age'] > 23) &
            (data['Occupation'] == 'Unemployed') &
            (data['Country'] == 'Citizen')
        ]
        st.write(f"Total: {unemployed.shape[0]}")
        st.dataframe(unemployed)

    if "Education vs Gender Count" in options:
        st.subheader("📘 Education vs Gender Count")
        edu_gender = data.groupby(['Education', 'Gender']).size().reset_index(name='Count')
        st.dataframe(edu_gender)

    if "Orphans by Parents & Gender" in options:
        st.subheader("🧒 Orphans by Parents & Gender")
        orphan = data.groupby(['Parents_Present', 'Gender']).size().reset_index(name='Count')
        st.dataframe(orphan)

    if "Parents Presence Distribution" in options:
        st.subheader("👨‍👩‍👧 Parents Presence Distribution")
        parents = data['Parents_Present'].value_counts()
        st.dataframe(parents)

else:
    st.info("👆 Please upload a CSV file to begin.")

