# 📊 ETL for Personal Finance (Excel)

This is a simple ETL (Extract, Transform, Load) script written in Python that reads financial transactions from a source Excel file, maps and categorizes the data according to your personal finance rules, and loads them into a cashflow table in your main Excel workbook.

The script:

✅ Reads transactions from a mobills_transactions.xlsx file (sheet Receitas e Despesas).

✅ Maps categories and subcategories to your custom finance structure.
✅ Sorts entries by date in ascending order.

✅ Inserts them into your copia_finanzas.xlsx cashflow table, preserving all styles, formulas, and validations.

✅ Allows a --dry-run mode for safe testing.

## 🚀 Usage

```bash
python etl_finance.py
```

You can also run in dry-run mode (no changes to your Excel file, only shows what would be inserted):

```bash
python etl_finance.py --dry-run
```

Or use different source / target files:

```bash
python etl_finance.py --source "my_new_transactions.xlsx" --dest "my_finances.xlsx"
```

## ⚙️ Requirements

- Python 3.10+ (recommended installed via scoop)
- Install dependencies

```
pip install -r requirements.txt
```

## Project Structure

```bash
etl-finanzas/
│
├── etl_finance.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   └── category_mapping.json
│
├── data/
│   ├── mobills_transactions.xlsx
│   └── copia_finanzas.xlsx
│
└── logs/
    └── etl.log (creado por el script)
```

## ✌️ Features

✅ Loads data from Excel (via openpyxl), no extra database or API needed.

✅ Fully customizable category & subcategory mapping.

✅ Keeps all your existing Excel formatting, data
validations, and formulas.

✅ Logs everything with levels INFO and WARNING.
