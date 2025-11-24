"""
XML building utilities for sitemap generation.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict
import xml.etree.ElementTree as ET

from config import (
    SITEMAP_NAMESPACE,
    COVEO_NAMESPACE,
    BASE_URL,
    DATE_FORMAT,
)
from validators import validate_sitemap_size


class XMLBuilder:
    """Builder for sitemap XML files."""

    @staticmethod
    def build_sitemap(url_entries: List[Dict[str, str]], output_path: Path) -> None:
        """
        Build an individual sitemap XML file.

        Args:
            url_entries: List of URL entry dictionaries
            output_path: Path where XML file will be saved
        """
        # Register namespace prefix
        ET.register_namespace('coveo', COVEO_NAMESPACE)

        # Build XML manually for better control over formatting
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append(f'<urlset xmlns="{SITEMAP_NAMESPACE}" xmlns:coveo="{COVEO_NAMESPACE}">')

        for entry in url_entries:
            lines.append('    <url>')
            lines.append(f'        <loc>{entry["url"]}</loc>')

            # Add lastmod if present
            if 'lastmod' in entry and entry['lastmod']:
                lines.append(f'        <lastmod>{entry["lastmod"]}</lastmod>')

            # Add Coveo metadata if present
            if 'metadata' in entry and entry['metadata']:
                lines.append('        <coveo:metadata>')
                for field_name, field_value in entry['metadata'].items():
                    lines.append(f'            <{field_name}>{field_value}</{field_name}>')
                lines.append('        </coveo:metadata>')

            lines.append('    </url>')

        lines.append('</urlset>')

        xml_string = '\n'.join(lines)

        # Validate size
        size_bytes = len(xml_string.encode('utf-8'))
        validate_sitemap_size(len(url_entries), size_bytes)

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_string)

        print(f"Generated sitemap: {output_path.name} ({len(url_entries)} URLs, {size_bytes:,} bytes)")

    @staticmethod
    def build_sitemap_index(sitemap_files: List[Path], output_path: Path) -> None:
        """
        Build main sitemap index XML file.

        Args:
            sitemap_files: List of individual sitemap file paths
            output_path: Path where index XML will be saved
        """
        # Get current date for lastmod
        current_date = datetime.now().strftime(DATE_FORMAT)

        # Build XML manually for better control over formatting
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append(f'<sitemapindex xmlns="{SITEMAP_NAMESPACE}">')

        # Add each sitemap
        for sitemap_file in sorted(sitemap_files):
            lines.append('    <sitemap>')
            lines.append(f'        <loc>{BASE_URL}{sitemap_file.name}</loc>')
            lines.append(f'        <lastmod>{current_date}</lastmod>')
            lines.append('    </sitemap>')

        lines.append('</sitemapindex>')

        xml_string = '\n'.join(lines)

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_string)

        print(f"Generated sitemap index: {output_path.name} ({len(sitemap_files)} sitemaps)")
