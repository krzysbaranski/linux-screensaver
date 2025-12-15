#!/usr/bin/env python3
"""
CSV Retro Screensaver - A GNOME screensaver that displays CSV data 
in retro command-line style with typing effects
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango
import csv
import gzip
import os
import random
import sys
from pathlib import Path
import pandas as pd

class RetroScreensaver(Gtk.Window):
    """Main screensaver window with retro terminal aesthetic"""
    
    def __init__(self, csv_folder=None):
        super().__init__(title="CSV Retro Screensaver")
        
        # Configuration
        self.csv_folder = csv_folder or os.path.expanduser("~/.local/share/csv-screensaver/data")
        self.current_text = ""
        self.display_text = ""
        self.char_index = 0
        self.typing_delay = 150  # Start with slow typing (milliseconds)
        self.min_typing_delay = 20  # End with fast typing
        self.delay_decrease_rate = 0.98  # How fast the typing accelerates
        self.timer_id = None
        self.current_dataset = []
        self.current_row = 0
        self.blink_state = True
        self.chars_typed = 0
        
        # Setup window
        self.setup_window()
        self.setup_ui()
        self.load_csv_data()
        self.start_typing()
        
    def setup_window(self):
        """Configure the window to be fullscreen and handle events"""
        self.fullscreen()
        self.set_decorated(False)
        
        # Make it exit on any key press or mouse click
        self.connect("key-press-event", self.on_key_press)
        self.connect("button-press-event", self.on_button_press)
        self.connect("destroy", Gtk.main_quit)
        
        # Set cursor invisible
        blank_cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "none")
        if blank_cursor:
            self.get_window().set_cursor(blank_cursor) if self.get_window() else None
        
    def setup_ui(self):
        """Create the retro terminal-style UI"""
        # Create main container
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_halign(Gtk.Align.FILL)
        box.set_valign(Gtk.Align.FILL)
        
        # Create scrolled window for text
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        # Create text view with retro styling
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_view.set_left_margin(20)
        self.text_view.set_right_margin(20)
        self.text_view.set_top_margin(20)
        self.text_view.set_bottom_margin(20)
        
        # Get text buffer
        self.text_buffer = self.text_view.get_buffer()
        
        # Apply retro styling
        self.apply_retro_style()
        
        # Add widgets
        scrolled.add(self.text_view)
        box.pack_start(scrolled, True, True, 0)
        self.add(box)
        
    def apply_retro_style(self):
        """Apply retro terminal color scheme and monospace font"""
        css_provider = Gtk.CssProvider()
        css = b"""
        * {
            background-color: #000000;
            color: #00FF00;
            font-family: "Courier New", "DejaVu Sans Mono", "Monospace";
            font-size: 14pt;
        }
        textview {
            background-color: #000000;
            color: #00FF00;
        }
        textview text {
            background-color: #000000;
            color: #00FF00;
        }
        """
        css_provider.load_from_data(css)
        
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, 
            css_provider, 
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Also set font via tags
        self.create_text_tags()
        
    def create_text_tags(self):
        """Create text formatting tags"""
        tag_table = self.text_buffer.get_tag_table()
        
        # Monospace tag
        mono_tag = Gtk.TextTag.new("mono")
        mono_tag.set_property("family", "monospace")
        mono_tag.set_property("foreground", "#00FF00")
        tag_table.add(mono_tag)
        
        # Header tag (brighter green)
        header_tag = Gtk.TextTag.new("header")
        header_tag.set_property("family", "monospace")
        header_tag.set_property("foreground", "#00FF00")
        header_tag.set_property("weight", Pango.Weight.BOLD)
        tag_table.add(header_tag)
        
        # Cursor tag (for blinking cursor effect)
        cursor_tag = Gtk.TextTag.new("cursor")
        cursor_tag.set_property("background", "#00FF00")
        cursor_tag.set_property("foreground", "#000000")
        tag_table.add(cursor_tag)
        
    def load_csv_data(self):
        """Load CSV files (including gzipped) and Parquet files from the specified folder"""
        if not os.path.exists(self.csv_folder):
            # Create folder and add sample data
            os.makedirs(self.csv_folder, exist_ok=True)
            self.create_sample_csv()
        
        # Find CSV, gzipped CSV, and Parquet files
        csv_files = list(Path(self.csv_folder).glob("*.csv"))
        csv_gz_files = list(Path(self.csv_folder).glob("*.csv.gz"))
        parquet_files = list(Path(self.csv_folder).glob("*.parquet"))
        
        all_files = csv_files + csv_gz_files + parquet_files
        
        if not all_files:
            self.current_text = "No CSV or Parquet files found in: " + self.csv_folder
            return
        
        # Pick a random file
        data_file = random.choice(all_files)
        
        try:
            # Load data based on file type
            if data_file.suffix == '.parquet':
                # Load Parquet file using pandas
                df = pd.read_parquet(data_file)
                # Convert to list of lists (header + rows)
                self.current_dataset = [df.columns.tolist()] + df.values.tolist()
            elif data_file.name.endswith('.csv.gz'):
                # Load gzipped CSV file
                with gzip.open(data_file, 'rt', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.current_dataset = list(reader)
            else:
                # Load regular CSV file
                with open(data_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.current_dataset = list(reader)
            
            if self.current_dataset:
                self.prepare_display_text()
            else:
                self.current_text = f"Empty file: {data_file.name}"
        except Exception as e:
            self.current_text = f"Error loading file: {str(e)}"
    
    def prepare_display_text(self):
        """Format CSV data for retro display"""
        if not self.current_dataset:
            return
        
        lines = []
        
        # Add retro header
        lines.append("=" * 70)
        lines.append("  DATA RETRIEVAL SYSTEM v1.0")
        lines.append("  [ CLASSIFIED INFORMATION ]")
        lines.append("=" * 70)
        lines.append("")
        lines.append("Initializing data stream...")
        lines.append("")
        
        # Determine column widths
        col_widths = []
        if self.current_dataset:
            num_cols = len(self.current_dataset[0])
            for col_idx in range(num_cols):
                max_width = max(
                    (len(str(row[col_idx])) if col_idx < len(row) else 0)
                    for row in self.current_dataset
                )
                col_widths.append(min(max_width + 2, 30))  # Cap at 30 chars
        
        # Format headers if first row looks like headers
        if self.current_dataset:
            header_row = self.current_dataset[0]
            header_line = " | ".join(
                str(cell)[:col_widths[i]].ljust(col_widths[i])
                for i, cell in enumerate(header_row) if i < len(col_widths)
            )
            lines.append(header_line)
            lines.append("-" * len(header_line))
            
            # Add data rows
            for row in self.current_dataset[1:]:
                if row:  # Skip empty rows
                    data_line = " | ".join(
                        str(cell)[:col_widths[i]].ljust(col_widths[i])
                        for i, cell in enumerate(row) if i < len(col_widths)
                    )
                    lines.append(data_line)
        
        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF DATA STREAM")
        lines.append("=" * 70)
        
        self.current_text = "\n".join(lines)
    
    def create_sample_csv(self):
        """Create sample CSV files for demonstration"""
        # Sample 1: Classic data
        sample1_path = os.path.join(self.csv_folder, "retro_computers.csv")
        with open(sample1_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Computer", "Year", "CPU", "RAM"])
            writer.writerow(["Commodore 64", "1982", "MOS 6510", "64 KB"])
            writer.writerow(["Apple II", "1977", "MOS 6502", "4 KB"])
            writer.writerow(["IBM PC", "1981", "Intel 8088", "16 KB"])
            writer.writerow(["Atari 800", "1979", "MOS 6502", "8 KB"])
            writer.writerow(["ZX Spectrum", "1982", "Zilog Z80", "16 KB"])
            writer.writerow(["Amiga 500", "1987", "Motorola 68000", "512 KB"])
        
        # Sample 2: Fun facts
        sample2_path = os.path.join(self.csv_folder, "fun_facts.csv")
        with open(sample2_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Fact ID", "Category", "Fact"])
            writer.writerow(["001", "Space", "A day on Venus is longer than its year"])
            writer.writerow(["002", "Ocean", "More people have been to space than the Mariana Trench"])
            writer.writerow(["003", "Nature", "Honey never spoils - it can last thousands of years"])
            writer.writerow(["004", "Tech", "The first computer bug was an actual moth"])
            writer.writerow(["005", "History", "Oxford University predates the Aztec Empire"])
    
    def start_typing(self):
        """Start the typing animation"""
        self.char_index = 0
        self.display_text = ""
        self.typing_delay = 150  # Reset to slow speed
        self.chars_typed = 0
        self.schedule_next_char()
    
    def schedule_next_char(self):
        """Schedule the next character to be typed"""
        if self.timer_id:
            GLib.source_remove(self.timer_id)
        
        self.timer_id = GLib.timeout_add(int(self.typing_delay), self.type_next_char)
    
    def type_next_char(self):
        """Add the next character to the display"""
        if self.char_index < len(self.current_text):
            # Add next character
            self.display_text += self.current_text[self.char_index]
            self.char_index += 1
            self.chars_typed += 1
            
            # Update display
            self.text_buffer.set_text(self.display_text + "█")  # Add cursor block
            
            # Accelerate typing speed
            if self.typing_delay > self.min_typing_delay:
                self.typing_delay *= self.delay_decrease_rate
            
            # Scroll to end
            end_iter = self.text_buffer.get_end_iter()
            self.text_view.scroll_to_iter(end_iter, 0.0, False, 0.0, 0.0)
            
            # Schedule next character
            self.schedule_next_char()
            return False
        else:
            # Typing complete, start blinking cursor
            self.start_cursor_blink()
            return False
    
    def start_cursor_blink(self):
        """Start blinking cursor after typing is complete"""
        if self.timer_id:
            GLib.source_remove(self.timer_id)
        
        self.timer_id = GLib.timeout_add(500, self.blink_cursor)
    
    def blink_cursor(self):
        """Toggle cursor visibility"""
        self.blink_state = not self.blink_state
        cursor = "█" if self.blink_state else " "
        self.text_buffer.set_text(self.display_text + cursor)
        
        # Scroll to end
        end_iter = self.text_buffer.get_end_iter()
        self.text_view.scroll_to_iter(end_iter, 0.0, False, 0.0, 0.0)
        
        return True  # Continue blinking
    
    def on_key_press(self, widget, event):
        """Exit on any key press"""
        Gtk.main_quit()
        return True
    
    def on_button_press(self, widget, event):
        """Exit on any mouse click"""
        Gtk.main_quit()
        return True

def main():
    """Main entry point"""
    csv_folder = None
    
    # Check for command-line argument
    if len(sys.argv) > 1:
        csv_folder = sys.argv[1]
    
    # Create and show window
    win = RetroScreensaver(csv_folder)
    win.show_all()
    
    # Set cursor invisible after window is realized
    def set_cursor_invisible(window):
        if window.get_window():
            blank_cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "none")
            if blank_cursor:
                window.get_window().set_cursor(blank_cursor)
        return False
    
    GLib.idle_add(set_cursor_invisible, win)
    
    # Start GTK main loop
    Gtk.main()

if __name__ == "__main__":
    main()
