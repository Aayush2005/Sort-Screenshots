# 🖼️ Automated Real-Time Screenshot Sorter

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![systemd](https://img.shields.io/badge/systemd-Service-blue)](https://www.freedesktop.org/wiki/Software/systemd/)

A lightweight automation project that **organizes your Android screenshots instantly** into app-specific folders on your Ubuntu PC.
It uses **Syncthing** for real-time file sync and a **persistent Python watcher** to auto-sort every new screenshot as it arrives, with **automatic back-sync** to your phone.

**Author:** Aayush

---

## 🚀 Overview

### Problem

Manually sorting screenshots on your phone is painful. Finding old screenshots in a 2,000+ image pile? Even worse.

### Solution

This project establishes a two-way sync pipeline between your **Android phone** and **Ubuntu PC**, where a Python script monitors incoming screenshots, sorts them into app folders, and syncs back to the device.

---

## 🧩 Architecture

**Flow:**

> Android → Syncthing → Ubuntu → Python Watcher → Organized Storage → Syncthing → Android

**Components:**

| Component     | Role                                        |
| ------------- | ------------------------------------------- |
| Android Phone | Captures screenshots, syncs via Syncthing   |
| Syncthing     | Secure sync pipeline between phone and PC   |
| Ubuntu PC     | Storage + sorting                           |
| `watcher.py`  | Detects new screenshots and auto-sorts them |

---

## 📂 Project Structure

```
Sort-Screenshots/
├── Screenshots/              # Source folder synced from Android
├── config/
│   └── app_map.json          # Mapping of package names → app folder names
├── screenshots_sorted/       # Destination folder for sorted screenshots (back-sync folder)
├── watcher.py                # Persistent Python watcher
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

<!-- ---

## 🎬 Demo

![Demo GIF](path/to/demo.gif)
*Take a screenshot on your phone → it instantly appears in the correct folder on Ubuntu and syncs back.*

> Replace `path/to/demo.gif` with your actual demo GIF or screenshots folder path.

--- -->

## 🛠️ Setup Guide

### 1️⃣ Install Dependencies

On Ubuntu PC:

```bash
sudo apt update
sudo apt install syncthing python3-venv python3-pip
```

Create a virtual environment and install Python dependencies:

```bash
git clone https://github.com/Aayush2005/Sort-Screenshots.git
cd Sort-Screenshots
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 2️⃣ Configure Syncthing

1. Install **Syncthing** on Android from Google Play Store.
2. On PC, run `syncthing` once to initialize.
3. Pair your devices using their **Device IDs**.
4. On Android: share the `Screenshots` folder, type = **Send Only**.
5. On Ubuntu: accept the folder, set **destination path** to `Sort-Screenshots/Screenshots`.
6. Create another folder `screenshots_sorted/` on PC for **back-sync**.

   * Share it via Syncthing with **Send & Receive**.
   * On Android, choose a destination path for sorted screenshots, e.g., `/Syncthing/SortedScreenshots`.

> **Tip:** Keep the folder marker file inside the synced folders; otherwise, Syncthing stops syncing.

---

### 3️⃣ Configure `app_map.json`

Edit `config/app_map.json` to define your app folders:

```json
{
  "com.instagram.android": "Instagram",
  "com.whatsapp": "WhatsApp",
  "com.google.android.youtube": "YouTube",
  "org.mozilla.firefox": "Firefox",
  "com.twitter.android": "Twitter",
  "com.brave.browser": "Brave",
  "com.android.chrome": "Chrome",
  "com.snapchat.android": "Snapchat",
  "com.linkedin.android": "LinkedIn",
  "com.pubg.imobile": "BGMI"
  --or anything else--
}
```

* Only apps in this list will have their own folder.
* Unknown apps go to `screenshots_sorted/Unsorted`.

---

### 4️⃣ Run the Watcher Manually (Optional)

```bash
source .venv/bin/activate
python3 watcher.py
```

* Batch-sorts existing screenshots on startup.
* Watches for new screenshots in real-time.

---

### 5️⃣ Run the Watcher as a systemd Service

Create `/etc/systemd/system/screenshot-watcher.service`:

```ini
[Unit]
Description=Screenshot Watcher Service
After=network.target

[Service]
Type=simple
ExecStart=full-path-to-venv-python -u full-path-to-watcher.py
WorkingDirectory=full-path-to-project-directory
Restart=always
StandardOutput=append:full-path-for-log-files
StandardError=append:full-path-for-log-files

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable screenshot-watcher
sudo systemctl start screenshot-watcher
```

Check status/logs:

```bash
sudo systemctl status screenshot-watcher
journalctl -u screenshot-watcher -f
```

---

### 6️⃣ Batch Sorting Existing Screenshots

```bash
python3 batch_sort.py
```

* Moves all screenshots from `Screenshots/` to their respective app folders.
* Sorted screenshots automatically sync back to your phone via Syncthing.

---

### 7️⃣ Enable Syncthing on Startup

```bash
# Disable any previously running system-wide Syncthing service
sudo systemctl disable syncthing@aayush.service
sudo systemctl stop syncthing@aayush.service

# Enable Syncthing to start automatically for your user
systemctl --user enable syncthing.service
systemctl --user start syncthing.service

# (Optional) Allow Syncthing to run even after logout
loginctl enable-linger $USER
```

---

### ⚡ Notes / Tips

* Watcher ignores `.tmp` files from Syncthing until fully written.
* Only screenshots matching `Screenshot_YYYY-MM-DD-HH-MM-SS-XXX_package.png/jpg` are processed.
* Unknown package names go to `Unsorted/`.
* Logs are written to `watcher.log`.
* Back-sync folder ensures sorted screenshots are available both on PC and phone.

---

### 📝 License

MIT License — free to use, modify, and share.
