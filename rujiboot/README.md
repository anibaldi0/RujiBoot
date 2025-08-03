# RujiBoot

**RujiBoot** is a free and open source tool to create bootable USB drives with GNU/Linux systems.  
It supports secure writing, SHA256 verification, and optional persistence (encrypted or not).  
Designed for privacy, portability and robustness.

---

## About the Project

RujiBoot was born out of necessity—and passion. One day, I needed to create a bootable USB to rescue my laptop
 because Ubuntu was too heavy. I thought about using Ventoy, but then I asked myself:  
**"If I'm learning to program, and ChatGPT is helping me… why not build my own bootable USB creator?"**

That idea sparked what would become RujiBoot: a powerful and minimalist tool for creating bootable USBs
 with optional SHA256 verification, persistence support, and a clean CLI/GUI interface.
 But I didn’t want it to stop there. I wanted this project to grow into something
 educational—something that could also serve future features like **pentesting labs**,
 tools for **Red Team and Blue Team exercises**, and sandboxed USB environments for cybersecurity learning.

The name "RujiBoot" comes from **my daughter, Ruji**, who also drew the project’s icon.
She was the one who encouraged me to study programming at UTN (National Technological University of Argentina),
even though I was already 56 years old. She saw that I wasn't passionate about my current job and
reminded me that it's never too late to reinvent yourself.

This project is also deeply tied to **my values**. RujiBoot is, and will always be, **free and open source software**,
because I grew up learning and building thanks to the culture of **free knowledge**
—just like public education in Argentina (at least, as long as it remains that way).  
This is my way of giving back to the community that gave me so much.

Whether you’re a Linux enthusiast, a sysadmin, a cybersecurity student, or just someone learning to code later in life—**RujiBoot is for you.**


---

## Features

- SHA256 verification of ISO files  
- Secure writing of ISO images to USB  
- Optional persistence support (unencrypted or encrypted)  
- USB formatting with FAT32  
- Change USB volume label  
- Anonymous mode (no logs) or persistent log mode  
- Multilanguage support: Spanish, Portuguese, English  
- Compatible with Debian, Ubuntu and derivatives  

---

## Requirements

- Python 3.7+  
- System dependencies:  
  - `mkfs.vfat`, `mlabel` (from dosfstools and mtools)  
  - `cryptsetup`  
  - `parted`, `udisks2`  

Install them with:

```bash
sudo apt install dosfstools mtools cryptsetup parted udisks2
```

---

## Installation

Clone and run:

```bash
git clone https://github.com/anibaldi0/RujiBoot.git
cd rujiboot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

AppImage and .deb builds will be available soon.

---

## Directory structure

```
rujiboot/
├── cli/                  # CLI interface
├── core/                 # Core logic (write, format, persistence)
├── utils/                # Shared utilities (i18n, logs, input)
├── lang/                 # Translation files (.json)
├── LICENSE               # GPLv3 license
└── README.md             # This file
```

CLI Menu Flow
RujiBoot uses a step-by-step interactive CLI with the following structure:

text
Copiar
Editar
1. Language Selection
   ├── Español
   ├── Português
   ├── English
   └── 0. Exit

2. Execution Mode Selection
   ├── 1. Audit mode (logs enabled)
   ├── 2. Anonymous mode (no logs)
   ├── 3. Help: What is each mode?
   └── 0. Return to language selection

3. Main Menu
   ├── 1. Write ISO to USB
   ├── 2. Unmount USB
   ├── 3. Verify SHA256 of ISO
   ├── 4. Help
   ├── 5. View logs (only in audit mode)
   ├── 9. Return to mode selection
   └── 0. Exit program

4. Context Menus
   ├── 4a. ISO Writer: Select ISO, choose write mode, optional SHA256 and label
   ├── 4b. USB Unmount: View and unmount mounted partitions
   ├── 4c. SHA256 Check: Calculate and compare ISO hash
   └── 4d. Help: Command usage and shell instructions

Option 9 in the main menu returns to the execution mode selector.

Option 0 in any top-level menu exits the program safely.

This structure ensures clarity, modularity, and flexibility for multilingual users.



---

## License

RujiBoot is released under the GNU General Public License v3 (GPLv3).  
It is 100% libre software, with no proprietary or opaque dependencies.

---

## Author

**Author**: Anibal Caeiro  
**GitHub**: [https://github.com/anibaldi0/RujiBoot](https://github.com/anibaldi0/RujiBoot)  
**Email**: inbox.nibal.ink@gmail.com  
**Website**: [www.rujiboot.nibal.ink](http://www.rujiboot.nibal.ink)  
**Project icon**: hand-drawn by Ruji Caeiro

---

## Contributions

Pull requests, bug reports and translations are welcome!
