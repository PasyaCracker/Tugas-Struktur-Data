"""
Big Integer Implementation using Linked List
=============================================
Setiap digit disimpan terbalik (reverse) dalam linked list.
Contoh: 1234 → node: 4 → 3 → 2 → 1
"""


# ─────────────────────────────────────────────
# BAGIAN 1: Linked List Dasar
# ─────────────────────────────────────────────

class Node:
    """Satu node menyimpan satu digit (0-9)."""

    def __init__(self, digit: int):
        if not (0 <= digit <= 9):
            raise ValueError(f"Digit harus 0-9, bukan {digit}")
        self.digit: int = digit
        self.next: "Node | None" = None

    def __repr__(self) -> str:
        return f"Node({self.digit})"


class DigitLinkedList:
    """
    Linked list untuk menyimpan digit angka secara terbalik.
    Angka 1234 disimpan: head → 4 → 3 → 2 → 1 → None
    """

    def __init__(self):
        self.head: Node | None = None
        self.size: int = 0

    # ── Insert ──────────────────────────────
    def append(self, digit: int) -> None:
        """Tambahkan digit ke akhir list (posisi paling signifikan)."""
        new_node = Node(digit)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, digit: int) -> None:
        """Tambahkan digit ke awal list (posisi paling tidak signifikan)."""
        new_node = Node(digit)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    # ── Delete ──────────────────────────────
    def remove_leading_zeros(self) -> None:
        """Hapus nol di akhir list (leading zeros pada angka asli)."""
        # Karena disimpan terbalik, leading zeros ada di AKHIR list
        if self.head is None:
            return
        # Kumpulkan semua node ke list sementara
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        # Hapus trailing zeros (= leading zeros pada angka asli)
        while len(nodes) > 1 and nodes[-1].digit == 0:
            nodes.pop()
            self.size -= 1
        # Rebuild
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        nodes[-1].next = None
        self.head = nodes[0]

    # ── Read / Display ───────────────────────
    def to_string(self) -> str:
        """Konversi linked list ke string angka (balik urutan node)."""
        digits = []
        current = self.head
        while current:
            digits.append(str(current.digit))
            current = current.next
        return "".join(reversed(digits)) if digits else "0"

    def to_list(self) -> list[int]:
        """Return list digit dalam urutan linked list (terbalik dari angka)."""
        result = []
        current = self.head
        while current:
            result.append(current.digit)
            current = current.next
        return result

    @classmethod
    def from_string(cls, number_str: str) -> "DigitLinkedList":
        """Buat DigitLinkedList dari string angka."""
        number_str = number_str.lstrip("0") or "0"
        ll = cls()
        # Masukkan terbalik agar digit terkecil ada di head
        for ch in reversed(number_str):
            ll.append(int(ch))
        return ll

    def __repr__(self) -> str:
        nodes = self.to_list()
        chain = " → ".join(str(d) for d in nodes)
        return f"[{chain}]  (= {self.to_string()})"


# ─────────────────────────────────────────────
# BAGIAN 2: Big Integer Class
# ─────────────────────────────────────────────

class BigInteger:
    """
    Big Integer menggunakan DigitLinkedList.
    Mendukung angka negatif dengan atribut `negative`.
    Operasi: +  -  *  //  %  **  abs  compare  gcd  factorial
    """

    def __init__(self, value: "int | str | BigInteger" = 0):
        self.negative: bool = False
        self._ll: DigitLinkedList = DigitLinkedList()

        if isinstance(value, BigInteger):
            self._ll = DigitLinkedList.from_string(value._ll.to_string())
            self.negative = value.negative
        elif isinstance(value, int):
            self.negative = value < 0
            self._ll = DigitLinkedList.from_string(str(abs(value)))
        elif isinstance(value, str):
            s = value.strip()
            if s.startswith("-"):
                self.negative = True
                s = s[1:]
            self._ll = DigitLinkedList.from_string(s)
        else:
            raise TypeError(f"Tidak bisa membuat BigInteger dari {type(value)}")

        self._normalize()

    # ── Internal helpers ─────────────────────

    def _normalize(self) -> None:
        """Hapus leading zeros dan pastikan nol tidak negatif."""
        self._ll.remove_leading_zeros()
        if self._ll.to_string() == "0":
            self.negative = False

    def _digits(self) -> list[int]:
        """Digit dalam urutan linked list (least significant first)."""
        return self._ll.to_list()

    @staticmethod
    def _from_digits(digits: list[int], negative: bool = False) -> "BigInteger":
        """Buat BigInteger dari list digit (least significant first)."""
        bi = BigInteger.__new__(BigInteger)
        bi.negative = negative
        bi._ll = DigitLinkedList()
        for d in digits:
            bi._ll.append(d)
        bi._normalize()
        return bi

    # ── Display ──────────────────────────────

    def __str__(self) -> str:
        s = self._ll.to_string()
        return ("-" + s) if self.negative else s

    def __repr__(self) -> str:
        return f"BigInteger('{self}')"

    def linked_list_repr(self) -> str:
        """Tampilkan representasi internal linked list."""
        nodes = self._digits()
        chain = " → ".join(str(d) for d in nodes)
        sign = "-" if self.negative else "+"
        return f"sign={sign}  digits(LSB first): [{chain}]  =  {self}"

    # ── Comparison ───────────────────────────

    @staticmethod
    def _abs_compare(a: "BigInteger", b: "BigInteger") -> int:
        """
        Bandingkan nilai absolut.
        Return: 1 jika |a| > |b|, -1 jika |a| < |b|, 0 jika sama.
        """
        da, db = a._digits(), b._digits()
        # Hapus leading zeros (dari ujung)
        while len(da) > 1 and da[-1] == 0:
            da.pop()
        while len(db) > 1 and db[-1] == 0:
            db.pop()
        if len(da) != len(db):
            return 1 if len(da) > len(db) else -1
        for x, y in zip(reversed(da), reversed(db)):
            if x != y:
                return 1 if x > y else -1
        return 0

    def __eq__(self, other) -> bool:
        other = _ensure_bigint(other)
        return self.negative == other.negative and self._abs_compare(self, other) == 0

    def __lt__(self, other) -> bool:
        other = _ensure_bigint(other)
        if self.negative != other.negative:
            return self.negative  # negatif < positif
        cmp = self._abs_compare(self, other)
        return (cmp == -1) if not self.negative else (cmp == 1)

    def __le__(self, other) -> bool:
        return self == other or self < other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    # ── Penjumlahan (+) ──────────────────────

    @staticmethod
    def _add_abs(a: "BigInteger", b: "BigInteger") -> "BigInteger":
        """Jumlahkan nilai absolut dua BigInteger."""
        da, db = a._digits(), b._digits()
        result = []
        carry = 0
        for i in range(max(len(da), len(db))):
            x = da[i] if i < len(da) else 0
            y = db[i] if i < len(db) else 0
            total = x + y + carry
            result.append(total % 10)
            carry = total // 10
        if carry:
            result.append(carry)
        return BigInteger._from_digits(result)

    def __add__(self, other: "BigInteger | int | str") -> "BigInteger":
        other = _ensure_bigint(other)
        # (+a) + (+b) atau (-a) + (-b)
        if self.negative == other.negative:
            res = self._add_abs(self, other)
            res.negative = self.negative
            res._normalize()
            return res
        # Beda tanda → gunakan pengurangan absolut
        cmp = self._abs_compare(self, other)
        if cmp == 0:
            return BigInteger(0)
        if cmp > 0:
            res = BigInteger._sub_abs(self, other)
            res.negative = self.negative
        else:
            res = BigInteger._sub_abs(other, self)
            res.negative = other.negative
        res._normalize()
        return res

    def __radd__(self, other) -> "BigInteger":
        return self.__add__(other)

    # ── Pengurangan (-) ──────────────────────

    @staticmethod
    def _sub_abs(larger: "BigInteger", smaller: "BigInteger") -> "BigInteger":
        """Kurangi |smaller| dari |larger|. Asumsi |larger| >= |smaller|."""
        da = larger._digits()[:]
        db = smaller._digits()[:]
        result = []
        borrow = 0
        for i in range(len(da)):
            x = da[i]
            y = db[i] if i < len(db) else 0
            diff = x - y - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result.append(diff)
        return BigInteger._from_digits(result)

    def __sub__(self, other: "BigInteger | int | str") -> "BigInteger":
        other = _ensure_bigint(other)
        # a - b = a + (-b)
        neg_other = BigInteger(other)
        neg_other.negative = not other.negative
        if neg_other._ll.to_string() == "0":
            neg_other.negative = False
        return self.__add__(neg_other)

    def __rsub__(self, other) -> "BigInteger":
        return _ensure_bigint(other).__sub__(self)

    def __neg__(self) -> "BigInteger":
        res = BigInteger(self)
        res.negative = not self.negative
        res._normalize()
        return res

    def __abs__(self) -> "BigInteger":
        res = BigInteger(self)
        res.negative = False
        return res

    # ── Perkalian (*) ────────────────────────

    def __mul__(self, other: "BigInteger | int | str") -> "BigInteger":
        other = _ensure_bigint(other)
        da, db = self._digits(), other._digits()
        result_digits = [0] * (len(da) + len(db))
        for i, x in enumerate(da):
            for j, y in enumerate(db):
                result_digits[i + j] += x * y
        # Normalisasi carry
        for k in range(len(result_digits) - 1):
            result_digits[k + 1] += result_digits[k] // 10
            result_digits[k] %= 10
        res = BigInteger._from_digits(result_digits)
        res.negative = self.negative != other.negative
        res._normalize()
        return res

    def __rmul__(self, other) -> "BigInteger":
        return self.__mul__(other)

    # ── Pembagian (//  dan  %) ───────────────

    def __floordiv__(self, other: "BigInteger | int | str") -> "BigInteger":
        other = _ensure_bigint(other)
        quotient, _ = self._divmod_abs(self, other)
        quotient.negative = self.negative != other.negative
        quotient._normalize()
        return quotient

    def __mod__(self, other: "BigInteger | int | str") -> "BigInteger":
        other = _ensure_bigint(other)
        _, remainder = self._divmod_abs(self, other)
        remainder.negative = self.negative  # sisa bertanda sama dengan dividend
        remainder._normalize()
        return remainder

    def __divmod__(self, other) -> tuple["BigInteger", "BigInteger"]:
        return self.__floordiv__(other), self.__mod__(other)

    @staticmethod
    def _divmod_abs(a: "BigInteger", b: "BigInteger") -> tuple["BigInteger", "BigInteger"]:
        """
        Long division pada nilai absolut.
        Return (quotient, remainder).
        """
        if b._ll.to_string() == "0":
            raise ZeroDivisionError("Pembagian dengan nol tidak diperbolehkan")

        zero = BigInteger(0)
        if BigInteger._abs_compare(a, b) < 0:
            return zero, BigInteger(a)

        # Ambil digit dari MSB ke LSB
        a_digits_msb = list(reversed(a._digits()))
        quotient_digits_msb = []
        current = BigInteger(0)

        for digit in a_digits_msb:
            # current = current * 10 + digit
            current = BigInteger._add_abs(
                BigInteger._from_digits(
                    [0] + current._digits()  # *10 → shift kiri = tambah 0 di LSB
                ),
                BigInteger._from_digits([digit])
            )
            # Cari berapa kali b masuk ke current (0-9)
            q = 0
            for candidate in range(9, 0, -1):
                if BigInteger._abs_compare(
                    BigInteger._from_digits(
                        BigInteger._mul_single(b._digits(), candidate)
                    ),
                    current
                ) <= 0:
                    q = candidate
                    break
            quotient_digits_msb.append(q)
            # current -= q * b
            if q > 0:
                sub = BigInteger._from_digits(
                    BigInteger._mul_single(b._digits(), q)
                )
                current = BigInteger._sub_abs(current, sub)

        quotient = BigInteger._from_digits(list(reversed(quotient_digits_msb)))
        return quotient, current

    @staticmethod
    def _mul_single(digits: list[int], scalar: int) -> list[int]:
        """Kalikan list digit dengan satu bilangan bulat kecil (0-9)."""
        result = []
        carry = 0
        for d in digits:
            total = d * scalar + carry
            result.append(total % 10)
            carry = total // 10
        if carry:
            result.append(carry)
        return result

    # ── Pangkat (**) ─────────────────────────

    def __pow__(self, exp: "BigInteger | int") -> "BigInteger":
        exp = _ensure_bigint(exp)
        if exp.negative:
            raise ValueError("Eksponen negatif tidak didukung untuk BigInteger")
        result = BigInteger(1)
        base = BigInteger(self)
        e = BigInteger(exp)
        zero = BigInteger(0)
        two = BigInteger(2)
        while e > zero:
            if (e % two) == BigInteger(1):   # e ganjil
                result = result * base
            base = base * base
            e = e // two
        return result

    # ── Operasi Tambahan ─────────────────────

    def gcd(self, other: "BigInteger | int") -> "BigInteger":
        """Algoritma Euclidean untuk GCD (FPB)."""
        a = abs(BigInteger(self))
        b = abs(_ensure_bigint(other))
        zero = BigInteger(0)
        while b != zero:
            a, b = b, a % b
        return a

    def lcm(self, other: "BigInteger | int") -> "BigInteger":
        """LCM (KPK) menggunakan LCM = |a*b| / GCD(a,b)."""
        other = _ensure_bigint(other)
        g = self.gcd(other)
        if g == BigInteger(0):
            return BigInteger(0)
        return abs(self * other) // g

    def is_even(self) -> bool:
        """Cek apakah BigInteger genap."""
        return self._digits()[0] % 2 == 0

    def is_zero(self) -> bool:
        return self._ll.to_string() == "0"

    def digit_sum(self) -> "BigInteger":
        """Jumlahkan semua digit (digital root step 1)."""
        return BigInteger(sum(self._digits()))

    def factorial(self) -> "BigInteger":
        """Hitung n! untuk BigInteger n >= 0."""
        if self.negative:
            raise ValueError("Faktorial tidak terdefinisi untuk angka negatif")
        result = BigInteger(1)
        i = BigInteger(2)
        while i <= self:
            result = result * i
            i = i + BigInteger(1)
        return result

    def __len__(self) -> int:
        """Jumlah digit (tanpa sign)."""
        return len(self._digits())


# ── Utility ──────────────────────────────────

def _ensure_bigint(value) -> BigInteger:
    if isinstance(value, BigInteger):
        return value
    return BigInteger(value)


# ─────────────────────────────────────────────
# DEMO / TEST
# ─────────────────────────────────────────────

def separator(title: str) -> None:
    print(f"\n{'═'*55}")
    print(f"  {title}")
    print('═'*55)


if __name__ == "__main__":

    separator("Representasi Linked List")
    a = BigInteger("1234")
    b = BigInteger("5678")
    print(f"a = {a}")
    print(f"  Internal: {a.linked_list_repr()}")
    print(f"b = {b}")
    print(f"  Internal: {b.linked_list_repr()}")

    separator("➕ Penjumlahan")
    print(f"  {a} + {b} = {a + b}")
    print(f"  999 + 1  = {BigInteger(999) + BigInteger(1)}")
    print(f"  -500 + 200 = {BigInteger(-500) + BigInteger(200)}")
    print(f"  -300 + -700 = {BigInteger(-300) + BigInteger(-700)}")

    separator("➖ Pengurangan")
    print(f"  {b} - {a} = {b - a}")
    print(f"  {a} - {b} = {a - b}")
    print(f"  1000 - 999 = {BigInteger(1000) - BigInteger(999)}")

    separator("✖️  Perkalian")
    print(f"  {a} * {b} = {a * b}")
    print(f"  -12 * 34 = {BigInteger(-12) * BigInteger(34)}")
    big = BigInteger("99999999999999999999")
    print(f"  99999999999999999999 * 2 = {big * BigInteger(2)}")

    separator("➗ Pembagian (floor div)")
    print(f"  {b} // {a} = {b // a}")
    print(f"  100 // 3 = {BigInteger(100) // BigInteger(3)}")
    print(f"  100 % 3  = {BigInteger(100) % BigInteger(3)}")
    print(f"  -17 // 5 = {BigInteger(-17) // BigInteger(5)}")

    separator("** Pangkat")
    print(f"  2 ** 10  = {BigInteger(2) ** BigInteger(10)}")
    print(f"  2 ** 64  = {BigInteger(2) ** BigInteger(64)}")
    print(f"  10 ** 20 = {BigInteger(10) ** BigInteger(20)}")

    separator("Operasi Tambahan")
    x, y = BigInteger(48), BigInteger(18)
    print(f"  GCD({x}, {y}) = {x.gcd(y)}")
    print(f"  LCM({x}, {y}) = {x.lcm(y)}")
    print(f"  10! = {BigInteger(10).factorial()}")
    print(f"  20! = {BigInteger(20).factorial()}")
    print(f"  Digit sum 9999 = {BigInteger(9999).digit_sum()}")
    print(f"  is_even(1234) = {BigInteger(1234).is_even()}")
    print(f"  is_even(1235) = {BigInteger(1235).is_even()}")

    separator("Perbandingan")
    print(f"  1234 == 1234 : {BigInteger(1234) == BigInteger(1234)}")
    print(f"  1234 <  5678 : {BigInteger(1234) < BigInteger(5678)}")
    print(f"  -10  >  -20  : {BigInteger(-10) > BigInteger(-20)}")

    separator("Angka Sangat Besar")
    n = BigInteger("12345678901234567890")
    m = BigInteger("98765432109876543210")
    print(f"  n = {n}")
    print(f"  m = {m}")
    print(f"  n + m = {n + m}")
    print(f"  m - n = {m - n}")
    print(f"  n * 3 = {n * BigInteger(3)}")
    print(f"  m // n ≈ {m // n}")