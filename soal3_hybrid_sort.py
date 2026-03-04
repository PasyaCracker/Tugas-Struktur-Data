"""
Soal 3 — Hybrid Sort
hybridSort(theSeq, threshold=10):
  - Gunakan insertion sort jika panjang sub-array <= threshold
  - Gunakan selection sort jika lebih besar
Bandingkan jumlah total operasi (comparisons + swaps) antara:
  hybrid sort, pure insertion sort, pure selection sort
pada array random berukuran 50, 100, 500.
"""

import random


# ── Insertion Sort (dengan counter) ───────────────────────────────────────────
def insertionSort(arr, start=0, end=None):
    if end is None:
        end = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(start + 1, end):
        key = arr[i]
        j = i - 1
        while j >= start:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return comparisons, swaps


# ── Selection Sort (dengan counter) ───────────────────────────────────────────
def selectionSort(arr, start=0, end=None):
    if end is None:
        end = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(start, end - 1):
        min_idx = i
        for j in range(i + 1, end):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return comparisons, swaps


# ── Hybrid Sort ────────────────────────────────────────────────────────────────
def hybridSort(theSeq, threshold=10):
    """
    Hybrid sort: insertion sort untuk sub-array <= threshold,
    selection sort untuk yang lebih besar.
    Mengembalikan (sorted_list, total_comparisons, total_swaps)
    """
    arr = theSeq.copy()
    total_comparisons = 0
    total_swaps = 0

    # Bagi array menjadi blok-blok berukuran threshold
    n = len(arr)
    for start in range(0, n, threshold):
        end = min(start + threshold, n)
        chunk_size = end - start
        if chunk_size <= threshold:
            c, s = insertionSort(arr, start, end)
        else:
            c, s = selectionSort(arr, start, end)
        total_comparisons += c
        total_swaps += s

    # Merge blok-blok yang sudah terurut dengan insertion sort final
    c, s = insertionSort(arr)
    total_comparisons += c
    total_swaps += s

    return arr, total_comparisons, total_swaps


# ── Pure wrappers ──────────────────────────────────────────────────────────────
def pureInsertionSort(theSeq):
    arr = theSeq.copy()
    c, s = insertionSort(arr)
    return arr, c, s


def pureSelectionSort(theSeq):
    arr = theSeq.copy()
    c, s = selectionSort(arr)
    return arr, c, s


# ── Benchmark ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Soal 3: Hybrid Sort ===\n")

    sizes = [50, 100, 500]
    header = f"{'Size':>6} | {'Algorithm':>20} | {'Comparisons':>12} | {'Swaps':>8} | {'Total Ops':>10}"
    print(header)
    print("-" * len(header))

    for size in sizes:
        random.seed(42)
        arr = [random.randint(1, 1000) for _ in range(size)]

        _, hc, hs = hybridSort(arr)
        _, ic, is_ = pureInsertionSort(arr)
        _, sc, ss = pureSelectionSort(arr)

        results = [
            ("Hybrid Sort",    hc, hs),
            ("Insertion Sort", ic, is_),
            ("Selection Sort", sc, ss),
        ]

        for i, (name, comps, swaps) in enumerate(results):
            label = str(size) if i == 0 else ""
            print(f"{label:>6} | {name:>20} | {comps:>12,} | {swaps:>8,} | {comps+swaps:>10,}")
        print()

    print("Catatan: Hybrid sort menggabungkan keunggulan insertion sort (efisien\n"
          "untuk data kecil/hampir terurut) dengan selection sort (minimum swaps).")
