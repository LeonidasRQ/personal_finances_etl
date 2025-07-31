"""
Main ETL pipeline orchestration.
"""

import logging
import sys
from typing import Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from etl.extractors import ExcelExtractor
from etl.transformers import CategoryMapper
from etl.loaders import ExcelLoader
from utils.logging_config import get_logger

logger = get_logger('pipeline')


class ETLPipeline:
    """Main ETL pipeline that orchestrates the extract, transform, and load operations."""
    
    def __init__(self, source_file: str, dest_file: str, mapping_file: str):
        """
        Initialize the ETL pipeline.
        
        Args:
            source_file: Path to source Excel file
            dest_file: Path to destination Excel file
            mapping_file: Path to category mapping JSON file
        """
        self.source_file = source_file
        self.dest_file = dest_file
        self.mapping_file = mapping_file
        
        # Initialize components
        self.extractor = ExcelExtractor(source_file)
        self.transformer = CategoryMapper(mapping_file)
        self.loader = ExcelLoader(dest_file)
    
    def run(self, dry_run: bool = False, validate_inputs: bool = True) -> dict:
        """
        Execute the complete ETL pipeline.
        
        Args:
            dry_run: If True, don't actually save changes to destination file
            validate_inputs: If True, validate input files before processing
            
        Returns:
            Dictionary with pipeline execution results
            
        Raises:
            Exception: If pipeline execution fails
        """
        try:
            logger.info("=" * 60)
            logger.info("Starting ETL Pipeline")
            logger.info("=" * 60)
            logger.info(f"Source: {self.source_file}")
            logger.info(f"Destination: {self.dest_file}")
            logger.info(f"Mapping: {self.mapping_file}")
            logger.info(f"Dry Run: {dry_run}")
            
            # Validate inputs if requested
            if validate_inputs:
                self._validate_inputs()
            
            # Extract phase
            logger.info("\n🔄 Phase 1: Extract")
            raw_transactions = self.extractor.extract()
            
            if not raw_transactions:
                logger.warning("No transactions extracted from source file")
                return {
                    "status": "completed",
                    "transactions_extracted": 0,
                    "transactions_transformed": 0,
                    "transactions_loaded": 0,
                    "dry_run": dry_run
                }
            
            # Transform phase
            logger.info("\n🔄 Phase 2: Transform")
            mapped_transactions = self.transformer.transform(raw_transactions)
            
            # Load phase
            logger.info("\n🔄 Phase 3: Load")
            loaded_count = self.loader.load(mapped_transactions, dry_run=dry_run)
            
            # Pipeline completion
            logger.info("\n" + "=" * 60)
            logger.info("ETL Pipeline Completed Successfully")
            logger.info("=" * 60)
            
            # Return results
            results = {
                "status": "completed",
                "transactions_extracted": len(raw_transactions),
                "transactions_transformed": len(mapped_transactions),
                "transactions_loaded": loaded_count,
                "dry_run": dry_run,
                "mapping_summary": self.transformer.get_mapping_summary()
            }
            
            self._log_summary(results)
            return results
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "transactions_extracted": 0,
                "transactions_transformed": 0,
                "transactions_loaded": 0,
                "dry_run": dry_run
            }
    
    def _validate_inputs(self) -> None:
        """
        Validate input files and formats.
        
        Raises:
            Exception: If validation fails
        """
        logger.info("Validating input files...")
        
        # Validate source file format
        if not self.extractor.validate_file_format():
            raise ValueError("Source file format validation failed")
        
        # Validate destination file format
        if not self.loader.validate_destination_format():
            raise ValueError("Destination file format validation failed")
        
        logger.info("✅ Input validation completed")
    
    def _log_summary(self, results: dict) -> None:
        """
        Log a summary of the pipeline execution.
        
        Args:
            results: Pipeline execution results
        """
        logger.info("📊 Pipeline Summary:")
        logger.info(f"   • Extracted: {results['transactions_extracted']} transactions")
        logger.info(f"   • Transformed: {results['transactions_transformed']} transactions")
        logger.info(f"   • Loaded: {results['transactions_loaded']} transactions")
        
        if 'mapping_summary' in results:
            mapping = results['mapping_summary']
            logger.info(f"   • Category mappings: {mapping['total_category_mappings']}")
            logger.info(f"   • Subcategory mappings: {mapping['total_subcategory_mappings']}")
        
        if results['dry_run']:
            logger.info("   • Mode: DRY RUN (no changes saved)")
        else:
            logger.info("   • Mode: LIVE (changes saved)")
    
    def get_pipeline_info(self) -> dict:
        """
        Get information about the pipeline configuration.
        
        Returns:
            Dictionary with pipeline information
        """
        return {
            "source_file": self.source_file,
            "dest_file": self.dest_file,
            "mapping_file": self.mapping_file,
            "extractor": type(self.extractor).__name__,
            "transformer": type(self.transformer).__name__,
            "loader": type(self.loader).__name__
        }
