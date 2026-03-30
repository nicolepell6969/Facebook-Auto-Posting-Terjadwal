# 🚀 FB Auto Poster Feat AI GEMINI

Script otomatisasi (Bot) berbasis Python CLI untuk memposting status dan media (foto/video) ke Facebook secara terjadwal. Sangat cocok dijalankan di VPS (Virtual Private Server) Linux sebagai *Social Media Manager* autopilot Anda yang beroperasi 24/7.

Dilengkapi dengan integrasi **Google Gemini AI** untuk menghasilkan *caption* yang unik, natural, dan menyesuaikan dengan waktu (pagi/siang/sore/malam) secara otomatis untuk menghindari deteksi *spam* Facebook.

---

## ✨ Fitur Utama

- **🧠 AI Caption Generator**: Membuat caption unik secara otomatis menggunakan Gemini AI sesuai dengan waktu sistem (sapaan pagi/siang/sore/malam).
- **📸 Auto-Media Upload**: Mengambil foto/video secara acak dari folder lokal (`media/`) untuk dipasangkan dengan caption.
- **🛡️ Anti-Spam History**: Mencatat konten teks manual dan media yang sudah diposting ke dalam `history.json` agar tidak terjadi *double-post*.
- **☁️ VPS Ready (Headless)**: Dikonfigurasi khusus agar berjalan mulus di *background* VPS Linux tanpa memerlukan tampilan GUI/Desktop (Anti-Crash, `--no-sandbox`).
- **🔍 Auto-Detect Chrome Version**: Otomatis menyesuaikan versi `undetected-chromedriver` dengan Google Chrome yang terinstal di sistem VPS untuk mencegah error *SessionNotCreatedException*.
- **🖥️ Pro CLI UI**: Tampilan log terminal yang profesional, rapi, dan menggunakan kode warna ANSI agar mudah dipantau.
- **📝 Manual Fallback**: Jika API Key AI kosong atau *error*, bot otomatis mengambil teks manual yang sudah Anda siapkan dari file `texts.txt`.

---

## ⚙️ Konfigurasi (`main.py`)

Sebelum menjalankan bot, Anda dapat menyesuaikan pengaturan utama di dalam file `main.py`. Berikut adalah blok konfigurasi yang tersedia beserta penjelasan fungsi dari masing-masing variabel:

```python
# ===================== KONFIGURASI UMUM =====================

COOKIE_FILE  = "cookies.json"  # Cookies akun untuk login (Autentikasi)
HISTORY_FILE = "history.json"  # Riwayat postingan (Anti-Spam / Anti-Double Post)
TEXTS_FILE   = "texts.txt"     # Daftar teks/caption manual (Fallback AI)
MEDIA_DIR    = "media"         # Folder penyimpanan file foto/video

SCHEDULE     = ["05:40", "15:00", "21:00"] # Jadwal eksekusi posting (Format 24 Jam)

# ===================== KONFIGURASI AI =======================

# Masukkan API Key Gemini Anda di bawah ini
GEMINI_API_KEY = "API-KEY-GEMINI"


📝 Penjelasan Detail Fungsi Variabel:

    COOKIE_FILE ("cookies.json")
    Berfungsi sebagai kunci masuk (autentikasi) ke akun Facebook Anda. Menggunakan cookies jauh lebih aman daripada menggunakan kombinasi email dan password, serta meminimalisir risiko akun terkena checkpoint atau pemblokiran oleh Facebook. Pastikan file ini berada di folder yang sama dengan script.

    HISTORY_FILE ("history.json")
    Sistem cerdas bot untuk merekam jejak aktivitas. Setiap kali bot berhasil memposting teks atau media, datanya akan dicatat di file ini. Ini memastikan bot tidak akan pernah memposting teks atau media yang sama dua kali. (Tips: Hapus file ini jika Anda ingin mengulang siklus postingan dari awal).

    TEXTS_FILE ("texts.txt")
    File sumber yang berisi kumpulan status/caption manual buatan Anda. Bot akan mengambil teks secara acak dari file ini jika Anda memutuskan untuk tidak memakai AI, atau jika kuota/server API Gemini sedang mengalami gangguan (fallback mechanism). Pisahkan setiap status di file ini menggunakan baris kosong (Enter 2x).

    MEDIA_DIR ("media")
    Direktori tempat Anda menyimpan seluruh stok konten visual (foto/video). Bot akan memilih satu file secara acak dari folder ini untuk diunggah bersamaan dengan caption. Jika Anda hanya ingin bot memposting teks/status biasa, biarkan folder ini kosong.

    SCHEDULE
    Daftar waktu atau jadwal kapan bot harus mulai bekerja. Gunakan format waktu 24 jam (contoh: 05:40, 15:00). Anda bebas menambahkan, mengurangi, atau mengubah jam tayang sesuai dengan jam ramai (prime time) audiens Anda. Pastikan jadwal ini disesuaikan dengan zona waktu VPS/Server Anda.

    GEMINI_API_KEY
    Fitur Autopilot AI. Jika Anda memasukkan kunci rahasia dari Google AI Studio di sini, bot akan secara otomatis memproduksi caption unik yang disesuaikan dengan waktu (pagi/siang/sore/malam). Jika variabel ini dibiarkan kosong (""), modul AI akan dinonaktifkan dan bot beralih ke mode manual (menggunakan TEXTS_FILE).
