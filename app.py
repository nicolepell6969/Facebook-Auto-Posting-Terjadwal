import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
import bot_core

app = Flask(__name__)

# Config paths
BASE_DIR = bot_core.BASE_DIR
MEDIA_DIR = bot_core.MEDIA_DIR
CONFIG_FILE = bot_core.CONFIG_FILE
TEXTS_FILE = bot_core.TEXTS_FILE
LOG_FILE = bot_core.LOG_FILE
COOKIE_FILE = bot_core.COOKIE_FILE
HISTORY_FILE = bot_core.HISTORY_FILE

# Set up scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"gemini_api_key": "", "schedule": []}

def refresh_schedule():
    scheduler.remove_all_jobs()
    config = load_config()
    for t in config.get("schedule", []):
        try:
            hour, minute = map(int, t.split(':'))
            scheduler.add_job(bot_core.do_post, 'cron', hour=hour, minute=minute, id=f'job_{t}')
            bot_core.log("INFO", f"Jadwal bot di-set untuk pukul {t}")
        except Exception as e:
            bot_core.log("ERROR", f"Gagal set jadwal {t}: {e}")

# Initialize schedule on startup
refresh_schedule()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    if request.method == 'POST':
        data = request.json
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        refresh_schedule()
        return jsonify({"status": "success", "message": "Konfigurasi diperbarui!"})
    return jsonify(load_config())

@app.route('/api/texts', methods=['GET', 'POST'])
def manage_texts():
    if request.method == 'POST':
        data = request.json
        with open(TEXTS_FILE, 'w', encoding='utf-8') as f:
            f.write(data.get('content', ''))
        return jsonify({"status": "success"})
    
    content = ""
    if os.path.exists(TEXTS_FILE):
        with open(TEXTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    return jsonify({"content": content})

@app.route('/api/cookies', methods=['GET', 'POST'])
def manage_cookies():
    if request.method == 'POST':
        data = request.json
        with open(COOKIE_FILE, 'w') as f:
            json.dump(data.get('cookies', []), f, indent=4)
        return jsonify({"status": "success"})
    
    cookies = []
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            try:
                cookies = json.load(f)
            except:
                cookies = []
    return jsonify({"cookies": cookies})

@app.route('/api/media', methods=['GET', 'POST'])
def manage_media():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(MEDIA_DIR, filename))
        return jsonify({"status": "success", "filename": filename})
    
    files = []
    if os.path.exists(MEDIA_DIR):
        files = os.listdir(MEDIA_DIR)
    return jsonify({"files": files})

@app.route('/media/<filename>')
def serve_media(filename):
    return send_from_directory(MEDIA_DIR, filename)

@app.route('/api/media/<filename>', methods=['DELETE'])
def delete_media(filename):
    path = os.path.join(MEDIA_DIR, secure_filename(filename))
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"status": "success"})
    return jsonify({"error": "File not found"}), 404

@app.route('/api/status', methods=['GET'])
def get_status():
    from apscheduler.schedulers.base import STATE_PAUSED
    is_running = scheduler.state != STATE_PAUSED
    return jsonify({"is_running": is_running})

@app.route('/api/action/toggle', methods=['POST'])
def toggle_automation():
    from apscheduler.schedulers.base import STATE_PAUSED
    if scheduler.state == STATE_PAUSED:
        scheduler.resume()
        bot_core.log("INFO", "Otomatisasi Bot (Scheduler) Dijalankan!")
        return jsonify({"status": "success", "is_running": True, "message": "Automation Started"})
    else:
        scheduler.pause()
        bot_core.log("WARNING", "Otomatisasi Bot (Scheduler) DIHENTIKAN Sementara!")
        return jsonify({"status": "success", "is_running": False, "message": "Automation Stopped"})

@app.route('/api/action/post_now', methods=['POST'])
def post_now():
    try:
        scheduler.add_job(bot_core.do_post, trigger='date')
        return jsonify({"status": "success", "message": "Proses posting dieksekusi di background!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            # Mengambil 50 baris terakhir
            lines = f.readlines()
            logs = [line.strip() for line in lines[-50:]]
    return jsonify({"logs": logs})

if __name__ == '__main__':
    bot_core.log("INFO", "Sistem Web UI dijalankan...")
    app.run(host='0.0.0.0', port=5000, debug=False)
