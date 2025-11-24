"""
Configuration settings for the sitemap generator.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Directory paths
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
EXAMPLES_DIR = BASE_DIR / "examples"

# Sitemap settings
BASE_URL = "https://www.polaris.com/sitemaps/"
MAX_URLS_PER_SITEMAP = 50000
MAX_SITEMAP_SIZE_MB = 50

# Default values
DEFAULT_CHANGEFREQ = "monthly"
DEFAULT_PRIORITY = "0.8"

# XML namespaces
SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
COVEO_NAMESPACE = "https://www.coveo.com/en/company/about-us"

# Metadata field configuration
# These are the CSV columns that will be mapped to Coveo metadata
METADATA_FIELDS = [
    "type",
    "manufacturer",
    "modelNumber",
    "title",
    "description",
    "category",
]

# CSV configuration
CSV_ENCODING = "utf-8"
REQUIRED_COLUMNS = ["url"]

# Date format
DATE_FORMAT = "%Y-%m-%d"
