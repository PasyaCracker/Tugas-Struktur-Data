"""
Soal 4 — Merge Tiga Sorted Lists
Implementasikan mergeThreeSortedLists(listA, listB, listC) dalam O(n)
menggunakan tiga pointer dalam satu pass.
Tidak boleh memanggil merge dua list secara bertahap.
"""


def mergeThreeSortedLists(listA, listB, listC):
    """
    Menggabungkan tiga sorted list menjadi satu sorted list.
    Kompleksitas: O(n) di mana n = total elemen dari ketiga list.
    Menggunakan tiga pointer, satu pass.
    """
    result = []
    i, j, k = 0, 0, 0
    na, nb, nc = len(listA), len(listB), len(listC)

    while i < na and j < nb and k < nc:
        a = listA[i]
        b = listB[j]
        c = listC[k]
        if a <= b and a <= c:
            result.append(a); i += 1
        elif b <= a and b <= c:
            result.append(b); j += 1
        else:
            result.append(c); k += 1

    # Salah satu list habis — merge sisa dua list yang masih ada
    while j < nb and k < nc:
        if listB[j] <= listC[k]:
            result.append(listB[j]); j += 1
        else:
            result.append(listC[k]); k += 1

    while i < na and k < nc:
        if listA[i] <= listC[k]:
            result.append(listA[i]); i += 1
        else:
            result.append(listC[k]); k += 1

    while i < na and j < nb:
        if listA[i] <= listB[j]:
            result.append(listA[i]); i += 1
        else:
            result.append(listB[j]); j += 1

    # Tambahkan sisa elemen list yang belum habis
    result.extend(listA[i:])
    result.extend(listB[j:])
    result.extend(listC[k:])

    return result


# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Soal 4: Merge Tiga Sorted Lists ===\n")

    # Contoh dari soal
    A, B, C = [1, 5, 9], [2, 6, 10], [3, 4, 7]
    result = mergeThreeSortedLists(A, B, C)
    print(f"mergeThreeSortedLists({A}, {B}, {C})")
    print(f"→ {result}")
    print(f"  Expected: [1, 2, 3, 4, 5, 6, 7, 9, 10]\n")

    # Edge cases
    print("--- Edge Cases ---")
    print(mergeThreeSortedLists([], [1, 3], [2, 4]))   # list kosong
    print(mergeThreeSortedLists([1], [1], [1]))         # semua sama
    print(mergeThreeSortedLists([1, 2, 3], [], []))     # dua list kosong
    print(mergeThreeSortedLists([10, 20], [5, 15, 25], [1, 30]))
