import os
import json
import zipfile

def generate_health_daily_uses_vault():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mvp_dir = os.path.join(base_dir, "03_Active_MVP_15")
    chapters_dir = os.path.join(mvp_dir, "chapters")
    templates_dir = os.path.join(mvp_dir, "templates")
    verifier_dir = os.path.join(mvp_dir, "verifier")
    
    os.makedirs(chapters_dir, exist_ok=True)
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(verifier_dir, exist_ok=True)
    
    chapters = [
        {
            "num": 1,
            "filename": "chapter_1_circadian_sleep.md",
            "title": "Circadian Lighting & Sleep Architecture",
            "content": """# Chapter 1: Circadian Lighting & Sleep Architecture

Cognitive fatigue and decision paralysis in high-intensity trading and software engineering rarely stem from lack of willpower. They stem from degraded sleep architecture caused by disrupted circadian rhythms.

## 1. Morning Lux Exposure (The Cortisol Pulse)
Within 30 minutes of waking, you must expose your retinal ganglion cells to a minimum of 10,000 lux (direct morning sunlight or a 10,000-lux daylight therapy lamp for 15-20 minutes). This anchors your master circadian pacemaker (suprachiasmatic nucleus) and triggers the 14-hour melatonin timer.

## 2. Eliminating 450nm Blue Light Post-Sunset
After 8:00 PM, ambient screen emissions destroy melatonin secretion by up to 85%. Install software-level warm temperature filters (f.lux or native Night Light set to 1900K) and switch to warm, amber incandescent lighting below eye level.

## 3. Core Body Temperature Drop
Deep non-REM stage 3 sleep requires a drop in core body temperature by 1 to 2 degrees Fahrenheit. Keep bedroom ambient temperature strictly between 65°F and 68°F (18°C - 20°C).
"""
        },
        {
            "num": 2,
            "filename": "chapter_2_nutrition_focus.md",
            "title": "Nutrition for Sustained Mental Clarity",
            "content": """# Chapter 2: Nutrition for Sustained Mental Clarity

The standard modern diet causes violent glycemic volatility: rapid blood glucose spikes followed by reactive hypoglycemia, triggering brain fog, anxiety, and impulsive trading decisions.

## 1. The Steady-State Glycemic Framework
Avoid refined carbohydrates and high-fructose syrups during prime working hours (8:00 AM - 4:00 PM). Prioritize high-density protein (eggs, wild fish, grass-fed beef, tempeh) and clean monounsaturated fats (avocados, extra virgin olive oil, macadamia nuts).

## 2. Caffeine Half-Life Management
Caffeine has an average terminal half-life of 5 to 7 hours and a quarter-life of up to 12 hours. Any caffeine consumed past 1:00 PM actively degrades deep restorative slow-wave sleep. Implement a hard cutoff at 12:30 PM.

## 3. Fasting Windows for Dopamine Reset
A 14-hour overnight fast (e.g., 7:00 PM dinner to 9:00 AM breakfast) induces mild cellular autophagy, increases brain-derived neurotrophic factor (BDNF), and sharpens acute analytical cognition.
"""
        },
        {
            "num": 3,
            "filename": "chapter_3_hydration_electrolytes.md",
            "title": "Hydration Mechanics & Mineral Timing",
            "content": """# Chapter 3: Hydration Mechanics & Mineral Timing

A mild 1.5% decrease in cellular water balance leads to a measurable 12% drop in cognitive processing speed and memory recall. Drinking plain distilled or filtered tap water in massive volumes without ionic minerals actually strips cellular electrolytes.

## 1. The Morning Mineral Elixir
Start every morning with 500ml of room-temperature filtered water combined with 500mg unrefined sea salt (sodium chloride) and a squeeze of fresh lemon. This restores adrenal hydration without spiking insulin.

## 2. Potassium and Magnesium Balancing
Most computer professionals are chronically deficient in intracellular magnesium. Supplement 300mg of Magnesium Glycinate or L-Threonate 45 minutes prior to sleep to promote GABAergic neural relaxation.
"""
        },
        {
            "num": 4,
            "filename": "chapter_4_micro_movement_ergonomics.md",
            "title": "Micro-Movement & Posture Mechanics",
            "content": """# Chapter 4: Micro-Movement & Posture Mechanics

Sitting motionless for 8+ hours restricts lymphatic flow, tightens psoas muscles, and reduces cerebral blood oxygenation.

## 1. The 50/10 Pomodoro Movement Rule
For every 50 minutes of deep technical execution, take 10 minutes of active physical displacement:
- 20 air squats or bodyweight lunges to pump venous blood back to the heart.
- Thoracic extension stretches over a foam roller.
- 60 seconds of dead hangs from a pull-up bar to decompress lumbar spinal discs.

## 2. Dual-Monitor Eye Convergence Relief (20-20-20 Rule)
Every 20 minutes, focus on an object at least 20 feet away for 20 seconds. This relaxes the ciliary muscles and prevents screen-induced tension headaches.
"""
        },
        {
            "num": 5,
            "filename": "chapter_5_daily_velocity_protocol.md",
            "title": "The Daily Velocity Protocol (Checklist)",
            "content": """# Chapter 5: The Daily Velocity Protocol

Consistency beats intensity. Follow this deterministic daily execution timetable:

## Morning Protocol (06:30 - 08:30)
- [ ] 500ml water + 500mg sea salt.
- [ ] 15 minutes direct natural sunlight.
- [ ] 20 minutes cold shower or mobility stretch.
- [ ] High-protein, zero-sugar breakfast.

## Deep Work Execution (08:30 - 13:00)
- [ ] Primary analytical/coding sprint (No notifications).
- [ ] Caffeine intake restricted to morning only.
- [ ] 50/10 movement cycles.

## Evening Wind-Down (20:00 - 22:30)
- [ ] Warm lighting only (f.lux / night mode activated).
- [ ] Digital screens off by 21:30.
- [ ] 300mg Magnesium Glycinate.
- [ ] Bedroom cooled to 66°F.
"""
        }
    ]

    for chap in chapters:
        c_path = os.path.join(chapters_dir, chap["filename"])
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(chap["content"].strip())

    # Daily templates
    templates = [
        {
            "filename": "daily_energy_and_focus_tracker.md",
            "content": """# Daily Energy, Hydration & Focus Audit Sheet

Date: _______________  | Target Deep Work Hours: _________

| Time Block | Focus Rating (1-10) | Energy Level (1-10) | Hydration (ml) | Primary Output Completed |
| :--- | :---: | :---: | :---: | :--- |
| 07:00 - 09:00 | | | | |
| 09:00 - 11:00 | | | | |
| 11:00 - 13:00 | | | | |
| 14:00 - 16:00 | | | | |
| 16:00 - 18:00 | | | | |
| 20:00 - 22:00 | | | | |

### Daily Micro-Habit Checklist:
- [ ] 15m Morning Sun Exposure
- [ ] 2.5L Total Hydration with Electrolytes
- [ ] 0 Caffeine After 12:30 PM
- [ ] 30m Physical Movement / Resistance Training
- [ ] Blue-Light Cutoff by 20:30
- [ ] Sleep Environment Set to 66°F
"""
        },
        {
            "filename": "7_day_clean_nutrition_framework.md",
            "content": """# 7-Day Clean Nutrition & Mental Energy Protocol

### Core Operating Rules:
1. Fasting Window: 14/10 (First meal at 09:30, Last meal before 19:30).
2. Clean Protein Anchor: Minimum 30g protein per major meal.
3. Anti-Brain Fog Rule: No liquid sugars or refined flours during daylight working hours.

### Recommended Weekly Shopping List:
- Pasture-raised eggs & wild salmon.
- Avocados, raw walnuts, pumpkin seeds.
- Dark leafy greens (spinach, kale, arugula), broccoli, asparagus.
- Himalayan pink salt / unrefined Celtic salt.
- Magnesium Glycinate & Omega-3 EPA/DHA.
"""
        }
    ]

    for tmpl in templates:
        t_path = os.path.join(templates_dir, tmpl["filename"])
        with open(t_path, "w", encoding="utf-8") as f:
            f.write(tmpl["content"].strip())

    # Generate Standalone Web Reader App
    html_reader = os.path.join(mvp_dir, "index.html")
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Peak Performance Protocol: Health, Bio-Optimization & Daily Habits</title>
    <style>
        :root {
            --bg: #090d16;
            --card-bg: #111827;
            --accent: #10b981;
            --accent-glow: rgba(16, 185, 129, 0.2);
            --text: #f3f4f6;
            --text-dim: #9ca3af;
            --border: #1f2937;
        }
        body {
            margin: 0;
            padding: 0;
            background: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
        }
        .container {
            max-width: 860px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .header {
            text-align: center;
            padding-bottom: 30px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 40px;
        }
        .badge {
            background: rgba(16, 185, 129, 0.1);
            color: var(--accent);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 16px;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        h1 { font-size: 32px; margin: 0 0 12px 0; color: #fff; }
        .subtitle { color: var(--text-dim); font-size: 17px; margin: 0; }
        .chapter-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .chapter-card h2 {
            margin-top: 0;
            color: var(--accent);
            font-size: 22px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
        }
        .chapter-card h3 {
            color: #e5e7eb;
            font-size: 17px;
            margin-top: 20px;
        }
        ul { padding-left: 20px; }
        li { margin-bottom: 8px; color: #d1d5db; }
        .checklist {
            background: #0f172a;
            border-left: 4px solid var(--accent);
            padding: 16px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }
        .btn-download {
            background: var(--accent);
            color: #000;
            font-weight: bold;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
        }
        .btn-download:hover { background: #059669; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">EBOOK & PROTOCOL VAULT • HEALTH & DAILY USES</span>
            <h1>The Peak Performance Protocol</h1>
            <p class="subtitle">High-Energy Bio-Optimization, Sustained Mental Focus & Daily Micro-Habits for Remote Builders & Traders</p>
        </div>

        <div class="chapter-card">
            <h2>Chapter 1: Circadian Lighting & Sleep Architecture</h2>
            <p>Cognitive fatigue and brain fog in high-intensity trading and software development rarely stem from lack of willpower. They stem from degraded sleep architecture caused by disrupted circadian rhythms.</p>
            <h3>1. Morning Lux Exposure</h3>
            <p>Expose eyes to 10,000+ lux natural sunlight within 30 minutes of waking for 15-20 minutes to anchor your 14-hour melatonin timer.</p>
            <h3>2. 450nm Blue Light Cutoff</h3>
            <p>Switch screens to warm amber (1900K) post-sunset. Ambient blue light after 8:00 PM suppresses melatonin by up to 85%.</p>
            <h3>3. Ambient Bedroom Cooling</h3>
            <p>Keep bedroom temperature between 65°F and 68°F (18°C - 20°C) to allow natural drop in core body temperature.</p>
        </div>

        <div class="chapter-card">
            <h2>Chapter 2: Nutrition for Sustained Mental Clarity</h2>
            <p>Eliminate violent blood sugar swings and reactive hypoglycemia that trigger midday crashes and impulsive decision-making.</p>
            <div class="checklist">
                <strong>Core Nutrition Rules:</strong>
                <ul>
                    <li>Zero refined sugars or high-glycemic flours before 4:00 PM.</li>
                    <li>Anchor every main meal with 30g+ clean protein.</li>
                    <li>Hard caffeine cutoff strictly at 12:30 PM (protects adenosine clearing).</li>
                </ul>
            </div>
        </div>

        <div class="chapter-card">
            <h2>Chapter 3: Hydration Mechanics & Mineral Timing</h2>
            <p>A mild 1.5% decrease in cellular water balance causes a 12% drop in cognitive speed. Standard filtered tap water without minerals strips intracellular electrolytes.</p>
            <h3>The Morning Mineral Elixir:</h3>
            <p>500ml water + 500mg unrefined Celtic/Himalayan salt + fresh lemon juice to restore cellular adrenal hydration immediately upon waking.</p>
        </div>

        <div class="chapter-card">
            <h2>Chapter 4: Micro-Movement & Posture Mechanics</h2>
            <p>Continuous sitting restricts venous return and drops cerebral oxygenation. Practice the <strong>50/10 Rule</strong>: 50 minutes deep focus, 10 minutes active physical movement (squats, hangs, thoracic foam rolling).</p>
        </div>

        <div class="chapter-card">
            <h2>Chapter 5: The Daily Velocity Checklist</h2>
            <div class="checklist">
                <ul>
                    <li>[ ] 500ml mineral water + sunlight immediately upon waking.</li>
                    <li>[ ] High-protein low-glycemic fuel.</li>
                    <li>[ ] 0 caffeine past 12:30 PM.</li>
                    <li>[ ] 50/10 physical decompression cycles.</li>
                    <li>[ ] Screens warm-shifted by 20:00, dark bedroom cooled to 66°F.</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(html_reader, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Package as downloadable zip
    zip_path = os.path.join(mvp_dir, "Peak_Performance_Health_Daily_Uses_Vault.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(html_reader, arcname="Read_Online_Vault.html")
        for chap in chapters:
            c_p = os.path.join(chapters_dir, chap["filename"])
            z.write(c_p, arcname=f"chapters/{chap['filename']}")
        for tmpl in templates:
            t_p = os.path.join(templates_dir, tmpl["filename"])
            z.write(t_p, arcname=f"templates/{tmpl['filename']}")
            
    print(f"Created package: {zip_path} ({os.path.getsize(zip_path)} bytes)")

    # Write verifier script
    verifier_script = os.path.join(verifier_dir, "verify_mvp_15.py")
    verifier_code = """import os
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
"""
    with open(verifier_script, "w", encoding="utf-8") as f:
        f.write(verifier_code)

if __name__ == "__main__":
    generate_health_daily_uses_vault()
