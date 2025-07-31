#!/usr/bin/env python3
"""
Test runner script for ETL Finance project.
This script provides different ways to run the tests.
"""

import sys
import subprocess
import os

def run_unittest():
    """Run tests using unittest."""
    print("Running legacy tests with unittest...")
    result = subprocess.run([sys.executable, "-m", "unittest", "tests.test_legacy_etl", "-v"], 
                          capture_output=False)
    return result.returncode

def run_pytest():
    """Run tests using pytest."""
    print("Running tests with pytest...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                          capture_output=False)
    return result.returncode

def run_pytest_with_coverage():
    """Run tests with coverage report."""
    print("Running tests with coverage...")
    
    # Coverage for both legacy etl_finance.py and new modular structure
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "--cov=src",
        "--cov=etl_finance", 
        "--cov-report=html", 
        "--cov-report=term-missing",
        "-v"
    ], capture_output=False)
    return result.returncode

def run_specific_tests():
    """Run specific test categories."""
    print("Available test categories:")
    print("  1. Legacy tests (test_legacy_etl.py)")
    print("  2. Model tests (test_models.py)")
    print("  3. All modular tests")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        return subprocess.run([sys.executable, "-m", "pytest", "tests/test_legacy_etl.py", "-v"]).returncode
    elif choice == "2":
        return subprocess.run([sys.executable, "-m", "pytest", "tests/test_models.py", "-v"]).returncode
    elif choice == "3":
        return subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--ignore=tests/test_legacy_etl.py"]).returncode
    else:
        print("Invalid choice")
        return 1

def main():
    """Main function to choose test runner."""
    if len(sys.argv) > 1:
        runner = sys.argv[1].lower()
        if runner == "unittest":
            return run_unittest()
        elif runner == "pytest":
            return run_pytest()
        elif runner == "coverage":
            return run_pytest_with_coverage()
        elif runner == "specific":
            return run_specific_tests()
        else:
            print(f"Unknown runner: {runner}")
            print("Available options: unittest, pytest, coverage, specific")
            return 1
    else:
        # Default to pytest
        return run_pytest()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
