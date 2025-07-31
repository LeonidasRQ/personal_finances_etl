"""
Configuration management for the ETL pipeline.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


@dataclass
class ETLConfig:
    """Configuration settings for the ETL pipeline."""
    source_file: str
    dest_file: str
    mapping_file: str
    log_file: str
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> 'ETLConfig':
        """
        Create configuration from environment variables.
        
        Args:
            env_file: Path to .env file (optional)
            
        Returns:
            ETLConfig instance
            
        Raises:
            ValueError: If required environment variables are missing
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # Get required environment variables
        source_file = os.getenv("SOURCE_FILE")
        dest_file = os.getenv("DEST_FILE")
        mapping_file = os.getenv("MAPPING_FILE")
        log_file = os.getenv("LOG_FILE")
        
        # Validate required variables
        missing = []
        if not source_file:
            missing.append("SOURCE_FILE")
        if not dest_file:
            missing.append("DEST_FILE")
        if not mapping_file:
            missing.append("MAPPING_FILE")
        if not log_file:
            missing.append("LOG_FILE")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return cls(
            source_file=source_file,
            dest_file=dest_file,
            mapping_file=mapping_file,
            log_file=log_file
        )
    
    def validate(self) -> None:
        """
        Validate that required files exist and are accessible.
        
        Raises:
            FileNotFoundError: If required input files don't exist
            PermissionError: If files are not accessible
        """
        # Check if source files exist
        source_path = Path(self.source_file)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {self.source_file}")
        if not source_path.is_file():
            raise ValueError(f"Source path is not a file: {self.source_file}")
        
        mapping_path = Path(self.mapping_file)
        if not mapping_path.exists():
            raise FileNotFoundError(f"Mapping file not found: {self.mapping_file}")
        if not mapping_path.is_file():
            raise ValueError(f"Mapping path is not a file: {self.mapping_file}")
        
        # Check if destination file is accessible (if it exists)
        dest_path = Path(self.dest_file)
        if dest_path.exists():
            if not dest_path.is_file():
                raise ValueError(f"Destination path is not a file: {self.dest_file}")
            # Check if file is writable
            if not os.access(dest_path, os.W_OK):
                raise PermissionError(f"Destination file is not writable: {self.dest_file}")
        else:
            # Check if parent directory exists and is writable
            parent_dir = dest_path.parent
            if not parent_dir.exists():
                raise FileNotFoundError(f"Destination directory does not exist: {parent_dir}")
            if not os.access(parent_dir, os.W_OK):
                raise PermissionError(f"Destination directory is not writable: {parent_dir}")
        
        # Ensure log directory exists
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def __str__(self) -> str:
        """Return string representation of configuration."""
        return (
            f"ETLConfig(\n"
            f"  source_file='{self.source_file}'\n"
            f"  dest_file='{self.dest_file}'\n"
            f"  mapping_file='{self.mapping_file}'\n"
            f"  log_file='{self.log_file}'\n"
            f")"
        )
