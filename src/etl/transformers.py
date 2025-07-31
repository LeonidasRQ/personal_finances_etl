"""
Data transformation module for mapping categories and transforming data.
"""

import json
import logging
import sys
from typing import List
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.data_models import RawTransaction, MappedTransaction, CategoryMapping
from utils.logging_config import get_logger

logger = get_logger('transformers')


class CategoryMapper:
    """Transforms raw transactions using category mapping."""
    
    def __init__(self, mapping_file: str):
        """
        Initialize the category mapper.
        
        Args:
            mapping_file: Path to the JSON mapping file
        """
        self.mapping_file = Path(mapping_file)
        if not self.mapping_file.exists():
            raise FileNotFoundError(f"Mapping file not found: {mapping_file}")
        
        self.mapping = self._load_mapping()
        self._validate_mapping()
    
    def _load_mapping(self) -> CategoryMapping:
        """
        Load category mapping from JSON file.
        
        Returns:
            CategoryMapping object
            
        Raises:
            json.JSONDecodeError: If JSON is invalid
            KeyError: If required keys are missing
        """
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate required keys
            if "category_to_subcategory" not in data:
                raise KeyError("Missing 'category_to_subcategory' in mapping file")
            if "subcategory_to_category" not in data:
                raise KeyError("Missing 'subcategory_to_category' in mapping file")
            
            return CategoryMapping(
                category_to_subcategory=data["category_to_subcategory"],
                subcategory_to_category=data["subcategory_to_category"]
            )
            
        except Exception as e:
            logger.error(f"Failed to load mapping from {self.mapping_file}: {e}")
            raise
    
    def _validate_mapping(self) -> None:
        """Validate the mapping configuration and log warnings."""
        warnings = self.mapping.validate()
        for warning in warnings:
            logger.warning(f"Mapping validation: {warning}")
    
    def transform(self, transactions: List[RawTransaction]) -> List[MappedTransaction]:
        """
        Transform raw transactions using category mapping.
        
        Args:
            transactions: List of raw transactions
            
        Returns:
            List of mapped transactions
        """
        logger.info(f"Starting transformation of {len(transactions)} transactions")
        
        mapped = []
        unmapped_categories = set()
        
        for transaction in transactions:
            try:
                mapped_transaction = self._map_single_transaction(transaction)
                mapped.append(mapped_transaction)
                
            except Exception as e:
                logger.error(f"Failed to map transaction {transaction}: {e}")
                # Track unmapped categories for reporting
                unmapped_categories.add(transaction.category_origin)
                
                # Create default mapping for failed transactions
                default_transaction = MappedTransaction(
                    date=transaction.date,
                    flow_type="Ingreso",  # Default to income
                    category="Otro",
                    subcategory="",
                    description=transaction.description,
                    amount=transaction.value
                )
                mapped.append(default_transaction)
        
        # Log unmapped categories
        if unmapped_categories:
            logger.warning(f"Unmapped categories found: {unmapped_categories}")
        
        # Sort by date
        mapped.sort(key=lambda x: x.date)
        
        logger.info(f"Transformation completed: {len(mapped)} transactions mapped")
        return mapped
    
    def _map_single_transaction(self, transaction: RawTransaction) -> MappedTransaction:
        """
        Map a single transaction using the category mapping.
        
        Args:
            transaction: Raw transaction to map
            
        Returns:
            Mapped transaction
        """
        # Get subcategory from category mapping
        subcategory = self.mapping.category_to_subcategory.get(
            transaction.category_origin, "Otro"
        )
        
        # Get base category from subcategory mapping
        category_base = self.mapping.subcategory_to_category.get(
            subcategory, "Ingreso"
        )
        
        # Determine flow type
        flow_type = "Ingreso" if category_base == "Ingreso" else "Egreso"
        
        # Set final category and subcategory based on flow type
        if flow_type == "Ingreso":
            category = subcategory
            final_subcategory = ""
        else:
            category = category_base
            final_subcategory = subcategory
        
        return MappedTransaction(
            date=transaction.date,
            flow_type=flow_type,
            category=category,
            subcategory=final_subcategory,
            description=transaction.description,
            amount=transaction.value
        )
    
    def get_mapping_summary(self) -> dict:
        """
        Get a summary of the mapping configuration.
        
        Returns:
            Dictionary with mapping statistics
        """
        return {
            "total_category_mappings": len(self.mapping.category_to_subcategory),
            "total_subcategory_mappings": len(self.mapping.subcategory_to_category),
            "unique_categories": len(set(self.mapping.subcategory_to_category.values())),
            "unique_subcategories": len(set(self.mapping.category_to_subcategory.values()))
        }
