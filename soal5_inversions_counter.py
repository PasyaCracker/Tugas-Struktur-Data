"""
Soal 5 — Inversions Counter
Sebuah inversion adalah pasangan (i, j) di mana i < j tapi arr[i] > arr[j].

a) countInversionsNaive(arr)  — brute force O(n²)
b) countInversionsSmart(arr) — modifikasi merge sort O(n log n)

Uji kedua fungsi dan bandingkan waktu eksekusi pada array
random berukuran 1000, 5000, dan 10000.
"""

import random
import time


# ── a) Naive O(n²) ────────────────────────────────────────────────────────────
def countInversionsNaive(arr):
    """Brute force: cek setiap pasangan (i, j). Kompleksitas O(n²)."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


# ── b) Smart O(n log n) via Merge Sort ────────────────────────────────────────
def countInversionsSmart(arr):
    """
    Modifikasi merge sort untuk menghitung inversions dalam O(n log n).
    Setiap kali elemen dari kanan dipilih saat merge, semua elemen
    yang tersisa di sisi kiri adalah inversions.
    """
    _, count = _merge_sort_count(arr[:])
    return count


def _merge_sort_count(arr):
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left, left_count  = _merge_sort_count(arr[:mid])
    right, right_count = _merge_sort_count(arr[mid:])
    merged, split_count = _merge_count(left, right)

    return merged, left_count + right_count + split_count


def _merge_count(left, right):
    merged = []
    inversions = 0
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            # left[i..] semua > right[j] → inversions
            inversions += len(left) - i
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark(size):
    random.seed(0)
    arr = [random.randint(1, 10_000) for _ in range(size)]

    # Naive
    t0 = time.perf_counter()
    naive_result = countInversionsNaive(arr)
    naive_time = time.perf_counter() - t0

    # Smart
    t0 = time.perf_counter()
    smart_result = countInversionsSmart(arr)
    smart_time = time.perf_counter() - t0

    assert naive_result == smart_result, "Hasil berbeda! Ada bug."
    return naive_result, naive_time, smart_time


if __name__ == "__main__":
    print("=== Soal 5: Inversions Counter ===\n")

    # Correctness check
    test = [3, 1, 2, 5, 4]
    print(f"Test array: {test}")
    print(f"  Naive  → {countInversionsNaive(test)}  inversions")
    print(f"  Smart  → {countInversionsSmart(test)}  inversions")
    print(f"  (Pairs: (3,1),(3,2),(5,4) = 3 inversions)\n")

    # Benchmark
    print(f"{'Size':>7} | {'Inversions':>12} | {'Naive (s)':>10} | {'Smart (s)':>10} | {'Speedup':>8}")
    print("-" * 60)

    for size in [1000, 5000, 10000]:
        inv, t_naive, t_smart = benchmark(size)
        speedup = t_naive / t_smart if t_smart > 0 else float('inf')
        print(f"{size:>7,} | {inv:>12,} | {t_naive:>10.4f} | {t_smart:>10.4f} | {speedup:>7.1f}x")

    print("\n--- Mengapa merge sort lebih cepat? ---")
    print(
        "Naive O(n²): untuk n=10.000 → ~50 juta perbandingan.\n"
        "Merge sort O(n log n): untuk n=10.000 → ~130 ribu operasi.\n\n"
        "Kunci insight merge sort:\n"
        "  Saat merge dua sub-array yang sudah terurut, jika elemen kanan\n"
        "  lebih kecil dari elemen kiri ke-i, maka SEMUA elemen kiri dari\n"
        "  posisi i ke akhir sub-array kiri pasti lebih besar (karena terurut).\n"
        "  Kita bisa langsung menambahkan (len_left - i) inversions sekaligus,\n"
        "  tanpa mengecek satu per satu → inilah yang menghemat waktu."
    )
