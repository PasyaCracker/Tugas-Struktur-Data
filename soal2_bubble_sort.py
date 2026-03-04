"""
Soal 2 — Bubble Sort dengan Analisis Langkah
Modifikasi bubbleSort() agar:
- Mengembalikan tuple (sorted_list, total_comparisons, total_swaps, passes_used)
- Mengimplementasikan early termination
- Mencetak state array setelah setiap pass
"""


def bubbleSort(arr):
    """
    Bubble sort dengan early termination dan analisis langkah.
    Returns: (sorted_list, total_comparisons, total_swaps, passes_used)
    """
    data = arr.copy()
    n = len(data)
    total_comparisons = 0
    total_swaps = 0
    passes_used = 0

    print(f"  Start : {data}")

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            total_comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                total_swaps += 1
                swapped = True

        passes_used += 1
        print(f"  Pass {passes_used:2d}: {data}")

        if not swapped:          # early termination
            break

    return data, total_comparisons, total_swaps, passes_used


def run_test(arr):
    print(f"\nInput: {arr}")
    sorted_arr, comps, swaps, passes = bubbleSort(arr)
    print(f"  → Sorted        : {sorted_arr}")
    print(f"  → Comparisons   : {comps}")
    print(f"  → Swaps         : {swaps}")
    print(f"  → Passes used   : {passes}")


# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Soal 2: Bubble Sort dengan Analisis Langkah ===")

    run_test([5, 1, 4, 2, 8])
    run_test([1, 2, 3, 4, 5])

    print("\n--- Penjelasan mengapa jumlah pass berbeda ---")
    print(
        "[5,1,4,2,8]: Array acak → banyak swap di tiap pass → butuh lebih banyak pass.\n"
        "[1,2,3,4,5]: Array sudah terurut → pass pertama tidak ada swap sama sekali\n"
        "             → early termination langsung aktif setelah 1 pass.\n"
        "Ini menunjukkan early termination sangat efektif untuk array yang sudah\n"
        "hampir atau sepenuhnya terurut, menghemat O(n) pass yang seharusnya O(n²)."
    )
