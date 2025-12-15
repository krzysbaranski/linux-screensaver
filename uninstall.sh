#!/bin/bash
# Uninstall script for CSV Retro Screensaver

set -e

echo "Uninstalling CSV Retro Screensaver..."

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo ./uninstall.sh"
    exit 1
fi

# Remove the screensaver script
if [ -f /usr/bin/csv-screensaver ]; then
    echo "Removing screensaver script..."
    rm /usr/bin/csv-screensaver
fi

# Remove the desktop file
if [ -f /usr/share/applications/csv-screensaver.desktop ]; then
    echo "Removing desktop entry..."
    rm /usr/share/applications/csv-screensaver.desktop
fi

echo ""
echo "Uninstallation complete!"
echo ""
echo "Note: Your CSV data files in ~/.local/share/csv-screensaver/data"
echo "have been preserved. You can remove them manually if desired."
echo ""
