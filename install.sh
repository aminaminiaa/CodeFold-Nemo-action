#!/bin/bash

echo "=== Installing CodeFold Nemo Action ==="
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check/Install libnotify
if ! command -v notify-send &> /dev/null; then
    echo "📦 Installing notification support..."
    if command -v apt &> /dev/null; then
        sudo apt install -y libnotify-bin
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y libnotify
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm libnotify
    else
        echo "⚠️  Could not install libnotify automatically. Please install manually."
    fi
else
    echo "✓ Notification support found"
fi

# Install codefold.py
echo ""
echo "📋 Installing codefold.py to /usr/local/bin..."
sudo cp codefold.py /usr/local/bin/
sudo chmod +x /usr/local/bin/codefold.py

if [ $? -eq 0 ]; then
    echo "✓ Script installed"
else
    echo "❌ Failed to install script"
    exit 1
fi

# Create actions directory
mkdir -p ~/.local/share/nemo/actions

# Install action file
echo "📋 Installing Nemo action..."
cp codefold.nemo_action ~/.local/share/nemo/actions/

if [ $? -eq 0 ]; then
    echo "✓ Nemo action installed"
else
    echo "❌ Failed to install Nemo action"
    exit 1
fi

# Restart Nemo
echo ""
echo "🔄 Restarting Nemo..."
nemo -q 2>/dev/null
sleep 1

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Usage:"
echo "  • Right-click on folder → CodeFold - Combine"
echo "  • Right-click on .txt file → CodeFold - Extract"
echo ""
echo "Terminal usage:"
echo "  codefold.py -c /path/to/project"
echo "  codefold.py -e combined.txt /output/dir"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
