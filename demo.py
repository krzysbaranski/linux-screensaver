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
        
        # Determine column widths
        col_widths = []
        if dataset:
            num_cols = len(dataset[0])
            for col_idx in range(num_cols):
                max_width = max(
                    (len(str(row[col_idx])) if col_idx < len(row) else 0)
                    for row in dataset
                )
                col_widths.append(max_width + 2)  # No cap on width
        
        # Format headers
        if dataset:
            header_row = dataset[0]
            header_line = " | ".join(
                str(cell).ljust(col_widths[i])
                for i, cell in enumerate(header_row) if i < len(col_widths)
            )
            lines.append(header_line)
            lines.append("-" * len(header_line))
            
            # Add data rows
            for row in dataset[1:]:
                if row:
                    data_line = " | ".join(
                        str(cell).ljust(col_widths[i])
                        for i, cell in enumerate(row) if i < len(col_widths)
                    )
                    lines.append(data_line)
        
        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF DATA STREAM")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
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
