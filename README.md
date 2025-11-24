# Polaris Sitemap Generator

A Python tool for generating XML sitemaps from CSV input files with Coveo metadata support.

## Features

- **Main sitemap index** ([sitemap.xml](output/sitemap.xml)) that refers to all individual sitemaps
- **Individual sitemaps** generated from CSV files (e.g., `manual_input.csv` → `manual.xml`)
- **Coveo metadata support** for rich search indexing
- **URL validation** and XML escaping
- **Configurable** base URLs and output locations

## Directory Structure

```
polaris_sitemap_generator/
├── input/              # Place CSV files here (*_input.csv)
├── output/             # Generated XML sitemaps
├── examples/           # Example sitemap files
└── src/                # Source code
```

## CSV Input Format

CSV files should be named with `_input.csv` suffix (e.g., `manual_input.csv`, `vehicles_input.csv`).

**Required column:**
- `url` - The page URL (first column)

**Optional columns** (automatically mapped to Coveo metadata):
- `type` - Content type
- `manufacturer` - Product manufacturer
- `modelNumber` - Model identifier
- `title` - Page title
- `lastmod` - Last modification date (YYYY-MM-DD format)
- Any other custom metadata fields

**Example CSV:**
```csv
url,type,manufacturer,modelNumber,title,lastmod
https://www.polaris.com/manual1.pdf,Manual,Polaris,RZR-1000,Polaris RZR-1000 Service Manual,2025-10-23
https://www.polaris.com/manual2.pdf,Manual,Polaris,RANGER-900,Polaris RANGER-900 Parts Manual,2025-10-22
```

## Usage

### Generate All Sitemaps

```bash
python3 src/sitemap_generator.py
```

This will:
1. Process all `*_input.csv` files in the [input/](input/) directory
2. Generate individual XML sitemaps in the [output/](output/) directory
3. Create a main [sitemap.xml](output/sitemap.xml) index file

### Generate Single Sitemap

```bash
python3 src/sitemap_generator.py --single input/manual_input.csv
```

### Custom Options

```bash
python3 src/sitemap_generator.py \
  --input ./my_input_dir \
  --output ./my_output_dir \
  --base-url https://www.polaris.com/sitemaps/
```

**Options:**
- `--input DIR` - Input directory containing CSV files (default: `input/`)
- `--output DIR` - Output directory for XML files (default: `output/`)
- `--base-url URL` - Base URL for sitemap locations (default: `https://www.polaris.com/sitemaps/`)
- `--single FILE` - Process only a single CSV file

## Output Format

### Individual Sitemap

Generated files follow the [sitemaps.org](http://sitemaps.org) protocol with Coveo metadata extensions:

```xml
<?xml version="1.0" ?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:coveo="https://www.coveo.com/en/company/about-us">
    <url>
        <loc>https://www.polaris.com/en-us/off-road/models/</loc>
        <lastmod>2025-10-23</lastmod>
        <coveo:metadata>
            <type>Vehicles</type>
            <manufacturer>Polaris</manufacturer>
            <modelNumber>RZR-1000</modelNumber>
            <title>Polaris RZR-1000 Service Manual</title>
        </coveo:metadata>
    </url>
</urlset>
```

### Sitemap Index

The main [sitemap.xml](output/sitemap.xml) references all individual sitemaps:

```xml
<?xml version="1.0" ?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://www.polaris.com/sitemaps/manual.xml</loc>
        <lastmod>2025-11-23</lastmod>
    </sitemap>
</sitemapindex>
```

## Configuration

Edit [src/config.py](src/config.py) to customize:

- `BASE_URL` - Base URL for sitemap locations
- `MAX_URLS_PER_SITEMAP` - Maximum URLs per sitemap (default: 50,000)
- `MAX_SITEMAP_SIZE_MB` - Maximum sitemap size (default: 50MB)
- `METADATA_FIELDS` - Metadata fields to include

## Deployment

1. Generate sitemaps: `python3 src/sitemap_generator.py`
2. Upload all XML files from [output/](output/) to your web server
3. Ensure they're accessible at your configured base URL
4. Submit the main sitemap to search engines (e.g., Google Search Console)

## Requirements

Python 3.6+ (uses only standard library modules, no external dependencies)

## Reference

See [examples/parts-manuals.xml](examples/parts-manuals.xml) for schema and structure of Coveo metadata.