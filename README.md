# OOP Problem Solving - Day 3: Dataset Processor

A reusable `DatasetProcessor` class built with OOP principles to handle common data processing tasks: loading, validating, cleaning, and transforming datasets.
## Project Structure

```
├── dataset_processor.py      # DatasetProcessor class
├── notebook-testing.ipynb    # Notebook that imports and tests the class
├── zomato.csv                # Zomato dataset
└── README.md
```

## What it does

The idea is simple: instead of writing data cleaning code directly in a notebook every time, we put all the common operations in a class (`DatasetProcessor`) inside a `.py` file and import it wherever needed.

The class covers:
- **Loading** — read CSV files using `from_csv()` classmethod
- **Validation** — check if expected columns exist (`validate_schema`) and if dtypes match (`validate_dtypes`)
- **Cleaning** — drop/fill missing values, remove duplicates
- **Transformation** — add derived columns, encode categoricals
- **Utility** — print dataset summary, export to CSV

Each cleaning/transform method returns a **new** `DatasetProcessor` instance so the original data stays untouched.

## How to use

```python
from dataset_processor import DatasetProcessor

# Load
dp = DatasetProcessor.from_csv('zomato.csv')

# Validate
dp.validate_schema(['name', 'rate', 'votes', 'cuisines'])

# Clean
dp_clean = dp.drop_missing(subset=['rate', 'cuisines'])
dp_clean = dp_clean.fill_missing(strategy='mode', columns=['dish_liked'])
dp_clean = dp_clean.drop_duplicates(subset=['name', 'address'])

# Transform — extract numeric rating from "4.1/5"
dp_final = dp_clean.add_column(
    'rating',
    lambda df: df['rate'].str.replace(r'\s*/\s*5', '', regex=True).apply(
        lambda x: float(x) if x.replace('.', '', 1).isdigit() else None
    )
)

# Summary
dp_final.summary()
```
