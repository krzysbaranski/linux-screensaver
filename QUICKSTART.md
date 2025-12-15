# Quick Start Guide

## For Users

### Installation

1. **Install dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
   
   # Fedora
   sudo dnf install python3-gobject gtk3
   
   # macOS
   brew install cairo pkg-config gtk+3 pygobject3
   export PKG_CONFIG_PATH="/opt/homebrew/Cellar/cairo/1.18.4/lib/pkgconfig:$PKG_CONFIG_PATH"
   ```

2. **Install the screensaver:**
   ```bash
   sudo ./install.sh
   ```

3. **Add your CSV files:**
   ```bash
   # Copy example files
   cp examples/*.csv ~/.local/share/csv-screensaver/data/
   
   # Or create your own CSV files
   nano ~/.local/share/csv-screensaver/data/my_data.csv
   ```

4. **Test it:**
   ```bash
   csv-screensaver
   ```

### Quick Demo (No Installation Required)

Run the terminal demo to see the typing effect:
```bash
./demo.py examples/
```

## For Developers

### File Structure

```
.
├── csv-screensaver.py      # Main GTK screensaver application
├── demo.py                 # Terminal demo version
├── install.sh              # Installation script
├── uninstall.sh           # Uninstallation script
├── csv-screensaver.desktop # GNOME desktop entry
├── requirements.txt        # Python dependencies
├── examples/               # Sample CSV files
│   ├── retro_computers.csv
│   ├── fun_facts.csv
│   └── programming_languages.csv
└── README.md              # Full documentation
```

### Key Features

1. **Progressive Typing Speed**: Starts at 150ms/char, accelerates to 20ms/char
2. **Retro Styling**: Green-on-black terminal aesthetic
3. **Auto CSV Discovery**: Randomly selects from available CSV files
4. **Fullscreen Mode**: True screensaver behavior
5. **Exit on Input**: Any key/click exits the screensaver

### Customization

Edit `csv-screensaver.py` to customize:
- **Colors**: Modify CSS in `apply_retro_style()` (currently #00FF00 on #000000)
- **Typing Speed**: Change `typing_delay` and `min_typing_delay`
- **Acceleration**: Adjust `delay_decrease_rate`
- **Data Location**: Set custom `csv_folder` path

### Testing Without GTK

Use the demo script for testing without a graphical environment:
```bash
python3 demo.py /path/to/csv/files
```

## CSV Format

CSV files should be UTF-8 encoded with:
- Header row (first row)
- Data rows (subsequent rows)
- Comma-separated values

Example:
```csv
Name,Value,Description
Item1,100,First item
Item2,200,Second item
```

## Troubleshooting

**Black screen on start?**
- Give it a few seconds - it starts with slow typing
- Check CSV files exist in the data directory

**No green text?**
- Some terminals may not support ANSI colors
- Try a different terminal emulator

**GTK errors?**
- Ensure python3-gi is installed
- Check GTK 3.0 is available

## Exit

Press **any key** or **click mouse** to exit the screensaver.
