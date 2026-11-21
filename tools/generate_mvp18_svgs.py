import os

svg_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03_Active_MVP_18", "svg")
os.makedirs(svg_dir, exist_ok=True)

svgs = {
    "01_cybersigil_winged_heart.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="chrome1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="25%" stop-color="#c084fc"/>
      <stop offset="50%" stop-color="#38bdf8"/>
      <stop offset="75%" stop-color="#f43f5e"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
    <linearGradient id="neonPink" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f43f5e"/>
      <stop offset="100%" stop-color="#a855f7"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="none"/>
  <!-- Cybersigilism Left Wing -->
  <path d="M 230 250 C 180 200 120 160 50 180 C 90 210 130 230 150 270 C 100 240 60 260 20 290 C 80 300 130 310 170 330 C 130 330 90 350 50 380 C 120 370 180 350 220 310 Z" fill="url(#chrome1)" stroke="#38bdf8" stroke-width="2"/>
  <!-- Cybersigilism Right Wing -->
  <path d="M 270 250 C 320 200 380 160 450 180 C 410 210 370 230 350 270 C 400 240 440 260 480 290 C 420 300 370 310 330 330 C 370 330 410 350 450 380 C 380 370 320 350 280 310 Z" fill="url(#chrome1)" stroke="#38bdf8" stroke-width="2"/>
  <!-- Thorn Spikes -->
  <path d="M 250 80 L 255 180 L 250 190 L 245 180 Z M 250 340 L 255 440 L 250 450 L 245 440 Z" fill="url(#neonPink)"/>
  <!-- Center Liquid Chrome Heart -->
  <path d="M 250 220 C 230 180 170 180 170 240 C 170 290 250 340 250 340 C 250 340 330 290 330 240 C 330 180 270 180 250 220 Z" fill="url(#chrome1)" stroke="#ffffff" stroke-width="4"/>
  <!-- Inner cyber core glow -->
  <circle cx="250" cy="255" r="14" fill="#ffffff" filter="drop-shadow(0 0 8px #38bdf8)"/>
  <polygon points="250,230 255,250 275,255 255,260 250,280 245,260 225,255 245,250" fill="#ffffff"/>
</svg>''',

    "02_y2k_tribal_cyber_cross.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="cyberChrome2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="30%" stop-color="#e2e8f0"/>
      <stop offset="60%" stop-color="#9333ea"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>
  <!-- Tribal Gothic Cyber Cross -->
  <g stroke="url(#cyberChrome2)" stroke-width="6" fill="none" stroke-linejoin="round">
    <!-- Vertical Spine -->
    <path d="M 250 40 Q 230 150 250 250 Q 270 350 250 460"/>
    <path d="M 250 40 Q 270 150 250 250 Q 230 350 250 460"/>
    <!-- Horizontal Crossbar -->
    <path d="M 60 200 Q 150 180 250 200 Q 350 220 440 200"/>
    <path d="M 60 200 Q 150 220 250 200 Q 350 180 440 200"/>
    <!-- Barbed thorn wraps -->
    <path d="M 220 120 L 280 140 M 280 110 L 220 150"/>
    <path d="M 220 280 L 280 300 M 280 270 L 220 310"/>
    <path d="M 120 180 L 140 240 M 110 240 L 150 180"/>
    <path d="M 360 180 L 380 240 M 350 240 L 390 180"/>
  </g>
  <!-- Core Halo and Gem -->
  <circle cx="250" cy="200" r="45" stroke="#38bdf8" stroke-width="3" fill="none"/>
  <polygon points="250,165 260,195 290,200 260,205 250,235 240,205 210,200 240,195" fill="#f43f5e"/>
</svg>''',

    "03_liquid_chrome_butterfly.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="gradButter" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#f472b6"/>
      <stop offset="70%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#818cf8"/>
    </linearGradient>
  </defs>
  <!-- Left Forewing -->
  <path d="M 245 230 C 180 110 80 80 40 140 C 10 190 60 260 160 260 C 210 260 235 245 245 230 Z" fill="url(#gradButter)" stroke="#ffffff" stroke-width="2"/>
  <!-- Left Hindwing -->
  <path d="M 240 250 C 180 260 90 280 80 350 C 70 410 160 440 200 370 C 220 330 235 280 240 250 Z" fill="url(#gradButter)" stroke="#ffffff" stroke-width="2"/>
  <!-- Right Forewing -->
  <path d="M 255 230 C 320 110 420 80 460 140 C 490 190 440 260 340 260 C 290 260 265 245 255 230 Z" fill="url(#gradButter)" stroke="#ffffff" stroke-width="2"/>
  <!-- Right Hindwing -->
  <path d="M 260 250 C 320 260 410 280 420 350 C 430 410 340 440 300 370 C 280 330 265 280 260 250 Z" fill="url(#gradButter)" stroke="#ffffff" stroke-width="2"/>
  <!-- Body and Antennae -->
  <ellipse cx="250" cy="270" rx="8" ry="50" fill="#ffffff"/>
  <path d="M 248 220 Q 210 170 190 150 M 252 220 Q 290 170 310 150" stroke="#f472b6" stroke-width="3" fill="none"/>
  <circle cx="188" cy="148" r="4" fill="#ffffff"/>
  <circle cx="312" cy="148" r="4" fill="#ffffff"/>
  <!-- Cyber star sparkles -->
  <polygon points="120,180 123,190 133,193 123,196 120,206 117,196 107,193 117,190" fill="#ffffff"/>
  <polygon points="380,180 383,190 393,193 383,196 380,206 377,196 367,193 377,190" fill="#ffffff"/>
</svg>''',

    "04_mecha_halo_angel.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="mechaGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
  </defs>
  <!-- Futuristic segmented halo -->
  <ellipse cx="250" cy="130" rx="140" ry="32" stroke="url(#mechaGold)" stroke-width="6" fill="none" stroke-dasharray="25, 10, 15, 10"/>
  <ellipse cx="250" cy="130" rx="110" ry="24" stroke="#38bdf8" stroke-width="2" fill="none"/>
  <!-- Central Cyber Eye / Core -->
  <path d="M 170 230 Q 250 160 330 230 Q 250 300 170 230 Z" fill="#0f172a" stroke="#38bdf8" stroke-width="4"/>
  <circle cx="250" cy="230" r="30" fill="url(#mechaGold)"/>
  <circle cx="250" cy="230" r="12" fill="#0f172a"/>
  <!-- Radiating mechanical feather blades -->
  <g fill="#e2e8f0" stroke="#0284c7" stroke-width="2">
    <polygon points="150,220 50,280 80,310 160,260"/>
    <polygon points="130,260 40,340 70,370 150,300"/>
    <polygon points="350,220 450,280 420,310 340,260"/>
    <polygon points="370,260 460,340 430,370 350,300"/>
  </g>
</svg>''',

    "05_barbed_wire_heart_lock.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="silverBarbed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#cbd5e1"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
  </defs>
  <!-- Shackle -->
  <path d="M 180 200 L 180 120 C 180 60 320 60 320 120 L 320 200" stroke="url(#silverBarbed)" stroke-width="22" fill="none" stroke-linecap="round"/>
  <!-- Heart Lock Body -->
  <path d="M 250 210 C 210 160 120 170 120 250 C 120 330 250 410 250 410 C 250 410 380 330 380 250 C 380 170 290 160 250 210 Z" fill="#1e1b4b" stroke="#f43f5e" stroke-width="8"/>
  <!-- Keyhole -->
  <circle cx="250" cy="265" r="14" fill="#f43f5e"/>
  <polygon points="244,270 256,270 260,305 240,305" fill="#f43f5e"/>
  <!-- Wrapped Barbed Wire -->
  <path d="M 100 240 Q 250 310 400 240 M 110 320 Q 250 390 390 310" stroke="url(#silverBarbed)" stroke-width="6" fill="none"/>
  <!-- Barbs -->
  <polygon points="170,260 185,275 160,270" fill="#ffffff"/>
  <polygon points="320,260 335,275 310,270" fill="#ffffff"/>
  <polygon points="240,340 255,355 230,350" fill="#ffffff"/>
</svg>''',

    "06_cybersigil_starburst.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="starGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="50%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
  </defs>
  <!-- 4 Primary Points -->
  <polygon points="250,20 265,220 480,250 265,280 250,480 235,280 20,250 235,220" fill="url(#starGrad)" stroke="#ffffff" stroke-width="2"/>
  <!-- 4 Secondary Points -->
  <polygon points="100,100 230,230 100,400 230,270 400,400 270,270 400,100 270,230" fill="#a855f7" opacity="0.8"/>
  <!-- Cybersigil Thorn Rings -->
  <circle cx="250" cy="250" r="100" stroke="#38bdf8" stroke-width="3" fill="none" stroke-dasharray="15, 12, 5, 12"/>
  <circle cx="250" cy="250" r="40" stroke="#f43f5e" stroke-width="2" fill="none"/>
  <circle cx="250" cy="250" r="12" fill="#ffffff"/>
</svg>''',

    "07_biomech_spine_vector.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bioGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="50%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>
  </defs>
  <!-- Vertebrae Stack -->
  <g fill="url(#bioGrad)" stroke="#0f172a" stroke-width="3">
    <!-- Top vertebra -->
    <path d="M 250 60 C 220 40 140 70 80 110 C 130 115 190 100 250 105 C 310 100 370 115 420 110 C 360 70 280 40 250 60 Z"/>
    <ellipse cx="250" cy="90" rx="20" ry="15" fill="#f43f5e"/>
    <!-- Vertebra 2 -->
    <path d="M 250 140 C 215 120 130 150 70 200 C 125 200 185 185 250 190 C 315 185 375 200 430 200 C 370 150 285 120 250 140 Z"/>
    <ellipse cx="250" cy="175" rx="24" ry="18" fill="#f43f5e"/>
    <!-- Vertebra 3 (Center) -->
    <path d="M 250 230 C 210 210 120 240 50 300 C 115 295 180 275 250 280 C 320 275 385 295 450 300 C 380 240 290 210 250 230 Z"/>
    <ellipse cx="250" cy="265" rx="28" ry="20" fill="#f43f5e"/>
    <!-- Vertebra 4 -->
    <path d="M 250 330 C 215 315 140 340 90 390 C 135 385 190 370 250 375 C 310 370 365 385 410 390 C 360 340 285 315 250 330 Z"/>
    <ellipse cx="250" cy="360" rx="24" ry="18" fill="#f43f5e"/>
    <!-- Tail Spike -->
    <polygon points="250,420 230,470 250,490 270,470"/>
  </g>
</svg>''',

    "08_kawaii_terminal_cat.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="termPink" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f472b6"/>
      <stop offset="100%" stop-color="#db2777"/>
    </linearGradient>
  </defs>
  <!-- Cat Ears on Monitor -->
  <polygon points="120,130 90,60 170,100" fill="url(#termPink)" stroke="#ffffff" stroke-width="4"/>
  <polygon points="125,120 105,75 160,105" fill="#fbcfe8"/>
  <polygon points="380,130 410,60 330,100" fill="url(#termPink)" stroke="#ffffff" stroke-width="4"/>
  <polygon points="375,120 395,75 340,105" fill="#fbcfe8"/>
  <!-- CRT Monitor Outer Casing -->
  <rect x="70" y="110" width="360" height="280" rx="30" fill="url(#termPink)" stroke="#ffffff" stroke-width="6"/>
  <!-- Screen Bezel -->
  <rect x="95" y="135" width="310" height="230" rx="16" fill="#090d16" stroke="#fbcfe8" stroke-width="3"/>
  <!-- Terminal Prompt Text -->
  <text x="120" y="180" font-family="monospace" font-size="20" font-weight="bold" fill="#4ade80">&gt; cat /dev/heart</text>
  <text x="120" y="220" font-family="monospace" font-size="18" fill="#38bdf8">while(alive) {</text>
  <text x="145" y="255" font-family="monospace" font-size="18" fill="#f472b6">  code(); love();</text>
  <text x="120" y="290" font-family="monospace" font-size="18" fill="#38bdf8">}</text>
  <!-- Blinking Cursor -->
  <rect x="145" y="310" width="14" height="22" fill="#4ade80"/>
  <!-- Monitor Stand Base -->
  <path d="M 210 390 L 290 390 L 320 440 L 180 440 Z" fill="#db2777" stroke="#ffffff" stroke-width="4"/>
</svg>''',

    "09_null_pointer_princess.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="crownGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
  </defs>
  <!-- Princess Tiara / Crown with Circuits -->
  <polygon points="150,160 170,110 210,140 250,80 290,140 330,110 350,160" fill="url(#crownGrad)" stroke="#ffffff" stroke-width="4"/>
  <circle cx="250" cy="80" r="10" fill="#38bdf8"/>
  <circle cx="170" cy="110" r="7" fill="#ec4899"/>
  <circle cx="330" cy="110" r="7" fill="#ec4899"/>
  <!-- Translucent Alert Card -->
  <rect x="60" y="190" width="380" height="220" rx="20" fill="#1e1b4b" stroke="#38bdf8" stroke-width="4"/>
  <!-- Title -->
  <text x="250" y="245" font-family="sans-serif" font-size="24" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="2">NULL POINTER</text>
  <text x="250" y="285" font-family="sans-serif" font-size="34" font-weight="900" fill="#f472b6" text-anchor="middle" letter-spacing="4">PRINCESS</text>
  <!-- Sub-bar -->
  <rect x="100" y="315" width="300" height="3" fill="#38bdf8"/>
  <text x="250" y="355" font-family="monospace" font-size="15" fill="#a7f3d0" text-anchor="middle">&lt;0x00000000 : EXCEPTION_CUTE&gt;</text>
  <text x="250" y="385" font-family="monospace" font-size="13" fill="#cbd5e1" text-anchor="middle">STATUS: UNCAUGHT_CRUSH</text>
</svg>''',

    "10_git_commit_and_chill.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <!-- Git Tree Graph -->
  <line x1="160" y1="120" x2="160" y2="380" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
  <path d="M 160 200 C 220 200 240 260 240 300 L 240 380" stroke="#f472b6" stroke-width="8" fill="none" stroke-linecap="round"/>
  <!-- Git Commit Nodes -->
  <circle cx="160" cy="140" r="18" fill="#38bdf8" stroke="#ffffff" stroke-width="4"/>
  <circle cx="160" cy="220" r="18" fill="#38bdf8" stroke="#ffffff" stroke-width="4"/>
  <circle cx="240" cy="310" r="18" fill="#f472b6" stroke="#ffffff" stroke-width="4"/>
  <circle cx="160" cy="360" r="22" fill="#4ade80" stroke="#ffffff" stroke-width="5"/>
  <!-- Cherry Blossom Flowers on nodes -->
  <circle cx="160" cy="140" r="6" fill="#fbcfe8"/>
  <circle cx="240" cy="310" r="6" fill="#fbcfe8"/>
  <!-- Typography Badge -->
  <rect x="230" y="130" width="220" height="70" rx="14" fill="#0f172a" stroke="#f472b6" stroke-width="3"/>
  <text x="245" y="160" font-family="monospace" font-size="16" font-weight="bold" fill="#4ade80">$ git commit -m</text>
  <text x="245" y="185" font-family="sans-serif" font-size="16" font-weight="bold" fill="#ffffff">"and chill ♡"</text>
  <!-- Sparkles -->
  <polygon points="360,250 363,260 373,263 363,266 360,276 357,266 347,263 357,260" fill="#fde047"/>
  <polygon points="100,280 103,290 113,293 103,296 100,306 97,296 87,293 97,290" fill="#fde047"/>
</svg>''',

    "11_sudo_make_me_coffee.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="steamGrad" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- Rising Steam Swirls as circuit lines -->
  <path d="M 210 170 Q 180 120 220 70 M 250 170 Q 280 110 240 60 M 290 170 Q 270 120 310 70" stroke="url(#steamGrad)" stroke-width="5" fill="none" stroke-linecap="round"/>
  <!-- Coffee Mug -->
  <path d="M 150 190 L 350 190 L 330 380 C 330 420 170 420 170 380 Z" fill="#1e293b" stroke="#ffffff" stroke-width="6"/>
  <!-- Mug Handle -->
  <path d="M 345 220 C 420 220 420 340 335 340" stroke="#ffffff" stroke-width="16" fill="none" stroke-linecap="round"/>
  <path d="M 345 220 C 400 220 400 340 335 340" stroke="#0f172a" stroke-width="6" fill="none" stroke-linecap="round"/>
  <!-- Front Emblem / Linux prompt -->
  <rect x="180" y="240" width="140" height="100" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="195" y="275" font-family="monospace" font-size="18" font-weight="bold" fill="#ec4899">sudo</text>
  <text x="195" y="300" font-family="monospace" font-size="15" fill="#f1f5f9">make me</text>
  <text x="195" y="325" font-family="monospace" font-size="15" font-weight="bold" fill="#38bdf8">coffee();</text>
</svg>''',

    "12_kawaii_floppy_diskette.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <!-- Floppy Casing -->
  <path d="M 100 80 L 360 80 L 400 120 L 400 420 L 100 420 Z" fill="#f472b6" stroke="#ffffff" stroke-width="8"/>
  <!-- Metal Shutter -->
  <rect x="160" y="80" width="180" height="130" fill="#cbd5e1" stroke="#475569" stroke-width="4"/>
  <rect x="200" y="105" width="45" height="80" rx="6" fill="#0f172a"/>
  <!-- Floppy Label Paper -->
  <rect x="130" y="240" width="240" height="150" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="3"/>
  <!-- Kawaii Blushing Face -->
  <circle cx="200" cy="290" r="12" fill="#0f172a"/>
  <circle cx="300" cy="290" r="12" fill="#0f172a"/>
  <!-- Eye highlights -->
  <circle cx="196" cy="286" r="4" fill="#ffffff"/>
  <circle cx="296" cy="286" r="4" fill="#ffffff"/>
  <!-- Blushes -->
  <ellipse cx="180" cy="310" rx="12" ry="6" fill="#f43f5e" opacity="0.6"/>
  <ellipse cx="320" cy="310" rx="12" ry="6" fill="#f43f5e" opacity="0.6"/>
  <!-- Cute Mouth -->
  <path d="M 235 305 Q 250 320 265 305" stroke="#0f172a" stroke-width="4" fill="none" stroke-linecap="round"/>
  <!-- Label Text -->
  <text x="250" y="365" font-family="monospace" font-size="15" font-weight="bold" fill="#db2777" text-anchor="middle">BACKUP_SOUL_1.44MB</text>
</svg>''',

    "13_hacker_girl_skull_bow.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bowGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f43f5e"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <!-- Stylized Cute Skull -->
  <path d="M 160 250 C 160 150 340 150 340 250 C 340 290 310 320 295 335 L 295 380 L 205 380 L 205 335 C 190 320 160 290 160 250 Z" fill="#ffffff" stroke="#0f172a" stroke-width="8"/>
  <!-- Heart-shaped Eye Sockets -->
  <path d="M 215 240 C 200 220 180 225 180 245 C 180 265 215 285 215 285 C 215 285 250 265 250 245 C 250 225 230 220 215 240 Z" fill="#0f172a"/>
  <path d="M 285 240 C 270 220 250 225 250 245 C 250 265 285 285 285 285 C 285 285 320 265 320 245 C 320 225 300 220 285 240 Z" fill="#0f172a"/>
  <!-- Teeth -->
  <line x1="225" y1="350" x2="225" y2="380" stroke="#0f172a" stroke-width="6"/>
  <line x1="250" y1="350" x2="250" y2="380" stroke="#0f172a" stroke-width="6"/>
  <line x1="275" y1="350" x2="275" y2="380" stroke="#0f172a" stroke-width="6"/>
  <!-- Giant Cyber Ribbon Bow on Head -->
  <!-- Left Wing of Bow -->
  <polygon points="250,150 140,80 130,190" fill="url(#bowGrad)" stroke="#ffffff" stroke-width="5"/>
  <!-- Right Wing of Bow -->
  <polygon points="250,150 360,80 370,190" fill="url(#bowGrad)" stroke="#ffffff" stroke-width="5"/>
  <!-- Center Knot -->
  <circle cx="250" cy="145" r="22" fill="#38bdf8" stroke="#ffffff" stroke-width="4"/>
</svg>''',

    "14_circuit_botanical_rose.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="roseNeon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff007f"/>
      <stop offset="50%" stop-color="#f43f5e"/>
      <stop offset="100%" stop-color="#9333ea"/>
    </linearGradient>
  </defs>
  <!-- Cybernetic Circuit Stem -->
  <path d="M 250 280 L 250 340 L 210 380 L 210 450" stroke="#22c55e" stroke-width="6" fill="none"/>
  <path d="M 250 340 L 290 380 L 290 450" stroke="#22c55e" stroke-width="6" fill="none"/>
  <!-- Circuit Soldering Node Pads -->
  <circle cx="210" cy="450" r="10" fill="#22c55e" stroke="#ffffff" stroke-width="3"/>
  <circle cx="290" cy="450" r="10" fill="#22c55e" stroke="#ffffff" stroke-width="3"/>
  <circle cx="250" cy="340" r="8" fill="#eab308"/>
  <!-- Circuit leaves -->
  <polygon points="210,380 150,380 180,410" fill="#15803d"/>
  <polygon points="290,380 350,380 320,410" fill="#15803d"/>
  <!-- Geometric Blooming Rose Petals -->
  <path d="M 250 90 C 180 90 140 160 180 220 C 140 230 150 290 250 290 C 350 290 360 230 320 220 C 360 160 320 90 250 90 Z" fill="url(#roseNeon)" stroke="#ffffff" stroke-width="4"/>
  <!-- Inner Rose Core -->
  <path d="M 250 140 C 220 140 200 170 220 200 C 200 210 210 240 250 240 C 290 240 300 210 280 200 C 300 170 280 140 250 140 Z" fill="#ffffff"/>
</svg>''',

    "15_frutiger_aero_bubble_fish.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="bubbleGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="40%" stop-color="#38bdf8" stop-opacity="0.5"/>
      <stop offset="80%" stop-color="#0284c7" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0.8"/>
    </radialGradient>
  </defs>
  <!-- Outer Aero Glass Water Sphere -->
  <circle cx="250" cy="250" r="170" fill="url(#bubbleGrad)" stroke="#ffffff" stroke-width="4"/>
  <ellipse cx="210" cy="150" rx="60" ry="25" fill="#ffffff" opacity="0.6" transform="rotate(-30 210 150)"/>
  <!-- Glossy Tropical Fish inside -->
  <g>
    <!-- Fish Body -->
    <ellipse cx="260" cy="250" rx="70" ry="40" fill="#f97316"/>
    <!-- Stripes -->
    <path d="M 240 215 Q 250 250 240 285 M 270 212 Q 280 250 270 288" stroke="#ffffff" stroke-width="12" fill="none"/>
    <!-- Tail Fin -->
    <polygon points="195,250 140,200 150,250 140,300" fill="#ea580c"/>
    <!-- Eye -->
    <circle cx="305" cy="240" r="7" fill="#ffffff"/>
    <circle cx="307" cy="240" r="3" fill="#000000"/>
  </g>
  <!-- Tiny water bubbles -->
  <circle cx="340" cy="180" r="16" fill="url(#bubbleGrad)" stroke="#ffffff" stroke-width="2"/>
  <circle cx="365" cy="150" r="10" fill="url(#bubbleGrad)" stroke="#ffffff" stroke-width="1"/>
</svg>''',

    "16_crt_error_404_heart.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="crtGlass" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0369a1"/>
      <stop offset="100%" stop-color="#082f49"/>
    </linearGradient>
  </defs>
  <!-- CRT Outer Box -->
  <rect x="70" y="80" width="360" height="320" rx="35" fill="#e0f2fe" stroke="#38bdf8" stroke-width="8"/>
  <!-- Bulging Screen -->
  <rect x="100" y="110" width="300" height="240" rx="20" fill="url(#crtGlass)" stroke="#0284c7" stroke-width="4"/>
  <!-- Pixel Heart -->
  <path d="M 250 170 C 230 140 190 140 190 180 C 190 220 250 250 250 250 C 250 250 310 220 310 180 C 310 140 270 140 250 170 Z" fill="#f43f5e"/>
  <!-- Error Text -->
  <text x="250" y="295" font-family="monospace" font-size="22" font-weight="900" fill="#ffffff" text-anchor="middle">ERROR 404</text>
  <text x="250" y="325" font-family="monospace" font-size="14" fill="#38bdf8" text-anchor="middle">&lt;EMOTION_NOT_FOUND&gt;</text>
  <!-- Reflection highlight -->
  <path d="M 115 125 L 300 125 C 240 155 140 185 115 125 Z" fill="#ffffff" opacity="0.3"/>
</svg>''',

    "17_glassmorphic_music_player.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="winampGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0.8"/>
    </linearGradient>
  </defs>
  <!-- Aero Glass Player Shell -->
  <rect x="90" y="100" width="320" height="300" rx="24" fill="url(#winampGrad)" stroke="#ffffff" stroke-width="4"/>
  <!-- Display Screen -->
  <rect x="120" y="130" width="260" height="100" rx="12" fill="#090d16" stroke="#38bdf8" stroke-width="2"/>
  <!-- Equalizer Bars -->
  <rect x="140" y="170" width="12" height="45" fill="#4ade80"/>
  <rect x="160" y="150" width="12" height="65" fill="#22c55e"/>
  <rect x="180" y="160" width="12" height="55" fill="#38bdf8"/>
  <rect x="200" y="145" width="12" height="70" fill="#a855f7"/>
  <rect x="220" y="175" width="12" height="40" fill="#f43f5e"/>
  <text x="250" y="175" font-family="sans-serif" font-size="14" font-weight="bold" fill="#ffffff">HYPERPOP.MP3</text>
  <text x="250" y="200" font-family="monospace" font-size="12" fill="#38bdf8">3:24 / 128kbps</text>
  <!-- Control Buttons -->
  <circle cx="160" cy="280" r="22" fill="#ffffff"/>
  <polygon points="155,270 170,280 155,290" fill="#0f172a"/>
  <circle cx="250" cy="280" r="28" fill="#f43f5e" stroke="#ffffff" stroke-width="3"/>
  <polygon points="245,268 262,280 245,292" fill="#ffffff"/>
  <circle cx="340" cy="280" r="22" fill="#ffffff"/>
  <polygon points="335,270 350,280 335,290" fill="#0f172a"/>
  <!-- Scrub Bar -->
  <rect x="130" y="340" width="240" height="8" rx="4" fill="#ffffff" opacity="0.5"/>
  <circle cx="210" cy="344" r="8" fill="#38bdf8" stroke="#ffffff" stroke-width="2"/>
</svg>''',

    "18_glossy_cloud_download.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="cloudAero" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#bae6fd"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </radialGradient>
  </defs>
  <!-- Glossy 3D Water Droplet Cloud -->
  <path d="M 180 320 C 120 320 90 260 140 220 C 130 160 210 130 250 170 C 290 120 380 140 370 210 C 420 240 400 320 340 320 Z" fill="url(#cloudAero)" stroke="#ffffff" stroke-width="5"/>
  <!-- Glowing Neon Down Arrow -->
  <polygon points="250,220 280,220 280,270 320,270 250,350 180,270 220,270 220,220" fill="#ffffff" stroke="#0284c7" stroke-width="4"/>
  <!-- Aero water droplets -->
  <circle cx="180" cy="370" r="10" fill="#38bdf8"/>
  <circle cx="250" cy="400" r="12" fill="#38bdf8"/>
  <circle cx="320" cy="370" r="8" fill="#38bdf8"/>
</svg>''',

    "19_retro_desktop_cursor_star.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="cursorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="60%" stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>
  </defs>
  <!-- Large Retro Translucent Mouse Pointer -->
  <polygon points="120,60 120,380 200,300 270,440 320,410 250,270 360,270" fill="url(#cursorGrad)" stroke="#0f172a" stroke-width="12" stroke-linejoin="round"/>
  <!-- Inner Highlight -->
  <polygon points="135,100 135,320 195,260 255,380 275,370 215,250 300,250" fill="#ffffff" opacity="0.6"/>
  <!-- Trail of Sparkle Stars -->
  <polygon points="380,80 385,100 405,105 385,110 380,130 375,110 355,105 375,100" fill="#fde047"/>
  <polygon points="420,180 423,195 438,198 423,201 420,216 417,201 402,198 417,195" fill="#f43f5e"/>
  <polygon points="340,340 344,355 359,358 344,361 340,376 336,361 321,358 336,355" fill="#38bdf8"/>
</svg>''',

    "20_fatal_exception_too_cute.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <!-- Windows Aero Translucent Dialog Box -->
  <rect x="50" y="110" width="400" height="280" rx="16" fill="#f1f5f9" stroke="#38bdf8" stroke-width="6"/>
  <!-- Titlebar -->
  <path d="M 50 126 C 50 117 57 110 66 110 L 434 110 C 443 110 450 117 450 126 L 450 155 L 50 155 Z" fill="#0284c7"/>
  <text x="75" y="142" font-family="sans-serif" font-size="16" font-weight="bold" fill="#ffffff">SYSTEM ALERT: EXCEPTION_0x77</text>
  <!-- Close Button X -->
  <rect x="415" y="120" width="24" height="24" rx="4" fill="#f43f5e"/>
  <text x="427" y="137" font-family="sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">✕</text>
  <!-- Warning Icon -->
  <circle cx="120" cy="225" r="32" fill="#f59e0b"/>
  <text x="120" y="240" font-family="sans-serif" font-size="42" font-weight="900" fill="#ffffff" text-anchor="middle">!</text>
  <!-- Dialog Text -->
  <text x="180" y="215" font-family="sans-serif" font-size="18" font-weight="bold" fill="#0f172a">Fatal Exception Detected:</text>
  <text x="180" y="245" font-family="sans-serif" font-size="16" fill="#475569">Target aesthetic exceeds</text>
  <text x="180" y="270" font-family="sans-serif" font-size="16" font-weight="bold" fill="#ec4899">maximum cute tolerances.</text>
  <!-- Action Buttons -->
  <rect x="220" y="320" width="100" height="38" rx="8" fill="#0284c7"/>
  <text x="270" y="344" font-family="sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">IGNORE</text>
  <rect x="335" y="320" width="90" height="38" rx="8" fill="#cbd5e1"/>
  <text x="380" y="344" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">CANCEL</text>
</svg>'''
}

for name, content in svgs.items():
    p = os.path.join(svg_dir, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(svgs)} SVGs in {svg_dir}")
