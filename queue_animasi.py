#!/usr/bin/env python3
"""
Animasi 5 Kasus Queue menggunakan Python curses
================================================
Kasus 1: Antrian Printer Bersama
Kasus 2: Permainan Hot Potato
Kasus 3: Antrian Rumah Sakit (Priority Queue)
Kasus 4: BFS (Breadth-First Search)
Kasus 5: Simulasi Loket Tiket Bandara
"""

import curses
import time
import random
from collections import deque

# ─────────────────────────────────────────────
#  WARNA
# ─────────────────────────────────────────────
def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1,  curses.COLOR_CYAN,    -1)   # judul
    curses.init_pair(2,  curses.COLOR_GREEN,   -1)   # sukses/enqueue
    curses.init_pair(3,  curses.COLOR_RED,     -1)   # hapus/dequeue
    curses.init_pair(4,  curses.COLOR_YELLOW,  -1)   # highlight
    curses.init_pair(5,  curses.COLOR_MAGENTA, -1)   # info
    curses.init_pair(6,  curses.COLOR_WHITE,   -1)   # normal
    curses.init_pair(7,  curses.COLOR_BLUE,    -1)   # kotak/border
    curses.init_pair(8,  curses.COLOR_BLACK,   curses.COLOR_CYAN)    # aktif node
    curses.init_pair(9,  curses.COLOR_BLACK,   curses.COLOR_GREEN)   # visited
    curses.init_pair(10, curses.COLOR_BLACK,   curses.COLOR_YELLOW)  # front/rear

# ─────────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────────
def safe_addstr(win, y, x, text, attr=0):
    """addstr yang aman terhadap batas layar."""
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x < 0:
        return
    max_len = w - x - 1
    if max_len <= 0:
        return
    try:
        win.addstr(y, x, text[:max_len], attr)
    except curses.error:
        pass

def draw_box(win, y, x, h, w, title="", color=7):
    """Gambar kotak dengan judul opsional."""
    attr = curses.color_pair(color)
    try:
        win.box()
    except curses.error:
        pass
    if title:
        safe_addstr(win, 0, 2, f" {title} ", curses.color_pair(1) | curses.A_BOLD)

def draw_queue_visual(win, queue_items, start_y, start_x, label="QUEUE", highlight_idx=-1):
    """Visualisasikan queue sebagai kotak-kotak horizontal."""
    safe_addstr(win, start_y, start_x, f"{label}:", curses.color_pair(1) | curses.A_BOLD)

    cell_w = 8
    col = start_x
    items = list(queue_items)

    if not items:
        safe_addstr(win, start_y + 1, start_x, "[ KOSONG ]", curses.color_pair(5))
        safe_addstr(win, start_y + 3, start_x, "  front                rear", curses.color_pair(6))
        return

    for i, item in enumerate(items):
        label_text = str(item)[:6]
        box_str = f"[{label_text:^6}]"
        if i == highlight_idx:
            attr = curses.color_pair(4) | curses.A_BOLD
        elif i == 0:
            attr = curses.color_pair(2) | curses.A_BOLD
        elif i == len(items) - 1:
            attr = curses.color_pair(3) | curses.A_BOLD
        else:
            attr = curses.color_pair(6)
        safe_addstr(win, start_y + 1, col, box_str, attr)
        col += cell_w

    # panah
    safe_addstr(win, start_y + 2, start_x, "  ↑ front", curses.color_pair(2))
    rear_x = start_x + (len(items) - 1) * cell_w
    safe_addstr(win, start_y + 2, rear_x, "  ↑ rear ", curses.color_pair(3))

def wait_key(win, msg="Tekan SPASI lanjut / Q keluar"):
    """Tunggu input pengguna."""
    h, w = win.getmaxyx()
    safe_addstr(win, h - 2, 2, f" {msg} ", curses.color_pair(4) | curses.A_BLINK)
    win.refresh()
    while True:
        ch = win.getch()
        if ch in (ord(' '), ord('\n'), curses.KEY_ENTER):
            return True
        if ch in (ord('q'), ord('Q')):
            return False

def header(win, title, subtitle=""):
    """Gambar header halaman."""
    win.clear()
    h, w = win.getmaxyx()
    bar = "═" * (w - 2)
    safe_addstr(win, 1, 1, bar, curses.color_pair(7))
    safe_addstr(win, 2, (w - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
    if subtitle:
        safe_addstr(win, 3, (w - len(subtitle)) // 2, subtitle, curses.color_pair(5))
    safe_addstr(win, 4, 1, bar, curses.color_pair(7))
    win.refresh()

def log_line(win, y, x, text, color=6):
    safe_addstr(win, y, x, text, curses.color_pair(color))

# ─────────────────────────────────────────────
#  KASUS 1: ANTRIAN PRINTER
# ─────────────────────────────────────────────
def kasus1_printer(win):
    header(win, "KASUS 1: Antrian Printer Bersama",
           "Dokumen dicetak sesuai urutan kedatangan (FIFO)")
    h, w = win.getmaxyx()

    docs = ["laporan.pdf", "tugas.docx", "foto.jpg", "slide.pptx", "notulen.txt"]
    queue = deque()
    printed = []
    log_y = 12

    safe_addstr(win, 6, 2, "Simulasi: User mengirim dokumen → Printer memproses (FIFO)", curses.color_pair(5))
    win.refresh()
    time.sleep(0.8)

    # ENQUEUE semua dokumen
    for i, doc in enumerate(docs):
        queue.append(doc)
        safe_addstr(win, 8, 2, f"📨 ENQUEUE: '{doc}' ditambahkan ke antrian", curses.color_pair(2) | curses.A_BOLD)
        draw_queue_visual(win, queue, 9, 2, "ANTRIAN PRINTER", highlight_idx=len(queue)-1)
        win.refresh()
        time.sleep(0.9)

    safe_addstr(win, 8, 2, "  ─── Semua dokumen masuk antrian. Printer mulai bekerja... ───  ", curses.color_pair(4))
    win.refresh()
    time.sleep(1.0)

    log_y = 13
    safe_addstr(win, log_y - 1, 2, "LOG PRINTER:", curses.color_pair(1) | curses.A_BOLD)

    # DEQUEUE dan cetak
    tick = 0
    while queue:
        doc = queue.popleft()
        printed.append(doc)

        safe_addstr(win, 8, 2, f"🖨️  DEQUEUE & MENCETAK: '{doc}'                   ", curses.color_pair(3) | curses.A_BOLD)
        draw_queue_visual(win, queue, 9, 2, "ANTRIAN PRINTER")

        log_line(win, log_y + tick, 4, f"✓ [{tick+1}] Mencetak: {doc}", 2)
        win.refresh()
        time.sleep(1.2)
        tick += 1

    safe_addstr(win, log_y + tick + 1, 2, "✅ Semua dokumen selesai dicetak!", curses.color_pair(2) | curses.A_BOLD)
    win.refresh()
    return wait_key(win)

# ─────────────────────────────────────────────
#  KASUS 2: HOT POTATO
# ─────────────────────────────────────────────
def kasus2_hot_potato(win):
    header(win, "KASUS 2: Permainan Hot Potato",
           "Simulasi oper benda melingkar — yang kena tersingkir!")
    h, w = win.getmaxyx()

    names = ["Andi", "Budi", "Citra", "Dedi", "Eka", "Fani"]
    num   = 3  # langkah oper per ronde
    queue = deque(names)
    ronde = 0

    safe_addstr(win, 6, 2, f"Pemain: {', '.join(names)}", curses.color_pair(5))
    safe_addstr(win, 7, 2, f"Aturan: setelah {num}× oper, pemegang kentang tersingkir", curses.color_pair(5))
    eliminated = []

    while len(queue) > 1:
        ronde += 1
        # hapus baris log lama
        for r in range(10, 22):
            safe_addstr(win, r, 2, " " * (w - 4), 0)

        safe_addstr(win, 9, 2, f"── RONDE {ronde} ──", curses.color_pair(1) | curses.A_BOLD)
        draw_queue_visual(win, queue, 10, 2, "PEMAIN")
        safe_addstr(win, 14, 2, f"Mengoper kentang {num} kali...", curses.color_pair(5))
        win.refresh()
        time.sleep(0.6)

        for step in range(num):
            holder = queue[0]
            safe_addstr(win, 15, 2, f"  🥔 Langkah {step+1}: '{holder}' oper ke berikutnya   ", curses.color_pair(4))
            queue.append(queue.popleft())
            draw_queue_visual(win, queue, 10, 2, "PEMAIN", highlight_idx=len(queue)-1)
            win.refresh()
            time.sleep(0.55)

        out = queue.popleft()
        eliminated.append(out)
        safe_addstr(win, 15, 2, f"  ❌ '{out}' tersingkir!                              ", curses.color_pair(3) | curses.A_BOLD)
        draw_queue_visual(win, queue, 10, 2, "PEMAIN")
        safe_addstr(win, 17, 2, f"Tersingkir: {', '.join(eliminated)}", curses.color_pair(3))
        win.refresh()
        time.sleep(1.1)

    winner = queue[0]
    safe_addstr(win, 19, 2, f"🏆 PEMENANG: {winner}!", curses.color_pair(2) | curses.A_BOLD)
    win.refresh()
    return wait_key(win)

# ─────────────────────────────────────────────
#  KASUS 3: ANTRIAN RUMAH SAKIT (PRIORITY QUEUE)
# ─────────────────────────────────────────────
def kasus3_rumah_sakit(win):
    header(win, "KASUS 3: Antrian Rumah Sakit (Priority Queue)",
           "Pasien darurat didahulukan — bukan murni FIFO")
    h, w = win.getmaxyx()

    LABEL = {0: "KRITIS  ", 1: "DARURAT ", 2: "MENENGAH", 3: "RINGAN  "}
    COLOR = {0: 3, 1: 4, 2: 5, 3: 2}

    pasien_datang = [
        ("Budi",  3),
        ("Ani",   0),
        ("Citra", 2),
        ("Dedi",  0),
        ("Eka",   1),
        ("Fira",  2),
    ]

    # Bounded Priority Queue: list of deques per level
    bpq = [deque() for _ in range(4)]
    arrival_order = []

    safe_addstr(win, 6, 2, "Prioritas: 0=KRITIS, 1=DARURAT, 2=MENENGAH, 3=RINGAN", curses.color_pair(5))
    safe_addstr(win, 7, 2, "Prioritas sama → FIFO (yang datang duluan dilayani duluan)", curses.color_pair(5))

    def draw_bpq():
        for lvl in range(4):
            col_attr = curses.color_pair(COLOR[lvl]) | curses.A_BOLD
            safe_addstr(win, 9 + lvl * 2, 2, f"P{lvl}[{LABEL[lvl]}]: ", col_attr)
            items = list(bpq[lvl])
            if items:
                safe_addstr(win, 9 + lvl * 2, 18, " → ".join(items), curses.color_pair(6))
            else:
                safe_addstr(win, 9 + lvl * 2, 18, "(kosong)         ", curses.color_pair(5))

    # ENQUEUE
    for name, prio in pasien_datang:
        bpq[prio].append(name)
        arrival_order.append((name, prio))
        safe_addstr(win, 17, 2,
                    f"📋 ENQUEUE: {name} → Prioritas {prio} [{LABEL[prio].strip()}]     ",
                    curses.color_pair(COLOR[prio]) | curses.A_BOLD)
        draw_bpq()
        win.refresh()
        time.sleep(0.9)

    safe_addstr(win, 17, 2, "  ─── Semua pasien terdaftar. Mulai pelayanan... ───  ", curses.color_pair(4))
    win.refresh()
    time.sleep(1.0)

    log_y = 19
    safe_addstr(win, log_y - 1, 2, "URUTAN LAYANAN:", curses.color_pair(1) | curses.A_BOLD)

    tick = 0
    for lvl in range(4):
        while bpq[lvl]:
            name = bpq[lvl].popleft()
            safe_addstr(win, 17, 2,
                        f"🏥 MELAYANI: {name} (P{lvl} - {LABEL[lvl].strip()})          ",
                        curses.color_pair(COLOR[lvl]) | curses.A_BOLD)
            draw_bpq()
            log_line(win, log_y + tick, 4, f"[{tick+1:2d}] {name:<8} (P{lvl} - {LABEL[lvl].strip()})", COLOR[lvl])
            win.refresh()
            time.sleep(1.0)
            tick += 1

    safe_addstr(win, log_y + tick + 1, 2, "✅ Semua pasien selesai dilayani!", curses.color_pair(2) | curses.A_BOLD)
    win.refresh()
    return wait_key(win)

# ─────────────────────────────────────────────
#  KASUS 4: BFS (Breadth-First Search)
# ─────────────────────────────────────────────
def kasus4_bfs(win):
    header(win, "KASUS 4: BFS — Breadth-First Search",
           "Pencarian jalur terpendek pada graf menggunakan queue")
    h, w = win.getmaxyx()

    # Graf sederhana
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
    }

    # Koordinat node untuk visualisasi (y, x)
    pos = {
        'A': (9,  20),
        'B': (13, 10),
        'C': (13, 30),
        'D': (17,  5),
        'E': (17, 15),
        'F': (17, 30),
    }

    safe_addstr(win, 6, 2, "Graf: A─B─D, A─C─F, B─E─F (pencarian mulai dari A)", curses.color_pair(5))
    safe_addstr(win, 7, 2, "BFS menjelajahi level demi level berkat sifat FIFO queue", curses.color_pair(5))

    def draw_graph(visited, current=None, in_queue=None):
        in_queue = in_queue or set()
        # gambar edge
        edges = [('A','B'), ('A','C'), ('B','D'), ('B','E'), ('C','F'), ('E','F')]
        for u, v in edges:
            uy, ux = pos[u]
            vy, vx = pos[v]
            mid_y = (uy + vy) // 2
            mid_x = (ux + vx) // 2
            safe_addstr(win, mid_y, mid_x, "─" if uy == vy else "│" if ux == vx else "╲", curses.color_pair(7))

        # gambar node
        for node, (ny, nx) in pos.items():
            if node == current:
                attr = curses.color_pair(8) | curses.A_BOLD
                sym = f"[{node}]"
            elif node in visited:
                attr = curses.color_pair(9) | curses.A_BOLD
                sym = f"({node})"
            elif node in in_queue:
                attr = curses.color_pair(4) | curses.A_BOLD
                sym = f"<{node}>"
            else:
                attr = curses.color_pair(6)
                sym = f" {node} "
            safe_addstr(win, ny, nx, sym, attr)

    # BFS
    start = 'A'
    visited = set()
    bfs_queue = deque()
    bfs_queue.append(start)
    visited.add(start)
    order = []
    log_y = 20

    safe_addstr(win, log_y - 1, 2, "TRAVERSAL ORDER:", curses.color_pair(1) | curses.A_BOLD)

    while bfs_queue:
        node = bfs_queue.popleft()
        order.append(node)

        draw_graph(set(order[:-1]), current=node, in_queue=set(bfs_queue))
        safe_addstr(win, 8, 2,
                    f"🔍 DEQUEUE: '{node}'  │ Queue: {list(bfs_queue)}         ",
                    curses.color_pair(3) | curses.A_BOLD)
        log_line(win, log_y, 4, f"  → Visit: {' → '.join(order)}  ", 2)
        win.refresh()
        time.sleep(1.1)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                bfs_queue.append(neighbor)
                draw_graph(set(order), current=node, in_queue=set(bfs_queue))
                safe_addstr(win, 8, 2,
                            f"📥 ENQUEUE: '{neighbor}'  │ Queue: {list(bfs_queue)}         ",
                            curses.color_pair(2) | curses.A_BOLD)
                win.refresh()
                time.sleep(0.7)

    safe_addstr(win, log_y + 1, 2,
                f"✅ BFS selesai! Urutan kunjungan: {' → '.join(order)}",
                curses.color_pair(2) | curses.A_BOLD)
    safe_addstr(win, log_y + 2, 2, "Legenda: [X]=Sedang diproses  (X)=Sudah dikunjungi  <X>=Dalam queue", curses.color_pair(5))
    win.refresh()
    return wait_key(win)

# ─────────────────────────────────────────────
#  KASUS 5: SIMULASI LOKET TIKET BANDARA
# ─────────────────────────────────────────────
def kasus5_bandara(win):
    header(win, "KASUS 5: Simulasi Loket Tiket Bandara",
           "Discrete event simulation — rata-rata waktu tunggu penumpang")
    h, w = win.getmaxyx()

    NUM_AGENTS   = 2
    NUM_MINUTES  = 30
    BETWEEN_TIME = 4    # rata-rata 1 penumpang per 4 menit
    SERVICE_TIME = 5    # lama layanan per penumpang

    queue      = deque()
    agents     = [None] * NUM_AGENTS  # (nama, start_service_time)
    total_wait = 0
    num_served = 0
    arrival_id = [0]

    def handle_arrival(t):
        if random.random() < 1 / BETWEEN_TIME:
            arrival_id[0] += 1
            name = f"P{arrival_id[0]:03d}"
            queue.append((name, t))
            return name
        return None

    def handle_begin(t):
        for i, ag in enumerate(agents):
            if ag is None and queue:
                name, arr_t = queue.popleft()
                agents[i] = (name, t, arr_t)
                return i, name, t - arr_t
        return None, None, 0

    def handle_end(t):
        for i, ag in enumerate(agents):
            if ag and t - ag[1] >= SERVICE_TIME:
                agents[i] = None
                return i, ag[0]
        return None, None

    safe_addstr(win, 6, 2,
                f"Parameter: {NUM_AGENTS} agen, durasi {NUM_MINUTES} mnt, "
                f"interval ±{BETWEEN_TIME} mnt, layanan {SERVICE_TIME} mnt/orang",
                curses.color_pair(5))

    log_y    = 18
    log_msgs = []

    def draw_state(t):
        # Queue
        q_items = [x[0] for x in queue]
        draw_queue_visual(win, q_items, 8, 2, "ANTRIAN PENUMPANG")

        # Agen
        safe_addstr(win, 12, 2, "LOKET:", curses.color_pair(1) | curses.A_BOLD)
        for i, ag in enumerate(agents):
            if ag:
                safe_addstr(win, 13 + i, 4,
                            f"[Loket {i+1}] 🧑 Melayani: {ag[0]} (mulai menit {ag[1]:2d})  ",
                            curses.color_pair(2))
            else:
                safe_addstr(win, 13 + i, 4,
                            f"[Loket {i+1}] ✅ Bebas / Menunggu penumpang             ",
                            curses.color_pair(5))

        # Statistik
        avg_wait = total_wait / num_served if num_served else 0
        safe_addstr(win, 16, 2,
                    f"⏱  Menit: {t:3d}/{NUM_MINUTES}  │  "
                    f"Dilayani: {num_served}  │  "
                    f"Rata2 Tunggu: {avg_wait:.2f} mnt  │  "
                    f"Antrian: {len(queue)}     ",
                    curses.color_pair(4) | curses.A_BOLD)

        # Log berjalan
        for li, msg in enumerate(log_msgs[-4:]):
            safe_addstr(win, log_y + li, 4, msg + " " * 60, curses.color_pair(6))

        win.refresh()

    for t in range(NUM_MINUTES + 1):
        # R1: kedatangan
        came = handle_arrival(t)
        if came:
            log_msgs.append(f"Mnt {t:2d}: {came} TIBA → antrian")

        # R2: mulai layanan
        idx, name, wait = handle_begin(t)
        if name:
            total_wait += wait
            log_msgs.append(f"Mnt {t:2d}: {name} DILAYANI loket {idx+1} (tunggu {wait} mnt)")

        # R3: selesai layanan
        idx2, name2 = handle_end(t)
        if name2:
            num_served += 1
            log_msgs.append(f"Mnt {t:2d}: {name2} SELESAI di loket {idx2+1}")

        draw_state(t)
        time.sleep(0.25)

    # Ringkasan
    avg_final = total_wait / num_served if num_served else 0
    safe_addstr(win, 23, 2,
                f"✅ Simulasi selesai!  Total dilayani: {num_served}  │  "
                f"Rata-rata tunggu: {avg_final:.2f} menit",
                curses.color_pair(2) | curses.A_BOLD)
    safe_addstr(win, 24, 2,
                "💡 Coba tambah 1 agen (NUM_AGENTS=3) untuk melihat penurunan waktu tunggu drastis!",
                curses.color_pair(5))
    win.refresh()
    return wait_key(win)

# ─────────────────────────────────────────────
#  MENU UTAMA
# ─────────────────────────────────────────────
def menu_utama(win):
    curses.curs_set(0)
    win.keypad(True)

    kasus = [
        ("Kasus 1", "Antrian Printer Bersama",          kasus1_printer),
        ("Kasus 2", "Permainan Hot Potato",              kasus2_hot_potato),
        ("Kasus 3", "Antrian Rumah Sakit (Priority)",    kasus3_rumah_sakit),
        ("Kasus 4", "BFS — Breadth-First Search",        kasus4_bfs),
        ("Kasus 5", "Simulasi Loket Tiket Bandara",      kasus5_bandara),
    ]

    pilihan = 0

    while True:
        win.clear()
        h, w = win.getmaxyx()

        # Header
        title = "╔══════════════════════════════════════════╗"
        safe_addstr(win, 1, (w - len(title)) // 2, title, curses.color_pair(7) | curses.A_BOLD)
        t2    = "║  ANIMASI QUEUE — Struktur Data Python    ║"
        safe_addstr(win, 2, (w - len(t2))   // 2, t2,    curses.color_pair(1) | curses.A_BOLD)
        t3    = "╚══════════════════════════════════════════╝"
        safe_addstr(win, 3, (w - len(t3))   // 2, t3,    curses.color_pair(7) | curses.A_BOLD)

        safe_addstr(win, 5, (w - 36) // 2, "Pilih kasus dengan ↑↓ lalu tekan ENTER:", curses.color_pair(5))

        for i, (no, nama, _) in enumerate(kasus):
            label = f"  {no}: {nama}  "
            x     = (w - len(label)) // 2
            if i == pilihan:
                safe_addstr(win, 7 + i * 2, x, label,
                            curses.color_pair(8) | curses.A_BOLD)
            else:
                safe_addstr(win, 7 + i * 2, x, label, curses.color_pair(6))

        safe_addstr(win, 7 + len(kasus) * 2 + 1, (w - 30) // 2,
                    "  [↑↓] Navigasi   [ENTER] Pilih   [Q] Keluar  ",
                    curses.color_pair(4))

        safe_addstr(win, h - 2, 2, "Dibuat untuk mata kuliah Struktur Data & Algoritma",
                    curses.color_pair(5))

        win.refresh()
        ch = win.getch()

        if ch == curses.KEY_UP:
            pilihan = (pilihan - 1) % len(kasus)
        elif ch == curses.KEY_DOWN:
            pilihan = (pilihan + 1) % len(kasus)
        elif ch in (curses.KEY_ENTER, ord('\n'), ord('\r'), ord(' ')):
            lanjut = kasus[pilihan][2](win)
            if not lanjut:
                break
        elif ch in (ord('q'), ord('Q')):
            break

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main(stdscr):
    init_colors()
    curses.curs_set(0)
    stdscr.timeout(-1)  # blocking input
    random.seed()
    menu_utama(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
