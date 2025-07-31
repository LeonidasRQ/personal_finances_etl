"""
Date utility functions for parsing and handling dates.
"""

import datetime
from typing import Union


def parse_date(date_input: Union[str, datetime.date, datetime.datetime]) -> datetime.date:
    """
    Parse various date formats into a date object.
    
    Args:
        date_input: Date as string, date object, or datetime object
        
    Returns:
        Parsed date object
        
    Raises:
        ValueError: If the date format is not recognized
    """
    if isinstance(date_input, datetime.date):
        return date_input
    
    if isinstance(date_input, datetime.datetime):
        return date_input.date()
    
    if isinstance(date_input, str):
        # Try common date formats
        formats = [
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m/%d/%Y",
            "%Y/%m/%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_input, fmt).date()
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_input}")
    
    raise TypeError(f"Unsupported date type: {type(date_input)}")


def format_date_for_excel(date_obj: datetime.date) -> datetime.date:
    """
    Format date for Excel output.
    
    Args:
        date_obj: Date to format
        
    Returns:
        Date formatted for Excel
    """
    return date_obj
