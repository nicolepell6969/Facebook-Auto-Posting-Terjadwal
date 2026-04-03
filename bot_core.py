import time, json, os, random, subprocess, re
from datetime import datetime

import undetected_chromedriver as uc
from fake_useragent import UserAgent

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import google.generativeai as genai

# ===================== KONFIGURASI UMUM =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_FILE = os.path.join(BASE_DIR, "cookies.json")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
TEXTS_FILE = os.path.join(BASE_DIR, "texts.txt")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
LOG_FILE = os.path.join(BASE_DIR, "app.log")

# ===================== UI & LOGGING =====================

class LogColor:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'

def log(level, message):
    ts = datetime.now().strftime("%H:%M:%S")
    
    if level == "INFO": prefix = f"[*] INFO   "
    elif level == "SUCCESS": prefix = f"[+] SUCCESS"
    elif level == "WARNING": prefix = f"[!] WARNING"
    elif level == "ERROR": prefix = f"[x] ERROR  "
    elif level == "WAIT": prefix = f"[~] WAIT   "
    elif level == "SKIP": prefix = f"[-] SKIP   "
    elif level == "AI": prefix = f"[✦] GEMINI "
    else: prefix = f"[*] {level.ljust(7)}"

    log_entry = f"[{ts}] {prefix} | {message}"
    print(log_entry)
    
    # Save to file for Web UI
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except:
        pass

def log_separator():
    msg = "---------------------------------------------------------"
    print(msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except: pass

# ===================== INIT FOLDER & FILE =====================

if not os.path.exists(TEXTS_FILE):
    with open(TEXTS_FILE, "w", encoding="utf-8") as f:
        f.write("Status otomatis pertama 🚀\n\nStatus kedua nih, cek profil ya!\n\nSelamat pagi semuanya!")
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# ===================== UTILS =====================

def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"gemini_api_key": "", "schedule": []}

def sanitize_text(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def human_type(el, text):
    safe_text = sanitize_text(text)
    for c in safe_text:
        el.send_keys(c)
        time.sleep(random.uniform(0.05, 0.15))

def get_chrome_major_version():
    if os.name == 'nt':
        import winreg
        try:
            # Check current user registry
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return int(version.split('.')[0])
        except Exception:
            try:
                # Check local machine registry
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome")
                version, _ = winreg.QueryValueEx(key, "version")
                return int(version.split('.')[0])
            except Exception:
                pass
                
    commands = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                match = re.search(r'(\d+)\.\d+\.\d+\.\d+', result.stdout)
                if match: return int(match.group(1))
        except FileNotFoundError:
            continue
    return 146 # Fallback specifically to 146 based on current log

def setup_driver():
    # Force desktop User-Agent to prevent Facebook from loading mobile (m.facebook.com) which breaks XPaths
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={ua}")
    
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    version = get_chrome_major_version()
    
    if version:
        log("INFO", f"Terdeteksi Chrome versi {version}. Menyesuaikan driver...")
        return uc.Chrome(options=options, version_main=version)
    else:
        log("WARNING", "Gagal mendeteksi versi Chrome otomatis. Menggunakan default...")
        return uc.Chrome(options=options)


# ===================== AI GENERATOR =====================

def generate_ai_caption():
    config = get_config()
    provider = config.get("ai_provider", "gemini")
    
    # 1. Deteksi jam saat ini di VPS
    jam = datetime.now().hour
    
    # 2. Tentukan suasana berdasarkan jam
    if 4 <= jam < 11:
        suasana = "pagi hari (berikan semangat pagi, ngopi, atau bersiap memulai hari)"
    elif 11 <= jam < 15:
        suasana = "siang hari (ingatkan istirahat, makan siang, atau menjaga fokus di tengah hari)"
    elif 15 <= jam < 18:
        suasana = "sore hari (sambut waktu pulang kerja, bersantai, atau evaluasi pencapaian hari ini)"
    else:
        suasana = "malam hari (ucapan selamat istirahat, renungan malam, atau persiapan tidur)"
        
    # 3. Masukkan suasana ke dalam Prompt AI secara dinamis
    prompt = f"""Buatkan 1 caption Facebook yang sangat menarik, natural, dan asik tentang motivasi kerja, bisnis, atau keseharian. 
    Konteks waktu saat ini adalah {suasana}. Wajib sesuaikan kata sapaan pembukanya dengan waktu tersebut!
    Gunakan bahasa Indonesia gaul tapi sopan. Gunakan emoji secukupnya. Jangan kaku seperti robot. Maksimal 3 kalimat pendek. Jangan berikan hashtag."""
    
    if provider == "gemini":
        api_key = config.get("gemini_api_key", "")
        if not api_key:
            return None
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
        except Exception as e:
            log("WARNING", f"Gemini API Error: {str(e).splitlines()[0] if str(e) else 'Unknown'}")
            
    elif provider == "openai":
        base_url = config.get("openai_base_url", "https://openrouter.ai/api/v1")
        api_key = config.get("openai_api_key", "")
        model_name = config.get("openai_model", "google/gemini-2.5-flash:free")
        
        if not api_key:
            return None
        import requests
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            res = requests.post(f"{base_url.rstrip('/')}/chat/completions", json=payload, headers=headers)
            res_json = res.json()
            if "choices" in res_json and len(res_json["choices"]) > 0:
                return res_json["choices"][0]["message"]["content"].strip()
            else:
                log("WARNING", f"OpenAI API Error: {res_json}")
        except Exception as e:
            log("WARNING", f"OpenAI/OpenRouter Network Error: {str(e)}")
            
    return None

# ===================== MANAJEMEN KONTEN =====================

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"posted_texts": [], "posted_media": []}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_content():
    history = load_history()
    selected_text = None
    is_ai = False
    
    log("AI", "Mencoba generate caption unik dengan AI...")
    ai_text = generate_ai_caption()
    
    if ai_text:
        selected_text = ai_text
        is_ai = True
        log("AI", "Caption AI berhasil dibuat!")
    else:
        log("INFO", "Beralih ke texts.txt (AI dinonaktifkan / gagal).")
        with open(TEXTS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            all_texts = [block.strip() for block in re.split(r'\n\s*\n', content) if block.strip()]
        avail_texts = [t for t in all_texts if t not in history["posted_texts"]]
        selected_text = random.choice(avail_texts) if avail_texts else None

    all_media = []
    if os.path.exists(MEDIA_DIR):
        all_media = [f for f in os.listdir(MEDIA_DIR) if os.path.isfile(os.path.join(MEDIA_DIR, f))]
    
    avail_media = [m for m in all_media if m not in history["posted_media"]]
    selected_media = random.choice(avail_media) if avail_media else None
    
    return selected_text, selected_media, history, is_ai

# ===================== CORE =====================

def do_post():
    log_separator()
    text, media_file, history, is_ai = get_content()
    
    if not text and not media_file:
        log("SKIP", "Semua teks manual & media sudah habis! Tambahkan konten baru.")
        return

    log("INFO", "Mempersiapkan Postingan Baru...")
    if text: 
        preview = text.replace('\n', ' ')[:40] + "..." if len(text) > 40 else text.replace('\n', ' ')
        label = "[AI Generated]" if is_ai else "[Manual Text]"
        log("INFO", f"Teks {label} : '{preview}'")
    if media_file: 
        log("INFO", f"Media : {media_file}")
    
    driver = None
    try:
        driver = setup_driver()
        log("INFO", "Membuka browser & menuju Facebook...")
        driver.get("https://www.facebook.com/")
        time.sleep(5)

        if not os.path.exists(COOKIE_FILE):
            log("ERROR", f"File {COOKIE_FILE} tidak ditemukan!")
            return

        with open(COOKIE_FILE, 'r') as f:
            # Handle empty file or different formats safely
            try:
                cookies = json.load(f)
            except json.JSONDecodeError:
                cookies = []
            
            for c in cookies:
                try: 
                    driver.add_cookie({
                        "name": c["name"], "value": c["value"],
                        "domain": c.get("domain", ".facebook.com"), "path": c.get("path", "/")
                    })
                except: pass

        log("INFO", "Menyuntikkan sesi (cookies)...")
        driver.refresh()
        time.sleep(5)

        log("INFO", "Mencari form pembuat status...")
        trigger_xpath = "//span[contains(text(), 'Apa yang Anda pikirkan') or contains(text(), \"What's on your mind\")]"
        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, trigger_xpath)))
        driver.execute_script("arguments[0].click();", btn)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
        time.sleep(2)

        if text:
            log("INFO", "Mengetik status...")
            box = driver.find_element(By.XPATH, "//div[@role='dialog']//div[@contenteditable='true']")
            driver.execute_script("arguments[0].focus();", box)
            human_type(box, text)
            time.sleep(2)

        if media_file:
            log("INFO", "Mengunggah media...")
            upload_inputs = driver.find_elements(By.XPATH, "//div[@role='dialog']//input[@type='file']") or driver.find_elements(By.XPATH, "//input[@type='file']")
            if upload_inputs:
                abs_path = os.path.abspath(os.path.join(MEDIA_DIR, media_file))
                upload_inputs[0].send_keys(abs_path)
                time.sleep(12) 
                log("INFO", "Media berhasil terunggah ke form.")
            else:
                log("WARNING", "Input file media tidak ditemukan di halaman.")

        try:
            next_btn_xpath = "//div[@role='dialog']//div[@role='button' and (.//span[text()='Berikutnya'] or .//span[text()='Next'])]"
            next_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, next_btn_xpath)))
            driver.execute_script("arguments[0].click();", next_btn)
            log("INFO", "Tombol 'Berikutnya' ditekan.")
            time.sleep(2) 
        except:
            pass 

        log("INFO", "Menekan tombol Posting...")
        post_btn_xpath = "//div[@role='dialog']//div[@role='button' and (@aria-label='Posting' or @aria-label='Post' or @aria-label='Kirim' or .//span[text()='Post' or text()='Posting'])]"
        post = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, post_btn_xpath)))
        driver.execute_script("arguments[0].click();", post)

        time.sleep(6) 
        log("SUCCESS", "POSTING BERHASIL DIKIRIM KE FACEBOOK!")

        if text and not is_ai: history["posted_texts"].append(text)
        if media_file: history["posted_media"].append(media_file)
        save_history(history)

    except Exception as e:
        if driver:
            try:
                debug_path = os.path.join(BASE_DIR, "debug_error.png")
                driver.save_screenshot(debug_path)
                log("INFO", f"Screenshot error disimpan di: {debug_path}")
            except:
                pass
        log("ERROR", f"Terjadi kegagalan proses: {str(e)}")

    finally:
        log_separator()
        if driver:
            try: driver.quit()
            except: pass
