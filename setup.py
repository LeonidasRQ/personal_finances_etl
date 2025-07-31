"""
Setup script for ETL Finance package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="etl-finance",
    version="1.0.0",
    author="Leonidas",
    description="A modular ETL pipeline for processing financial data from Excel files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[req for req in requirements if not req.startswith("pytest") and not req.startswith("black") and not req.startswith("flake8")],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "flake8>=7.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "etl-finance=scripts.run_etl:main",
            "etl-validate=scripts.validate_data:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    zip_safe=False,
)
