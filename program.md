# Program Directive: AI Factory

## Core Mission
Build and validate focused micro-software assets, Chrome extensions, scrapers, and data tools that solve painful, high-intent problems, moving rapidly through:
$$\$1/\text{day} \longrightarrow \$10/\text{day} \longrightarrow \$100/\text{day}$$

## Locked Human Rules (Read-Only for all AI Agents)
1. **Never spend more than 24 hours on an MVP.** Every idea must go from research to working code within a single day.
2. **The 200-Impression Kill Switch:** Drive 200 targeted views to the offer/tool. If it produces zero revenue or zero signups, log it as `KILLED` in `00_Brain/experiments.md` and move to the next Opportunity Card.
3. **No Heavy Code in Claude:** Claude is the CEO, Architect & Brutal Verifier. It must never write hundreds of lines of boilerplate code—that wastes rolling quota.
4. **Claude-Only Architect & Verifier Lock:** The Architect & Verifier role must remain Claude (via Claude Web, Antigravity Claude pool, or LiteLLM Claude bridges) to prevent quality degradation.
5. **Zero Token Waste:** AI sessions must be kept stateless using `HANDOFF.md`. Never feed full 20,000-token chat histories into models when a 20-line handoff summary suffices.
