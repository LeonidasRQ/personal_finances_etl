# 🧾 Python Finance ETL

A modular ETL (Extract, Transform, Load) pipeline built in Python, designed to automate the ingestion of financial transactions from Excel files, map their categories, and load them into structured Excel cashflow workbooks.

---

## 🚀 Features

✅ **Modular Architecture** - Separate modules for extraction, transformation, and loading  
✅ **Type Safety** - Full type hints and data validation using dataclasses  
✅ **Comprehensive Testing** - Unit tests with 94% coverage  
✅ **Category Mapping** - Dynamic category mapping via JSON configuration  
✅ **Excel Integration** - Preserves formatting, formulas, and table structures  
✅ **Dry-run Mode** - Preview changes without saving  
✅ **Environment Configuration** - Configurable via environment variables  
✅ **Logging** - Comprehensive logging with file and console output  
✅ **Data Validation** - Input validation and error handling

---

## 📂 Project Structure

```bash
python_excel/
├── src/                           # Source code
│   ├── etl/                      # ETL pipeline modules
│   │   ├── extractors.py         # Data extraction from Excel
│   │   ├── transformers.py       # Category mapping and transformation
│   │   ├── loaders.py            # Data loading to Excel
│   │   └── pipeline.py           # Main pipeline orchestration
│   ├── models/
│   │   └── data_models.py        # Data classes and schemas
│   ├── utils/
│   │   ├── excel_utils.py        # Excel utility functions
│   │   ├── date_utils.py         # Date parsing utilities
│   │   └── logging_config.py     # Logging configuration
│   └── config/
│       └── settings.py           # Configuration management
├── scripts/
│   ├── run_etl.py                # Main entry point
│   └── validate_data.py          # Data validation script
├── tests/                        # Test suite
│   ├── fixtures/                 # Test data
│   ├── conftest.py              # Test configuration
│   └── test_*.py                # Test modules
├── config/
│   └── category_mapping.json    # Category mapping configuration
├── logs/                         # Log files
├── .env                          # Environment variables
├── requirements.txt              # Dependencies
├── setup.py                      # Package setup
└── README.md
```

---

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .[dev]
```

---

## ⚙️ Configuration

### 📌 Environment Variables

Create a `.env` file in the project root:

```env
DEST_FILE="path/to/your/destination.xlsx"
SOURCE_FILE="path/to/your/source.xlsx"
MAPPING_FILE="config/category_mapping.json"
LOG_FILE="logs/etl_run.log"
```

### 🗺️ Category Mapping

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
