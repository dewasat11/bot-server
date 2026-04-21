import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time
import os
from datetime import datetime
from openai import OpenAI

# ── KONFIGURASI ──────────────────────────────────────────────
TOKEN        = "8009319057:AAHGaZIOU1hnAC_tkVWFwBxAiqnnIAewZW8"
ANTIGRAVITY_URL = "http://127.0.0.1:8045/v1"
API_KEY      = "sk-1de606aad7c241bdac511958f7853b6e"
MAX_HISTORY  = 8

# Inisialisasi OpenAI Client
client = OpenAI(base_url=ANTIGRAVITY_URL, api_key=API_KEY)

SYSTEM_PROMPT = (
    "Kamu AI serba bisa (mas_dewa_bot). Jawab informatif, padat, natural. "
    "Bahas apa saja (sains, sejarah, dll) menyesuaikan gaya bahasa user. "
    "PENTING: Jawab Teks Biasa TANPA markdown (*bold*, _italic_, #) sama sekali. "
    "Jika tidak tahu, jujur saja. Jangan kepanjangan."
)

MODELS_PRIORITY = ["claude-sonnet-4-6", "gemini-3-flash", "gpt-oss-120b-medium"]

# ── DATABASE ────────────────────────────────────────────────
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {"histories": {}, "facts": {}}
    return {"histories": {}, "facts": {}}

def save_data():
    data = {"histories": chat_histories, "facts": user_facts}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

db = load_data()
chat_histories = db.get("histories", {})
user_facts = db.get("facts", {})

bot = telebot.TeleBot(TOKEN)

def get_time_context():
    now = datetime.now()
    hour = now.hour
    if 5 <= hour < 11: return "Pagi"
    elif 11 <= hour < 15: return "Siang"
    elif 15 <= hour < 18: return "Sore"
    else: return "Malam"

def get_history(chat_id):
    cid = str(chat_id)
    if cid not in chat_histories:
        chat_histories[cid] = []
    return chat_histories[cid]

def trim_history(chat_id):
    cid = str(chat_id)
    h = chat_histories.get(cid, [])
    if len(h) > MAX_HISTORY:
        chat_histories[cid] = h[-MAX_HISTORY:]


def ask_ai(chat_id, user_text, user_name="User"):
    history = get_history(chat_id)
    history.append({"role": "user", "content": user_text})
    trim_history(chat_id)
    
    # Konteks Waktu & Fakta
    waktu = get_time_context()
    cid = str(chat_id)
    fakta = user_facts.get(cid, "Belum ada fakta khusus.")
    
    dynamic_system = (
        f"{SYSTEM_PROMPT}\n\n"
        f"[KONTEKS SAAT INI]\n"
        f"- Waktu: Selamat {waktu} (Jam {datetime.now().strftime('%H:%M')})\n"
        f"- Nama User: {user_name}\n"
        f"- Fakta User: {fakta}\n\n"
        "PENTING: Gunakan fakta di atas jika relevan untuk membuat percakapan lebih akrab. "
        "Jika user memberi tahu fakta baru tentang dirinya, ingatlah baik-baik."
    )

    # Looping melalui daftar model prioritas (Failover)
    for model_id in MODELS_PRIORITY:
        print(f"   [AI] Mencoba model: {model_id}...")
        
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # Menggunakan library OpenAI (Chat Completions)
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": dynamic_system},
                        *history
                    ],
                    max_tokens=600,
                    timeout=45
                )
                
                reply = response.choices[0].message.content
                
                if not reply:
                    print(f"      ! {model_id} memberikan jawaban kosong.")
                    break

                # Berhasil! Simpan ke history dan database
                history.append({"role": "assistant", "content": reply})
                save_data()
                
                return reply.replace("**", "").replace("*", "")

            except Exception as e:
                err_msg = str(e).lower()
                print(f"      ! Error pada {model_id}: {err_msg}")
                
                # Jika error 503 atau overloaded, coba lagi atau ganti model
                if "503" in err_msg or "overloaded" in err_msg:
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        print(f"      ! Mencoba model cadangan...")
                        break 
                else:
                    # Error lain (misal 401), langsung coba model lain
                    break

    return "⚠ Semua model sedang sibuk saat ini. Mohon coba beberapa saat lagi."

# ── HANDLERS ─────────────────────────────────────────────────
@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    chat_histories[message.chat.id] = []   # reset history tiap kali /start
    
    first_name = message.from_user.first_name or "Pengguna"
    
    txt = (
        f"Halo {first_name}! Saya mas_dewa — asisten AI kamu!\n\n"
        "Ketik apa saja untuk mulai mengobrol. Saya akan menjawab secepat kilat! ⚡"
    )
    bot.reply_to(message, txt)


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    cid = str(message.chat.id)
    chat_histories[cid] = []
    save_data()
    bot.reply_to(message, "✅ Riwayat percakapan telah direset. Mulai percakapan baru!")




@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if not message.text:
        bot.reply_to(message, "Maaf, saya hanya bisa memproses pesan teks.")
        return

    # Tampilkan indikator "sedang mengetik..."
    bot.send_chat_action(message.chat.id, "typing")
    
    first_name = message.from_user.first_name or "Pengguna"
    reply = ask_ai(message.chat.id, message.text, first_name)
    bot.reply_to(message, reply)

# ── START ─────────────────────────────────────────────────────
print(f"✅ mas_dewa_bot AKTIF (Mode: Aware & Failover)")
print(f"   Model Utama : {MODELS_PRIORITY[0]}")
print(f"   URL Server  : {ANTIGRAVITY_URL}")
print("   Bot siap melayani di Telegram. Tekan Ctrl+C untuk berhenti.\n")
bot.infinity_polling()
