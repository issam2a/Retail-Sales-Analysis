#  Time Intelligence Measures

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