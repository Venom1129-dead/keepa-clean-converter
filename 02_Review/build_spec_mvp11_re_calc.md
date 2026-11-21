# BUILD SPECIFICATION: MVP_11 — Retro Memory Offset & CWCheat Address Calculator

## 1. Executive Summary & Market Fit
- **Category:** Reverse Engineering & Game Modding Tools (RE AI)
- **Source Research:** Google Doc Product #11 — *"RE AI"* & *"Reverse engineering tools / game patches"*
- **Target Audience:** Emulator hobbyists, ROM hackers, PPSSPP/RetroArch modders, and reverse engineering students.
- **Problem Solved:** Manually calculating RAM pointer offsets, flipping little-endian 32-bit hex bytes, and formatting valid CWCheat code syntax (`_C0`, `_L 0x2...`) is tedious and error-prone.
- **The 10% Wedge:** A clean, instant, client-side browser calculator that performs:
  1. Base pointer + Offset hex arithmetic.
  2. Little-Endian <-> Big-Endian byte swapper (8-bit, 16-bit, 32-bit, 64-bit).
  3. 1-Click CWCheat & Action Replay syntax generator with clipboard copy.
  4. Memory search difference diff helper (find dynamic memory shifts).

---

## 2. Technical Requirements
- **Format:** Pure client-side HTML5 + Vanilla JS + CSS3 (Zero external npm libraries).
- **Math Verification:**
  - Standard PPSSPP RAM base: `0x08800000`
  - Valid CWCheat type `0x2` (32-bit write), type `0x1` (16-bit write), type `0x0` (8-bit write).
- **Monetization Angle:**
  - Free web utility on GitHub Pages (`https://venom1129-dead.github.io/retro-memory-calc/`).
  - $9 "Modder Pro Cheat Sheet & Memory Table Vault" linking to Gumroad storefront.

---

## 3. Directory Layout
```
03_Active_MVP_11/
├── frontend/
│   ├── index.html        # Clean retro hacker terminal UI
│   ├── styles.css        # Matrix / retro CRT aesthetics with high readability
│   └── app.js            # Hex math, endian swapping, and CWCheat formatter
└── verifier/
    └── test_re_calc.py   # Deterministic validation of hex arithmetic and syntax rules
```
