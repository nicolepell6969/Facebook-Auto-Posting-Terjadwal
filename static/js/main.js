document.addEventListener('DOMContentLoaded', () => {
    // --- Navigation ---
    const navItems = document.querySelectorAll('.nav-item');
    const pages = document.querySelectorAll('.page');
    const pageTitle = document.getElementById('current-page-title');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = item.getAttribute('data-target');
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            pages.forEach(p => p.classList.remove('active'));
            document.getElementById(`page-${targetId}`).classList.add('active');
            
            pageTitle.innerText = item.innerText;
        });
    });

    // --- Toast Notification ---
    function showToast(message, type='success') {
        const toast = document.getElementById('toast');
        toast.innerText = message;
        toast.style.borderLeftColor = type === 'error' ? 'var(--danger)' : 'var(--primary)';
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3000);
    }

    // --- Load Data ---
    let currentSchedule = [];

    async function fetchConfig() {
        const res = await fetch('/api/config');
        const data = await res.json();
        
        document.getElementById('ai-provider').value = data.ai_provider || 'gemini';
        document.getElementById('gemini-api').value = data.gemini_api_key || '';
        document.getElementById('openai-url').value = data.openai_base_url || 'https://openrouter.ai/api/v1';
        document.getElementById('openai-api').value = data.openai_api_key || '';
        document.getElementById('openai-model').value = data.openai_model || 'google/gemini-2.5-flash:free';
        
        document.getElementById('ai-provider').dispatchEvent(new Event('change'));
        
        currentSchedule = data.schedule || [];
        renderSchedule(currentSchedule);
        updateDashboardStat();
    }

    async function fetchTexts() {
        const res = await fetch('/api/texts');
        const data = await res.json();
        document.getElementById('texts-content').value = data.content || '';
    }

    async function fetchCookies() {
        const res = await fetch('/api/cookies');
        const data = await res.json();
        document.getElementById('cookies-content').value = JSON.stringify(data.cookies || [], null, 2);
    }

    async function fetchStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();
            updateToggleButton(data.is_running);
        } catch(e) {}
    }

    function updateToggleButton(isRunning) {
        const btn = document.getElementById('btn-toggle-automation');
        const statusInd = document.querySelector('.status-indicator');
        if(isRunning) {
            btn.innerHTML = '<i class="fa-solid fa-stop"></i> Stop Automation';
            btn.style.background = 'var(--danger)';
            statusInd.className = 'status-indicator online';
            statusInd.innerText = 'Automation ON';
        } else {
            btn.innerHTML = '<i class="fa-solid fa-play"></i> Start Automation';
            btn.style.background = 'var(--success)';
            statusInd.className = 'status-indicator';
            statusInd.style.color = 'var(--text-muted)';
            statusInd.innerText = 'Automation Paused';
        }
    }

    async function fetchMedia() {
        const res = await fetch('/api/media');
        const data = await res.json();
        const gallery = document.getElementById('media-gallery');
        gallery.innerHTML = '';
        
        data.files.forEach(file => {
            const ext = file.split('.').pop().toLowerCase();
            const el = document.createElement('div');
            el.className = 'media-item';
            
            let preview = '';
            if(['mp4','mov','webm'].includes(ext)) {
                preview = `<video src="/media/${file}" muted loop onmouseover="this.play()" onmouseout="this.pause()"></video>`;
            } else {
                preview = `<img src="/media/${file}" alt="${file}">`;
            }
            
            el.innerHTML = `
                ${preview}
                <div class="media-item-overlay">
                    <button class="btn-delete-media" onclick="deleteMedia('${file}')"><i class="fa-solid fa-trash"></i></button>
                </div>
            `;
            gallery.appendChild(el);
        });
        document.getElementById('stat-media-count').innerText = data.files.length;
    }

    async function fetchLogs() {
        const res = await fetch('/api/logs');
        const data = await res.json();
        const term = document.getElementById('terminal-log');
        term.innerHTML = '';
        data.logs.forEach(line => {
            const p = document.createElement('p');
            p.innerText = line;
            if(line.includes("ERROR")) p.className = "log-text error";
            else if(line.includes("WARNING")) p.className = "log-text warning";
            else if(line.includes("SUCCESS")) p.className = "log-text success";
            else if(line.includes("GEMINI")) p.className = "log-text ai";
            else p.className = "log-text info";
            term.appendChild(p);
        });
        term.scrollTop = term.scrollHeight; // auto scroll
    }

    function updateDashboardStat() {
        document.getElementById('stat-schedule-count').innerText = currentSchedule.length;
    }

    function renderSchedule(schedules) {
        const list = document.getElementById('schedule-list');
        list.innerHTML = '';
        schedules.forEach(s => {
            const el = document.createElement('div');
            el.className = 'schedule-chip';
            el.innerHTML = `<span><i class="fa-regular fa-clock"></i> ${s}</span> <i class="fa-solid fa-xmark" onclick="removeSchedule('${s}')"></i>`;
            list.appendChild(el);
        });
    }

    // --- Actions ---
    
    document.getElementById('ai-provider').addEventListener('change', (e) => {
        if(e.target.value === 'openai') {
            document.getElementById('gemini-config-box').style.display = 'none';
            document.getElementById('openai-config-box').style.display = 'block';
        } else {
            document.getElementById('gemini-config-box').style.display = 'block';
            document.getElementById('openai-config-box').style.display = 'none';
        }
    });
    
    // Add Schedule inline function
    window.removeSchedule = (time) => {
        currentSchedule = currentSchedule.filter(t => t !== time);
        renderSchedule(currentSchedule);
    };

    window.deleteMedia = async (filename) => {
        if(!confirm(`Hapus file ${filename}?`)) return;
        const res = await fetch(`/api/media/${filename}`, { method: 'DELETE' });
        if(res.ok) {
            showToast('Media dihapus!');
            fetchMedia();
        }
    };

    document.getElementById('btn-add-schedule').addEventListener('click', () => {
        const val = document.getElementById('new-schedule-time').value;
        if(val && !currentSchedule.includes(val)) {
            currentSchedule.push(val);
            renderSchedule(currentSchedule);
            document.getElementById('new-schedule-time').value = '';
        }
    });

    document.getElementById('form-config').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            ai_provider: document.getElementById('ai-provider').value,
            gemini_api_key: document.getElementById('gemini-api').value,
            openai_base_url: document.getElementById('openai-url').value,
            openai_api_key: document.getElementById('openai-api').value,
            openai_model: document.getElementById('openai-model').value,
            schedule: currentSchedule
        };
        
        const res = await fetch('/api/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        if(res.ok) showToast('Pengaturan API & Jadwal Disimpan!');
        updateDashboardStat();
    });

    document.getElementById('form-texts').addEventListener('submit', async (e) => {
        e.preventDefault();
        const val = document.getElementById('texts-content').value;
        const res = await fetch('/api/texts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ content: val })
        });
        if(res.ok) showToast('File Teks (Fallback) Disimpan!');
    });

    document.getElementById('form-cookies').addEventListener('submit', async (e) => {
        e.preventDefault();
        const val = document.getElementById('cookies-content').value;
        try {
            const parsed = JSON.parse(val);
            const res = await fetch('/api/cookies', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ cookies: parsed })
            });
            if(res.ok) showToast('Cookies Facebook Tersimpan!');
        } catch(err) {
            showToast('Format Cookies JSON tidak valid!', 'error');
        }
    });

    // Upload Media
    document.getElementById('btn-upload-click').addEventListener('click', () => {
        document.getElementById('file-upload-input').click();
    });
    
    document.getElementById('file-upload-input').addEventListener('change', async (e) => {
        if(!e.target.files.length) return;
        const file = e.target.files[0];
        
        const progBox = document.getElementById('upload-progress');
        const progFill = progBox.querySelector('.progress-fill');
        progBox.style.display = 'block';
        progFill.style.width = '10%';
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const res = await fetch('/api/media', {
                method: 'POST',
                body: formData
            });
            progFill.style.width = '100%';
            
            setTimeout(() => {
                progBox.style.display = 'none';
                if(res.ok) {
                    showToast('Media berhasil diunggah!');
                    fetchMedia();
                } else {
                    showToast('Gagal mengunggah media', 'error');
                }
            }, 500);
        } catch(err) {
            progBox.style.display = 'none';
            showToast('Error Server', 'error');
        }
        e.target.value = ''; // reset
    });

    document.getElementById('btn-toggle-automation').addEventListener('click', async () => {
        try {
            const res = await fetch('/api/action/toggle', {method: 'POST'});
            const data = await res.json();
            updateToggleButton(data.is_running);
            showToast(data.message);
            fetchLogs();
        } catch(e) {
            showToast('Gagal merespon', 'error');
        }
    });

    // Force post Trigger
    document.getElementById('btn-force-post').addEventListener('click', async () => {
        showToast('Memulai Bot di Background... Periksa Log!');
        await fetch('/api/action/post_now', {method: 'POST'});
        setTimeout(fetchLogs, 2000);
    });
    
    document.getElementById('btn-refresh-log').addEventListener('click', fetchLogs);

    // Initial Fetch
    fetchStatus();
    fetchConfig();
    fetchTexts();
    fetchCookies();
    fetchMedia();
    fetchLogs();
    
    // Auto-refresh logs if dashboard active
    setInterval(() => {
        if(document.getElementById('page-dashboard').classList.contains('active')){
            fetchLogs();
        }
    }, 5000);
});
