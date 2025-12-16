"""
CSV parsing utilities for sitemap generation.
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional

from config import CSV_ENCODING, REQUIRED_COLUMNS, METADATA_FIELDS
from validators import validate_url, validate_date, validate_metadata_field, ValidationError


class CSVParser:
    """Parser for CSV files containing sitemap URL data."""

    def __init__(self, csv_path: Path):
        """
        Initialize CSV parser.

        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = Path(csv_path)
        self.rows = []
        self.headers = []

    def parse(self) -> List[Dict[str, str]]:
        """
        Parse CSV file and return list of URL entries.

        Returns:
            List of dictionaries containing URL and metadata

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValidationError: If CSV is invalid
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        with open(self.csv_path, 'r', encoding=CSV_ENCODING) as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames

            if not self.headers:
                raise ValidationError(f"CSV file has no headers: {self.csv_path}")

            # Validate required columns
            self._validate_headers()

            # Parse rows
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                try:
                    parsed_row = self._parse_row(row, row_num)
                    if parsed_row:  # Skip empty rows
                        self.rows.append(parsed_row)
                except ValidationError as e:
                    print(f"Warning: Skipping row {row_num} in {self.csv_path.name}: {e}")
                    continue

        return self.rows

    def _validate_headers(self) -> None:
        """
        Validate that required columns are present.

        Raises:
            ValidationError: If required columns are missing
        """
        missing_columns = []
        for required_col in REQUIRED_COLUMNS:
            if required_col not in self.headers:
                missing_columns.append(required_col)

        if missing_columns:
            raise ValidationError(
                f"Missing required columns in {self.csv_path.name}: {', '.join(missing_columns)}"
            )

    def _parse_row(self, row: Dict[str, str], row_num: int) -> Optional[Dict[str, str]]:
        """
        Parse and validate a single CSV row.

        Args:
            row: Dictionary of row data
            row_num: Row number for error reporting

        Returns:
            Parsed row dictionary or None if row is empty

        Raises:
            ValidationError: If row data is invalid
        """
        # Get URL (required)
        url = row.get('url', '')
        if url is None:
            return None
        url = url.strip()

        # Skip empty rows
        if not url:
            return None

        # Validate URL
        validate_url(url)

        # Build parsed row
        parsed = {'url': url}

        # Parse lastmod if present
        if 'lastmod' in row and row['lastmod']:
            parsed['lastmod'] = validate_date(row['lastmod'])

        # Parse metadata fields
        metadata = {}
        for field in self.headers:
            # Skip special fields or None fields
            if not field or field in ['url', 'lastmod']:
                continue

            # Get field value
            value = row.get(field, '')
            if value is None:
                continue
            value = value.strip()

            # Only include non-empty values
            if value:
                sanitized_value = validate_metadata_field(field, value)
                if sanitized_value:
                    metadata[field] = sanitized_value

        if metadata:
            parsed['metadata'] = metadata

        return parsed

    @staticmethod
    def discover_csv_files(input_dir: Path) -> List[Path]:
        """
        Discover all CSV files in input directory.

        Args:
            input_dir: Directory to search

        Returns:
            List of CSV file paths
        """
        input_dir = Path(input_dir)
        if not input_dir.exists():
            return []

        # Find all CSV files
        csv_files = list(input_dir.glob('*.csv'))
        return sorted(csv_files)

    @staticmethod
    def get_output_name(csv_path: Path) -> str:
        """
        Generate output XML filename from CSV filename.

        Args:
            csv_path: Path to CSV file

        Returns:
            Output XML filename (e.g., 'polaris.csv' -> 'polaris.xml')
        """
        name = csv_path.stem  # Get filename without extension
        return f"{name}.xml"
