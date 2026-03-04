"""
Soal 1 — Modified Binary Search
Implementasikan countOccurrences(sortedList, target) dalam O(log n)
menggunakan dua kali binary search (batas kiri dan batas kanan).
"""


def countOccurrences(sortedList, target):
    """
    Menghitung berapa kali target muncul dalam sortedList.
    Kompleksitas: O(log n)
    """
    left_bound = find_left(sortedList, target)
    if left_bound == -1:
        return 0
    right_bound = find_right(sortedList, target)
    return right_bound - left_bound + 1


def find_left(arr, target):
    """Binary search untuk menemukan indeks paling kiri dari target."""
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            result = mid
            hi = mid - 1      # terus cari ke kiri
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


def find_right(arr, target):
    """Binary search untuk menemukan indeks paling kanan dari target."""
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            result = mid
            lo = mid + 1      # terus cari ke kanan
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


# ── Test ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    arr = [1, 2, 4, 4, 4, 4, 7, 9, 12]

    print("=== Soal 1: Modified Binary Search ===\n")
    print(f"Array: {arr}")
    print(f"countOccurrences(arr, 4)  → {countOccurrences(arr, 4)}  (expected: 4)")
    print(f"countOccurrences(arr, 5)  → {countOccurrences(arr, 5)}  (expected: 0)")
    print(f"countOccurrences(arr, 1)  → {countOccurrences(arr, 1)}  (expected: 1)")
    print(f"countOccurrences(arr, 12) → {countOccurrences(arr, 12)} (expected: 1)")
    print(f"countOccurrences(arr, 99) → {countOccurrences(arr, 99)} (expected: 0)")
