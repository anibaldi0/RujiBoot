#!/bin/bash

# === RujiBoot Installation Script ===
# Description: Installs RujiBoot CLI, launcher icon, and desktop shortcut

# Exit on any error
set -e

# Paths
INSTALL_DIR="/opt/rujiboot"
DESKTOP_FILE="/usr/share/applications/rujiboot.desktop"
ICON_FILE="/usr/share/icons/hicolor/128x128/apps/rujiboot_icon.png"
EXECUTABLE="/usr/local/bin/rujiboot"

echo "[*] Installing RujiBoot..."

# Create install directory
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r cli core data gui logs menus utils "$INSTALL_DIR"
sudo cp main.py "$INSTALL_DIR"
sudo cp requirements.txt "$INSTALL_DIR"
sudo cp -r installer "$INSTALL_DIR"

# Install icon
sudo cp installer/icons/rujiboot_icon.png "$ICON_FILE"

# Install launcher script
echo -e "#!/bin/bash\npython3 $INSTALL_DIR/main.py" | sudo tee "$EXECUTABLE" > /dev/null
sudo chmod +x "$EXECUTABLE"

# Create .desktop launcher
sudo tee "$DESKTOP_FILE" > /dev/null <<EOF
[Desktop Entry]
Name=RujiBoot
Comment=Create bootable USB drives with GNU/Linux
Exec=rujiboot
Icon=rujiboot_icon
Terminal=true
Type=Application
Categories=Utility;System;
StartupNotify=true
EOF

# Make .desktop executable
sudo chmod +x "$DESKTOP_FILE"

# Update icon cache (optional, ignore error if fails)
sudo gtk-update-icon-cache /usr/share/icons/hicolor || true

# Detect user's desktop directory dynamically
DESKTOP_DIR=$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")

if [ -d "$DESKTOP_DIR" ]; then
    cp "$DESKTOP_FILE" "$DESKTOP_DIR/RujiBoot.desktop"
    chmod +x "$DESKTOP_DIR/RujiBoot.desktop"
    echo "[+] Desktop icon created at $DESKTOP_DIR/RujiBoot.desktop"
else
    echo "[!] Warning: Could not find Desktop directory. Skipping shortcut."
fi

echo "[+] RujiBoot installed successfully!"
echo "[+] You can launch it from the applications menu or the Desktop icon."
