# iiSU OST Downloader (Fan-version)

A standalone GUI utility designed to automatically enhance your **iiSULauncher** experience by downloading and syncing Game OSTs directly to your Android device via ADB.


<img width="590" height="674" alt="Screenshot 2026-02-24 234603" src="https://github.com/user-attachments/assets/16dd10b3-e377-4083-a39a-5c5c8594b5b9" />

## 📁 Package Contents

The provided folder includes everything you need to run the app without installing Python:

* **`musicui.exe`**: The main application.
* **`platform-tools/`**: Contains `adb.exe` for communication with your Android device.
* **`ffmpeg.exe`**: Handles audio conversion and processing.
* **`ffplay.exe` / `ffprobe.exe**`: Supporting tools for media handling.

## 🚀 Features

* **Zero Installation:** Portable version that includes all dependencies (FFmpeg & ADB).
* **Automated Scanning:** Recursively scans your Android device for console and game folders.
* **Smart Name Cleaning:** Strips version numbers and tags (e.g., `[USA]`, `(v1.0)`) for better search results.
* **YouTube Integration:** Automatically finds the best "Main Theme" for each game using `yt-dlp`.
* **Duplicate Prevention:** Checks for existing `music.mp3` files to avoid redundant downloads.

## 🛠️ Setup & Usage

1. **Connect your Device:** Plug your Android device into your PC and ensure **USB Debugging** is enabled in Developer Options.
2. **Run the App:** Open `musicui.exe`.
3. **Configure Paths:**
* **ADB Path:** Click **Browse** and select `adb.exe` inside the `platform-tools` folder.
* **Base Device Path:** Usually set to the default iiSULauncher media path.
* **Search Suffix:** Set your preferred search term (default: "main theme ost").


4. **Start:** Click **Start Download & Push** and watch the logs in real-time.

---

## **Note on FFmpeg:** The application is configured to look for `ffmpeg.exe` in the root folder. Ensure it remains in the same directory as `musicui.exe` for the conversion process to work.

## ⚙️ How it works

1. **Scan:** The app uses ADB to list subfolders in your Android directory.
2. **Clean:** It turns a folder named `Super Mario World (USA) [v1.1]` into `Super Mario World`.
3. **Download:** It searches YouTube, downloads the audio, and uses FFmpeg to convert it to a 192kbps MP3.
4. **Sync:** The resulting `music.mp3` is pushed directly to the specific game folder on your device.

## ⚠️ Disclaimer

This tool is a fan-made project for personal use. Please respect copyright laws and the Terms of Service of content platforms. The developer is not responsible for any data loss or issues caused by modifying files on your device.

---

### 🤝 Contributing

Feel free to fork this project, report issues, or submit pull requests.

**Developed by:** [KorndanaiMos](https://github.com/KorndanaiMos)

---

**Would you like me to create a "Quick Start" image or a GIF-style description of these steps to add to the visual appeal?**
