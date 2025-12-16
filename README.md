# Sitemap Generator

A Python tool for generating XML sitemaps from CSV input files with Coveo metadata support.

## Features

- **Main sitemap index** ([sitemap.xml](output/sitemap.xml)) that refers to all individual sitemaps
- **Individual sitemaps** generated from CSV files (e.g., `polaris.csv` → `polaris.xml`)
- **Coveo metadata support** for rich search indexing
- **URL validation** and XML escaping
- **Configurable** base URLs and output locations
- **Multiple site support** - Each CSV file becomes its own sitemap

## Directory Structure

```
sitemap_generator/
├── input/              # Place CSV files here (*.csv)
├── output/             # Generated XML sitemaps
├── examples/           # Example sitemap files
└── src/                # Source code
```

## CSV Input Format

Each CSV file in the input directory will generate a corresponding XML sitemap. Name your CSV files descriptively (e.g., `polaris.csv`, `blog.csv`, `products.csv`).

**Required column:**
- `url` - The page URL (first column)

**Optional columns** (automatically mapped to Coveo metadata):
- `type` - Content type
- `manufacturer` - Product manufacturer
- `modelNumber` - Model identifier
- `title` - Page title
- `lastmod` - Last modification date (YYYY-MM-DD format)
- Any other custom metadata fields

**Example CSV (polaris.csv):**
```csv
url,type,topic
https://www.polaris.com/en-us/off-road/models/,Vehicles,Models
https://www.polaris.com/en-us/off-road/ranger/,Vehicles,By Brand
```

**Example CSV (blog.csv):**
```csv
url,type,category,lastmod
https://example.com/blog/post1,Article,News,2025-10-23
https://example.com/blog/post2,Article,Tutorial,2025-10-22
```

## Usage

### Generate All Sitemaps

```bash
python3 src/sitemap_generator.py
```

This will:
1. Process all `*.csv` files in the [input/](input/) directory
2. Generate individual XML sitemaps in the [output/](output/) directory
   (e.g., `polaris.csv` → `polaris.xml`, `blog.csv` → `blog.xml`)
3. Create a main [sitemap.xml](output/sitemap.xml) index file

### Generate Single Sitemap

```bash
python3 src/sitemap_generator.py --single input/polaris.csv
```

### Custom Options

```bash
python3 src/sitemap_generator.py \
  --input ./my_input_dir \
  --output ./my_output_dir \
  --base-url https://example.com/sitemaps/
```

Or set via environment variable:
```bash
export SITEMAP_BASE_URL=https://example.com/sitemaps/
python3 src/sitemap_generator.py
```

**Options:**
- `--input DIR` - Input directory containing CSV files (default: `input/`)
- `--output DIR` - Output directory for XML files (default: `output/`)
- `--base-url URL` - Base URL for sitemap locations (default: from env or `https://example.com/sitemaps/`)
- `--single FILE` - Process only a single CSV file

## Output Format

### Individual Sitemap

Generated files follow the [sitemaps.org](http://sitemaps.org) protocol with Coveo metadata extensions:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:coveo="https://www.coveo.com/en/company/about-us">
    <url>
        <loc>https://www.polaris.com/en-us/off-road/models/</loc>
        <coveo:metadata>
            <type>Vehicles</type>
            <topic>Models</topic>
        </coveo:metadata>
    </url>
</urlset>
```

### Sitemap Index

The main [sitemap.xml](output/sitemap.xml) references all individual sitemaps:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://example.com/sitemaps/polaris.xml</loc>
        <lastmod>2025-11-24</lastmod>
    </sitemap>
    <sitemap>
        <loc>https://example.com/sitemaps/blog.xml</loc>
        <lastmod>2025-11-24</lastmod>
    </sitemap>
</sitemapindex>
```

## Configuration

Edit [src/config.py](src/config.py) to customize:

- `BASE_URL` - Base URL for sitemap locations
- `MAX_URLS_PER_SITEMAP` - Maximum URLs per sitemap (default: 50,000)
- `MAX_SITEMAP_SIZE_MB` - Maximum sitemap size (default: 50MB)
- `METADATA_FIELDS` - Metadata fields to include

## Multiple Sites Example

You can manage sitemaps for multiple sites or content types in one place:

```
input/
├── polaris.csv        # Polaris website URLs
├── blog.csv           # Blog URLs
└── products.csv       # Product catalog URLs

↓ python3 src/sitemap_generator.py

output/
├── polaris.xml        # Generated from polaris.csv
├── blog.xml           # Generated from blog.csv
├── products.xml       # Generated from products.csv
└── sitemap.xml        # Main index referencing all three
```

## Deployment

### GitHub Pages Deployment

1. Set the base URL:
   ```bash
   export SITEMAP_BASE_URL=https://ericfordelon.github.io/polaris_sitemap_generator/output/
   ```

2. Generate sitemaps:
   ```bash
   python3 src/sitemap_generator.py
   ```

3. Commit and push to GitHub:
   ```bash
   git add output/*.xml
   git commit -m "Update sitemaps"
   git push
   ```

4. Enable GitHub Pages in repository settings (if not already enabled)

5. Submit the main sitemap to search engines:
   `https://ericfordelon.github.io/polaris_sitemap_generator/output/sitemap.xml`

### Traditional Deployment

1. Generate sitemaps: `python3 src/sitemap_generator.py`
2. Upload all XML files from [output/](output/) to your web server
3. Ensure they're accessible at your configured base URL
4. Submit the main sitemap to search engines (e.g., Google Search Console)

## Requirements

Python 3.6+ (uses only standard library modules, no external dependencies)

## Reference

See [examples/parts-manuals.xml](examples/parts-manuals.xml) for schema and structure of Coveo metadata.