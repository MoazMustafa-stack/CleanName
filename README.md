<div align="center">

> **Made for VIT students by a VIT student** 🎓

# Filename Cleaner

### *Simple. Safe. Fast.*

> Clean up filenames by removing metadata prefixes. No installation required.

[![Release](https://img.shields.io/github/release/MoazMustafa-stack/CleanName?style=for-the-badge&color=blue)](https://github.com/MoazMustafa-stack/CleanName/releases/latest)
[![License](https://img.shields.io/github/license/MoazMustafa-stack/CleanName?style=for-the-badge)](LICENSE)

---

</div>

## Download

| Platform | Download |
|----------|----------|
| **Windows** | [`.exe`](https://github.com/MoazMustafa-stack/CleanName/releases/latest) |
| **Linux** | [Binary](https://github.com/MoazMustafa-stack/CleanName/releases/latest) |
| **From Source** | Python 3.10+ |

> **[View all releases](https://github.com/MoazMustafa-stack/CleanName/releases)**

---

## Built With

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Tkinter-FFD700?style=for-the-badge&logoColor=black" />
  <img src="https://img.shields.io/badge/PyInstaller-1E1E1E?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088F0?style=for-the-badge&logo=github-actions&logoColor=white" />
</p>

---

## What It Does

Filename Cleaner takes messy filenames like this:

```
FALLSEM2025-26_VL_BSTS302P_00100_SS_2025-07-28_The-Celebrity-problem.pdf
```

And renames them to:

```
The-Celebrity-problem.pdf
```

**The rule is simple:** Keep only the part of the filename after the *last underscore*, and preserve the file extension. If there's no underscore, the filename stays the same.

## Download & Run

### Windows
1. Go to [Releases](../../releases)
2. Download `filename-cleaner.exe` (latest version)
3. Run it — no installation needed
4. Drag & drop files or use "Add Files..."

### Linux
1. Go to [Releases](../../releases)
2. Download `filename-cleaner` (latest version)
3. Make it executable:
   ```bash
   chmod +x filename-cleaner
   ```
4. Run it:
   ```bash
   ./filename-cleaner
   ```
5. Drag & drop files or use "Add Files..."

### From Source (Python 3.10+)
If you prefer to run from source:

```bash
# Clone or download this repository
git clone <repo-url>
cd filename-cleaner

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/file_renamer_gui.py
```

## How to Use

1. **Open the app** (executable or from source)
2. **Add files:**
   - Drag & drop files into the gray area, OR
   - Click "Add Files..." and select files
3. **Preview:** The list shows `OLD_FILENAME → NEW_FILENAME` (dry-run, nothing is changed yet)
4. **Rename:** Click "Rename Files" and confirm in the dialog
5. **Done:** Files are renamed in place; the list updates with new names

## Safety Features

- **Dry-run by default:** Files are not changed until you click "Rename Files" and confirm
- **No overwrite without permission:** If a target filename already exists, it will be skipped unless you check "Allow overwrite (dangerous)"
- **No data collection:** Filename Cleaner runs entirely on your machine — no internet, no analytics, no cloud
- **Directories are ignored:** Only files are processed
- **Friendly error messages:** If something goes wrong, you'll see a clear message

## Features

- ✅ Drag & drop support
- ✅ Batch rename multiple files
- ✅ Preview before applying changes
- ✅ Cross-platform (Windows, Linux)
- ✅ Small & fast
- ✅ No complex settings

## Troubleshooting

**The app won't start (on Linux/Unix)**
- Ensure the executable has execute permissions:
  ```bash
  chmod +x filename-cleaner
  ```

**Drag & drop doesn't work**
- If running from source, install `tkinterdnd2`:
  ```bash
  pip install tkinterdnd2
  ```
- Executables have drag & drop built-in.

**"Allow overwrite" is unchecked but it says targets exist**
- This is correct behavior. The app lists targets that exist; they will be skipped unless you check "Allow overwrite".

---

## 🤝 Contributing & Feedback

Found a bug? Have a suggestion? Open an [issue](https://github.com/MoazMustafa-stack/CleanName/issues) or submit a pull request.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with ❤️ using Python & Tkinter**

</div>