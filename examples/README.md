# Example CSV Files

This directory contains example CSV files that demonstrate the CSV Retro Screensaver.

## Files

- **retro_computers.csv** - Classic computers from the 1970s and 1980s
- **fun_facts.csv** - Interesting trivia from various fields
- **programming_languages.csv** - Popular programming languages and their creators
- **long_lines.csv** - Example with long content to demonstrate horizontal panning

## Usage

Copy these files to your screensaver data directory:

```bash
cp examples/*.csv ~/.local/share/csv-screensaver/data/
```

Or use them directly:

```bash
./csv-screensaver.py examples/
```

## Creating Your Own

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

The screensaver will automatically format and display your data in retro style!
