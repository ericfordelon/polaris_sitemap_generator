#!/usr/bin/env python3
"""
Main sitemap generator script.

Generates individual sitemaps from CSV files and creates a main sitemap index.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from config import INPUT_DIR, OUTPUT_DIR, BASE_URL
from csv_parser import CSVParser
from xml_builder import XMLBuilder
from validators import ValidationError


class SitemapGenerator:
    """Main sitemap generation orchestrator."""

    def __init__(self, input_dir: Path, output_dir: Path, base_url: str):
        """
        Initialize sitemap generator.

        Args:
            input_dir: Directory containing CSV input files
            output_dir: Directory where XML files will be saved
            base_url: Base URL for sitemap locations
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.base_url = base_url.rstrip('/') + '/'

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self) -> List[Path]:
        """
        Generate all sitemaps from CSV files in input directory.

        Returns:
            List of generated sitemap file paths
        """
        # Discover CSV files
        csv_files = CSVParser.discover_csv_files(self.input_dir)

        if not csv_files:
            print(f"No CSV files found in {self.input_dir}")
            print(f"Looking for files matching pattern: *_input.csv")
            return []

        print(f"Found {len(csv_files)} CSV file(s)")
        print()

        # Generate individual sitemaps
        generated_files = []
        for csv_file in csv_files:
            try:
                sitemap_file = self.generate_sitemap(csv_file)
                if sitemap_file:
                    generated_files.append(sitemap_file)
            except Exception as e:
                print(f"Error processing {csv_file.name}: {e}")
                continue

        print()
        return generated_files

    def generate_sitemap(self, csv_path: Path) -> Optional[Path]:
        """
        Generate a single sitemap from a CSV file.

        Args:
            csv_path: Path to CSV file

        Returns:
            Path to generated XML file, or None if generation failed
        """
        print(f"Processing {csv_path.name}...")

        try:
            # Parse CSV
            parser = CSVParser(csv_path)
            url_entries = parser.parse()

            if not url_entries:
                print(f"  Warning: No valid URLs found in {csv_path.name}")
                return None

            # Generate output filename
            output_name = CSVParser.get_output_name(csv_path)
            output_path = self.output_dir / output_name

            # Build XML
            XMLBuilder.build_sitemap(url_entries, output_path)

            return output_path

        except ValidationError as e:
            print(f"  Validation error: {e}")
            return None
        except Exception as e:
            print(f"  Error: {e}")
            return None

    def generate_index(self, sitemap_files: List[Path]) -> Optional[Path]:
        """
        Generate main sitemap index.

        Args:
            sitemap_files: List of individual sitemap file paths

        Returns:
            Path to generated sitemap index file
        """
        if not sitemap_files:
            print("No sitemaps to include in index")
            return None

        index_path = self.output_dir / "sitemap.xml"

        # Update base URL in config for XML builder
        import config
        original_base_url = config.BASE_URL
        config.BASE_URL = self.base_url

        try:
            XMLBuilder.build_sitemap_index(sitemap_files, index_path)
            return index_path
        finally:
            # Restore original base URL
            config.BASE_URL = original_base_url

    def run(self) -> int:
        """
        Run the complete sitemap generation process.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        print("=" * 70)
        print("Polaris Sitemap Generator")
        print("=" * 70)
        print()

        # Generate individual sitemaps
        sitemap_files = self.generate_all()

        if not sitemap_files:
            print("No sitemaps generated")
            return 1

        # Generate sitemap index
        print("Generating sitemap index...")
        index_file = self.generate_index(sitemap_files)

        if not index_file:
            return 1

        print()
        print("=" * 70)
        print("Generation complete!")
        print("=" * 70)
        print()
        print(f"Generated {len(sitemap_files)} sitemap(s) in: {self.output_dir}")
        print(f"Main sitemap index: {index_file.name}")
        print()
        print("Next steps:")
        print(f"1. Upload all XML files from {self.output_dir} to your web server")
        print(f"2. Ensure they are accessible at: {self.base_url}")
        print(f"3. Submit {self.base_url}sitemap.xml to search engines")
        print()

        return 0


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Generate XML sitemaps from CSV input files with Coveo metadata support"
    )

    parser.add_argument(
        '--input',
        type=str,
        default=str(INPUT_DIR),
        help=f'Input directory containing CSV files (default: {INPUT_DIR})'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=str(OUTPUT_DIR),
        help=f'Output directory for XML files (default: {OUTPUT_DIR})'
    )

    parser.add_argument(
        '--base-url',
        type=str,
        default=BASE_URL,
        help=f'Base URL for sitemap locations (default: {BASE_URL})'
    )

    parser.add_argument(
        '--single',
        type=str,
        help='Process only a single CSV file instead of all files in input directory'
    )

    args = parser.parse_args()

    # Create generator
    generator = SitemapGenerator(
        input_dir=args.input,
        output_dir=args.output,
        base_url=args.base_url
    )

    # Run generation
    if args.single:
        # Process single file
        csv_path = Path(args.single)
        if not csv_path.exists():
            print(f"Error: File not found: {csv_path}")
            return 1

        print(f"Processing single file: {csv_path.name}")
        sitemap_file = generator.generate_sitemap(csv_path)

        if sitemap_file:
            print(f"\nGenerated: {sitemap_file}")
            return 0
        else:
            return 1
    else:
        # Process all files
        return generator.run()


if __name__ == '__main__':
    sys.exit(main())
