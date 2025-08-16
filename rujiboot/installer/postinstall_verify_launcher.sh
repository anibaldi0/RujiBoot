#!/bin/bash
# Path: installer/postinstall_verify_launcher.sh
# Description: Post-install script to verify RujiBoot launcher and desktop entry

DESKTOP_FILE="$HOME/.local/share/applications/rujiboot.desktop"
ICON_FILE="/usr/share/icons/hicolor/128x128/apps/rujiboot_icon.png"
DESKTOP_COPY="$HOME/Escritorio/rujiboot.desktop"

echo "[*] Verifying RujiBoot desktop launcher..."

# Check if desktop entry exists
if [[ ! -f "$DESKTOP_FILE" ]]; then
    echo "[!] Desktop launcher not found at $DESKTOP_FILE"
    exit 1
fi

# Check if it is executable
chmod +x "$DESKTOP_FILE"
echo "[+] Desktop launcher exists and is now executable."

# Check if icon exists
if [[ ! -f "$ICON_FILE" ]]; then
    echo "[!] Icon file not found: $ICON_FILE"
    exit 1
else
    echo "[+] Icon file found."
fi

# Copy to Desktop (if user has it)
if [[ -d "$HOME/Escritorio" ]]; then
    cp "$DESKTOP_FILE" "$DESKTOP_COPY"
    chmod +x "$DESKTOP_COPY"
    echo "[+] Shortcut copied to Desktop."
else
    echo "[*] Desktop folder not found. Skipping shortcut copy."
fi

echo "[✓] RujiBoot launcher verified."
exit 0
