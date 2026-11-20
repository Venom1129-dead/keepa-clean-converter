# Launch Assets: Local AI VRAM & Quantization Sizing Cockpit (MVP #6)
- **Target Price:** $9 Lifetime License / Free Open-Source Core
- **Format:** In-Browser Single-Page Web App / GitHub Pages
- **Primary Channels:** r/LocalLLaMA, r/MachineLearning, Hugging Face Spaces, GitHub, Product Hunt

---

## 1. Product Title & Taglines
- **Title:** Local AI VRAM & Quantization Sizing Cockpit
- **Subtitle:** Never hit a CUDA Out-of-Memory (OOM) error again. Real-time model weights, GQA KV cache scaling, and GPU tok/sec calculator.
- **Product Summary:**
  Running local open-weight LLMs (Llama 3.1, Qwen 2.5, DeepSeek, Mistral) without calculating your KV cache leads to instant CUDA OOM crashes when context lengths grow. Calculate exact VRAM footprints across 7 quantization levels (Q2_K to FP16), visualize KV cache scaling up to 128k context, and benchmark token generation speeds against your GPU's actual memory bandwidth.

---

## 2. Reddit Value-First Launch Pitch (r/LocalLLaMA & r/selfhosted)
> **Subject:** Built a zero-bloat, client-side VRAM & KV Cache calculator so you never hit CUDA OOM crashes at 32k/128k context
>
> Hey everyone,
> Like many on this sub, I kept running into CUDA OOM errors whenever I pushed Llama 3 or Qwen past 8k context, even though the base model weights fit on my 12GB RTX 3060.
> Most online calculators only compute the static weights (`params * bpw / 8`) and ignore the fact that FP16 KV cache consumes an extra 16GB of VRAM at 128k context!
>
> I built a lightweight, 100% private in-browser calculator:
> - **Accurate GQA KV Cache Math:** Computes exact KV memory by layer, head count, and precision (FP16, FP8, Q4).
> - **Inference Speed Estimator:** Estimates generation tokens/second based on your GPU's actual memory bus bandwidth (GB/s).
> - **1-Click Launch Command:** Generates the exact `ollama run` command for the quant that safely fits your hardware.
>
> Free live web tool: [Link]
