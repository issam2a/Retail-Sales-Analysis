# Retail Sales Analysis

A weekly data project analyzing the Superstore dataset to extract actionable business insights.

## Project Overview
This project demonstrates an end-to-end data analysis workflow:
1. Import Superstore dataset into MySQL.
2. Clean and preprocess the data using SQL queries.
3. Conduct exploratory data analysis (EDA) and calculate key business KPIs.
4. Automate KPI extraction with Python scripts, exporting results to CSV files for further visualization and reporting.

## Key Business KPIs
- Total revenue & profit
- Profit margin
- Average order value (AOV)
- Top customers and products
- Regional and segment sales trends
- Shipping analysis

## How to Run
1. Set up a MySQL database and import the `Superstore.csv` dataset.
2. Run the SQL scripts in the `sql/` folder to clean data and calculate KPIs.
3. Activate your Python virtual environment and install dependencies:
```bash
pip install pandas mysql-connector-python

Run the Python automation script to export KPIs as CSV:

python python/run_kpi_queries.py

Future Plans

Visualize KPIs using Python (Matplotlib/Seaborn) and Power BI.

Explore predictive analytics on sales and customer behavior.

Author

Issam Issa – [LinkedIn](www.linkedin.com/in/issam-issa)