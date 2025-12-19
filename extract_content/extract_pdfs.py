#!/usr/bin/env python3
"""
PDF Content Extractor

Extracts text content and metadata from PDF files and outputs as JSON.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install it with: pip install PyPDF2")
    sys.exit(1)


class PDFExtractor:
    """Extract content from PDF files."""

    def __init__(self, pdf_dir: Path, output_file: Path, base_uri: str = ""):
        """
        Initialize PDF extractor.

        Args:
            pdf_dir: Directory containing PDF files
            output_file: Path to output JSON file
            base_uri: Base URI for generating document URIs (optional)
        """
        self.pdf_dir = Path(pdf_dir)
        self.output_file = Path(output_file)
        self.base_uri = base_uri.rstrip('/') + '/' if base_uri else ''

    def extract_title_from_metadata(self, pdf_reader: PyPDF2.PdfReader) -> Optional[str]:
        """
        Extract title from PDF metadata.

        Args:
            pdf_reader: PyPDF2 reader object

        Returns:
            Title from metadata or None if not found
        """
        try:
            metadata = pdf_reader.metadata
            if metadata and metadata.get('/Title'):
                title = metadata.get('/Title')
                # Clean up title
                if isinstance(title, str):
                    return title.strip()
        except Exception as e:
            print(f"  Warning: Could not read metadata: {e}")
        return None

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract all text from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content
        """
        text_content = []

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    try:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
                    except Exception as e:
                        print(f"  Warning: Could not extract text from page {page_num}: {e}")

        except Exception as e:
            print(f"  Error reading PDF: {e}")
            return ""

        return '\n'.join(text_content)

    def get_title_from_filename(self, filename: str) -> str:
        """
        Generate title from filename.

        Args:
            filename: PDF filename

        Returns:
            Formatted title based on filename
        """
        # Remove .pdf extension and replace underscores/hyphens with spaces
        title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        # Capitalize words
        title = ' '.join(word.capitalize() for word in title.split())
        return title

    def extract_pdf(self, pdf_path: Path) -> Dict[str, str]:
        """
        Extract content from a single PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with title, body, and uri
        """
        print(f"Processing: {pdf_path.name}")

        # Generate URI
        uri = f"{self.base_uri}{pdf_path.name}"

        # Try to extract title from metadata first
        title = None
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                title = self.extract_title_from_metadata(pdf_reader)
        except Exception as e:
            print(f"  Warning: Could not read PDF for metadata: {e}")

        # Fall back to filename if no title in metadata
        if not title:
            title = self.get_title_from_filename(pdf_path.name)
            print(f"  Using filename as title: {title}")
        else:
            print(f"  Found title in metadata: {title}")

        # Extract text content
        body = self.extract_text_from_pdf(pdf_path)
        body_length = len(body)
        print(f"  Extracted {body_length} characters")

        return {
            "title": title,
            "body": body,
            "uri": uri
        }

    def extract_all(self) -> List[Dict[str, str]]:
        """
        Extract content from all PDF files in directory.

        Returns:
            List of extracted document dictionaries
        """
        if not self.pdf_dir.exists():
            print(f"Error: Directory not found: {self.pdf_dir}")
            return []

        # Find all PDF files
        pdf_files = sorted(self.pdf_dir.glob('*.pdf'))

        if not pdf_files:
            print(f"No PDF files found in {self.pdf_dir}")
            return []

        print(f"Found {len(pdf_files)} PDF file(s)")
        print()

        documents = []
        for pdf_path in pdf_files:
            try:
                doc = self.extract_pdf(pdf_path)
                documents.append(doc)
                print()
            except Exception as e:
                print(f"  Error processing {pdf_path.name}: {e}")
                print()
                continue

        return documents

    def save_to_json(self, documents: List[Dict[str, str]]) -> None:
        """
        Save extracted documents to JSON file.

        Args:
            documents: List of document dictionaries
        """
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(documents)} document(s) to: {self.output_file}")

    def run(self) -> int:
        """
        Run the extraction process.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        print("=" * 70)
        print("PDF Content Extractor")
        print("=" * 70)
        print()

        documents = self.extract_all()

        if not documents:
            print("No documents extracted")
            return 1

        self.save_to_json(documents)

        print()
        print("=" * 70)
        print("Extraction complete!")
        print("=" * 70)

        return 0


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract text content and metadata from PDF files"
    )

    parser.add_argument(
        '--input',
        type=str,
        default='static',
        help='Input directory containing PDF files (default: static/)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='extract_content/pdfs.json',
        help='Output JSON file (default: extract_content/pdfs.json)'
    )

    parser.add_argument(
        '--base-uri',
        type=str,
        default='https://ericfordelon.github.io/polaris_sitemap_generator/static/',
        help='Base URI for document URIs'
    )

    args = parser.parse_args()

    extractor = PDFExtractor(
        pdf_dir=args.input,
        output_file=args.output,
        base_uri=args.base_uri
    )

    sys.exit(extractor.run())


if __name__ == '__main__':
    main()
