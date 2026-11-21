import os
import zipfile
import json

BADGE_SPECS = [
    # Category 1: Developer & Terminal Lore (1-12)
    {"id": "badge_01_git_push_force", "name": "Git Push Force", "cat": "Developer Lore", "text": "GIT FORCE", "icon": "branch_blast"},
    {"id": "badge_02_sudo_su", "name": "Sudo Su Root", "cat": "Developer Lore", "text": "SUDO SU", "icon": "crown_terminal"},
    {"id": "badge_03_exit_zero", "name": "Exit Code Zero", "cat": "Developer Lore", "text": "EXIT 0", "icon": "check_hex"},
    {"id": "badge_04_localhost_3000", "name": "Localhost 3000", "cat": "Developer Lore", "text": "127.0.0.1", "icon": "loopback_radar"},
    {"id": "badge_05_stack_overflow", "name": "Stack Overflow", "cat": "Developer Lore", "text": "STACK OVER", "icon": "burst_bars"},
    {"id": "badge_06_infinite_loop", "name": "Infinite Loop", "cat": "Developer Lore", "text": "WHILE TRUE", "icon": "ouroboros_circuit"},
    {"id": "badge_07_syntax_error", "name": "Syntax Error", "cat": "Developer Lore", "text": "SYNTAX ERR", "icon": "broken_bracket"},
    {"id": "badge_08_rm_rf_root", "name": "RM RF Slash", "cat": "Developer Lore", "text": "RM -RF /*", "icon": "biohazard_slash"},
    {"id": "badge_09_segfault_core", "name": "Segmentation Fault", "cat": "Developer Lore", "text": "SEGFAULT", "icon": "memory_dump"},
    {"id": "badge_10_merge_conflict", "name": "Merge Conflict", "cat": "Developer Lore", "text": "HEAD >>>", "icon": "divergent_nodes"},
    {"id": "badge_11_binary_coffee", "name": "Binary Fuel", "cat": "Developer Lore", "text": "01000011", "icon": "tech_mug"},
    {"id": "badge_12_404_not_found", "name": "404 Not Found", "cat": "Developer Lore", "text": "ERR 404", "icon": "void_triangle"},

    # Category 2: Cyberpunk & Neural Tech (13-25)
    {"id": "badge_13_neural_interface", "name": "Neural Interface", "cat": "Cyberpunk Tech", "text": "NEURAL LINK", "icon": "synapse_hex"},
    {"id": "badge_14_quantum_core", "name": "Quantum Core", "cat": "Cyberpunk Tech", "text": "Q-CORE 9", "icon": "atom_stabilizer"},
    {"id": "badge_15_cyber_matrix", "name": "Cyber Matrix", "cat": "Cyberpunk Tech", "text": "MATRIX PROTO", "icon": "grid_nexus"},
    {"id": "badge_16_glitch_protocol", "name": "Glitch Protocol", "cat": "Cyberpunk Tech", "text": "SYSTEM GLITCH", "icon": "offset_polygon"},
    {"id": "badge_17_bio_circuit", "name": "Bio-Synthetics", "cat": "Cyberpunk Tech", "text": "BIO-CHIP", "icon": "dna_circuit"},
    {"id": "badge_18_sub_orbital", "name": "Sub-Orbital Uplink", "cat": "Cyberpunk Tech", "text": "UPLINK 500", "icon": "satellite_dish"},
    {"id": "badge_19_neon_shinigami", "name": "Cyber Shinigami", "cat": "Cyberpunk Tech", "text": "SHINIGAMI", "icon": "cyber_visor_mask"},
    {"id": "badge_20_kinetic_booster", "name": "Kinetic Booster", "cat": "Cyberpunk Tech", "text": "BOOST 88", "icon": "chevron_thrust"},
    {"id": "badge_21_plasma_vent", "name": "Plasma Vent Reactor", "cat": "Cyberpunk Tech", "text": "PLASMA CORE", "icon": "radiation_triad"},
    {"id": "badge_22_augmented_vision", "name": "Augmented Vision", "cat": "Cyberpunk Tech", "text": "HUD OPTIC", "icon": "crosshair_reticle"},
    {"id": "badge_23_holo_driver", "name": "Hologram Driver", "cat": "Cyberpunk Tech", "text": "HOLO EMIT", "icon": "prism_beam"},
    {"id": "badge_24_night_city_syndicate", "name": "Sector 07 Syndicate", "cat": "Cyberpunk Tech", "text": "SECTOR 07", "icon": "city_grid"},
    {"id": "badge_25_synthetic_dream", "name": "Synthetic Dream", "cat": "Cyberpunk Tech", "text": "DREAM STATE", "icon": "crescent_chip"},

    # Category 3: Hardware & Silicon Circuitry (26-38)
    {"id": "badge_26_silicon_wafer", "name": "Silicon 3nm Wafer", "cat": "Hardware & Silicon", "text": "3NM WAFER", "icon": "die_microchip"},
    {"id": "badge_27_overclock_ghz", "name": "Overclock 6.0 GHz", "cat": "Hardware & Silicon", "text": "6.0 GHZ", "icon": "tachometer_gauge"},
    {"id": "badge_28_nanotech_lattice", "name": "Nanotech Lattice", "cat": "Hardware & Silicon", "text": "NANO LATTICE", "icon": "graphene_honeycomb"},
    {"id": "badge_29_optical_bus", "name": "Photonic Optical Bus", "cat": "Hardware & Silicon", "text": "OPTIC BUS", "icon": "fiber_conduit"},
    {"id": "badge_30_pcb_tracer", "name": "Gold PCB Tracer", "cat": "Hardware & Silicon", "text": "BUS LINE", "icon": "trace_maze"},
    {"id": "badge_31_fpga_logic", "name": "FPGA Gate Array", "cat": "Hardware & Silicon", "text": "GATE ARRAY", "icon": "logic_gate"},
    {"id": "badge_32_cryo_cooler", "name": "Cryogenic Sub-Zero", "cat": "Hardware & Silicon", "text": "CRYO -196C", "icon": "snowflake_chip"},
    {"id": "badge_33_vram_buffer", "name": "GDDR7 High Bandwidth", "cat": "Hardware & Silicon", "text": "GDDR7 HBM", "icon": "bus_cluster"},
    {"id": "badge_34_solid_state", "name": "Solid State Storage", "cat": "Hardware & Silicon", "text": "NVME GEN5", "icon": "flash_nand"},
    {"id": "badge_35_bus_frequency", "name": "Clock Multiplier", "cat": "Hardware & Silicon", "text": "CLK MULTI", "icon": "tuning_crystal"},
    {"id": "badge_36_power_phase", "name": "VRM Power Phase", "cat": "Hardware & Silicon", "text": "16+2 PHASE", "icon": "capacitor_array"},
    {"id": "badge_37_thermal_sink", "name": "Vapor Chamber Sink", "cat": "Hardware & Silicon", "text": "VAPOR CHMBR", "icon": "fin_heatsink"},
    {"id": "badge_38_cmos_battery", "name": "CMOS RTC Keeper", "cat": "Hardware & Silicon", "text": "RTC 3.3V", "icon": "coin_cell"},

    # Category 4: Hacker Security & Cryptography (39-50)
    {"id": "badge_39_zero_day", "name": "Zero Day Exploit", "cat": "Hacker & Crypto", "text": "ZERO DAY", "icon": "cracked_shield"},
    {"id": "badge_40_cipher_lock", "name": "RSA 4096 Bit", "cat": "Hacker & Crypto", "text": "RSA 4096", "icon": "padlock_cipher"},
    {"id": "badge_41_firewall_shield", "name": "Firewall Defense", "cat": "Hacker & Crypto", "text": "FIREWALL", "icon": "layered_bastion"},
    {"id": "badge_42_terminal_ghost", "name": "Terminal Ghost In Shell", "cat": "Hacker & Crypto", "text": "GHOST DAEMON", "icon": "specter_terminal"},
    {"id": "badge_43_packet_sniffer", "name": "Promiscuous Packet", "cat": "Hacker & Crypto", "text": "PROMISCUOUS", "icon": "shark_fin_wifi"},
    {"id": "badge_44_hash_collision", "name": "SHA-256 Collision", "cat": "Hacker & Crypto", "text": "SHA-256", "icon": "hex_dual_nodes"},
    {"id": "badge_45_dark_web_relay", "name": "Onion Router Relay", "cat": "Hacker & Crypto", "text": "TOR RELAY", "icon": "onion_rings"},
    {"id": "badge_46_honeypot_trap", "name": "Active Honeypot Trap", "cat": "Hacker & Crypto", "text": "HONEYPOT", "icon": "trap_hex"},
    {"id": "badge_47_brute_force", "name": "Brute Force Engine", "cat": "Hacker & Crypto", "text": "BRUTE KEYS", "icon": "battering_ram"},
    {"id": "badge_48_man_in_middle", "name": "Interception Probe", "cat": "Hacker & Crypto", "text": "MITM PROBE", "icon": "intercept_bridge"},
    {"id": "badge_49_privilege_escalation", "name": "Privilege Escalation", "cat": "Hacker & Crypto", "text": "ROOT ESC", "icon": "staircase_arrow"},
    {"id": "badge_50_dead_drop", "name": "Digital Dead Drop", "cat": "Hacker & Crypto", "text": "DEAD DROP", "icon": "encrypted_vault"}
]

def generate_svg(spec, index):
    title = spec["name"]
    text = spec["text"]
    cat = spec["cat"]
    num_str = f"{index+1:02d}"

    # Generate custom geometric SVG elements based on spec
    # Colors: high-contrast dark cyberpunk palette with bright cyan / magenta / amber highlights
    palette = [
        {"stroke": "#00f0ff", "accent": "#ff007f", "dark": "#0a0e17"},
        {"stroke": "#ffd700", "accent": "#00f0ff", "dark": "#0d1117"},
        {"stroke": "#ff007f", "accent": "#00f0ff", "dark": "#120a17"},
        {"stroke": "#39ff14", "accent": "#00f0ff", "dark": "#08140c"}
    ]
    pal = palette[index % len(palette)]
    stroke = pal["stroke"]
    accent = pal["accent"]

    # Geometric inner design
    shape_type = index % 5
    if shape_type == 0:
        # Hexagon with inner cross & nodes
        inner_geom = f'''
        <polygon points="50,22 74,36 74,64 50,78 26,64 26,36" fill="none" stroke="{stroke}" stroke-width="2.5" />
        <circle cx="50" cy="50" r="12" fill="none" stroke="{accent}" stroke-width="2" />
        <line x1="50" y1="28" x2="50" y2="72" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="3,2" />
        <line x1="32" y1="50" x2="68" y2="50" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="3,2" />
        <circle cx="50" cy="50" r="4" fill="{accent}" />
        '''
    elif shape_type == 1:
        # Microchip die with bus traces
        inner_geom = f'''
        <rect x="30" y="30" width="40" height="40" rx="4" fill="none" stroke="{stroke}" stroke-width="2.5" />
        <rect x="38" y="38" width="24" height="24" fill="{accent}" opacity="0.15" />
        <line x1="20" y1="38" x2="30" y2="38" stroke="{stroke}" stroke-width="2" />
        <line x1="20" y1="50" x2="30" y2="50" stroke="{stroke}" stroke-width="2" />
        <line x1="20" y1="62" x2="30" y2="62" stroke="{stroke}" stroke-width="2" />
        <line x1="70" y1="38" x2="80" y2="38" stroke="{stroke}" stroke-width="2" />
        <line x1="70" y1="50" x2="80" y2="50" stroke="{stroke}" stroke-width="2" />
        <line x1="70" y1="62" x2="80" y2="62" stroke="{stroke}" stroke-width="2" />
        <circle cx="50" cy="50" r="6" fill="{accent}" />
        '''
    elif shape_type == 2:
        # Tech reticle crosshairs & target circles
        inner_geom = f'''
        <circle cx="50" cy="50" r="26" fill="none" stroke="{stroke}" stroke-width="2" stroke-dasharray="8,4" />
        <circle cx="50" cy="50" r="16" fill="none" stroke="{accent}" stroke-width="2" />
        <line x1="50" y1="16" x2="50" y2="28" stroke="{stroke}" stroke-width="2" />
        <line x1="50" y1="72" x2="50" y2="84" stroke="{stroke}" stroke-width="2" />
        <line x1="16" y1="50" x2="28" y2="50" stroke="{stroke}" stroke-width="2" />
        <line x1="72" y1="50" x2="84" y2="50" stroke="{stroke}" stroke-width="2" />
        <polygon points="50,44 56,50 50,56 44,50" fill="{stroke}" />
        '''
    elif shape_type == 3:
        # Cyber shield & firewall core
        inner_geom = f'''
        <path d="M50 20 L76 30 L76 54 C76 68 50 80 50 80 C50 80 24 68 24 54 L24 30 Z" fill="none" stroke="{stroke}" stroke-width="2.5" />
        <path d="M50 28 L68 36 L68 52 C68 62 50 71 50 71 C50 71 32 62 32 52 L32 36 Z" fill="{accent}" opacity="0.2" stroke="{accent}" stroke-width="1.5" />
        <circle cx="50" cy="48" r="7" fill="{stroke}" />
        <line x1="50" y1="55" x2="50" y2="64" stroke="{stroke}" stroke-width="2.5" />
        '''
    else:
        # Atomic orbital & Quantum particle
        inner_geom = f'''
        <circle cx="50" cy="50" r="8" fill="{accent}" />
        <ellipse cx="50" cy="50" rx="28" ry="10" fill="none" stroke="{stroke}" stroke-width="2" transform="rotate(30 50 50)" />
        <ellipse cx="50" cy="50" rx="28" ry="10" fill="none" stroke="{stroke}" stroke-width="2" transform="rotate(-30 50 50)" />
        <ellipse cx="50" cy="50" rx="28" ry="10" fill="none" stroke="{accent}" stroke-width="1.5" transform="rotate(90 50 50)" />
        <circle cx="68" cy="40" r="3" fill="{stroke}" />
        <circle cx="32" cy="60" r="3" fill="{stroke}" />
        '''

    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="500" height="500">
  <!-- Metadata: {title} | {cat} | ID: {spec["id"]} -->
  <defs>
    <style>
      .badge-bg {{ fill: #070913; }}
      .badge-border {{ fill: none; stroke: {stroke}; stroke-width: 2.5; }}
      .badge-num {{ font-family: 'Rajdhani', 'Segoe UI', monospace; font-size: 5px; font-weight: 700; fill: {stroke}; letter-spacing: 1px; }}
      .badge-text {{ font-family: 'Orbitron', 'Segoe UI', sans-serif; font-size: 5.5px; font-weight: 800; fill: #ffffff; letter-spacing: 1px; text-anchor: middle; }}
    </style>
  </defs>

  <!-- Outer Cut-Corner Octagon Frame -->
  <polygon points="12,4 88,4 96,12 96,88 88,96 12,96 4,88 4,12" class="badge-bg" />
  <polygon points="12,4 88,4 96,12 96,88 88,96 12,96 4,88 4,12" class="badge-border" />
  
  <!-- Corner Registration Markers -->
  <line x1="8" y1="16" x2="16" y2="8" stroke="{accent}" stroke-width="1.5" />
  <line x1="84" y1="8" x2="92" y2="16" stroke="{accent}" stroke-width="1.5" />
  <line x1="92" y1="84" x2="84" y2="92" stroke="{accent}" stroke-width="1.5" />
  <line x1="16" y1="92" x2="8" y2="84" stroke="{accent}" stroke-width="1.5" />

  <!-- Technical Spec Label -->
  <text x="12" y="11" class="badge-num">SYS//{num_str}</text>
  <text x="88" y="11" class="badge-num" text-anchor="end">SEC//{spec["id"][:4].upper()}</text>

  <!-- Core Graphic Geometry -->
  {inner_geom}

  <!-- Lower Tech Data Ribbon & Callout -->
  <rect x="18" y="84" width="64" height="8" rx="2" fill="{pal['dark']}" stroke="{accent}" stroke-width="1" />
  <text x="50" y="90" class="badge-text">{text}</text>
</svg>
'''
    return svg_content.strip()

def build_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    svg_dir = os.path.join(base_dir, "svg")
    os.makedirs(svg_dir, exist_ok=True)

    print(f"[*] Generating 50 Cyberpunk & Tech Badge SVGs into {svg_dir}...")
    manifest = []
    svg_files = []

    for idx, spec in enumerate(BADGE_SPECS):
        filename = f"{spec['id']}.svg"
        filepath = os.path.join(svg_dir, filename)
        content = generate_svg(spec, idx)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        svg_files.append(filepath)
        manifest.append({
            "index": idx + 1,
            "id": spec["id"],
            "filename": filename,
            "title": spec["name"],
            "category": spec["cat"],
            "text": spec["text"]
        })

    # Save manifest.json
    manifest_path = os.path.join(base_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"[+] Generated manifest.json with {len(manifest)} items.")

    # Create License & Readme
    license_path = os.path.join(base_dir, "COMMERCIAL_LICENSE.txt")
    with open(license_path, "w", encoding="utf-8") as f:
        f.write("""COMMERCIAL RIGHTS & RESALE LICENSE
=====================================================
Package: 50 Minimalist Cyberpunk & Tech Badge Vector SVG Pack
Licensee: Authorized Purchaser (Single User / Studio)
Issuer: Antigravity Autonomous Income Lab

PERMITTED USES:
1. Unlimited commercial print-on-demand production (T-shirts, hoodies, stickers, posters, mugs, phone cases) on Printify, Redbubble, Merch by Amazon, Etsy, etc.
2. Digital product inclusion: UI icons, game textures, web emblems, and application assets.
3. Resale as physical printed goods without unit limits or additional royalties.

RESTRICTIONS:
1. You may NOT resell or redistribute the raw standalone SVG files as a vector clipart bundle.
2. You may NOT claim original vector copyright of the unprinted source files.

(C) 2026 Antigravity Lab. All rights reserved.
""")

    readme_path = os.path.join(base_dir, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""50 MINIMALIST CYBERPUNK & TECH BADGE VECTOR SVG PACK
=====================================================
Thank you for downloading!

INCLUDED IN THIS BUNDLE:
- 50 Raw Scalable Vector Graphics (.SVG)
  - 100% vector-scalable to any billboard or apparel dimension without rasterization or pixel loss.
  - Compatible with Adobe Illustrator, Inkscape, Figma, CorelDraw, Cricut Design Space, Canva.
  - Formatted at 500x500 native viewBox with clean polygon math.
- Complete COMMERCIAL_LICENSE.txt granting unlimited print-on-demand rights.
- Full metadata catalog in manifest.json.

CATEGORIES INCLUDED:
1. Developer & Terminal Lore (Badges 01-12)
2. Cyberpunk & Neural Tech (Badges 13-25)
3. Hardware & Silicon Circuitry (Badges 26-38)
4. Hacker Security & Cryptography (Badges 39-50)
""")

    # Create ZIP distribution package
    zip_path = os.path.join(base_dir, "Cyberpunk_Tech_Badges_50_Pack.zip")
    print(f"[*] Packaging into {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in svg_files:
            zipf.write(f, arcname=f"svg/{os.path.basename(f)}")
        zipf.write(manifest_path, arcname="manifest.json")
        zipf.write(license_path, arcname="COMMERCIAL_LICENSE.txt")
        zipf.write(readme_path, arcname="README.txt")

    print(f"[SUCCESS] Packaged {len(svg_files)} SVGs into {zip_path} ({os.path.getsize(zip_path)} bytes).")

if __name__ == "__main__":
    build_all()
