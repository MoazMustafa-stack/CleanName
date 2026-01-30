# Filename Cleaner

A small, safe desktop utility that helps you clean up filenames by removing unwanted metadata prefixes. Works on Windows and Linux — no Python installation required.

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

## License

This project is provided under the MIT License. See [LICENSE](LICENSE) for details.