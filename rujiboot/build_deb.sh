#!/bin/bash

echo "[*] Cleaning old builds..."
rm -rf build_pkg

echo "[*] Creating folder structure..."
mkdir -p build_pkg/rujiboot_1.0/DEBIAN
mkdir -p build_pkg/rujiboot_1.0/usr/bin
mkdir -p build_pkg/rujiboot_1.0/opt/rujiboot

echo "[*] Setting permissions..."
chmod 0755 build_pkg/rujiboot_1.0/DEBIAN

echo "[*] Writing control file..."
cat <<EOF > build_pkg/rujiboot_1.0/DEBIAN/control
Package: rujiboot
Version: 1.0
Section: utils
Priority: optional
Architecture: all
Maintainer: Anibal Caeiro <anibal@nibal.ink>
Description: RujiBoot - CLI/GUI tool for writing GNU/Linux ISOs to USB drives
EOF
chmod 0644 build_pkg/rujiboot_1.0/DEBIAN/control

echo "[*] Copying project files..."
rsync -a --exclude=venv --exclude=build_pkg ./ build_pkg/rujiboot_1.0/opt/rujiboot/

echo "[*] Creating launcher..."
echo '#!/bin/bash
python3 /opt/rujiboot/main.py "$@"' > build_pkg/rujiboot_1.0/usr/bin/rujiboot
chmod +x build_pkg/rujiboot_1.0/usr/bin/rujiboot

echo "[*] Building .deb package..."
dpkg-deb --build build_pkg/rujiboot_1.0

echo "[+] Done! Your package is: build_pkg/rujiboot_1.0.deb"
