# ============================================
# 1. DEDUPLIKASI
# ============================================
def deduplikasi(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Test
print("=== 1. Deduplikasi ===")
print(deduplikasi([1, 2, 3, 2, 1, 4, 3, 5]))  # [1, 2, 3, 4, 5]
print(deduplikasi(["a", "b", "a", "c", "b"])) # ['a', 'b', 'c']


# ============================================
# 2. INTERSECTION DUA ARRAY
# ============================================
def intersection(list1, list2):
    set2 = set(list2)
    return list({x for x in list1 if x in set2})

# Test
print("\n=== 2. Intersection Dua Array ===")
print(intersection([1, 2, 3, 4], [2, 4, 6, 8]))  # [2, 4]
print(intersection(["a", "b", "c"], ["b", "c", "d"]))  # ['b', 'c']


# ============================================
# 3. ANAGRAM CHECK
# ============================================
def is_anagram(str1, str2):
    if len(str1) != len(str2):
        return False
    
    hitungan = {}
    for char in str1.lower():
        hitungan[char] = hitungan.get(char, 0) + 1
    for char in str2.lower():
        hitungan[char] = hitungan.get(char, 0) - 1
    
    return all(v == 0 for v in hitungan.values())

# Test
print("\n=== 3. Anagram Check ===")
print(is_anagram("listen", "silent"))  # True
print(is_anagram("hello", "world"))   # False
print(is_anagram("Race", "care"))     # True


# ============================================
# 4. FIRST RECURRING CHARACTER
# ============================================
def first_recurring_char(s):
    seen = set()
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    return None  # Tidak ada karakter berulang

# Test
print("\n=== 4. First Recurring Character ===")
print(first_recurring_char("abcabc"))  # 'a'
print(first_recurring_char("abcdef"))  # None
print(first_recurring_char("aabbc"))   # 'a'


# ============================================
# 5. SIMULASI BUKU TELEPON
# ============================================
def buku_telepon():
    kontak = {}

    while True:
        print("\n===== BUKU TELEPON =====")
        print("1. Tambah Kontak")
        print("2. Cari Kontak")
        print("3. Tampilkan Semua")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            nama = input("Nama: ").strip()
            nomor = input("Nomor: ").strip()
            if nama and nomor:
                kontak[nama] = nomor
                print(f"✅ Kontak '{nama}' berhasil ditambahkan.")
            else:
                print("❌ Nama dan nomor tidak boleh kosong.")

        elif pilihan == "2":
            nama = input("Cari nama: ").strip()
            if nama in kontak:
                print(f"📞 {nama}: {kontak[nama]}")
            else:
                print(f"❌ Kontak '{nama}' tidak ditemukan.")

        elif pilihan == "3":
            if kontak:
                print("\n📒 Daftar Kontak:")
                for nama, nomor in kontak.items():
                    print(f"  {nama}: {nomor}")
            else:
                print("📭 Buku telepon kosong.")

        elif pilihan == "4":
            print("👋 Keluar dari buku telepon.")
            break

        else:
            print("❌ Pilihan tidak valid.")

# Jalankan buku telepon
buku_telepon()