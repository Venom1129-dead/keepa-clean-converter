import os
import sys
import re

def verify_game():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, "frontend")
    
    html_path = os.path.join(frontend_dir, "index.html")
    css_path = os.path.join(frontend_dir, "styles.css")
    audio_path = os.path.join(frontend_dir, "audio.js")
    game_path = os.path.join(frontend_dir, "game.js")

    print("[*] Verifying CyberDash 2099 Game Assets...")

    for path, name in [(html_path, "index.html"), (css_path, "styles.css"), 
                       (audio_path, "audio.js"), (game_path, "game.js")]:
        assert os.path.exists(path), f"Missing file: {name}"
        assert os.path.getsize(path) > 100, f"File {name} too small or empty"
        print(f" [+] Found {name}: {os.path.getsize(path)} bytes")

    # 1. HTML Verification
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert '<canvas id="gameCanvas"' in html, "Missing gameCanvas element"
    assert 'id="currentScore"' in html, "Missing currentScore HUD element"
    assert 'id="highScore"' in html, "Missing highScore HUD element"
    assert 'audio.js' in html and 'game.js' in html, "Missing script includes"
    assert 'gumroad.com' in html or 'Get Source Code' in html, "Missing monetization CTA"
    print(" [+] HTML structure verified.")

    # 2. CSS Verification
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert '--neon-cyan' in css and '--neon-pink' in css, "Missing neon color vars"
    assert 'canvas-wrapper' in css, "Missing canvas styling"
    assert '.ui-overlay' in css, "Missing overlay modal styles"
    print(" [+] CSS styles and neon palette verified.")

    # 3. Audio Verification
    with open(audio_path, "r", encoding="utf-8") as f:
        audio = f.read()
    assert 'class SoundEngine' in audio, "Missing SoundEngine class"
    assert 'createOscillator' in audio, "Missing Web Audio oscillator synthesis"
    assert 'playJump' in audio, "Missing playJump function"
    assert 'playDoubleJump' in audio, "Missing playDoubleJump function"
    assert 'playScoreChime' in audio, "Missing playScoreChime function"
    assert 'playCrash' in audio, "Missing playCrash function"
    print(" [+] Procedural Web Audio engine verified.")

    # 4. Game Physics & Loop Verification
    with open(game_path, "r", encoding="utf-8") as f:
        game = f.read()
    assert 'jumpPower' in game and 'gravity' in game, "Missing jump physics definitions"
    assert 'checkCollision' in game, "Missing AABB collision detection"
    assert 'localStorage.getItem' in game and 'cyberdash_highscore' in game, "Missing high score persistence"
    assert 'requestAnimationFrame' in game, "Missing 60fps render loop"
    assert 'spawnObstacle' in game, "Missing obstacle generator"
    assert 'createBurst' in game, "Missing particle burst generator"
    print(" [+] Game physics, collision system, and loop verified.")

    print("\n[SUCCESS] ALL VERIFICATION CHECKS PASSED FOR MVP_09 (Exit Code 0).")

if __name__ == "__main__":
    verify_game()
