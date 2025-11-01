# census_dashboard_all_ops.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App setup
st.set_page_config(page_title="Census Data Analysis (Full)", layout="wide")
st.title("📊 Census Data Analysis Dashboard — Full (All operations)")

# Helper plotting functions
def plot_bar(series, title, xlabel="", ylabel="Value", rotate=True):
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=series.index, y=series.values, ax=ax)
    if rotate:
        plt.xticks(rotation=45, ha='right')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

def plot_pie(series, title):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(series, labels=series.index, autopct='%1.1f%%', startangle=140)
    ax.set_title(title)
    st.pyplot(fig)

def plot_hist(x, title, bins=30):
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(x.dropna(), kde=True, ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

def plot_scatter(df, xcol, ycol, hue=None, title="Scatter"):
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=df, x=xcol, y=ycol, hue=hue, ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

# File upload
uploaded_file = st.file_uploader("📂 Upload CSV (no header) or leave blank to load sample", type="csv")

if uploaded_file is None:
    st.info("Upload your census CSV file. Columns expected (no header): Age, Education, Marital_Status, Gender, Occupation, Income, Parents_Present, Country, Native, Weeks_Worked")
    st.stop()

# Load data and set column names
column_names = [
    'Age', 'Education', 'Marital_Status', 'Gender',
    'Occupation', 'Income', 'Parents_Present',
    'Country', 'Native', 'Weeks_Worked'
]
try:
    df = pd.read_csv(uploaded_file, names=column_names, header=None)
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# Basic cleaning & dtype conversions
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
df['Weeks_Worked'] = pd.to_numeric(df['Weeks_Worked'], errors='coerce')
# Fill missing strings if needed
df['Education'] = df['Education'].fillna('Unknown')
df['Gender'] = df['Gender'].fillna('Unknown')
df['Occupation'] = df['Occupation'].fillna('Unknown')
df['Country'] = df['Country'].fillna('Unknown')
df['Parents_Present'] = df['Parents_Present'].fillna('Unknown')

st.success("✅ File loaded and preprocessed.")
st.subheader("🔎 Data sample")
st.dataframe(df.head())

# Sidebar grouping of operations
st.sidebar.header("📂 Operations (select one or more)")
group = st.sidebar.radio("Choose category", ["Education", "Income & Employment", "Demographics & Filters"])

if group == "Education":
    ops = st.sidebar.multiselect("Education operations",
        [
            "Education Distribution (graph)",
            "Education Level Count (table)",
            "College Dropouts (Somecollegebutnodegree) (table)",
            "Average Income by Education (graph)",
            "Education vs Gender Count (table)"
        ])
elif group == "Income & Employment":
    ops = st.sidebar.multiselect("Income & Employment operations",
        [
            "Gender-wise Total Income (graph)",
            "Per Capita Income by Gender (table)",
            "Tax Estimation by Gender 10% (graph)",
            "Income Distribution Histogram (graph)",
            "Income vs Age Scatter (graph)",
            "Top 5 Occupations by Income (graph)",
            "Income by Country (graph)",
            "Non-Citizen Income Share (table)"
        ])
else:
    ops = st.sidebar.multiselect("Demographics & Filters",
        [
            "Working Population % (text)",
            "Non-Citizens Working % (text)",
            "Citizens Age >23 Unemployed (table)",
            "Employable Widows & Divorced (table)",
            "Senior Citizens (55-60) (table)",
            "Citizens Above 60 (table)",
            "Parents Presence Distribution (table)",
            "Orphans by Parents & Gender (table)",
            "Gender Ratio by Occupation (table)"
        ])

# ---- EDUCATION OPS ----
if "Education Distribution (graph)" in ops:
    st.subheader("🎓 Education Distribution")
    edu_counts = df['Education'].value_counts()
    plot_bar(edu_counts, "Education Distribution", xlabel="Education Level", ylabel="Count")

if "Education Level Count (table)" in ops:
    st.subheader("🎓 Education Level Count (table)")
    st.dataframe(df['Education'].value_counts().rename_axis('Education').reset_index(name='Count'))

if "College Dropouts (Somecollegebutnodegree) (table)" in ops:
    st.subheader("🎓 College Dropouts (Somecollegebutnodegree)")
    dropouts = df[df['Education'] == "Somecollegebutnodegree"]
    st.write(f"Count: {len(dropouts)}")
    st.dataframe(dropouts)

if "Average Income by Education (graph)" in ops:
    st.subheader("📈 Average Income by Education")
    avg_inc_edu = df.groupby('Education')['Income'].mean().sort_values(ascending=False)
    plot_bar(avg_inc_edu, "Average Income by Education", xlabel="Education", ylabel="Avg Income")

if "Education vs Gender Count (table)" in ops:
    st.subheader("📘 Education vs Gender Count")
    edu_gender = df.groupby(['Education', 'Gender']).size().reset_index(name='Count')
    st.dataframe(edu_gender)

# ---- INCOME & EMPLOYMENT OPS ----
if "Gender-wise Total Income (graph)" in ops:
    st.subheader("💰 Gender-wise Total Income")
    g_income = df.groupby('Gender')['Income'].sum()
    if g_income.sum() == 0:
        st.warning("Income column appears to be empty or zero for all rows.")
    plot_bar(g_income, "Total Income by Gender", xlabel="Gender", ylabel="Total Income")

if "Per Capita Income by Gender (table)" in ops:
    st.subheader("💹 Per Capita (Average) Income by Gender")
    per_capita = df.groupby('Gender')['Income'].mean().reset_index().rename(columns={'Income': 'Per_Capita_Income'})
    st.dataframe(per_capita)

if "Tax Estimation by Gender 10% (graph)" in ops:
    st.subheader("💸 Tax Estimation by Gender (10%)")
    tax = df.groupby('Gender')['Income'].sum() * 0.10
    plot_bar(tax, "Estimated Tax by Gender (10%)", xlabel="Gender", ylabel="Tax Amount")

if "Income Distribution Histogram (graph)" in ops:
    st.subheader("📊 Income Distribution")
    plot_hist(df['Income'], "Income Distribution (Histogram)")

if "Income vs Age Scatter (graph)" in ops:
    st.subheader("📈 Income vs Age")
    plot_scatter(df.dropna(subset=['Age','Income']), 'Age', 'Income', hue='Gender', title="Income vs Age by Gender")

if "Top 5 Occupations by Income (graph)" in ops:
    st.subheader("🏆 Top 5 Occupations by Total Income")
    occ_income = df.groupby('Occupation')['Income'].sum().sort_values(ascending=False).head(5)
    plot_bar(occ_income, "Top 5 Occupations by Income", xlabel="Occupation", ylabel="Total Income")

if "Income by Country (graph)" in ops:
    st.subheader("🌍 Income by Country")
    country_income = df.groupby('Country')['Income'].sum().sort_values(ascending=False)
    plot_bar(country_income, "Total Income by Country", xlabel="Country", ylabel="Total Income")

if "Non-Citizen Income Share (table)" in ops:
    st.subheader("💵 Income Generated by Non-Citizens")
    non_cit_income = df[df['Country'] != 'Citizen']['Income'].sum()
    st.write(f"Total Income by Non-Citizens: {non_cit_income:,.2f}")

# ---- DEMOGRAPHIC & FILTER OPS ----
if "Working Population % (text)" in ops:
    st.subheader("⚙️ Working Population Percentage")
    working = df[df['Occupation'].str.lower() != 'unemployed']
    percent_working = (len(working) / len(df)) * 100 if len(df) > 0 else 0
    st.write(f"Working population: {percent_working:.2f}%")

if "Non-Citizens Working % (text)" in ops:
    st.subheader("🌎 Non-Citizens Working Percentage")
    non_citizens = df[df['Country'] != 'Citizen']
    working_noncit = non_citizens[non_citizens['Occupation'].str.lower() != 'unemployed']
    pct_noncit = (len(working_noncit) / len(non_citizens) * 100) if len(non_citizens) > 0 else 0
    st.write(f"{pct_noncit:.2f}% of non-citizens are employed")

if "Citizens Age >23 Unemployed (table)" in ops:
    st.subheader("🙍 Citizens Age >23 Without Employment")
    unemployed = df[(df['Age'] > 23) & (df['Occupation'].str.lower() == 'unemployed') & (df['Country'] == 'Citizen')]
    st.write(f"Count: {len(unemployed)}")
    st.dataframe(unemployed)

if "Employable Widows & Divorced (table)" in ops:
    st.subheader("👩 Employable Widows & Divorced")
    emp_widow_div = df[(df['Marital_Status'].isin(['Widowed','Divorced'])) & (df['Occupation'].str.lower() != 'unemployed')]
    st.write(f"Count: {len(emp_widow_div)}")
    st.dataframe(emp_widow_div)

if "Senior Citizens (55-60) (table)" in ops:
    st.subheader("👴 Senior Citizens (55–60)")
    senior = df[(df['Age'] >= 55) & (df['Age'] < 60)]
    st.write(f"Count: {len(senior)}")
    st.dataframe(senior)

if "Citizens Above 60 (table)" in ops:
    st.subheader("👵 Citizens Above 60")
    above60 = df[(df['Age'] > 60) & (df['Country'] == 'Citizen')]
    st.write(f"Count: {len(above60)}")
    st.dataframe(above60)

if "Parents Presence Distribution (table)" in ops:
    st.subheader("👪 Parents Presence Distribution")
    st.dataframe(df['Parents_Present'].value_counts().rename_axis('Parents_Present').reset_index(name='Count'))

if "Orphans by Parents & Gender (table)" in ops:
    st.subheader("🧒 Orphans by Parents & Gender")
    orphan_stats = df.groupby(['Parents_Present','Gender']).size().reset_index(name='Count')
    st.dataframe(orphan_stats)

if "Gender Ratio by Occupation (table)" in ops:
    st.subheader("⚖️ Gender Ratio by Occupation")
    gender_occ = df.groupby(['Occupation','Gender']).size().unstack(fill_value=0)
    st.dataframe(gender_occ)

# End
st.markdown("---")
st.write("App: full census analysis — all ops available. Choose operations from the sidebar.")

