"""
Data models for the ETL pipeline.

These classes define the structure of data as it flows through the pipeline.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class RawTransaction:
    """Raw transaction data as extracted from the source Excel file."""
    date: date
    description: str
    value: float
    category_origin: str

    def __post_init__(self):
        """Validate the transaction data after initialization."""
        if self.value < 0:
            raise ValueError("Transaction value cannot be negative")
        if not self.category_origin:
            raise ValueError("Category origin is required")


@dataclass
class MappedTransaction:
    """Transformed transaction data with mapped categories."""
    date: date
    flow_type: str
    category: str
    subcategory: str
    description: str
    amount: float

    def __post_init__(self):
        """Validate the mapped transaction data."""
        if self.flow_type not in ["Ingreso", "Egreso"]:
            raise ValueError(f"Invalid flow_type: {self.flow_type}")
        if self.amount <= 0:
            raise ValueError("Amount must be positive")


@dataclass
class CategoryMapping:
    """Category mapping configuration."""
    category_to_subcategory: dict[str, str]
    subcategory_to_category: dict[str, str]

    def validate(self) -> list[str]:
        """
        Validate the mapping for potential issues.
        
        Returns:
            List of warning messages about potential issues.
        """
        warnings = []
        
        # Check for duplicate subcategories in subcategory_to_category
        seen_categories = {}
        for subcategory, category in self.subcategory_to_category.items():
            if subcategory in seen_categories:
                warnings.append(
                    f"Duplicate subcategory '{subcategory}' maps to both "
                    f"'{seen_categories[subcategory]}' and '{category}'"
                )
            seen_categories[subcategory] = category
        
        # Check for orphaned mappings
        mapped_subcategories = set(self.category_to_subcategory.values())
        defined_subcategories = set(self.subcategory_to_category.keys())
        
        orphaned = mapped_subcategories - defined_subcategories
        if orphaned:
            warnings.append(f"Orphaned subcategories (no category mapping): {orphaned}")
        
        return warnings
