# HANDOFF.md — Master Project State & Seamless Session Continuation
**Project:** Autonomous AI Income Ecosystem & Trading AI Factory  
**Workspace:** `c:\Users\myven\Downloads\antigravity ai income`  
**Protocol:** Strictly governed by `AGENTS.md` (Chief Coordinator & Manager Posture, 5–10% lean manager effort, Claude Chief Risk Auditor, Cline Technical Worker, Researcher Market Scraper).  
**Current Date/Time:** November 21, 2026  

---

## 1. User Rules & Core Invariants (Non-Negotiable)
1. **Zero Face / Live Verification Invariant:**
   - NEVER use or recommend any platform that requires live selfie, biometric, or face video verification.
   - User permits: Standard email/Google login, bank account number / IFSC / SWIFT, and PayPal.
   - **Amazon KDP is Permanently DROPPED:** User explicitly stated: *"i don't want to sign up for amazon kdp"*. Do NOT revisit or ask user to sign up for Amazon KDP.
2. **Current Storefront Status (Gumroad Unlocked):**
   - User has already signed in to Gumroad and **successfully added their payment method**.
   - Gumroad is 100% active and ready to receive sales revenue right now.
   - Allowed zero-face storefront platforms: **Gumroad**, **itch.io** (indie games/tools), **Payhip** (instant PayPal/Stripe digital downloads), and **GitHub Pages** (free hosting).
3. **The Manager Posture Invariant (ANTI-SOLO DRIFT RULE):**
   - Antigravity operates strictly as Chief Coordinator & Planner (5–10% of total effort).
   - Heavy execution is divided among:
     - **Claude Sonnet 4.6 (Thinking):** Chief Risk Auditor & Council Gatekeeper (`aiincome_review_plan` / review gate).
     - **Cline (Gemini 3.8 Flash High):** Application, UI & Technical Worker.
     - **Researcher (Gemini 3.8 Flash High):** Market Scraper & Scraper Worker.
   - In EVERY report presented to the user, include the transparent per-model percentage breakdown table totaling exactly 100%.
4. **Universal Portability Invariant:**
   - ZERO hardcoded personal paths (`C:\Users\username\...`) in any script, config, or test.
   - Always verify with `python tools/storage_audit.py` (must report Exit Code 0 and 0 hardcoded paths).
5. **Strict Scope Constraint:**
   - Built strictly upon lines 1–73 (`Income types.`) of `01_Research/google_doc_income_types.txt`. Never read past line 73.
6. **Zero-Capital Invariant:**
   - ₹0 / $0 spend limit. No paid APIs, no subscriptions.

---

## 2. Inventory of Completed Deliverables (100% Built, Verified & Pushed)
All 18 MVPs + Trading AI Engine are built, tested with automated test scripts (Exit Code 0), and pushed to Git remote (`origin main`):

| Category / Asset | File Path / Directory | Core Value Proposition |
| :--- | :--- | :--- |
| **Trading AI Engine** | `05_Trading_AI/Trend_Pullback_Alpha_Engine_v1.0.zip` | Binance BTCUSDT trend pullback alpha (+21.66% return, 3.57 Sharpe) + PineScript |
| **MVP 01** | `03_Active_MVP/keepa_clean_converter.html` | Client-side Keepa Amazon price & sales CSV converter (Live on GitHub Pages) |
| **MVP 02** | `03_Active_MVP_02/shopify_normalizer.html` | Shopify supplier-to-catalog CSV normalizer & SKU mapper |
| **MVP 03** | `03_Active_MVP_03/Notion_Invoice_Automator_v1.0.zip` | Zero-setup client invoice & time tracker for Notion |
| **MVP 04** | `03_Active_MVP_04/SEO_Metadata_Extractor_Chrome_Extension_v1.0.zip` | 1-click SEO OpenGraph & Twitter Card validator |
| **MVP 05** | `03_Active_MVP_05/` | Upwork Connects-to-Contract ROI Estimator |
| **MVP 06** | `03_Active_MVP_06/` | Local LLM VRAM & GPU Sizing Calculator |
| **MVP 07** | `03_Active_MVP_07/` | Crypto DCA Volatility & Position Sizer |
| **MVP 08** | `03_Active_MVP_08/` | How to Do Things Faster with AI Playbook Ebook Vault |
| **MVP 09** | `03_Active_MVP_09/CyberDash_2099_v1.0.zip` | Pure HTML5 Canvas Cyberpunk game (Live on GitHub Pages, ready for itch.io) |
| **MVP 10** | `03_Active_MVP_10/50_Cyberpunk_Vector_SVGs_Pack.zip` | 50 Commercial Vector SVGs for digital merch & apparel |
| **MVP 11** | `03_Active_MVP_11/` | RetroMemory RAM & Hardware Budget Allocator |
| **MVP 12** | `03_Active_MVP_12/` | Event Budget Splitter & Vendor Tracker |
| **MVP 13** | `03_Active_MVP_13/` | PC Privacy & Windows Telemetry Audit Hub |
| **MVP 14** | `03_Active_MVP_14/KidTech_Activity_Book_Pack_PrintReady.zip` | Printable Kids' Coloring, Handwriting & Activity Workbook |
| **MVP 15** | `03_Active_MVP_15/Peak_Performance_Health_Daily_Uses_Vault.zip` | Peak Performance Health & Daily Habits Micro-Guide Vault |
| **MVP 16** | `03_Active_MVP_16/Community_QA_Platform_Vault.zip` | Nexus Community QA Engine (Lines 19, 61, 70) |
| **MVP 17** | `03_Active_MVP_17/RE_AI_Deal_Analyzer_Vault.zip` | Real Estate Cap Rate & Cash Flow Analyzer (Line 34) |
| **MVP 18** | `03_Active_MVP_18/Kawaii_Cyber_Tech_Merch_Pack.zip` | 20 Vector Merch SVGs for Printify / Apparel (Line 36) |

---

## 3. Dedicated Browser & Infrastructure Setup
- **Dedicated Profile Directory:** `%LOCALAPPDATA%\AIIncome_Dedicated_Browser` (isolated from personal browsing).
- **Desktop Launcher:** `C:\Users\myven\Desktop\Launch_Dedicated_AI_Browser.bat`
- **Remote Debugging:** Localhost only (`127.0.0.1:9222`).
- **Permanent Anti-Crash & Zero-Freeze Shield:**
  - Automatically executes `tools/patch_chrome_preferences.py` prior to launch (`exit_type=Normal`, `exited_cleanly=true`).
  - Flags: `--disable-session-crashed-bubble --hide-crash-restore-bubble --noerrdialogs`.
  - Flags: `--renderer-process-limit=4 --process-per-site --enable-features=MemorySaverMode,DiscardHeavyTabs,AutomaticTabDiscarding`.
  - Background priority: `/belownormal` (guarantees Windows UI / mouse / typing never stutters).
- **Power Management:** Windows active scheme set to **`Balanced`** (Dynamic CPU clock scaling).
- **Tools:**
  - `tools/system_turbo_cleaner.py`: Flushes inactive working sets (`EmptyWorkingSet`) and kills orphan background workers.
  - `tools/notify_user.py`: Loud 100% volume audio notification using Microsoft Zira voice.

---

## 4. How to Start a Fresh Chat with Zero Loss
When starting a new conversation in this workspace:
1. Click **New Chat** (or open a fresh chat window) in the Antigravity IDE.
2. In the very first prompt, paste this single line:
   ```text
   Read HANDOFF.md and continue as Chief Coordinator under AGENTS.md. Gumroad payment method is connected. Report next publishing steps.
   ```
3. The new agent session will immediately read this file, inherit 100% of the project context, and proceed without asking any duplicate questions.
