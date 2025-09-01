#  Discount Banding (Helper Column)

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