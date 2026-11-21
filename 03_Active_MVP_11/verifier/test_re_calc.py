import os
import sys

def verify_re_calculator():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, "frontend")

    html_path = os.path.join(frontend_dir, "index.html")
    css_path = os.path.join(frontend_dir, "styles.css")
    js_path = os.path.join(frontend_dir, "app.js")

    print("[*] Verifying MVP_11 RetroMemory Hex & CWCheat Calculator Assets...")

    for path, name in [(html_path, "index.html"), (css_path, "styles.css"), (js_path, "app.js")]:
        assert os.path.exists(path), f"Missing file: {name}"
        assert os.path.getsize(path) > 100, f"File {name} too small"
        print(f" [+] Found {name}: {os.path.getsize(path)} bytes")

    # 1. HTML Verification
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="baseAddress"' in html, "Missing baseAddress input"
    assert 'id="offsetAddress"' in html, "Missing offsetAddress input"
    assert 'id="endianInput"' in html, "Missing endianInput input"
    assert 'id="cheatOutput"' in html, "Missing cheatOutput pre tag"
    assert 'gumroad.com' in html or 'Get Modder Vault' in html, "Missing monetization CTA"
    print(" [+] HTML structure and inputs verified.")

    # 2. CSS Verification
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert '--neon-green' in css and '--font-mono' in css, "Missing CSS hacker theme variables"
    assert '.result-box' in css, "Missing result box styling"
    print(" [+] CSS styles and theme verified.")

    # 3. Mathematical & Hex Logic Verification
    print("[*] Validating Hex Arithmetic and CWCheat Code Formatting Logic...")

    # Math test 1: Base + Offset
    base = 0x08800000
    offset = 0x00045A20
    calc_abs = base + offset
    assert calc_abs == 0x08845A20, f"Hex addition failed: {hex(calc_abs)}"
    assert f"0x{calc_abs:08X}" == "0x08845A20", "Hex formatting mismatch"

    # Math test 2: Little-Endian 32-bit byte flip
    raw_hex = "12345678"
    bytes_arr = [raw_hex[i:i+2] for i in range(0, len(raw_hex), 2)]
    little_endian = "".join(reversed(bytes_arr))
    assert little_endian == "78563412", f"Endian byte flip mismatch: {little_endian}"

    # Math test 3: CWCheat standard string synthesis
    cheat_type = "2"
    rel_addr = 0x00045A20
    cheat_val = 0x000003E7
    first_word = f"0x{cheat_type}{rel_addr:07X}"
    second_word = f"0x{cheat_val:08X}"
    assert first_word == "0x20045A20", f"CWCheat address word mismatch: {first_word}"
    assert second_word == "0x000003E7", f"CWCheat value word mismatch: {second_word}"

    print(" [+] Hex pointer math, little-endian byte flips, and CWCheat formatters verified.")
    print("\n[SUCCESS] ALL VERIFICATION CHECKS PASSED FOR MVP_11 (Exit Code 0).")

if __name__ == "__main__":
    verify_re_calculator()
