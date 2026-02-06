#!/usr/bin/env python3
"""
Demo script for CSV Retro Screensaver typing effect (terminal version)
Demonstrates the typing animation without requiring GTK
"""

import csv
import gzip
import os
import random
import time
import sys
from pathlib import Path
import pandas as pd

class TypingDemo:
    """Demonstrates the typing effect in a terminal"""
    
    def __init__(self, csv_folder=None):
        self.csv_folder = csv_folder or os.path.expanduser("~/.local/share/csv-screensaver/data")
        self.typing_delay = 0.150  # Start with slow typing (seconds)
        self.min_typing_delay = 0.020  # End with fast typing
        self.delay_decrease_rate = 0.98
    
    def limit_dataset_rows(self, dataset, max_rows=10000):
        """Limit dataset to header + max_rows randomly selected data rows"""
        if len(dataset) > 1:
            header = [dataset[0]]
            data_rows = dataset[1:]
            if len(data_rows) > max_rows:
                data_rows = random.sample(data_rows, max_rows)
            return header + data_rows
        return dataset
        
    def load_csv_data(self):
        """Load CSV files (including gzipped) and Parquet files"""
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder, exist_ok=True)
            self.create_sample_csv()
        
        # Find CSV, gzipped CSV, and Parquet files
        csv_files = list(Path(self.csv_folder).glob("*.csv"))
        csv_gz_files = list(Path(self.csv_folder).glob("*.csv.gz"))
        parquet_files = list(Path(self.csv_folder).glob("*.parquet"))
        
        all_files = csv_files + csv_gz_files + parquet_files
        
        if not all_files:
            return "No CSV or Parquet files found in: " + self.csv_folder
        
        # Use first file
        data_file = all_files[0]
        
        try:
            # Load data based on file type (case-insensitive)
            file_name_lower = data_file.name.lower()
            if file_name_lower.endswith('.parquet'):
                # Load Parquet file using pandas
                df = pd.read_parquet(data_file)
                # Convert to list of lists (header + rows) and limit rows
                dataset = self.limit_dataset_rows(
                    [df.columns.tolist()] + df.values.tolist()
                )
            elif file_name_lower.endswith('.csv.gz'):
                # Load gzipped CSV file
                with gzip.open(data_file, 'rt', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    dataset = list(reader)
                # Limit to header + 10,000 randomly selected rows
                dataset = self.limit_dataset_rows(dataset)
            else:
                # Load regular CSV file
                with open(data_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    dataset = list(reader)
                # Limit to header + 10,000 randomly selected rows
                dataset = self.limit_dataset_rows(dataset)
            
            if dataset:
                return self.format_data(dataset, data_file.name)
            else:
                return f"Empty file: {data_file.name}"
        except Exception as e:
            return f"Error loading file: {str(e)}"
    
    def format_data(self, dataset, filename):
        """Format CSV data for retro display"""
        lines = []
        
        # Add retro header
        lines.append("=" * 70)
        lines.append("  DATA RETRIEVAL SYSTEM v1.0")
        lines.append("  [ CLASSIFIED INFORMATION ]")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Loading file: {filename}")
        lines.append("")
        
        # Determine number of columns and decide on display strategy
        if not dataset:
            return "\n".join(lines)
            
        num_cols = len(dataset[0])
        
        # For tables with few columns (<=3), use wrapped display without truncation
        # For tables with many columns, use truncated display with panning
        use_wrapped_display = num_cols <= 3
        
        if use_wrapped_display:
            # Pretty wrapped display for quote-like content
            lines.extend(self._format_wrapped_table(dataset))
        else:
            # Traditional truncated display for wide tables
            lines.extend(self._format_truncated_table(dataset))
        
        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF DATA STREAM")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def _truncate_cell(self, cell_text, max_width):
        """Truncate cell content to max_width, adding ellipsis if needed"""
        if len(cell_text) > max_width:
            # Reserve 3 characters for ellipsis
            if max_width >= 3:
                return cell_text[:max_width - 3] + "..."
            else:
                return cell_text[:max_width]
        else:
            return cell_text.ljust(max_width)
    
    def _wrap_text(self, text, width):
        """Wrap text to specified width, breaking at word boundaries"""
        if len(text) <= width:
            return [text]
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            # Calculate space needed: word length + 1 space if not first word
            space_needed = word_length if not current_line else word_length + 1
            
            if current_length + space_needed <= width:
                current_line.append(word)
                current_length += space_needed
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines if lines else [text]
    
    def _format_wrapped_table(self, dataset):
        """Format table with text wrapping for easy reading of long content"""
        lines = []
        
        if not dataset:
            return lines
        
        # Calculate column widths based on headers (not data)
        header_row = dataset[0]
        num_cols = len(header_row)
        
        # Use a reasonable width for wrapping (60 chars for content columns)
        wrap_width = 60
        header_widths = [max(len(str(h)), 10) for h in header_row]
        
        # Format header
        header_line = " | ".join(
            str(cell).ljust(header_widths[i])
            for i, cell in enumerate(header_row)
        )
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # Add data rows with wrapping
        for row in dataset[1:]:
            if not row:
                continue
            
            # Wrap each cell's content
            wrapped_cells = []
            max_wrapped_lines = 1
            
            for i, cell in enumerate(row):
                cell_text = str(cell) if cell is not None else ""
                # For first column (usually ID/chapter), don't wrap
                # For other columns, wrap to width
                if i == 0:
                    wrapped = [cell_text]
                else:
                    wrapped = self._wrap_text(cell_text, wrap_width)
                wrapped_cells.append(wrapped)
                max_wrapped_lines = max(max_wrapped_lines, len(wrapped))
            
            # Output each line of the wrapped cells
            for line_idx in range(max_wrapped_lines):
                line_parts = []
                for col_idx in range(num_cols):
                    if col_idx < len(wrapped_cells):
                        if line_idx < len(wrapped_cells[col_idx]):
                            content = wrapped_cells[col_idx][line_idx]
                        else:
                            content = ""
                        # Pad to column width (or wrap_width for content columns)
                        if col_idx == 0:
                            width = header_widths[col_idx]
                        else:
                            width = wrap_width
                        line_parts.append(content.ljust(width))
                    else:
                        line_parts.append("")
                
                lines.append(" | ".join(line_parts))
            
            # Add a blank line between rows for readability
            lines.append("")
        
        return lines
    
    def _format_truncated_table(self, dataset):
        """Format table with truncated columns (original behavior)"""
        lines = []
        
        # Determine column widths (capped at 30 characters)
        MAX_COL_WIDTH = 30
        col_widths = []
        
        num_cols = len(dataset[0])
        for col_idx in range(num_cols):
            max_width = max(
                (len(str(row[col_idx])) if col_idx < len(row) else 0)
                for row in dataset
            )
            # Cap width at MAX_COL_WIDTH
            col_widths.append(min(max_width, MAX_COL_WIDTH))
        
        # Format headers
        header_row = dataset[0]
        header_line = " | ".join(
            self._truncate_cell(str(cell), col_widths[i])
            for i, cell in enumerate(header_row) if i < len(col_widths)
        )
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # Add data rows
        for row in dataset[1:]:
            if row:  # Skip empty rows
                data_line = " | ".join(
                    self._truncate_cell(str(cell), col_widths[i])
                    for i, cell in enumerate(row) if i < len(col_widths)
                )
                lines.append(data_line)
        
        return lines
    
    def create_sample_csv(self):
        """Create sample CSV files"""
        # Sample: Retro computers
        sample_path = os.path.join(self.csv_folder, "retro_computers.csv")
        with open(sample_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Computer", "Year", "CPU", "RAM"])
            writer.writerow(["Commodore 64", "1982", "MOS 6510", "64 KB"])
            writer.writerow(["Apple II", "1977", "MOS 6502", "4 KB"])
            writer.writerow(["IBM PC", "1981", "Intel 8088", "16 KB"])
            writer.writerow(["Atari 800", "1979", "MOS 6502", "8 KB"])
            writer.writerow(["ZX Spectrum", "1982", "Zilog Z80", "16 KB"])
    
    def type_text(self, text):
        """Display text with typing effect"""
        # Clear screen
        print("\033[2J\033[H", end='')
        
        # Set green text on black background
        print("\033[32m\033[40m", end='')
        
        current_delay = self.typing_delay
        
        for i, char in enumerate(text):
            print(char, end='', flush=True)
            
            if char != '\n':  # Don't delay on newlines as much
                time.sleep(current_delay)
                
                # Accelerate typing
                if current_delay > self.min_typing_delay:
                    current_delay *= self.delay_decrease_rate
        
        # Add blinking cursor
        print("█", end='', flush=True)
        
        # Reset colors
        print("\033[0m")
        print("\n\nPress Ctrl+C to exit")

def main():
    """Main entry point"""
    csv_folder = None
    if len(sys.argv) > 1:
        csv_folder = sys.argv[1]
    
    demo = TypingDemo(csv_folder)
    text = demo.load_csv_data()
    
    try:
        demo.type_text(text)
        time.sleep(10)  # Keep visible for 10 seconds
    except KeyboardInterrupt:
        print("\n\033[0m\nDemo terminated.")

if __name__ == "__main__":
    main()
