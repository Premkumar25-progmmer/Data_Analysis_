# Data_Analysis_📊 Census Data Analysis Dashboard-by Prem kumar
# 🔗 Live App: https://dataanalysis-bypremkumar.streamlit.app/

 This Streamlit-based web app performs an extensive analysis of census data to explore education, income, employment, and demographic patterns.
It combines 25+ different operations — with interactive charts and filter-based data tables — to provide a complete understanding of a population dataset.

🗂️ Key Features
🎓 Education-Based Analysis

Education Distribution (Bar Chart)

College Dropouts Listing

Average Income by Education

Education Level Count

Education vs Gender Count

💵 Income & Employment Analysis

Gender-wise Total Income (Bar Chart)

Per Capita Income by Gender

Tax Estimation by Gender (10%)

Income Distribution (Histogram)

Income vs Age (Scatter Plot)

Top 5 Occupations by Income

Income by Country (Bar Chart)

Non-Citizen Income Share

🌍 Demographics & Citizen Analysis

Working Population %

Non-Citizens Working %

Citizens Above 60

Senior Citizens (55–60)

Employable Widows & Divorced

Citizens Above 23 Without Employment

Parents Presence Distribution

Orphans by Parents & Gender

Gender Ratio by Occupation

📈 Tech Stack

Python 3.x

Streamlit — Web app framework

Pandas — Data manipulation

Matplotlib & Seaborn — Data visualization

🧩 File Structure
📁 census-data-analysis/
│
├── census_dashboard_all_ops.py   # Main Streamlit app
├── requirements.txt               # Dependencies
└── README.md                      # Project documentation

⚙️ How to Run Locally

Install dependencies

pip install -r requirements.txt


Run the Streamlit app

streamlit run census_dashboard_all_ops.py


Upload your CSV file

File should not have headers.

Columns must be in this exact order:

Age, Education, Marital_Status, Gender, Occupation, Income, Parents_Present, Country, Native, Weeks_Worked


Use the sidebar to select:

Category (Education, Income & Employment, or Demographics)

One or more operations to display

🌐 How to Deploy on Streamlit Cloud

Push your project to GitHub (include the .py, requirements.txt, and README.md files).

Go to https://share.streamlit.io
.

Click “New app” → Choose your repository → Select:

census_dashboard_all_ops.py


Streamlit Cloud installs packages automatically and launches your app.

✅ Deployed App Link:
👉 https://dataanalysisbypremkumar.streamlit.app/

📊 Example Outputs

Education Distribution → Bar Chart of education categories.

Gender-wise Income → Total income comparison by gender.

Tax Estimation → Estimated 10% tax by gender.

Income by Country → Country-wise income totals.

Senior Citizens (55–60) → Filtered list of senior citizens.

👨‍💻 Developer

Chilkamarri Prem Kumar
🎓 B.Tech — Artificial Intelligence & Data Science
📍 Hyderabad, India

🔗 Live Demo: https://dataanalysisbypremkumar.streamlit.app/

🏁 License

This project is open-source and can be used for educational and analytical purposes.
