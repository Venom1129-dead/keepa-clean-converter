# Playbook: Energy & Token Optimization Protocol (Zero-Waste Setup)
- **Category:** System Optimization / Resource Preservation
- **Owner:** Cline (Implementation) & Antigravity (Specs)

---

## 1. Compute & Battery Preservation (Hardware Layer)
1. **No Polling Loops:** Background scripts and monitors must never poll in tight `while True: sleep(1)` loops. Use OS file watches or manual baton checks.
2. **Prune Orphan CLI Processes:** Terminate zombie `cline-cli` or orphan node processes when idle:
   - Command: `Get-Process cline-cli | Stop-Process` when finished.
3. **Local Client-Side Computing:** Tools (like Keepa Clean Converter) must run in browser RAM via Web Workers—never spin up heavy local server stacks or GPU models when lightweight vanilla JS does the job with 0% CPU idle.

---

## 2. Model Quota & Token Preservation (AI Layer)
1. **Stateless Chat Principle:** Never maintain a 40+ turn conversation in any AI model. Every new turn in a bloated chat re-sends the entire history, wasting 10x the tokens and power.
   - Rule: After 5 turns, summarize into `HANDOFF.md` and start a clean session.
2. **Context Compression:** Raw 20,000-token web scrapes or transcripts must be pre-filtered using `tools/harvest.py` and NotebookLM into 400-word Opportunity Cards before showing to Claude or Gemini.
3. **Tiered Model Routing:**
   - Free Web Scrapers & Perplexity: Raw searches.
   - Codex / Cline: Code edits.
   - Claude: 1-prompt verifications.
   - Gemini Argon/Neon/Hydrogen: Reserved strictly for high-difficulty multi-agent reasoning.
