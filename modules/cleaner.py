import os
import sys
import platform
import shutil
import tempfile
import subprocess
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.chrome.options import Options as CHOptions

class CleanerBase:
    def __init__(self, logs_yolu):
        self.logs_yolu = logs_yolu

    def tarayici_bul(self, status_msg):
        bulunanlar = []
        os_tipi = platform.system()
        adaylar = {
            "Zen Browser": ["zen", "zen-browser", "zen-bin", "/opt/zen-browser-bin/zen-bin", "zen.exe"],
            "Google Chrome": ["google-chrome", "google-chrome-stable", "chrome.exe", "Google Chrome"],
            "Brave": ["brave-browser", "brave.exe", "Brave Browser"],
            "Firefox": ["firefox", "firefox.exe", "Firefox.app"],
            "Microsoft Edge": ["microsoft-edge", "msedge.exe", "Microsoft Edge"]
        }
        mac_apps = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Firefox.app/Contents/MacOS/firefox", "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser", "/Applications/Zen Browser.app/Contents/MacOS/zen"]
        
        for isim, komutlar in adaylar.items():
            for k in komutlar:
                yol = k if os_tipi == "Windows" and k.endswith(".exe") else (k if os.path.isabs(k) else shutil.which(k))
                if not yol and os_tipi == "Darwin":
                    for mapp in mac_apps:
                        if isim.lower() in mapp.lower() and os.path.exists(mapp): yol = mapp; break
                if yol and os.path.exists(yol):
                    try:
                        with open(yol, 'rb') as f:
                            b = f.read(100).decode('utf-8', errors='ignore')
                            if b.startswith("#!") and "exec " in b:
                                p = b.split("exec ")[1].split()[0].replace('"', '').replace("'", "")
                                if os.path.exists(p): yol = p
                    except: pass
                    if not any(b['yol'] == yol for b in bulunanlar): bulunanlar.append({"isim": isim, "yol": yol})
                    break
        return bulunanlar

    def get_driver_and_profile(self, tarayici):
        home = Path.home()
        os_tipi = platform.system()
        profil_yolu = None
        paths = {
            "Linux": {"Zen": home / ".config/zen", "Chrome": home / ".config/google-chrome", "Firefox": home / ".mozilla/firefox", "Brave": home / ".config/BraveSoftware/Brave-Browser", "Edge": home / ".config/microsoft-edge"},
            "Windows": {"Zen": Path(os.environ.get('APPDATA', '')) / "zen/Profiles", "Chrome": Path(os.environ.get('LOCALAPPDATA', '')) / "Google/Chrome/User Data", "Firefox": Path(os.environ.get('APPDATA', '')) / "Mozilla/Firefox/Profiles", "Brave": Path(os.environ.get('LOCALAPPDATA', '')) / "BraveSoftware/Brave-Browser/User Data", "Edge": Path(os.environ.get('LOCALAPPDATA', '')) / "Microsoft/Edge/User Data"},
            "Darwin": {"Zen": home / "Library/Application Support/zen/Profiles", "Chrome": home / "Library/Application Support/Google/Chrome", "Firefox": home / "Library/Application Support/Firefox/Profiles", "Brave": home / "Library/Application Support/BraveSoftware/Brave-Browser", "Edge": home / "Library/Application Support/Microsoft Edge"}
        }
        key = next((k for k in ["Zen", "Chrome", "Firefox", "Brave", "Edge"] if k in tarayici['isim']), None)
        if key and os_tipi in paths:
            base_path = paths[os_tipi][key]
            if base_path.exists():
                candidates = [p for p in base_path.rglob("*") if p.is_dir() and ("Default" in p.name or "Profile" in p.name or ".default" in p.name)]
                if candidates: profil_yolu = str(max(candidates, key=lambda x: x.stat().st_mtime))
        
        temp_dir = None
        if profil_yolu:
            temp_dir = tempfile.mkdtemp()
            ignore = shutil.ignore_patterns('lock', 'parent.lock', 'lock-file', 'Cache*', 'cache*', 'GPUCache')
            shutil.copytree(profil_yolu, temp_dir, dirs_exist_ok=True, ignore=ignore)
            profil_yolu = temp_dir

        if "Firefox" in tarayici['isim'] or "Zen" in tarayici['isim']:
            opts = FFOptions()
            opts.binary_location = tarayici['yol']
            if profil_yolu:
                opts.add_argument("-profile")
                opts.add_argument(profil_yolu)
            return webdriver.Firefox(options=opts), temp_dir
        else:
            opts = CHOptions()
            opts.binary_location = tarayici['yol']
            if profil_yolu:
                opts.add_argument(f"--user-data-dir={profil_yolu}")
            return webdriver.Chrome(options=opts), temp_dir
