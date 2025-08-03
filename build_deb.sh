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
DESKTOP_LINK="$HOME/Desktop/RujiBoot.desktop"

echo "[*] Installing RujiBoot..."

# Create install directory
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r rujiboot/* "$INSTALL_DIR"

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
Categories=Utility;
EOF

# Make sure it's executable and update icon cache
sudo chmod +x "$DESKTOP_FILE"
sudo gtk-update-icon-cache /usr/share/icons/hicolor || true

# Copy launcher to user's desktop
cp "$DESKTOP_FILE" "$DESKTOP_LINK"
chmod +x "$DESKTOP_LINK"

echo "[+] RujiBoot installed successfully!"
echo "[+] You can launch it from the applications menu or the Desktop icon."
