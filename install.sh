#!/bin/bash
# Installation script for CSV Retro Screensaver

set -e

echo "Installing CSV Retro Screensaver..."

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo ./install.sh"
    exit 1
fi

# Copy the screensaver script
echo "Installing screensaver script..."
cp csv-screensaver.py /usr/bin/csv-screensaver
chmod +x /usr/bin/csv-screensaver

# Copy the desktop file
echo "Installing desktop entry..."
mkdir -p /usr/share/applications
cp csv-screensaver.desktop /usr/share/applications/

# Create data directory for the user who ran sudo
ACTUAL_USER=${SUDO_USER:-$USER}
ACTUAL_HOME=$(eval echo ~$ACTUAL_USER)
DATA_DIR="$ACTUAL_HOME/.local/share/csv-screensaver/data"

echo "Creating data directory at $DATA_DIR..."
mkdir -p "$DATA_DIR"
chown -R $ACTUAL_USER:$ACTUAL_USER "$ACTUAL_HOME/.local/share/csv-screensaver"

echo ""
echo "Installation complete!"
echo ""
echo "To use the screensaver:"
echo "1. Place your CSV files in: $DATA_DIR"
echo "2. Run manually with: csv-screensaver"
echo "3. Or configure it in your GNOME screensaver settings"
echo ""
echo "Sample CSV files will be created automatically on first run."
echo ""
