#!/usr/bin/python3

import http.server
import socketserver
import os
import socket
import re
import html
from datetime import datetime

# --- Configuration ---
PORT = 42069
# ---------------------

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            self.list_directory(path)
            return
        super().do_GET()

    def list_directory(self, path):
        try:
            list_dir = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        list_dir.sort(key=lambda a: a.lower())
        r = []
        displaypath = html.escape(os.path.basename(path) or 'LAN Share')
        
        r.append('<!DOCTYPE html><html lang="en"><head>')
        r.append('<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">')
        r.append(f'<title>⚡ LAN Share: {displaypath}</title>')
        
        # --- CSS Flair (Self-Contained) ---
        r.append("""
            <style>
                :root { --primary: #4f46e5; --bg: #f8fafc; --card: #ffffff; --text: #1e293b; }
                body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; display: flex; justify-content: center; }
                .container { width: 100%; max-width: 900px; }
                header { margin-bottom: 2rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 1rem; }
                h2 { margin: 0; display: flex; align-items: center; gap: 10px; color: var(--primary); }
                
                .upload-card { background: var(--card); padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 30px; }
                .upload-card h3 { margin-top: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 8px; }
                
                .file-list { background: var(--card); border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); overflow: hidden; }
                .file-item { display: flex; align-items: center; padding: 12px 20px; border-bottom: 1px solid #f1f5f9; text-decoration: none; color: inherit; transition: background 0.2s; }
                .file-item:hover { background: #f1f5f9; }
                .file-item:last-child { border-bottom: none; }
                .file-icon { font-size: 1.4rem; margin-right: 15px; width: 30px; text-align: center; }
                .file-info { flex-grow: 1; }
                .file-name { font-weight: 500; font-size: 1.05rem; }
                .file-meta { font-size: 0.85rem; color: #64748b; }

                /* Progress Bar Styling */
                #progress-wrapper { display: none; margin-top: 20px; }
                progress { width: 100%; height: 12px; border-radius: 6px; appearance: none; }
                progress::-webkit-progress-bar { background-color: #e2e8f0; border-radius: 6px; }
                progress::-webkit-progress-value { background-color: var(--primary); border-radius: 6px; }
                
                .btn { background: var(--primary); color: white; border: none; padding: 10px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }
                .btn:hover { opacity: 0.9; }
                input[type="file"] { border: 1px solid #cbd5e1; padding: 8px; border-radius: 6px; width: 100%; max-width: 300px; margin-bottom: 10px; }
                #status { margin-top: 10px; font-size: 0.9rem; font-weight: 500; color: #475569; }
            </style>
        """)
        r.append('</head><body><div class="container">')
        
        # Header
        r.append(f'<header><h2><span>📂</span> {displaypath}</h2><p style="margin:5px 0 0 0; color:#64748b;">Local Network File Sharing</p></header>')
        
        # Upload Card
        r.append('<div class="upload-card">')
        r.append('<h3><span>📤</span> Upload New File</h3>')
        r.append('<input type="file" id="fileInput">')
        r.append('<button class="btn" onclick="uploadFile()">Push to Server ⚡</button>')
        r.append('<div id="progress-wrapper"><progress id="progressBar" value="0" max="100"></progress>')
        r.append('<div id="status">Ready...</div></div></div>')
        
        # File List Card
        r.append('<div class="file-list">')
        
        # Back Link
        if self.path != '/':
             r.append(f'<a href="../" class="file-item"><span class="file-icon">⬅️</span><div class="file-info"><div class="file-name">Go Back</div></div></a>')

        for name in list_dir:
            fullname = os.path.join(path, name)
            is_dir = os.path.isdir(fullname)
            icon = "📁" if is_dir else "📄"
            suffix = "/" if is_dir else ""
            
            # Get file stats
            stats = os.stat(fullname)
            size = f"{stats.st_size / 1024 / 1024:.2f} MB" if not is_dir else "Folder"
            mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')

            r.append(f'''
                <a href="{name}{suffix}" class="file-item">
                    <span class="file-icon">{icon}</span>
                    <div class="file-info">
                        <div class="file-name">{html.escape(name)}</div>
                        <div class="file-meta">{size} • Last modified {mtime}</div>
                    </div>
                    <span style="color:#cbd5e1; font-size:1.2rem;">{"›" if is_dir else "⬇️"}</span>
                </a>
            ''')
            
        r.append('</div>') # Close file-list
        r.append('<p style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:30px;">Python-Powered LAN Share • Standard Lib Only</p>')

        # JavaScript for Progress & AJAX
        r.append("""
            <script>
            function uploadFile() {
                const fileInput = document.getElementById("fileInput");
                const file = fileInput.files[0];
                if (!file) { alert("Please select a file first!"); return; }
                
                const formData = new FormData();
                formData.append("file", file);

                const xhr = new XMLHttpRequest();
                const wrapper = document.getElementById("progress-wrapper");
                const bar = document.getElementById("progressBar");
                const status = document.getElementById("status");
                
                wrapper.style.display = "block";
                status.innerText = "Connecting...";

                xhr.upload.addEventListener("progress", (e) => {
                    if (e.lengthComputable) {
                        const percent = (e.loaded / e.total) * 100;
                        bar.value = Math.round(percent);
                        status.innerText = "🚀 Uploading: " + Math.round(percent) + "% (" + (e.loaded/1048576).toFixed(1) + " MB)";
                    }
                });

                xhr.onload = () => {
                    if (xhr.status == 200) {
                        status.innerHTML = "✅ <b>Success!</b> Refreshing list...";
                        setTimeout(() => location.reload(), 800);
                    } else {
                        status.innerText = "❌ Upload failed!";
                    }
                };

                xhr.open("POST", window.location.pathname, true);
                xhr.send(formData);
            }
            </script>
        """)
        
        r.append('</div></body></html>')
        
        encoded = ''.join(r).encode('utf-8', 'surrogateescape')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self):
        """Streaming POST to disk - efficient memory usage."""
        try:
            ctype = self.headers['Content-Type']
            boundary = ctype.split("boundary=")[1].encode()
            remainbytes = int(self.headers['Content-Length'])
            
            line = self.rfile.readline()
            remainbytes -= len(line)
            if not boundary in line: return

            line = self.rfile.readline()
            remainbytes -= len(line)
            fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
            if not fn: return
            
            # Clean filename and path
            filename = os.path.basename(fn[0])
            out_path = os.path.join(self.translate_path(self.path), filename)
            
            while line.strip():
                line = self.rfile.readline()
                remainbytes -= len(line)
            
            with open(out_path, 'wb') as out:
                preline = self.rfile.readline()
                remainbytes -= len(preline)
                while remainbytes > 0:
                    line = self.rfile.readline()
                    remainbytes -= len(line)
                    if boundary in line:
                        preline = preline.rstrip(b'\r\n')
                        out.write(preline)
                        break
                    else:
                        out.write(preline)
                        preline = line

            self.send_response(200)
            self.end_headers()
        except Exception:
            self.send_error(500)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except: return '127.0.0.1'
    finally: s.close()

if __name__ == '__main__':
    ip = get_ip()
    print(f"\n🚀 LAN Share Server Live!")
    print(f"🔗 URL: http://{ip}:{PORT}")
    print(f"📂 Folder: {os.getcwd()}")
    print("-" * 30)

    with http.server.ThreadingHTTPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down... 👋")

