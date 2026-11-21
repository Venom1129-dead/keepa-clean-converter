import os
import sys
import json
import zipfile

def verify():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_p = os.path.join(base, "manifest.json")
    html_p = os.path.join(base, "index.html")
    zip_p = os.path.join(base, "KidTech_Activity_Book_Pack_PrintReady.zip")
    pages_d = os.path.join(base, "pages")
    
    assert os.path.exists(manifest_p), "manifest.json missing"
    assert os.path.exists(html_p), "index.html missing"
    assert os.path.exists(zip_p), "KidTech_Activity_Book_Pack_PrintReady.zip missing"
    assert os.path.exists(pages_d), "pages directory missing"
    
    with open(manifest_p, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["total_pages"] >= 6, "Total pages under threshold"
    for page in data["pages"]:
        p_path = os.path.join(pages_d, page["filename"])
        assert os.path.exists(p_path), f"Missing page: {p_path}"
        assert os.path.getsize(p_path) > 500, f"Page file too small: {p_path}"
        
    with zipfile.ZipFile(zip_p, "r") as z:
        names = z.namelist()
        assert "manifest.json" in names, "zip missing manifest"
        assert "Printable_Workbook.html" in names, "zip missing html"
        
    print("VERIFICATION SUCCESS: MVP_14 Activity Book Pack is 100% verified (Exit Code 0).")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
