# Build Spec: Local AI VRAM & Quantization Calculator + GPU Sizing Engine
- **Asset ID:** MVP_06
- **Target Revenue:** $9 one-time license / Free Core
- **Format:** Client-Side Web Application (HTML5 + CSS3 + Vanilla JS)
- **Deployment:** GitHub Pages (100% Free Static Hosting)
- **Dependencies:** 0 paid APIs, 0 backend servers, 100% offline math engine.

---

## 1. Problem Statement & Proof-of-Wallet Signal
With the explosion of open-weight LLMs (Llama-3.1, Qwen-2.5, DeepSeek, Mistral, Gemma 2), millions of AI developers, homelabbers, and indie hackers struggle to determine whether a model fits in their GPU VRAM (6GB, 8GB, 12GB, 16GB, 24GB).
Users constantly hit CUDA Out-Of-Memory (OOM) crashes because they calculate only model weights and forget that KV Cache scales linearly with context length (e.g., 32k or 128k context can consume 8GB+ of VRAM on KV cache alone!).

---

## 2. The 10% Wedge Solution
A fast, interactive VRAM Sizing Cockpit:
1. **Model Parameter & Architecture Library:** Pre-configured architectures (1.5B, 3B, 7B/8B, 14B, 32B, 70B) with exact attention head counts and hidden dimensions.
2. **Quantization Precision Engine:**
   - 2-bit (Q2_K)
   - 3-bit (Q3_K_M)
   - 4-bit (Q4_K_M / AWQ / GPTQ)
   - 5-bit (Q5_K_M)
   - 6-bit (Q6_K)
   - 8-bit (Q8_0)
   - 16-bit (FP16 / BF16)
3. **KV Cache & Context Scaling Calculator:**
   - Computes KV cache memory: `2 * n_layers * n_kv_heads * head_dim * context_length * bytes_per_element`
   - Supports FP16, FP8, and Q4 KV cache quantization.
4. **Hardware Matchmaker & Speed Estimator:**
   - Pre-configured GPUs (RTX 3060 12GB, RTX 4070 12GB, RTX 3090/4090 24GB, Apple Silicon M1-M4 16-128GB, Tesla P40, Mac Studio).
   - Estimates tokens/sec generation based on memory bandwidth (`Bandwidth (GB/s) / Model Size (GB)`).
5. **Deterministic OOM Safety Warning:**
   - Flags if Total VRAM > GPU VRAM (with 1.2 GB OS/CUDA buffer included).

---

## 3. Architecture & File Tree
```plaintext
03_Active_MVP_06/
├── frontend/
│   ├── index.html       <-- Interactive VRAM calculator & GPU visualizer
│   ├── app.js           <-- VRAM computation engine & hardware presets
│   └── styles.css       <-- Dark modern developer UI
└── verifier/
    ├── test_vram.py     <-- Deterministic verification suite
    └── expected_models.json
```

---

## 4. Deterministic Acceptance Criteria
- [ ] VRAM formula matches llama.cpp / vLLM memory allocations within ±3%.
- [ ] Correctly identifies KV cache explosion at 32k/128k context.
- [ ] Passes automated test suite with Exit Code 0.
- [ ] Deployed to live GitHub Pages repository.
