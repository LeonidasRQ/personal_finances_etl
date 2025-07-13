# 🧾 Python Finance ETL

A modular ETL (Extract, Transform, Load) tool built in Python, designed to automate the ingestion of financial transactions from a source Excel file (like Mobills export), map their categories and subcategories, and load them into a structured Excel cashflow workbook (such as your personal finance tracker).

---

## 🚀 Features

✅ Load transactions from a configurable Excel source file  
✅ Map categories and subcategories dynamically via JSON config  
✅ Insert into an existing cashflow Excel workbook, extending tables, formulas & validations  
✅ Dry-run mode to preview changes without saving  
✅ Loads environment variables from `.env`  
✅ Modular, easy to extend

---

## 📂 Project structure

```bash
etl-finanzas/
├── config/
│   └── category_mapping.json
|
├── logs/
|   └── etl.log (created by script)0
|
├── .env
├── .gitignore
├── etl_finance.py
├── README.md
└── requirements.txt
```

## ⚙️ Configuration

### 📌 .env file

All your critical settings are stored in `.env`:

```env
DEST_FILE=""
SOURCE_FILE=""
MAPPING_FILE=""
LOG_FILE="logs/etl_run.log"
```

This is loaded via `python-dotenv`

### Mapping JSON

Example mapping.json to control how your original categories are transformed:

```json
{
  "category_to_subcategory": {
    "Supermarket": "Groceries",
    "Restaurant": "Eating Out",
    "Transportation": "Commute",
    "Salary": "Salary"
  },
  "subcategory_to_category": {
    "Groceries": "Needs",
    "Eating Out": "Wants",
    "Commute": "Needs",
    "Salary": "Income"
  }
}
```

This makes it easy to change your classification without modifying Python code.

## Installation

1. Clone the repo

```
git clone git@github.com:LeonidasRQ/personal_finances_etl.git
cd personal_finances_etl
```

2. Create virtual environment

```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies

```
pip install -r requirements.txt
```

## 🚀 Usage

Run your ETL pipeline like this

```
python etl_finance.py
```

Want to test without writing changes to your cashflow file?

```
python etl_finance.py --dry-run
```

You’ll see logs of all planned inserts without modifying your file.

## ⚙️ Requirements

- Python 3.10+ (recommended installed via scoop)

## 🤝 Contributing

PRs & suggestions welcome!
You can file issues or ideas for additional transformations (like VAT splitting, multi-currency support).

## 📝 License

MIT — do what you want, but no guarantees.
