# 📘 Retail Sales Power BI – DAX Measures & Columns

---

## 🔹 1. Base Measures

These are the foundation for everything else.

```
Total Sales = SUM('Sales'[Sales])

```

➡️ Adds up sales across all orders.

```
Total Profit = SUM('Sales'[Profit])

```

➡️ Sums all profit.

```
Profit Margin % = DIVIDE([Total Profit], [Total Sales])

```

➡️ Shows profitability as a percentage of sales.

---

## 🔹 2. Time Intelligence Measures

Require a proper **Date table** linked to `Sales[Order Date]`.

```
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))

```

➡️ Last year’s sales for the same period.

```
Sales YoY % = DIVIDE([Total Sales] - [Sales LY], [Sales LY])

```

➡️ Growth % compared to last year.

```
Sales YTD = TOTALYTD([Total Sales], 'Date'[Date])

```

➡️ Year-to-date sales.

```
Sales YTD LY = CALCULATE([Sales YTD], SAMEPERIODLASTYEAR('Date'[Date]))

```

➡️ YTD sales from the previous year.

```
Sales YTD YoY % = DIVIDE([Sales YTD] - [Sales YTD LY], [Sales YTD LY])

```

➡️ Growth % for YTD compared to last year.

---

## 🔹 3. Discount Banding (Helper Column)

```
Discount Band =
SWITCH(
    TRUE(),
    'Sales'[Discount] = 0, "0%",
    'Sales'[Discount] <= 0.10, "0–10%",
    'Sales'[Discount] <= 0.20, "10–20%",
    'Sales'[Discount] <= 0.30, "20–30%",
    'Sales'[Discount] <= 0.40, "30–40%",
    "40%+"
)

```

➡️ Groups discount values into readable categories for analysis.

---

### 🔹 3.1 Band Index for Sorting

```
Discount Band Index =
SWITCH(
    TRUE(),
    'Sales'[Discount] = 0, 1,
    'Sales'[Discount] <= 0.10, 2,
    'Sales'[Discount] <= 0.20, 3,
    'Sales'[Discount] <= 0.30, 4,
    'Sales'[Discount] <= 0.40, 5,
    6
)

```

➡️ Numeric order for bands (hidden column, used for **Sort by Column**).

---

## 🔹 4. Ranking & Top-N

```
Rank Product by Sales =
RANKX(
    ALL('Sales'[Product Name]),
    [Total Sales],
    ,
    DESC,
    DENSE
)

```

➡️ Ranks products by sales, highest = rank 1.

```
Show TopN =
IF([Rank Product by Sales] <= 10, 1, 0)

```

➡️ Keeps only Top 10 products (used as visual filter).

👉 If you add a **What-if parameter (TopN)**:

```
Show TopN =
IF([Rank Product by Sales] <= 'TopN'[TopN Value], 1, 0)

```

➡️ User can dynamically choose Top 5, 10, 20 products.

---

## 🔹 5. Conditional Formatting Helper (Optional)

```
Profit Color =
IF([Total Profit] < 0, "Red", "Green")

```

➡️ Used in visuals (Data Colors → Format by → Field value) to automatically color bars/cards.

# ✅ How to Use This Library

- Start with **Base measures** → use them in cards and charts.
- Add **Time intelligence** → for YoY and YTD analysis.
- Create **Discount Band + Index** → for clean profit/discount visuals.
- Use **Ranking** → for Top-N charts.
- Apply **Formatting helpers** → for red/green storytelling.
