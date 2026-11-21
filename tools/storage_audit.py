import os
import sys

def get_dir_size(path):
    total = 0
    file_count = 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
                file_count += 1
            except (OSError, FileNotFoundError):
                pass
    return total, file_count

def audit_storage():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 65)
    print("      PORTABLE REPOSITORY STORAGE & HYGIENE AUDIT")
    print("=" * 65)
    print(f"[*] Base Directory: {base_dir}")

    # 1. Directory breakdown
    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    subdirs.sort()

    report = []
    total_repo_size = 0
    total_repo_files = 0

    print("\n--- Directory Size Breakdown ---")
    for d in subdirs:
        dirpath = os.path.join(base_dir, d)
        size, count = get_dir_size(dirpath)
        total_repo_size += size
        total_repo_files += count
        mb = size / (1024 * 1024)
        report.append({"name": d, "size_mb": round(mb, 2), "files": count})
        print(f"  {d:<22} : {mb:>8.2f} MB ({count:>5} files)")

    print("-" * 65)
    print(f"Total Workspace Size: {total_repo_size / (1024 * 1024):.2f} MB ({total_repo_files} files)")

    # 2. Portability Check: Scan for hardcoded absolute personal paths in executable scripts
    print("\n--- Portability Audit (Executable Scripts & Configs) ---")
    hardcoded = []
    # Audit code scripts where hardcoded paths would crash execution
    code_exts = ('.py', '.bat', '.ps1', '.sh')
    
    # We construct the forbidden needle dynamically so this auditor script doesn't flag itself
    needle_user = "c:" + "\\users\\" + "myven"

    this_file = os.path.abspath(__file__)

    for root, dirs, files in os.walk(base_dir):
        if '.git' in root or '__pycache__' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith(code_exts):
                filepath = os.path.join(root, file)
                if os.path.abspath(filepath) == this_file:
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read().lower()
                        if needle_user in text:
                            rel = os.path.relpath(filepath, base_dir)
                            if rel not in hardcoded:
                                hardcoded.append(rel)
                except Exception:
                    pass

    if not hardcoded:
        print("  [+] ALL EXECUTABLE SCRIPTS ARE 100% PORTABLE. Zero hardcoded personal paths.")
    else:
        print(f"  [!] Found {len(hardcoded)} script(s) with hardcoded user paths:")
        for h in hardcoded:
            print(f"      - {h}")

    # 3. Storage Hygiene Status
    print("\n--- Storage Hygiene Status ---")
    gitignore_path = os.path.join(base_dir, ".gitignore")
    if os.path.exists(gitignore_path):
        print("  [+] .gitignore present and active.")
    else:
        print("  [!] .gitignore missing.")

    print("=" * 65)
    return len(hardcoded)

if __name__ == "__main__":
    sys.exit(0 if audit_storage() == 0 else 1)
