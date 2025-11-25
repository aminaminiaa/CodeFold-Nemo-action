#!/bin/bash

echo "=== Uninstalling CodeFold ==="
echo ""

# Remove script
if [ -f /usr/local/bin/codefold.py ]; then
    echo "🗑️  Removing codefold.py..."
    sudo rm -f /usr/local/bin/codefold.py
    echo "✓ Script removed"
fi

# Remove action file
if [ -f ~/.local/share/nemo/actions/codefold.nemo_action ]; then
    echo "🗑️  Removing Nemo action..."
    rm -f ~/.local/share/nemo/actions/codefold.nemo_action
    echo "✓ Nemo action removed"
fi

# Restart Nemo
echo ""
echo "🔄 Restarting Nemo..."
nemo -q 2>/dev/null
sleep 1

echo ""
echo "✅ CodeFold uninstalled successfully!"
