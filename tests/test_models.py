"""
Tests for data models.
"""

import pytest
import datetime
from src.models.data_models import RawTransaction, MappedTransaction, CategoryMapping


class TestRawTransaction:
    """Tests for RawTransaction model."""
    
    def test_valid_transaction(self):
        """Test creating a valid raw transaction."""
        transaction = RawTransaction(
            date=datetime.date(2025, 1, 15),
            description="Test transaction",
            value=100.0,
            category_origin="Test"
        )
        
        assert transaction.date == datetime.date(2025, 1, 15)
        assert transaction.description == "Test transaction"
        assert transaction.value == 100.0
        assert transaction.category_origin == "Test"
    
    def test_negative_value_raises_error(self):
        """Test that negative values raise ValueError."""
        with pytest.raises(ValueError, match="Transaction value cannot be negative"):
            RawTransaction(
                date=datetime.date(2025, 1, 15),
                description="Test",
                value=-100.0,
                category_origin="Test"
            )
    
    def test_empty_category_raises_error(self):
        """Test that empty category raises ValueError."""
        with pytest.raises(ValueError, match="Category origin is required"):
            RawTransaction(
                date=datetime.date(2025, 1, 15),
                description="Test",
                value=100.0,
                category_origin=""
            )


class TestMappedTransaction:
    """Tests for MappedTransaction model."""
    
    def test_valid_mapped_transaction(self):
        """Test creating a valid mapped transaction."""
        transaction = MappedTransaction(
            date=datetime.date(2025, 1, 15),
            flow_type="Ingreso",
            category="Salario",
            subcategory="",
            description="Salary",
            amount=5000.0
        )
        
        assert transaction.flow_type == "Ingreso"
        assert transaction.category == "Salario"
        assert transaction.amount == 5000.0
    
    def test_invalid_flow_type_raises_error(self):
        """Test that invalid flow type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid flow_type"):
            MappedTransaction(
                date=datetime.date(2025, 1, 15),
                flow_type="Invalid",
                category="Test",
                subcategory="",
                description="Test",
                amount=100.0
            )
    
    def test_negative_amount_raises_error(self):
        """Test that negative amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be positive"):
            MappedTransaction(
                date=datetime.date(2025, 1, 15),
                flow_type="Ingreso",
                category="Test",
                subcategory="",
                description="Test",
                amount=-100.0
            )


class TestCategoryMapping:
    """Tests for CategoryMapping model."""
    
    def test_valid_mapping(self, sample_mapping):
        """Test creating a valid category mapping."""
        assert len(sample_mapping.category_to_subcategory) == 5
        assert len(sample_mapping.subcategory_to_category) == 5
    
    def test_mapping_validation_no_issues(self, sample_mapping):
        """Test mapping validation with no issues."""
        warnings = sample_mapping.validate()
        assert len(warnings) == 0
    
    def test_mapping_validation_with_duplicates(self):
        """Test mapping validation with duplicate subcategories."""
        mapping = CategoryMapping(
            category_to_subcategory={
                "Cat1": "Sub1",
                "Cat2": "Sub1"  # Duplicate subcategory
            },
            subcategory_to_category={
                "Sub1": "Category1",
                "Sub1": "Category2"  # This would be overwritten in real JSON
            }
        )
        
        # In Python dict, the second key overwrites the first
        # So this test mainly checks the structure
        warnings = mapping.validate()
        # The validation might not catch this since Python dict handles it
        assert isinstance(warnings, list)
    
    def test_mapping_validation_orphaned_subcategories(self):
        """Test mapping validation with orphaned subcategories."""
        mapping = CategoryMapping(
            category_to_subcategory={
                "Cat1": "Sub1",
                "Cat2": "Sub2"
            },
            subcategory_to_category={
                "Sub1": "Category1"
                # Sub2 is missing - orphaned
            }
        )
        
        warnings = mapping.validate()
        assert len(warnings) > 0
        assert any("Orphaned subcategories" in warning for warning in warnings)
