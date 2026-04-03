# 🚀 FB Auto Poster Feat AI GEMINI (Web UI Edition)

Bot otomatisasi berbasis Python yang mengotomatiskan posting status teks dan media (foto/video) ke beranda Facebook secara terjadwal. Sangat cocok dijalankan di VPS (Virtual Private Server) Windows/Linux atau komputer pribadi sebagai *Social Media Manager autopilot* yang beroperasi 24/7.

Kini, bot beroperasi secara penuh di belakang layar *(background)* dan dikendalikan melalui sebuah **Web Dashboard berdesain Modern Premium**. Aplikasi ini juga dilengkapi integrasi cerdas dari **Google Gemini AI** untuk menghasilkan status yang paling *relate* secara dinamis menyesuaikan suasana dan waktu setempat.

---

## ✨ Fitur Utama (Pembaruan Versi Web)

- 🌐 **Dashboard UI Premium**: Anda tidak lagi memelototi terminal teks hitam yang membosankan. Kendalikan segala sesuatunya di jendela peramban (*browser*) yang dirancang sangat anggun dengan tema *Dark Mode Window/Glassmorphism*.
- ⏸️ **Sistem Start/Stop Automation (Scheduler)**: Bot bisa dikendalikan kapanpun untuk jeda (*Pause*) dan mulai kembali (*Resume*) mem-posting berbekal integrasi mulus menggunakan library `APScheduler`. Tinggalkan penjadwalan kuno `time.sleep()`.
- 🖼️ **Manajemen Multimedia Bawaan**: Mendukung galeri dan fasilitas fitur **Drag & Drop Upload**. Anda dapat menaruh semua aset kampanye (foto & video) melalui panel tanpa melacak folder server. 
- 🤖 **AI Prompt Awarness & Pengaturan Kustom**: Masukkan API Gemini milik Anda di Dashboard. Jika koneksi API habis (*limit*), bot secara diam-diam akan mengalihkan postingannya menggunakan **Teks Manual (Fallback)** yang juga dapat diedit dari Dashboard.
- 🍪 **Manajemen Session via Cookies**: Mengubah *Cookies JSON Login Facebook* sangat mudah pakai input tabel. Mode *headless* dengan User-Agent Desktop modern dijamin akan selalu aman dari pemeriksaan Anti-Bot (seperti *Checkpoint/Captcha/Verifikasi 2 Langkah*).
- 📸 **Auto-Detect Windows/Linux Chrome & Debug Screenshot**: Auto-mendownload ChromeDriver versi paling pas. Bila bot kebingungan menemukan *form update status*, akan ada fitur Tangkap Layar ke error otomatis bernama `debug_error.png` yang siap diperiksa!

---

## 🛠️ Instalasi

1. Pastikan Anda sudah mempunyai Python terpasang (disarankan versi 3.10 ke atas) dan Google Chrome *(browser)* standar.
2. Lakukan clone ke repository ini:
   ```bash
   git clone https://github.com/nicolepell6969/Facebook-Auto-Posting-Terjadwal.git
   cd Facebook-Auto-Posting-Terjadwal
   ```
3. Unduh seluruh komponen program tambahan (*requirements/library*):
   ```bash
   pip install flask apscheduler werkzeug undetected_chromedriver fake_useragent selenium google-generativeai
   ```

## 🚀 Cara Penggunaan

Penggunaan bot telah dialihkan sepenuhnya menggunakan peladen Flask:

1. Nyalakan sistem inti peladen dengan perintah:
   ```bash
   python app.py
   ```
2. Terminal akan memunculkan informasi URL lokal. Apabila berhasil, silakan buka peramban dan meluncur ke tautan di bawah ini:
   👉 **`http://127.0.0.1:5000/`**
3. Lakukan pengaturan pertama Anda pada bagian:
   - **Session Cookies**: Paste kode cookie akun Facebook Anda dari add-on *EditThisCookie* ke tabel Cookies.
   - **Teks Manual**: Isi beberapa status jika layanan AI Anda ditangguhkan.
   - **Schedule & AI**: Pasang API Key *Gemini* (Opsional), kemudian atur daftar jam.
4. Terakhir, klik **[Start Automation]** di pojok kanan atas Dashboard.  Anda juga dapat melakukan uji coba pertunjukan sekejap menekan lambang pelatuk kecil **[Petir (⚡)]** untuk mengeksekusi bot sekarang juga secara *Realtime*.

---

*Hak Cipta Repository Asli dan Modifikasi Dilindungi.*
