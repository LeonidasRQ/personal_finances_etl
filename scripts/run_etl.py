#!/usr/bin/env python3
"""
Main entry point for the ETL Finance pipeline.

This script provides a command-line interface for running the financial data ETL process.
"""

import argparse
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from etl.pipeline import ETLPipeline
from config.settings import ETLConfig
from utils.logging_config import setup_logging


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Financial Data ETL Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default configuration
  python run_etl.py
  
  # Run in dry-run mode
  python run_etl.py --dry-run
  
  # Use custom environment file
  python run_etl.py --config .env.test
  
  # Enable verbose logging
  python run_etl.py --verbose
  
  # Skip input validation
  python run_etl.py --no-validate
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without saving changes to the destination file"
    )
    
    parser.add_argument(
        "--config",
        help="Path to environment configuration file (default: .env)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging output"
    )
    
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip input file validation"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show pipeline configuration and exit"
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Main function for the ETL pipeline.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Load configuration
        try:
            config = ETLConfig.from_env(args.config)
            config.validate()
        except Exception as e:
            print(f"❌ Configuration error: {e}", file=sys.stderr)
            return 1
        
        # Setup logging
        logger = setup_logging(config.log_file, verbose=args.verbose)
        
        # Show configuration info if requested
        if args.info:
            print("ETL Pipeline Configuration:")
            print(config)
            return 0
        
        # Create and configure pipeline
        pipeline = ETLPipeline(
            source_file=config.source_file,
            dest_file=config.dest_file,
            mapping_file=config.mapping_file
        )
        
        # Log pipeline info
        if args.verbose:
            info = pipeline.get_pipeline_info()
            logger.info("Pipeline Configuration:")
            for key, value in info.items():
                logger.info(f"  {key}: {value}")
        
        # Run the pipeline
        results = pipeline.run(
            dry_run=args.dry_run,
            validate_inputs=not args.no_validate
        )
        
        # Handle results
        if results["status"] == "completed":
            if args.dry_run:
                print(f"✅ [DRY RUN] Would process {results['transactions_loaded']} transactions")
            else:
                print(f"✅ Successfully processed {results['transactions_loaded']} transactions")
            return 0
        else:
            print(f"❌ Pipeline failed: {results.get('error', 'Unknown error')}", file=sys.stderr)
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
