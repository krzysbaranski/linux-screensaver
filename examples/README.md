# Example Data Files

This directory contains example data files that demonstrate the CSV Retro Screensaver.

## Files

- **retro_computers.csv** - Classic computers from the 1970s and 1980s
- **fun_facts.csv** - Interesting trivia from various fields
- **programming_languages.csv** - Popular programming languages and their creators
- **space_missions.csv.gz** - Space missions (gzipped CSV format)
- **operating_systems.parquet** - Operating systems (Parquet format)

## Supported File Formats

The screensaver supports the following formats:
- **CSV** (`.csv`) - Standard comma-separated values
- **Gzipped CSV** (`.csv.gz`) - Compressed CSV files
- **Parquet** (`.parquet`) - Apache Parquet columnar format
- **long_lines.csv** - Example with long content to demonstrate horizontal panning

## Usage

Copy these files to your screensaver data directory:

```bash
cp examples/* ~/.local/share/csv-screensaver/data/
```

Or use them directly:

```bash
./csv-screensaver.py examples/
```

## Creating Your Own

### CSV Files
CSV files should follow this format:
1. First row contains headers
2. Subsequent rows contain data
3. Fields are separated by commas
4. Use UTF-8 encoding

Example:
```csv
Column1,Column2,Column3
Value1,Value2,Value3
Value4,Value5,Value6
```

### Gzipped CSV Files
Create gzipped CSV files to save space:
```python
import csv
import gzip

with gzip.open('mydata.csv.gz', 'wt', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Header1', 'Header2'])
    writer.writerow(['Value1', 'Value2'])
```

### Parquet Files
Create Parquet files using pandas:
```python
import pandas as pd

df = pd.DataFrame({
    'Column1': ['Value1', 'Value2'],
    'Column2': ['Value3', 'Value4']
})
df.to_parquet('mydata.parquet', index=False)
```

The screensaver will automatically format and display your data in retro style!
