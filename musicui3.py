import os
import re
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import webbrowser
import yt_dlp

TARGET_FILENAME = "music"

def run_adb(adb_path, command):
    full_cmd = f'"{adb_path}" {command}'
    return subprocess.run(full_cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='ignore')

def clean_game_name(folder_name):
    cleaned = re.sub(r'[\(\[].*?[\)\]]', '', folder_name)
    cleaned = re.sub(r'v\d+\.\d+\.\d+', '', cleaned)
    cleaned = cleaned.replace('-', ' ').replace(':', ' ')
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

class ThorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AYN Thor OST Downloader")
        self.root.geometry("620x720")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        content_frame = tk.Frame(root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(content_frame, text="ADB Path (on your PC):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w")
        adb_frame = tk.Frame(content_frame, bg="#f0f0f0")
        adb_frame.pack(fill=tk.X, pady=(2, 0))
        self.adb_entry = ttk.Entry(adb_frame, font=("Arial", 9))
        self.adb_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.adb_entry.insert(0, r"C:\platform-tools\adb.exe")
        ttk.Button(adb_frame, text="Browse...", command=self.browse_adb).pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Label(content_frame, text="Base Device Path (on AYN Thor):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.path_entry = ttk.Entry(content_frame, font=("Arial", 9))
        self.path_entry.pack(fill=tk.X, pady=(2, 0))
        self.path_entry.insert(0, "/sdcard/Android/media/com.iisulauncher/iiSULauncher/assets/media/roms/consoles")
        
        path_helper_frame = tk.Frame(content_frame, bg="#f0f0f0")
        path_helper_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(path_helper_frame, text="Check Connection", command=self.check_device).pack(side=tk.LEFT)

        tk.Label(content_frame, text="Custom Search Query (Suffix):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(15, 0))
        self.query_entry = ttk.Entry(content_frame, font=("Arial", 9))
        self.query_entry.pack(fill=tk.X, pady=(2, 15))
        self.query_entry.insert(0, "main theme ost")

        self.start_btn = tk.Button(content_frame, text="Start Download & Push", command=self.start_process, 
                                   bg="#0078d7", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=25, pady=8, cursor="hand2")
        self.start_btn.pack(pady=10)

        tk.Label(content_frame, text="Logs:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(content_frame, height=15, font=("Consolas", 9), state='disabled', bg="white")
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        status_frame = tk.Frame(root, bg="#e0e0e0", bd=1, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(status_frame, text="ver 1.0.0", bg="#e0e0e0", fg="#4a4a4a", font=("Arial", 8)).pack(side=tk.LEFT, padx=10, pady=2)
        github_link = tk.Label(status_frame, text="KorndanaiMos (GitHub)", bg="#e0e0e0", fg="#0066cc", font=("Arial", 8), cursor="hand2")
        github_link.pack(side=tk.RIGHT, padx=10, pady=2)
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/KorndanaiMos"))

    def browse_adb(self):
        filepath = filedialog.askopenfilename(title="Select adb.exe", filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")])
        if filepath:
            self.adb_entry.delete(0, tk.END)
            self.adb_entry.insert(0, os.path.normpath(filepath))

    def check_device(self):
        adb_path = self.adb_entry.get().strip()
        result = run_adb(adb_path, "devices")
        if "device\n" in result.stdout or "device\r\n" in result.stdout:
            messagebox.showinfo("Success", "AYN Thor detected!")
        else:
            messagebox.showerror("Error", "Device not found. Check cable and USB Debugging.")

    def log_message(self, message):
        def append():
            self.log_area.config(state='normal')
            self.log_area.insert(tk.END, message + "\n")
            self.log_area.see(tk.END)
            self.log_area.config(state='disabled')
        self.root.after(0, append)

    def start_process(self):
        self.start_btn.config(state='disabled', bg="#cccccc")
        self.log_area.config(state='normal')
        self.log_area.delete('1.0', tk.END)
        self.log_area.config(state='disabled')
        self.log_message("--- Starting process ---")
        
        adb_path = self.adb_entry.get().strip()
        base_path = self.path_entry.get().strip()
        query_suffix = self.query_entry.get().strip()

        thread = threading.Thread(target=self.process_games, args=(adb_path, base_path, query_suffix))
        thread.daemon = True
        thread.start()

    def process_games(self, adb_path, base_path, query_suffix):
        check_path = run_adb(adb_path, f'shell "ls -d \\"{base_path}\\""')
        if "No such file" in check_path.stderr or not check_path.stdout.strip():
            self.log_message(f"❌ Error: Path not found on device: {base_path}")
            self.reset_ui()
            return

        consoles = self.get_subfolders(adb_path, base_path)
        if not consoles:
            self.log_message("❌ Error: No console folders found.")
            self.reset_ui()
            return

        for console in consoles:
            if console.lower() in ['update', 'dlc', 'temp', 'data', 'media']: continue
            console_path = f"{base_path}/{console}"
            self.log_message(f"\n📁 Checking Console: [{console}]")
            
            games = self.get_subfolders(adb_path, console_path)
            for game_folder in games:
                if game_folder.lower() in ['update', 'dlc', 'migrated file']: continue
                full_game_path = f"{console_path}/{game_folder}"
                
                if self.check_music_exists(adb_path, full_game_path):
                    self.log_message(f" ⏩ Skipped: {game_folder} (Already has music)")
                    continue
                
                self.log_message(f" ⏳ Processing: {game_folder}")
                game_title = clean_game_name(game_folder)
                self.download_and_push(adb_path, game_title, full_game_path, query_suffix)

        self.log_message("\n✅ --- Process Completed ---")
        self.reset_ui()

    def get_subfolders(self, adb_path, path):
        result = run_adb(adb_path, f'shell "ls -F \\"{path}\\""')
        if result.returncode != 0: return []
        return [f.strip('/') for f in result.stdout.splitlines() if f.endswith('/')]

    def check_music_exists(self, adb_path, full_path):
        file_path = f"{full_path}/{TARGET_FILENAME}.mp3"
        result = run_adb(adb_path, f'shell "ls \\"{file_path}\\""')
        return TARGET_FILENAME in result.stdout

    def download_and_push(self, adb_path, game_name, target_path, query_suffix):
        temp_file = "temp_music.mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_music.%(ext)s',
            'postprocessor_args': {'ffmpeg': ['-t', '120']},
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'quiet': True,
            'no_warnings': True
        }
        try:
            self.log_message(f"   > Searching YouTube...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch1:{game_name} {query_suffix}"])
            
            if os.path.exists(temp_file):
                self.log_message(f"   > Pushing to device...")
                dest = f"{target_path}/{TARGET_FILENAME}.mp3"
                push_res = run_adb(adb_path, f'push "{temp_file}" "{dest}"')
                
                if push_res.returncode == 0:
                    self.log_message(f"   [OK] Success!")
                else:
                    self.log_message(f"   [Fail] ADB Push Error: {push_res.stderr.strip()}")
                
                os.remove(temp_file)
            else:
                self.log_message(f"   [Fail] Download failed (No temp file created)")
        except Exception as e:
            self.log_message(f"   [Error] {str(e)}")

    def reset_ui(self):
        self.root.after(0, lambda: self.start_btn.config(state='normal', bg="#0078d7"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ThorApp(root)
    root.mainloop()