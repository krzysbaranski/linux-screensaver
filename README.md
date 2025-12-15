# CSV Retro Screensaver

A fun and engaging Linux/GNOME screensaver that displays CSV datasets in a retro command-line style with realistic typing effects. Watch as data appears character-by-character, starting slow like a hesitant typist and accelerating to blazing-fast speeds!

## Preview

```
======================================================================
  DATA RETRIEVAL SYSTEM v1.0
  [ CLASSIFIED INFORMATION ]
======================================================================

Loading file: retro_computers.csv

Computer       | Year   | CPU              | RAM     
-----------------------------------------------------
Commodore 64   | 1982   | MOS 6510         | 64 KB   
Apple II       | 1977   | MOS 6502         | 4 KB    
IBM PC         | 1981   | Intel 8088       | 16 KB   
Atari 800      | 1979   | MOS 6502         | 8 KB    
ZX Spectrum    | 1982   | Zilog Z80        | 16 KB   
Amiga 500      | 1987   | Motorola 68000   | 512 KB  

======================================================================
END OF DATA STREAM
======================================================================
█
```

*Displayed in classic green-on-black terminal style with smooth typing animation!*

## Features

- 🎨 **Retro Terminal Aesthetic**: Classic green-on-black terminal display
- ⌨️ **Realistic Typing Animation**: Characters appear one at a time with progressive speed-up
- 📊 **CSV Data Display**: Reads and formats CSV files from a configured folder
- 🎲 **Random Selection**: Picks random CSV files for variety
- 💾 **Sample Data Included**: Comes with fun retro computing facts to get started
- 🔒 **Screensaver Mode**: Fullscreen with exit on any key/mouse click

## Requirements

- Python 3.6+
- GTK+ 3.0
- PyGObject (Python GTK bindings)

## Installation

### Automated Installation

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Or on Fedora
sudo dnf install python3-gobject gtk3

# Install the screensaver
sudo ./install.sh
```

### Manual Installation

```bash
# Copy the screensaver script
sudo cp csv-screensaver.py /usr/bin/csv-screensaver
sudo chmod +x /usr/bin/csv-screensaver

# Copy the desktop entry
sudo cp csv-screensaver.desktop /usr/share/applications/

# Create data directory
mkdir -p ~/.local/share/csv-screensaver/data
```

## Usage

### Running Manually

```bash
# Run with default data directory (~/.local/share/csv-screensaver/data)
csv-screensaver

# Or specify a custom CSV folder
csv-screensaver /path/to/your/csv/files
```

### Adding Your CSV Files

1. Place your CSV files in: `~/.local/share/csv-screensaver/data/`
2. Files should have a header row and data rows
3. The screensaver will randomly select and display them

Example CSV format:
```csv
Name,Year,Description
Item 1,2023,First item
Item 2,2024,Second item
```

### GNOME Screensaver Integration

The screensaver can be configured in GNOME settings:
1. Open **Settings** → **Privacy** → **Screen Lock**
2. The CSV Retro Screensaver should appear in available screensavers
3. Select it and configure your screen lock timing

## How It Works

The screensaver:
1. Loads a random CSV file from your data folder
2. Formats it in a retro terminal style with borders and formatting
3. Types out the content character-by-character
4. Starts with slow typing (150ms per character)
5. Accelerates progressively to fast typing (20ms per character)
6. For long lines that don't fit on screen, automatically pans horizontally across the content
7. Shows a blinking cursor when complete
8. Exits on any key press or mouse click

### Long Line Support

The screensaver now fully supports CSV files with long content:
- **No line wrapping**: Long lines are displayed in their entirety without breaking
- **Automatic panning**: The view smoothly scrolls left and right to show all content
- **No column truncation**: All column data is displayed, regardless of length

## Customization

You can modify the screensaver behavior by editing `csv-screensaver.py`:

- **Initial typing speed**: Change `self.typing_delay = 150` (in milliseconds)
- **Final typing speed**: Change `self.min_typing_delay = 20`
- **Acceleration rate**: Change `self.delay_decrease_rate = 0.98`
- **Panning speed**: Change `self.pan_speed = 2` (pixels per frame)
- **Colors**: Modify the CSS in `apply_retro_style()` method
- **Data folder**: Change `self.csv_folder` default path

## Sample Data

The screensaver includes sample CSV files:
- `retro_computers.csv`: Classic 1980s computers
- `fun_facts.csv`: Interesting trivia

These are automatically created on first run if no CSV files exist.

## Uninstallation

```bash
sudo ./uninstall.sh
```

Or manually:
```bash
sudo rm /usr/bin/csv-screensaver
sudo rm /usr/share/applications/csv-screensaver.desktop
```

## Troubleshooting

**Problem**: Screensaver doesn't start
- Check that Python 3 and GTK dependencies are installed
- Try running from terminal: `csv-screensaver` to see error messages

**Problem**: No data displayed
- Ensure CSV files exist in `~/.local/share/csv-screensaver/data/`
- Check CSV files are properly formatted with headers

**Problem**: Screen doesn't go fullscreen
- This may happen in some window managers
- Try running with `csv-screensaver` from terminal

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! Some ideas:
- Additional color schemes (amber, white, etc.)
- More typing effect variations
- Sound effects
- Support for other data formats (JSON, XML, etc.)
- Configuration file support

## Credits

Created for nostalgic computer enthusiasts who remember when green screens and slow modems were cutting-edge technology! 💚
