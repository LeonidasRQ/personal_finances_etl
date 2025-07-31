#!/usr/bin/env python3
"""
Data validation script for the ETL Finance pipeline.

This script validates the source data and mapping configuration without running the full pipeline.
"""

import argparse
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from etl.extractors import ExcelExtractor
from etl.transformers import CategoryMapper
from etl.loaders import ExcelLoader
from config.settings import ETLConfig
from utils.logging_config import setup_logging


def validate_source_file(file_path: str) -> tuple[bool, list[str]]:
    """
    Validate the source Excel file.
    
    Args:
        file_path: Path to source file
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        extractor = ExcelExtractor(file_path)
        
        # Validate file format
        if not extractor.validate_file_format():
            issues.append("Invalid file format")
        
        # Try to extract data
        transactions = extractor.extract()
        if not transactions:
            issues.append("No valid transactions found")
        else:
            print(f"✅ Found {len(transactions)} valid transactions")
            
            # Show sample transactions
            print("\nSample transactions:")
            for i, trans in enumerate(transactions[:3]):
                print(f"  {i+1}. {trans.date} | {trans.category_origin} | ${trans.value:.2f}")
            if len(transactions) > 3:
                print(f"  ... and {len(transactions) - 3} more")
        
    except Exception as e:
        issues.append(f"Extraction failed: {e}")
    
    return len(issues) == 0, issues


def validate_mapping_file(file_path: str) -> tuple[bool, list[str]]:
    """
    Validate the mapping configuration file.
    
    Args:
        file_path: Path to mapping file
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        mapper = CategoryMapper(file_path)
        
        # Get mapping summary
        summary = mapper.get_mapping_summary()
        print(f"✅ Mapping loaded successfully")
        print(f"   • Category mappings: {summary['total_category_mappings']}")
        print(f"   • Subcategory mappings: {summary['total_subcategory_mappings']}")
        print(f"   • Unique categories: {summary['unique_categories']}")
        print(f"   • Unique subcategories: {summary['unique_subcategories']}")
        
        # Validate mapping
        warnings = mapper.mapping.validate()
        if warnings:
            issues.extend(warnings)
        
    except Exception as e:
        issues.append(f"Mapping validation failed: {e}")
    
    return len(issues) == 0, issues


def validate_destination_file(file_path: str) -> tuple[bool, list[str]]:
    """
    Validate the destination Excel file.
    
    Args:
        file_path: Path to destination file
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        loader = ExcelLoader(file_path)
        
        # Validate file format
        if not loader.validate_destination_format():
            issues.append("Invalid destination file format")
        else:
            print("✅ Destination file format is valid")
        
    except Exception as e:
        issues.append(f"Destination validation failed: {e}")
    
    return len(issues) == 0, issues


def main() -> int:
    """
    Main function for data validation.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Validate ETL pipeline data and configuration files"
    )
    
    parser.add_argument(
        "--config",
        help="Path to environment configuration file (default: .env)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = ETLConfig.from_env(args.config)
        
        # Setup logging
        setup_logging(config.log_file, verbose=args.verbose)
        
        print("🔍 ETL Data Validation")
        print("=" * 50)
        
        all_valid = True
        
        # Validate source file
        print(f"\n📁 Validating source file: {config.source_file}")
        source_valid, source_issues = validate_source_file(config.source_file)
        if not source_valid:
            all_valid = False
            print("❌ Source file validation failed:")
            for issue in source_issues:
                print(f"   • {issue}")
        
        # Validate mapping file
        print(f"\n🗺️  Validating mapping file: {config.mapping_file}")
        mapping_valid, mapping_issues = validate_mapping_file(config.mapping_file)
        if not mapping_valid:
            all_valid = False
            print("❌ Mapping file validation failed:")
            for issue in mapping_issues:
                print(f"   • {issue}")
        elif mapping_issues:  # Warnings
            print("⚠️  Mapping validation warnings:")
            for issue in mapping_issues:
                print(f"   • {issue}")
        
        # Validate destination file
        print(f"\n📊 Validating destination file: {config.dest_file}")
        dest_valid, dest_issues = validate_destination_file(config.dest_file)
        if not dest_valid:
            all_valid = False
            print("❌ Destination file validation failed:")
            for issue in dest_issues:
                print(f"   • {issue}")
        
        # Summary
        print("\n" + "=" * 50)
        if all_valid:
            print("✅ All validations passed! Pipeline is ready to run.")
            return 0
        else:
            print("❌ Some validations failed. Please fix the issues before running the pipeline.")
            return 1
            
    except Exception as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
