
"""
LABIRIN ACAK - Berjalan di Windows tanpa install apapun!
Jalankan: python labirin.py
"""
import tkinter as tk
from tkinter import ttk
import random, time
from collections import deque

# ── Arah ──────────────────────────────────────────────────────────────────────
N,S,E,W = 0,1,2,3
OPP={N:S,S:N,E:W,W:E}
DR={N:-1,S:1,E:0,W:0}
DC={N:0,S:0,E:1,W:-1}

# ── Generator labirin (DFS + extra loop) ──────────────────────────────────────
def make_maze(rows, cols, complexity=7):
    pas=[[set() for _ in range(cols)] for _ in range(rows)]
    vis=[[False]*cols for _ in range(rows)]
    stk=[(0,0)]; vis[0][0]=True
    while stk:
        r,c=stk[-1]; dirs=[N,S,E,W]; random.shuffle(dirs); moved=False
        for d in dirs:
            nr,nc=r+DR[d],c+DC[d]
            if 0<=nr<rows and 0<=nc<cols and not vis[nr][nc]:
                pas[r][c].add(d); pas[nr][nc].add(OPP[d])
                vis[nr][nc]=True; stk.append((nr,nc)); moved=True; break
        if not moved: stk.pop()
    # extra loop = lebih membingungkan
    extra=int(rows*cols*(11-complexity)*0.025)
    for _ in range(extra):
        r=random.randint(0,rows-1); c=random.randint(0,cols-1)
        d=random.choice([N,S,E,W]); nr,nc=r+DR[d],c+DC[d]
        if 0<=nr<rows and 0<=nc<cols:
            pas[r][c].add(d); pas[nr][nc].add(OPP[d])
    return pas

def bfs(pas, rows, cols, start=(0,0)):
    end=(rows-1,cols-1); q=deque([(start,[start])]); seen={start}
    while q:
        (r,c),path=q.popleft()
        if (r,c)==end: return path
        for d in pas[r][c]:
            nr,nc=r+DR[d],c+DC[d]
            if (nr,nc) not in seen:
                seen.add((nr,nc)); q.append(((nr,nc),path+[(nr,nc)]))
    return []

# ── Warna ─────────────────────────────────────────────────────────────────────
BG       = "#0f0f14"
CLR_WALL = "#2a2a3a"
CLR_PATH = "#1a1a28"
CLR_TRAL = "#1a4a3a"   # jejak solusi
CLR_PLAY = "#00d4ff"   # titik pemain
CLR_STAR = "#00ff88"   # start
CLR_END  = "#ff4455"   # exit
CLR_DONE = "#ffd700"   # menang

# ── Layar pilih versi ─────────────────────────────────────────────────────────
class MenuScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Labirin Acak")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center(400, 340)
        self._build()

    def _center(self, w, h):
        sw=self.root.winfo_screenwidth(); sh=self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):
        f=tk.Frame(self.root, bg=BG, padx=30, pady=20); f.pack(fill="both",expand=True)

        tk.Label(f, text="LABIRIN ACAK", font=("Consolas",22,"bold"),
                 bg=BG, fg=CLR_PLAY).pack(pady=(10,4))
        tk.Label(f, text="Pilih versi yang ingin dimainkan",
                 font=("Consolas",11), bg=BG, fg="#888").pack(pady=(0,20))

        # Versi 1
        btn1=tk.Button(f, text="▶  Versi SIMPEL\n(langsung main, pure random)",
            font=("Consolas",11,"bold"), bg="#0a3a2a", fg=CLR_STAR,
            activebackground="#0d5a40", activeforeground="white",
            relief="flat", bd=0, padx=10, pady=12, cursor="hand2",
            command=lambda: self._launch("simple"))
        btn1.pack(fill="x", pady=6)

        # Versi 2
        btn2=tk.Button(f, text="⚙  Versi CUSTOM\n(atur baris, kolom, kerumitan)",
            font=("Consolas",11,"bold"), bg="#0a2a4a", fg="#55aaff",
            activebackground="#0d3a6a", activeforeground="white",
            relief="flat", bd=0, padx=10, pady=12, cursor="hand2",
            command=lambda: self._launch("custom"))
        btn2.pack(fill="x", pady=6)

        tk.Label(f, text="Titik biru bergerak sendiri menyelesaikan labirin",
                 font=("Consolas",9), bg=BG, fg="#555").pack(pady=(16,0))

    def _launch(self, mode):
        self.root.destroy()
        root2=tk.Tk()
        if mode=="simple":
            SimpleGame(root2)
        else:
            CustomSetup(root2)
        root2.mainloop()

# ── Game canvas ───────────────────────────────────────────────────────────────
class MazeCanvas:
    """Shared canvas drawing & solve logic untuk kedua versi."""

    def __init__(self, root, rows, cols, complexity, title="Labirin"):
        self.root=root; self.rows=rows; self.cols=cols; self.cmplx=complexity
        self.root.configure(bg=BG)
        self.root.title(title)

        # Hitung ukuran cell agar muat layar
        sw=root.winfo_screenwidth()-80; sh=root.winfo_screenheight()-120
        self.cell=max(8, min(40, sw//cols, sh//rows))
        cw=cols*self.cell; ch=rows*self.cell

        # Header
        self.hdr=tk.Label(root, text="", font=("Consolas",10),
                           bg=BG, fg="#aaa")
        self.hdr.pack(pady=(8,2))

        # Canvas
        self.cv=tk.Canvas(root, width=cw, height=ch, bg=CLR_PATH,
                          highlightthickness=1, highlightbackground="#333")
        self.cv.pack(padx=20, pady=4)

        # Footer
        self.ftr=tk.Label(root, text="", font=("Consolas",10),
                           bg=BG, fg="#888")
        self.ftr.pack(pady=(2,8))

        self._new_game()

        # Keyboard
        root.bind("<KeyPress>", self._key)
        root.focus_set()

    def _new_game(self):
        self.pas=make_maze(self.rows, self.cols, self.cmplx)
        self.player=[0,0]
        self.path=bfs(self.pas,self.rows,self.cols)
        self.trail=set(); self.pidx=0
        self.solving=True; self.won=False
        self.moves=0; self.t0=time.time()
        self._draw_all()
        self._schedule()

    def _schedule(self):
        delay=max(30, 260-self.cmplx*20)   # ms antar langkah
        self._tick(delay)

    def _tick(self, delay):
        if not self.solving or self.won:
            return
        if self.pidx < len(self.path):
            r,c=self.path[self.pidx]
            self.trail.add((r,c))
            self.player=[r,c]; self.pidx+=1; self.moves+=1
            self._draw_all()
            if self.player==[self.rows-1,self.cols-1]:
                self.won=True; self._draw_all(); return
        else:
            self.solving=False
        self.root.after(delay, lambda: self._tick(delay))

    # ── Drawing ───────────────────────────────────────────────────────────────
    def _draw_all(self):
        self.cv.delete("all")
        cs=self.cell
        for r in range(self.rows):
            for c in range(self.cols):
                x=c*cs; y=r*cs
                # Warna sel
                if [r,c]==self.player:
                    fill=CLR_PATH
                elif r==0 and c==0:
                    fill="#0a3a1a"
                elif r==self.rows-1 and c==self.cols-1:
                    fill="#3a0a10"
                elif (r,c) in self.trail:
                    fill=CLR_TRAL
                else:
                    fill=CLR_PATH
                self.cv.create_rectangle(x,y,x+cs,y+cs,fill=fill,outline="")

                # Dinding
                wt=max(1,cs//6)
                if N not in self.pas[r][c]:
                    self.cv.create_line(x,y,x+cs,y,fill=CLR_WALL,width=wt)
                if S not in self.pas[r][c]:
                    self.cv.create_line(x,y+cs,x+cs,y+cs,fill=CLR_WALL,width=wt)
                if W not in self.pas[r][c]:
                    self.cv.create_line(x,y,x,y+cs,fill=CLR_WALL,width=wt)
                if E not in self.pas[r][c]:
                    self.cv.create_line(x+cs,y,x+cs,y+cs,fill=CLR_WALL,width=wt)

        # Label S dan E
        if cs>=14:
            self.cv.create_text(cs//2, cs//2, text="S",
                fill=CLR_STAR, font=("Consolas",max(8,cs//3),"bold"))
            self.cv.create_text((self.cols-1)*cs+cs//2,(self.rows-1)*cs+cs//2,
                text="E", fill=CLR_END, font=("Consolas",max(8,cs//3),"bold"))

        # Titik pemain
        pr,pc=self.player
        px=pc*cs+cs//2; py=pr*cs+cs//2
        rad=max(3,cs//2-max(2,cs//6))
        self.cv.create_oval(px-rad,py-rad,px+rad,py+rad,
                            fill=CLR_PLAY, outline="white", width=max(1,cs//10))

        # Update header & footer
        elapsed=int(time.time()-self.t0)
        self.hdr.config(text=f"Labirin {self.rows}×{self.cols}  |  "
                             f"Kerumitan: {self.cmplx}/10  |  "
                             f"Langkah: {self.moves}  |  Waktu: {elapsed}s")
        if self.won:
            self.ftr.config(
                text=f"★ SELESAI! {self.moves} langkah, {elapsed}s  |  R = labirin baru  |  ESC = keluar",
                fg=CLR_DONE, font=("Consolas",11,"bold"))
        else:
            st="[AUTO BERJALAN]" if self.solving else "[PAUSE]"
            self.ftr.config(
                text=f"{st}  |  SPASI=pause/lanjut  WASD/↑↓←→=manual  R=baru  ESC=keluar",
                fg="#777")

    def _key(self, e):
        k=e.keysym
        if k=="Escape":
            self.root.destroy()
            root2=tk.Tk(); MenuScreen(root2); root2.mainloop()
            return
        if k=="r" or k=="R":
            self._new_game(); return
        if k=="space":
            if not self.won:
                self.solving=not self.solving
                if self.solving:
                    delay=max(30,260-self.cmplx*20)
                    self._tick(delay)
            return
        if self.solving or self.won: return
        move={
            "Up":(-1,0),"Down":(1,0),"Left":(0,-1),"Right":(0,1),
            "w":(-1,0),"s":(1,0),"a":(0,-1),"d":(0,1),
            "W":(-1,0),"S":(1,0),"A":(0,-1),"D":(0,1),
        }.get(k)
        if move:
            dr,dc=move
            dir_key={((-1,0)):N,((1,0)):S,((0,1)):E,((0,-1)):W}[move]
            if dir_key in self.pas[self.player[0]][self.player[1]]:
                self.player[0]+=dr; self.player[1]+=dc; self.moves+=1
                if self.player==[self.rows-1,self.cols-1]: self.won=True
                self._draw_all()

# ── Versi Simpel ──────────────────────────────────────────────────────────────
class SimpleGame:
    def __init__(self, root):
        root.update_idletasks()
        sh=root.winfo_screenheight()-140; sw=root.winfo_screenwidth()-80
        rows=min(28,max(6, sh//20))
        cols=min(48,max(6, sw//20))
        cmplx=random.randint(5,10)   # kerumitan pure random
        MazeCanvas(root, rows, cols, cmplx, "Labirin Acak — Simpel")

# ── Versi Custom: setup ───────────────────────────────────────────────────────
class CustomSetup:
    def __init__(self, root):
        self.root=root
        root.title("Labirin Custom — Pengaturan")
        root.configure(bg=BG)
        root.resizable(False,False)
        sw=root.winfo_screenwidth(); sh=root.winfo_screenheight()
        w,h=420,380
        root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self._build()

    def _build(self):
        f=tk.Frame(self.root,bg=BG,padx=30,pady=20); f.pack(fill="both",expand=True)

        tk.Label(f,text="PENGATURAN LABIRIN",font=("Consolas",18,"bold"),
                 bg=BG,fg=CLR_PLAY).pack(pady=(0,20))

        self.vars={}
        fields=[
            ("Jumlah Baris",  "rows",  "15", 5, 40),
            ("Jumlah Kolom",  "cols",  "20", 5, 60),
            ("Kerumitan",     "cmplx", "7",  1, 10),
        ]
        for lbl,key,default,mn,mx in fields:
            row=tk.Frame(f,bg=BG); row.pack(fill="x",pady=6)
            tk.Label(row,text=f"{lbl} ({mn}–{mx})",width=20,anchor="w",
                     font=("Consolas",11),bg=BG,fg="#aaa").pack(side="left")
            var=tk.StringVar(value=default)
            self.vars[key]=(var,mn,mx)
            e=tk.Entry(row,textvariable=var,width=6,font=("Consolas",13,"bold"),
                       bg="#1a1a2a",fg="white",insertbackground="white",
                       relief="flat",bd=4)
            e.pack(side="left",padx=8)
            # Slider
            sl=tk.Scale(row,from_=mn,to=mx,orient="horizontal",
                        variable=tk.IntVar(),
                        bg=BG,fg="#555",troughcolor="#1a1a2a",
                        highlightthickness=0,bd=0,showvalue=False,
                        length=120,
                        command=lambda v,var=var: var.set(str(int(float(v)))))
            sl.set(int(default))
            sl.pack(side="left")

        self.err=tk.Label(f,text="",font=("Consolas",10),bg=BG,fg=CLR_END)
        self.err.pack(pady=4)

        tk.Button(f,text="▶  MULAI LABIRIN",
                  font=("Consolas",13,"bold"),
                  bg="#0a3a2a",fg=CLR_STAR,
                  activebackground="#0d5a40",activeforeground="white",
                  relief="flat",bd=0,padx=10,pady=12,cursor="hand2",
                  command=self._start).pack(fill="x",pady=(8,0))

        tk.Label(f,text="Titik biru bergerak otomatis — SPASI pause/lanjut",
                 font=("Consolas",9),bg=BG,fg="#444").pack(pady=(10,0))

    def _start(self):
        try:
            vals={}
            for key,(var,mn,mx) in self.vars.items():
                v=int(var.get())
                if not (mn<=v<=mx): raise ValueError(f"{key} harus {mn}-{mx}")
                vals[key]=v
        except ValueError as ex:
            self.err.config(text=str(ex)); return
        self.root.destroy()
        root2=tk.Tk()
        MazeCanvas(root2,vals["rows"],vals["cols"],vals["cmplx"],"Labirin Custom")
        root2.mainloop()

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__=="__main__":
    root=tk.Tk()
    MenuScreen(root)
    root.mainloop()
