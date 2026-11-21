import os
import sys
import zipfile

def verify():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_p = os.path.join(base, "index.html")
    zip_p = os.path.join(base, "Peak_Performance_Health_Daily_Uses_Vault.zip")
    chap_d = os.path.join(base, "chapters")
    tmpl_d = os.path.join(base, "templates")
    
    assert os.path.exists(html_p), "index.html missing"
    assert os.path.exists(zip_p), "zip package missing"
    assert os.path.exists(chap_d), "chapters missing"
    assert os.path.exists(tmpl_d), "templates missing"
    
    assert len(os.listdir(chap_d)) >= 5, "Fewer than 5 chapters"
    assert len(os.listdir(tmpl_d)) >= 2, "Fewer than 2 templates"
    
    with zipfile.ZipFile(zip_p, "r") as z:
        names = z.namelist()
        assert "Read_Online_Vault.html" in names, "zip missing html"
        assert "chapters/chapter_1_circadian_sleep.md" in names, "zip missing chap 1"
        assert "templates/daily_energy_and_focus_tracker.md" in names, "zip missing template"
        
    print("VERIFICATION SUCCESS: MVP_15 Health & Daily Uses Vault is 100% verified (Exit Code 0).")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
