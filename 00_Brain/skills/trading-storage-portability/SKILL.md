---
name: trading-storage-portability
description: Master rules for absolute zero-hardcoded path portability and automated disk storage management across any PC, drive letter, or operating environment.
---

# Trading Storage Management & Portability Protocol

## 1. The Portability Law (Zero Personal Path Invariant)
The workspace must run seamlessly whether it is placed at:
- `C:\Users\myven\Downloads\antigravity ai income`
- `D:\TradingEngine`
- `E:\Portable_AI\` on a USB stick
- `/home/user/trading/` on Linux

### Mandatory Code Rules:
1. **Python:**
   ```python
   # Correct (100% Portable):
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   DATA_DIR = os.path.join(BASE_DIR, "05_Trading_AI", "data")

   # FORBIDDEN (Will fail audit):
   DATA_DIR = "C:\\Users\\myven\\Downloads\\..."
   ```
2. **Windows Batch Scripts (`.bat`):**
   ```batch
   :: Correct (100% Portable):
   cd /d "%~dp0\.."
   set "WORKSPACE=%~dp0\.."

   :: FORBIDDEN:
   cd "C:\Users\myven\..."
   ```
3. **PowerShell Scripts (`.ps1`):**
   ```powershell
   # Correct (100% Portable):
   $Workspace = Split-Path -Parent $PSScriptRoot

   # FORBIDDEN:
   $Workspace = "C:\Users\myven\..."
   ```

---

## 2. Storage Management & Disk Hygiene
1. **Never Commit Raw Data to Git:**
   - Raw CSVs and tick-by-tick logs can grow to 50GB+.
   - All raw data is stored in `05_Trading_AI/data/cache/` which is ignored by `.gitignore`.
2. **Parquet & Compressed Columnar Storage:**
   - OHLCV price series are stored as `.parquet` files using Snappy or ZSTD compression.
   - Saves 85–90% disk space compared to uncompressed CSVs.
3. **SQLite Database Vacuuming:**
   - For trade journals and metadata, SQLite databases use WAL mode (`PRAGMA journal_mode=WAL;`).
   - Automated pruning script vacuums old logs every Sunday.
4. **Automated Portability & Storage Audit:**
   ```bash
   # Scans all files, computes directory weights, checks .gitignore and flags any personal path violations
   python tools/storage_audit.py
   ```
   Must return **Exit Code 0** before any code is marked `VERIFIED_COMPLETE`.
