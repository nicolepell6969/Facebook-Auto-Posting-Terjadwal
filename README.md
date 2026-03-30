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

# ===================== KONFIGURASI UMUM =====================

COOKIE_FILE = "cookies.json" # cookies ambil untuk login auth
HISTORY_FILE = "history.json" # history posting agar tidak double post teks dan media yang sama
TEXTS_FILE = "texts.txt" # opsi isi teks untuk caption jika tidak pakai api AI
MEDIA_DIR = "media" # list foto / video untuk di unggah jika hanya teks saja kosongkan

SCHEDULE = ["05:40", "15:00", "21:00"] # jadwal waktu untuk posting bisa di tambah

# ===================== KONFIGURASI AI =======================

# Masukkan API Key Gemini Anda di bawah ini
GEMINI_API_KEY = "API-KEY-GEMINI" 



## ⚙️ Persyaratan Sistem

1. Python 3.8 atau lebih baru.
2. Google Chrome terinstal di sistem / VPS.
   - *Untuk Ubuntu/Debian:* `sudo apt update && sudo apt install google-chrome-stable`
3. Akun Facebook aktif dengan *cookies* yang sudah diekspor.
