# Pygame Snake Modern (Snake & Apple)

Game klasik Snake (Ular Makan Apel) yang diimplementasikan menggunakan Python dan pustaka **Pygame** dengan visual modern, desain berpola *checkerboard*, antarmuka skor elegan, serta pergerakan ular yang mulus.

---

## 🎮 Fitur Permainan

- **Desain Visual Modern:**
  - Latar belakang arena bermain dengan pola kotak-kotak (*checkerboard grid*) bernuansa tema gelap (*dark theme*).
  - Kepala ular memiliki mata yang otomatis menghadap sesuai arah jalan.
  - Badan ular memiliki sudut tumpul (*border radius*) dengan efek ruas terpisah.
  - Apel digambar lengkap dengan efek kilau (*highlight*) dan daun.
- **Sistem UI & Skor:**
  - Header panel terpisah di bagian atas untuk menampilkan skor saat ini (`APEL`) dan skor tertinggi sesi (`BEST`).
- **Pencegahan Bug Arah:**
  - Menggunakan sistem penyangga arah (`next_dir`) untuk mencegah pemain berbalik arah $180^\circ$ secara instan yang biasanya memicu *self-collision* tidak sengaja.
- **Layar Game Over & Reset Cepat:**
  - Layar transparan redup (*semi-transparent overlay*) saat kalah.
  - Tombol pintas untuk langsung memulai ulang permainan tanpa harus membuka ulang aplikasi.

---

## 📋 Prasyarat

Pastikan komputer Anda telah terinstal:
- **Python 3.8+**
- Pustaka **Pygame**

### Instalasi Dependensi
Jalankan perintah berikut di terminal / command prompt:
```bash
pip install pygame
```

---

## 🚀 Cara Menjalankan

1. Buka terminal dan arahkan ke direktori proyek:
   ```bash
   cd "D:\ALL CODE\Personal\snake_apple"
   ```
2. Jalankan skrip Python:
   ```bash
   python snake_apple.py
   ```

---

## 🕹️ Kontrol Permainan

| Tombol | Aksi |
| :--- | :--- |
| `↑` (Panah Atas) | Bergerak ke Atas |
| `↓` (Panah Bawah) | Bergerak ke Bawah |
| `←` (Panah Kiri) | Bergerak ke Kiri |
| `→` (Panah Kanan) | Bergerak ke Kanan |
| `SPASI` | Mengulang permainan setelah Game Over |
| `Esc` / Tutup Jendela | Keluar dari permainan |

---

## 🧠 Penjelasan Arsitektur & Logika Kode (`snake_apple.py`)

Skrip [snake_apple.py](file:///D:/ALL%20CODE/Personal/snake_apple/snake_apple.py) memiliki alur kerja yang terstruktur dan mudah dipelajari:

### 1. Inisialisasi & Konstanta (Baris 1–32)
- **Dimensi Layar:** 
  - Lebar: `400px`
  - Tinggi total: `460px` (termasuk `HEADER_HEIGHT = 60px` untuk area informasi skor, menyisakan `400x400px` untuk arena bermain).
  - Ukuran grid: `GRID_SIZE = 20px`, membentuk matriks 20 x 20 petak bermain.
- **Kecepatan (`FPS = 10`):** Mengatur kecepatan gerak ular sebanyak 10 langkah per detik.
- **Palet Warna:** Menggunakan perpaduan warna modern (Slate/Dark Gray, Emerald Green, Vibrant Red, dan Gold).

### 2. State & Data Game (Baris 33–41)
- `snake`: List koordinat `(x, y)` yang merepresentasikan ruas tubuh ular. Elemen indeks `0` adalah kepala ular.
- `snake_dir` & `next_dir`: Vektor pergeseran `(dx, dy)` yang menentukan arah gerak ular pada setiap *tick*.
- `score` & `high_score`: Menyimpan jumlah apel yang berhasil dimakan serta rekor tertinggi selama aplikasi aktif.
- `game_over`: Status penanda apakah pemain kalah.

### 3. Fungsi-Fungsi Utama
- **`spawn_food()` (Baris 42–49):**
  - Mengacak koordinat `(x, y)` baru kelipatan `GRID_SIZE` di dalam batas arena bermain (`HEADER_HEIGHT` hingga `HEIGHT`).
  - Memastikan apel tidak muncul tepat di atas koordinat tubuh ular (`if (x, y) not in snake`).
- **`reset_game()` (Baris 51–59):**
  - Mengembalikan ular ke posisi tengah awal, mengosongkan arah gerak, mereset skor, memunculkan apel baru, dan menonaktifkan status `game_over`.
- **`draw_grid()` (Baris 60–68):**
  - Menggambar pola papan catur bergantian antara `BG_COLOR_1` dan `BG_COLOR_2` untuk mempermudah pemain memperkirakan jarak dan baris petak.
- **`draw_snake()` (Baris 69–98):**
  - Menggambar kepala dengan sudut membulat (`border_radius=6`).
  - Menghitung posisi pupil mata ular berdasarkan arah pergerakan `snake_dir`.
  - Menggambar ruas badan yang sedikit diperkecil (`rect.inflate(-2, -2)`) agar memberikan efek ruas bersambung.
- **`draw_apple()` (Baris 99–108):**
  - Menggambar lingkaran buah merah, titik pantulan cahaya putih-merah muda, serta elips daun hijau di atasnya.
- **`draw_ui()` (Baris 109–120):**
  - Menggambar latar panel header gelap dan garis pemisah.
  - Merender teks skor saat ini dan skor tertinggi (*High Score* berwarna emas).
- **`draw_game_over()` (Baris 121–133):**
  - Membuat `Surface` dengan transparansi alpha (`SRCALPHA`) untuk meredupkan tampilan arena.
  - Menampilkan teks merah besar **"GAME OVER"** dan instruksi untuk menekan tombol **SPASI**.

### 4. Game Loop Utama (Baris 135–188)
Siklus permainan berjalan berulang kali setiap frame dengan 3 tahapan:
1. **Event Handling (Input):**
   - Mendeteksi penutupan jendela (`pygame.QUIT`).
   - Menerima tombol panah untuk mengubah `next_dir` (dibatasi agar pemain tidak bisa langsung memutar arah $180^\circ$ berlawanan dengan arah gerak saat ini).
   - Menangkap tombol `SPASI` saat kondisi `game_over` untuk memanggil `reset_game()`.
2. **Game Logic Update:**
   - Menghitung koordinat kepala baru: `head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])`.
   - Menambahkan kepala baru ke depan list (`snake.insert(0, head)`).
   - Memeriksa tabrakan dengan apel menggunakan `colliderect`. Jika kena apel, skor bertambah dan apel baru di-*spawn*; jika tidak, ujung ekor dibuang (`snake.pop()`) agar panjang ular tetap.
   - Memeriksa tabrakan batas luar (dinding) dan tabrakan kepala dengan badan sendiri (`head in snake[1:]`). Jika bertabrakan, status berubah menjadi `game_over = True`.
3. **Render & Refresh:**
   - Menggambar ulang grid, apel, ular, UI, dan overlay Game Over (jika kalah).
   - Memperbarui tampilan layar dengan `pygame.display.flip()`.
   - Mengontrol waktu jeda per frame dengan `clock.tick(FPS)`.

---

## 💡 Ide Pengembangan Lanjutan

Jika ingin mengembangkan fitur lebih lanjut pada proyek ini, berikut beberapa ide yang dapat ditambahkan:
1. **Kecepatan Dinamis (*Difficulty Scaling*):** Tingkatkan nilai `FPS` secara bertahap seiring bertambahnya skor.
2. **Penyimpanan Rekor Permanen (*Persistent High Score*):** Simpan skor tertinggi ke dalam berkas teks atau JSON (`high_score.json`).
3. **Efek Suara (*Sound Effects*):** Tambahkan suara saat memakan apel menggunakan `pygame.mixer.Sound`.
4. **Variasi Apel Spesial:** Tambahkan apel emas bernilai poin ganda atau apel racun yang mengurangi panjang tubuh ular.
