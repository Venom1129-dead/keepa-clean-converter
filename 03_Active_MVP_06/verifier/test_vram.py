#!/usr/bin/env python3
"""
03_Active_MVP_06/verifier/test_vram.py
Deterministic verification tests for Local AI VRAM & Quantization Calculator.
"""

import sys

def calculate_weights_gb(params_b, bits_per_weight):
    bytes_total = params_b * 1e9 * (bits_per_weight / 8.0)
    return round(bytes_total / (1024**3), 2)

def calculate_kv_cache_gb(n_layers, n_kv_heads, head_dim, context_len, bytes_per_elem=2.0):
    # 2 * n_layers * n_kv_heads * head_dim * context_len * bytes_per_elem
    total_bytes = 2 * n_layers * n_kv_heads * head_dim * context_len * bytes_per_elem
    return round(total_bytes / (1024**3), 2)

def calculate_total_vram(params_b, bits_per_weight, n_layers, n_kv_heads, head_dim, context_len, kv_bytes=2.0, cuda_overhead=0.8):
    weights = calculate_weights_gb(params_b, bits_per_weight)
    kv = calculate_kv_cache_gb(n_layers, n_kv_heads, head_dim, context_len, kv_bytes)
    total = round(weights + kv + cuda_overhead, 2)
    return {
        "weights_gb": weights,
        "kv_cache_gb": kv,
        "cuda_overhead_gb": cuda_overhead,
        "total_vram_gb": total
    }

def estimate_tokens_per_sec(weights_gb, gpu_bandwidth_gbps):
    if weights_gb <= 0:
        return 0.0
    # Generation phase is memory-bandwidth bound: tokens/sec ≈ Bandwidth / Model Size
    return round(gpu_bandwidth_gbps / weights_gb, 1)

def test_llama3_8b_vram():
    # Llama 3.1 8B: 8.03B params, 32 layers, 8 KV heads (GQA), 128 head dim
    # Q4_K_M (~4.5 bits/weight)
    params = 8.03
    bpw = 4.5
    layers = 32
    kv_heads = 8
    head_dim = 128

    # 1. Standard 8k context
    res_8k = calculate_total_vram(params, bpw, layers, kv_heads, head_dim, 8192)
    print(f"[+] Llama-3.1 8B (Q4_K_M @ 8k context): {res_8k['total_vram_gb']} GB total")
    assert 4.1 <= res_8k["weights_gb"] <= 4.3
    assert res_8k["kv_cache_gb"] == 1.00  # 1 GB exactly for 8k FP16 KV
    assert 5.9 <= res_8k["total_vram_gb"] <= 6.1  # Fits on RTX 3060 / 4060 8GB

    # 2. Ultra-long 128k context (KV cache explosion test)
    res_128k = calculate_total_vram(params, bpw, layers, kv_heads, head_dim, 131072)
    print(f"[+] Llama-3.1 8B (Q4_K_M @ 128k context): {res_128k['total_vram_gb']} GB total (KV Cache: {res_128k['kv_cache_gb']} GB)")
    assert res_128k["kv_cache_gb"] == 16.00  # KV cache is 16 GB!
    assert 20.8 <= res_128k["total_vram_gb"] <= 21.2  # Requires 24GB GPU (RTX 3090/4090)

def test_hardware_bandwidth_inference():
    # RTX 4090: 1008 GB/s bandwidth. Llama-3 8B Q4 (~4.21 GB)
    speed_4090 = estimate_tokens_per_sec(4.21, 1008)
    print(f"[+] RTX 4090 estimated tok/sec: {speed_4090} t/s")
    assert speed_4090 >= 200.0

    # RTX 3060: 360 GB/s bandwidth. Llama-3 8B Q4 (~4.21 GB)
    speed_3060 = estimate_tokens_per_sec(4.21, 360)
    print(f"[+] RTX 3060 estimated tok/sec: {speed_3060} t/s")
    assert 80.0 <= speed_3060 <= 90.0

if __name__ == "__main__":
    print("=== RUNNING LOCAL AI VRAM CALCULATION TESTS ===")
    try:
        test_llama3_8b_vram()
        test_hardware_bandwidth_inference()
        print("\n=== ALL VRAM MATH TESTS PASSED (EXIT CODE 0) ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
