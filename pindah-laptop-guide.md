# Panduan Instalasi & Konfigurasi Bot di Laptop Baru

Dokumen ini berisi panduan langkah demi langkah untuk memindahkan dan menjalankan **Web Chatbot (HTML)** dan **Telegram Bot (Python)** di laptop lain. Karena kamu akan menggunakan akun Antigravity yang berbeda, hal utama yang harus diubah adalah **API Key**.

---

## Tahap 1: Persiapan File
Pindahkan file berikut ini dari laptop lamamu ke laptop baru (bisa pakai flashdisk, Google Drive, dsb):
1. `chatbot-antigravity.html`
2. `bot.py`

---

## Tahap 2: Buka dan Jalankan Antigravity Tools di Laptop Baru

1. Buka terminal/Command Prompt di laptop baru.
2. Jalankan perintah instalasi Antigravity (jika belum terinstal). Jika sudah, langsung jalankan:
   ```bash
   antigravity start
   ```
3. Saat server Antigravity berjalan, ia akan menampilkan alamat lokal (biasanya `http://127.0.0.1:8045`) beserta **API Key** akunmu di terminal.
4. **Copy / Catat API Key** tersebut. Bentuknya biasanya berawalan `sk-...` (contoh: `sk-1234abcd5678efgh`).

---

## Tahap 3: Update API Key pada File HTML

1. Buka file `chatbot-antigravity.html` menggunakan Text Editor (Notepad, VS Code, Sublime, dll).
2. Scroll ke bagian skrip Javascript di baris sekitar 480+. Cari blok konfigurasi berikut:
   ```javascript
   const CONFIG = {
     baseUrl: 'http://127.0.0.1:8045',
     apiKey:  'sk-ganti-dengan-api-key-yang-baru',  // <--- UBAH DI SINI
     maxHistory: 8,
     ...
   ```
3. Ganti teks `apiKey` lama dengan API Key yang baru kamu salin dari Antigravity di laptop tersebut.
4. Simpan file (`Ctrl + S`).
5. Klik ganda (double-click) file `chatbot-antigravity.html` untuk membukanya di browser Google Chrome / Safari.
6. Coba tes chat untuk memastikan sudah tersambung!

---

## Tahap 4: Update API Key pada File Telegram Bot (bot.py)

1. Buka file `bot.py` menggunakan Text Editor.
2. Di bagian atas (sekitar baris ke-6 sampai ke-10), cari konfigurasi berikut:
   ```python
   # ── KONFIGURASI ──────────────────────────────────────────────
   TOKEN        = "8009319057:AAHGaZIOU1hnAC_tkVWFwBxAiqnnIAewZW8"
   ANTIGRAVITY_URL = "http://127.0.0.1:8045"
   API_KEY      = "sk-ganti-dengan-api-key-yang-baru" # <--- UBAH DI SINI
   MAX_HISTORY  = 8
   ```
3. Ganti `API_KEY` lama dengan API Key baru di laptop tersebut. *(Catatan: Nilai `TOKEN` Telegram tidak perlu diubah, kecuali kamu membuat bot Telegram baru di BotFather).*
4. Simpan file (`Ctrl + S`).

---

## Tahap 5: Instalasi Dependensi Python & Menjalankan Bot Tele

Karena ini di laptop baru, kamu harus menginstal library Python yang dibutuhkan agar file `bot.py` bisa berjalan.

1. Buka terminal atau Command Prompt.
2. Arahkan ke folder tempat kamu menyimpan `bot.py` (contoh: `cd Downloads`).
3. Ketik perintah berikut lalu tekan Enter untuk menginstal pustaka (library):
   ```cmd
   pip install pyTelegramBotAPI requests
   ```
4. Jika instalasi sukses, jalankan bot dengan perintah:
   ```cmd
   python bot.py
   ```
5. Jika keluar tulisan `✅ mas_dewa_bot berjalan dengan fitur Multi-Model UI...`, berarti bot kamu sudah aktif!

---

## Troubleshooting Cepat

* **Muncul Error `ConnectionError: Tidak bisa terhubung...` di bot tele:** Pastikan terminal yang menjalankan `antigravity start` masih terbuka dan aktif.
* **HTML muncul alert error merah:** Pastikan kamu tidak tidak sengaja menghapus tanda kutip tunggal (`'`) saat mengganti API Key di `chatbot-antigravity.html`.
* **Bot Tele diam saja saat dikirim pesan:** Pastikan terminal yang menjalankan `python bot.py` di laptop tersebut tidak tertutup atau *sleep*.
