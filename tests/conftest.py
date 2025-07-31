"""
Test configuration fixtures for pytest.
"""

import pytest
import datetime
import tempfile
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.data_models import RawTransaction, MappedTransaction, CategoryMapping


@pytest.fixture
def sample_mapping():
    """Sample category mapping for testing."""
    return CategoryMapping(
        category_to_subcategory={
            "Salary": "Salario",
            "Supermarket": "Mercado",
            "Transportation": "Transporte",
            "Loans": "Prestamos",
            "Others": "Otro"
        },
        subcategory_to_category={
            "Salario": "Ingreso",
            "Mercado": "Necesidades", 
            "Transporte": "Necesidades",
            "Prestamos": "Gustos",
            "Otro": "Ingreso"
        }
    )


@pytest.fixture
def sample_raw_transactions():
    """Sample raw transactions for testing."""
    return [
        RawTransaction(
            date=datetime.date(2025, 1, 15),
            description="Monthly salary",
            value=5000.0,
            category_origin="Salary"
        ),
        RawTransaction(
            date=datetime.date(2025, 1, 16),
            description="Grocery shopping",
            value=150.0,
            category_origin="Supermarket"
        ),
        RawTransaction(
            date=datetime.date(2025, 1, 17),
            description="Bus fare",
            value=25.0,
            category_origin="Transportation"
        )
    ]


@pytest.fixture
def sample_mapped_transactions():
    """Sample mapped transactions for testing."""
    return [
        MappedTransaction(
            date=datetime.date(2025, 1, 15),
            flow_type="Ingreso",
            category="Salario",
            subcategory="",
            description="Monthly salary",
            amount=5000.0
        ),
        MappedTransaction(
            date=datetime.date(2025, 1, 16),
            flow_type="Egreso",
            category="Necesidades",
            subcategory="Mercado",
            description="Grocery shopping",
            amount=150.0
        )
    ]


@pytest.fixture
def temp_excel_file():
    """Create a temporary Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        yield f.name
    # Cleanup happens automatically


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        yield f.name
    # Cleanup happens automatically


@pytest.fixture
def mock_workbook():
    """Mock Excel workbook for testing."""
    wb = Mock()
    ws = Mock()
    wb.active = ws
    
    # Mock table
    table = Mock()
    table.ref = "A1:H10"
    ws.tables = {"Table1": table}
    ws.tables.values.return_value = [table]
    
    return wb, ws, table
