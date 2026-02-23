Hash Table — Analogi Parkiran Mobil 🚗
Hash Table itu seperti gedung parkir dengan 20 slot bernomor. 
Setiap mobil punya nomor plat, dan kita pakai rumus hash(nomor_plat) % 20 untuk menentukan slot parkirnya.
Misalnya mobil "B 1234 ABC" menghasilkan angka 47, maka 47 % 20 = 7, artinya mobil itu parkir di slot 7.
Masalah muncul ketika slot sudah terisi, yang disebut collision. 
Solusinya adalah Linear Probing — geser ke slot berikutnya sampai ketemu yang kosong.
Kalau slot 7 penuh, coba slot 8, kalau masih penuh coba slot 9, dan seterusnya.
Kode ini memvisualisasikan proses tersebut secara animasi. 
Alurnya ada 5 fase: START (mobil datang dan hitung slot tujuan),
COLLISION (slot penuh), PROBE (geser ke slot berikutnya), PLACE (berhasil parkir), dan PAUSE (tampilkan hasilnya sebentar).
Ada juga indikator Load Factor yang menunjukkan tingkat kepenuhan parkiran.
Rumusnya adalah jumlah slot terisi dibagi total slot. 
Load factor 0.3 berarti parkiran masih sepi, 0.7 mulai ramai dan susah cari slot, sedangkan 0.9 ke atas berarti hampir penuh dan antri panjang.
Animasi ini bisa dikontrol dengan keyboard: SPACE untuk pause/resume,
tombol panah kanan-kiri untuk maju-mundur langkah (saat pause), R untuk mengulang dari awal, dan Q atau ESC untuk keluar.
Intinya, Hash Table adalah cara komputer menyimpan data secara efisien — persis seperti sistem parkir otomatis yang mencari slot kosong dengan cepat dan teratur.
