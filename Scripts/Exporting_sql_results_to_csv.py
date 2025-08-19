import mysql.connector
import pandas as pd
import os

# ---------------------------
# Database Connection Config
# ---------------------------
db_config = {
    "host": "localhost",      # change if needed
    "user": "root",           #  MySQL username
    "password": "**********",  #  MySQL password
    "database": "retail_sales"  #  database name
}

# ---------------------------
# Output folder for CSVs
# ---------------------------
output_dir = "kpi_exports"
os.makedirs(output_dir, exist_ok=True)

# ---------------------------
# Define Queries (grouped)
# ---------------------------
queries = {
    "basic_exploration": {
        "total_transactions": "SELECT COUNT(*) AS total_transactions FROM sales;",
        "distinct_customers": "SELECT COUNT(DISTINCT CustomerID) AS Customers_count FROM sales;",
        "distinct_products": "SELECT COUNT(DISTINCT ProductID) AS Products_count FROM sales;",
        "total_revenue_profit": "SELECT SUM(Sales) AS total_revenue, SUM(Profit) AS total_profit FROM sales;",
        "profit_margin": "SELECT ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_margin FROM sales;",
        "avg_order_value": "SELECT ROUND(SUM(Sales) / COUNT(DISTINCT OrderID), 2) AS AOV FROM sales;",
        "shipmode_count": "SELECT COUNT(ShipMode), ShipMode FROM sales GROUP BY ShipMode ORDER BY COUNT(ShipMode);"
    },
    "customer_analysis": {
        "top_customers_by_sales": """
            SELECT CustomerName, SUM(Sales) AS total_sales,
                   RANK() OVER(ORDER BY SUM(Sales) DESC) AS sales_Rank
            FROM sales GROUP BY CustomerName ORDER BY sales_Rank LIMIT 10;
        """,
        "customers_by_profit": """
            SELECT CustomerName, SUM(Profit) AS Profit_contribution
            FROM sales GROUP BY CustomerName ORDER BY Profit_contribution DESC LIMIT 10;
        """,
        "repeat_customers": """
            SELECT CustomerName, COUNT(OrderID) AS order_count
            FROM sales GROUP BY CustomerName HAVING COUNT(OrderID) > 1
            ORDER BY order_count DESC;
        """,
        "repeat_customers_percentage": """
            SELECT (COUNT(*) / (SELECT COUNT(DISTINCT CustomerName) FROM sales)) * 100 
            AS repeated_customers_percentage
            FROM (SELECT CustomerName FROM sales GROUP BY CustomerName HAVING COUNT(OrderID) > 1) AS repeated_customers;
        """
    },
    "product_analysis": {
        "best_selling_items": """
            SELECT ProductName, COUNT(Quantity) AS items_sold
            FROM sales GROUP BY ProductName ORDER BY items_sold DESC LIMIT 10;
        """,
        "best_selling_revenue": """
            SELECT ProductName, SUM(Sales) AS product_total_sales
            FROM sales GROUP BY ProductName ORDER BY product_total_sales DESC;
        """,
        "most_profitable_subcategories": """
            SELECT SubCategory, SUM(Profit) AS subcategory_profit
            FROM sales GROUP BY SubCategory ORDER BY subcategory_profit DESC;
        """,
        "loss_making_products": """
            SELECT ProductName, SUM(Profit) AS total_loss
            FROM sales GROUP BY ProductName HAVING total_loss < 0 ORDER BY total_loss ASC;
        """,
        "low_margin_products": """
            SELECT ProductName, Category, SubCategory,
                   SUM(Sales) AS total_sales, SUM(Profit) AS total_profit,
                   ROUND(SUM(Profit) / SUM(Sales), 2) * 100 AS profit_margin
            FROM sales GROUP BY ProductName, Category, SubCategory
            HAVING profit_margin < 20
            ORDER BY profit_margin ASC;
        """
    },
    "regional_segment_analysis": {
        "sales_by_region": "SELECT Region, SUM(Sales) AS sales_by_region FROM sales GROUP BY Region ORDER BY sales_by_region DESC;",
        "sales_by_segment": "SELECT Segment, SUM(Sales) AS segment_sales FROM sales GROUP BY Segment ORDER BY segment_sales DESC;",
        "sales_by_state": "SELECT State, SUM(Sales) AS total_state_sales FROM sales GROUP BY State ORDER BY total_state_sales DESC LIMIT 10;"
    },
    "time_analysis": {
        "sales_by_year": "SELECT YEAR(OrderDate) AS Order_year, SUM(Sales) AS sales_by_year FROM sales GROUP BY YEAR(OrderDate) ORDER BY sales_by_year DESC;",
        "sales_by_month": """
            SELECT month, sales_by_month, RANK() OVER(ORDER BY sales_by_month DESC) AS sales_rank
            FROM (
                SELECT MONTH(OrderDate) AS month, SUM(Sales) AS sales_by_month
                FROM sales GROUP BY MONTH(OrderDate)
            ) AS monthly_sales ORDER BY sales_rank;
        """,
        "sales_by_year_month": """
            SELECT month, year, total_sales, RANK() OVER(ORDER BY total_sales DESC) AS sales_rank
            FROM (
                SELECT MONTH(OrderDate) AS month, YEAR(OrderDate) AS year, SUM(Sales) AS total_sales
                FROM sales GROUP BY YEAR(OrderDate), MONTH(OrderDate)
            ) AS yearly_sales ORDER BY sales_rank;
        """,
        "seasonality_analysis": """
            SELECT month, year, quarter, total_sales, RANK() OVER(ORDER BY total_sales DESC) AS sales_rank
            FROM (
                SELECT MONTH(OrderDate) AS month, QUARTER(OrderDate) AS quarter, YEAR(OrderDate) AS year,
                       SUM(Sales) AS total_sales
                FROM sales GROUP BY YEAR(OrderDate), MONTH(OrderDate), QUARTER(OrderDate)
            ) AS yearly_sales ORDER BY sales_rank;
        """
    },
    "shipping_analysis": {
        "orders_by_shipmode": "SELECT ShipMode, COUNT(OrderID) AS Orders_count FROM sales GROUP BY ShipMode ORDER BY Orders_count DESC;",
        "orders_percentage": """
            SELECT ShipMode, COUNT(OrderID) AS Orders_count,
                   (COUNT(OrderID) / (SELECT COUNT(*) FROM sales)) * 100 AS Order_percentage
            FROM sales GROUP BY ShipMode ORDER BY Orders_count DESC;
        """,
        "avg_shipping_time": """
            SELECT ShipMode, AVG(DATEDIFF(ShipDate, OrderDate)) AS avg_Shipment_days
            FROM sales GROUP BY ShipMode ORDER BY avg_Shipment_days;
        """,
        "same_day_delays": """
            SELECT ShipMode, DATEDIFF(ShipDate, OrderDate) AS days
            FROM sales WHERE ShipMode LIKE 'Same Day' AND DATEDIFF(ShipDate, OrderDate) > 1;
        """
    }
}

# ---------------------------
# Run Queries & Export
# ---------------------------
def run_queries():
    conn = mysql.connector.connect(**db_config)
    for group, qs in queries.items():
        print(f"Running {group} queries...")
        group_dir = os.path.join(output_dir, group)
        os.makedirs(group_dir, exist_ok=True)

        for name, query in qs.items():
            df = pd.read_sql(query, conn)
            csv_path = os.path.join(group_dir, f"{name}.csv")
            df.to_csv(csv_path, index=False)
            print(f"  -> Saved {name}.csv")

    conn.close()
    print("✅ All queries executed and CSVs exported!")

if __name__ == "__main__":
    run_queries()


