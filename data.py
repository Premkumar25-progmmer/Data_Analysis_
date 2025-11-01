import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup
st.set_page_config(page_title="Census Data Analysis Dashboard", layout="wide")
st.title("📊 Census Data Analysis Dashboard - Developed by Prem Kumar")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload Census CSV File", type="csv")

if uploaded_file is not None:
    # Define columns manually (if CSV has no header)
    column_names = [
        'Age', 'Education', 'Marital_Status', 'Gender',
        'Occupation', 'Income', 'Parents_Present',
        'Country', 'Native', 'Weeks_Worked'
    ]
    data = pd.read_csv(uploaded_file, names=column_names, header=None)
    st.success("✅ File uploaded successfully!")

    # Convert numeric fields
    data['Income'] = pd.to_numeric(data['Income'], errors='coerce')
    data['Weeks_Worked'] = pd.to_numeric(data['Weeks_Worked'], errors='coerce')
    data['Age'] = pd.to_numeric(data['Age'], errors='coerce')

    # Sidebar for selecting multiple operations
    st.sidebar.header("📊 Select Analysis Operations")
    operations = st.sidebar.multiselect(
        "Choose analyses to perform:",
        [
            "Education Distribution",
            "Average Income by Education",
            "Gender-wise Total Income",
            "Tax Estimation by Gender",
            "Employable Widows & Divorced",
            "Senior Citizens (55–60)",
            "Citizens Above 60",
            "Citizens Age >23 Unemployed",
            "Working Population %",
            "Non-Citizens Working %",
            "Income by Country",
            "Income by Occupation",
            "Top 5 Occupations by Income",
            "Per Capita Income by Gender",
            "Average Weeks Worked by Education",
            "Orphans by Parents & Gender",
            "Education vs Gender Count",
            "Parents Presence Distribution",
            "Education Level Count",
            "Gender Ratio by Occupation",
            "Income Distribution (Histogram)",
            "Income vs Age (Scatter Plot)",
            "Gender-wise Income (Pie Chart)",
            "Education vs Avg Income (Bar)",
            "Income Share by Citizens vs Non-Citizens"
        ]
    )

    # Function for bar chart plotting
    def plot_bar(data_series, title, xlabel="", ylabel="Count"):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=data_series.index, y=data_series.values, palette="viridis", ax=ax)
        plt.xticks(rotation=45, ha='right')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        st.pyplot(fig)

    # Now perform selected operations
    if "Education Distribution" in operations:
        st.subheader("🎓 Education Distribution")
        edu_counts = data['Education'].value_counts()
        plot_bar(edu_counts, "Education Distribution", "Education Level")

    if "Average Income by Education" in operations:
        st.subheader("💰 Average Income by Education")
        avg_income = data.groupby('Education')['Income'].mean().sort_values(ascending=False)
        plot_bar(avg_income, "Average Income by Education", "Education", "Average Income")

    if "Gender-wise Total Income" in operations:
        st.subheader("💵 Gender-wise Total Income")
        gender_income = data.groupby('Gender')['Income'].sum()
        plot_bar(gender_income, "Total Income by Gender", "Gender", "Total Income")

    if "Tax Estimation by Gender" in operations:
        st.subheader("💸 Estimated Tax by Gender (10%)")
        tax_rate = 0.10
        tax = data.groupby('Gender')['Income'].sum() * tax_rate
        plot_bar(tax, "Tax to Collect by Gender", "Gender", "Tax Amount")

    if "Employable Widows & Divorced" in operations:
        st.subheader("👩 Employable Widows & Divorced")
        emp = data[
            (data['Marital_Status'].isin(['Widowed', 'Divorced'])) &
            (data['Occupation'] != 'Unemployed')
        ]
        st.write(f"Count: {emp.shape[0]}")
        st.dataframe(emp)

    if "Senior Citizens (55–60)" in operations:
        st.subheader("👴 Senior Citizens (55–60)")
        senior = data[(data['Age'] >= 55) & (data['Age'] < 60)]
        st.write(f"Total: {senior.shape[0]}")
        st.dataframe(senior)

    if "Citizens Above 60" in operations:
        st.subheader("👵 Citizens Above Age 60")
        old = data[(data['Age'] > 60) & (data['Country'] == 'Citizen')]
        st.write(f"Total: {old.shape[0]}")
        st.dataframe(old)

    if "Citizens Age >23 Unemployed" in operations:
        st.subheader("🙍‍♂️ Citizens Age >23 Without Employment")
        unemployed = data[
            (data['Age'] > 23) & (data['Occupation'] == 'Unemployed') & (data['Country'] == 'Citizen')
        ]
        st.write(f"Count: {unemployed.shape[0]}")
        st.dataframe(unemployed)

    if "Working Population %" in operations:
        st.subheader("⚙️ Working Population Percentage")
        working = data[data['Occupation'] != 'Unemployed']
        percent = (len(working) / len(data)) * 100
        st.write(f"Working Population: {percent:.2f}%")

    if "Non-Citizens Working %" in operations:
        st.subheader("🌍 Non-Citizens Working Percentage")
        non_cit = data[data['Country'] != 'Citizen']
        working_nc = non_cit[non_cit['Occupation'] != 'Unemployed']
        percent = (len(working_nc) / len(non_cit) * 100) if len(non_cit) > 0 else 0
        st.write(f"{percent:.2f}% of Non-Citizens are Employed")

    if "Income by Country" in operations:
        st.subheader("🌎 Income Distribution by Country")
        country_income = data.groupby('Country')['Income'].sum().sort_values(ascending=False)
        plot_bar(country_income, "Total Income by Country", "Country", "Total Income")

    if "Income by Occupation" in operations:
        st.subheader("💼 Income by Occupation")
        occ_income = data.groupby('Occupation')['Income'].sum().sort_values(ascending=False)
        plot_bar(occ_income, "Income by Occupation", "Occupation", "Income")

    if "Top 5 Occupations by Income" in operations:
        st.subheader("🏆 Top 5 Occupations by Income")
        top5 = data.groupby('Occupation')['Income'].sum().nlargest(5)
        plot_bar(top5, "Top 5 Occupations by Income", "Occupation", "Total Income")

    if "Per Capita Income by Gender" in operations:
        st.subheader("💹 Per Capita Income by Gender")
        pci = data.groupby('Gender')['Income'].mean()
        plot_bar(pci, "Average Income per Person by Gender", "Gender", "Per Capita Income")

    if "Average Weeks Worked by Education" in operations:
        st.subheader("📆 Average Weeks Worked by Education")
        avg_weeks = data.groupby('Education')['Weeks_Worked'].mean()
        plot_bar(avg_weeks, "Average Weeks Worked by Education", "Education", "Weeks Worked")

    if "Orphans by Parents & Gender" in operations:
        st.subheader("🧒 Orphans by Parents Presence & Gender")
        parent_stats = data.groupby(['Parents_Present', 'Gender']).size().reset_index(name='Count')
        st.dataframe(parent_stats)

    if "Education vs Gender Count" in operations:
        st.subheader("📘 Education vs Gender Count")
        edu_gender = data.groupby(['Education', 'Gender']).size().reset_index(name='Count')
        st.dataframe(edu_gender)

    if "Parents Presence Distribution" in operations:
        st.subheader("👨‍👩‍👧 Parents Presence Distribution")
        parents = data['Parents_Present'].value_counts()
        plot_bar(parents, "Parents Presence Distribution", "Parents_Present")

    if "Education Level Count" in operations:
        st.subheader("🎓 Education Level Count")
        edu_count = data['Education'].value_counts()
        st.dataframe(edu_count)

    if "Gender Ratio by Occupation" in operations:
        st.subheader("⚖️ Gender Ratio by Occupation")
        gender_occ = data.groupby(['Occupation', 'Gender']).size().unstack(fill_value=0)
        st.dataframe(gender_occ)

    if "Income Distribution (Histogram)" in operations:
        st.subheader("📊 Income Distribution (Histogram)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data['Income'].dropna(), kde=True, color='skyblue', ax=ax)
        st.pyplot(fig)

    if "Income vs Age (Scatter Plot)" in operations:
        st.subheader("Income vs Age (Scatter Plot)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=data, x='Age', y='Income', hue='Gender', ax=ax)
        st.pyplot(fig)

    if "Gender-wise Income (Pie Chart)" in operations:
        st.subheader(" Gender-wise Income (Pie Chart)")
        gender_income = data.groupby('Gender')['Income'].sum()
        fig, ax = plt.subplots()
        ax.pie(gender_income, labels=gender_income.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig)

    if "Education vs Avg Income (Bar)" in operations:
        st.subheader(" Education vs Avg Income (Bar Chart)")
        edu_income = data.groupby('Education')['Income'].mean().sort_values(ascending=False)
        plot_bar(edu_income, "Education vs Average Income", "Education", "Income")

    if "Income Share by Citizens vs Non-Citizens" in operations:
        st.subheader(" Income Share: Citizens vs Non-Citizens")
        share = data.groupby('Country')['Income'].sum()
        fig, ax = plt.subplots()
        ax.pie(share, labels=share.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig)

else:
    st.info(" Please upload a CSV file to start the analysis.")

