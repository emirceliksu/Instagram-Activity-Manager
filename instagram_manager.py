import os
import sys
import subprocess

def install_deps():
    deps = ["instagrapi", "rich", "selenium", "deep-translator", "pyotp", "python-dotenv"]
    need_install = []
    
    is_venv = sys.prefix != sys.base_prefix
    if not is_venv:
        venv_path = os.path.join(os.getcwd(), ".env_insta")
        python_exe = os.path.join(venv_path, "bin", "python") if os.name != "nt" else os.path.join(venv_path, "Scripts", "python.exe")
        
        if not os.path.exists(venv_path):
            print("[*] Initializing environment...")
            try:
                subprocess.check_call([sys.executable, "-m", "venv", ".env_insta"])
            except:
                print("[!] Error creating venv. Please install 'python3-venv'.")
                sys.exit(1)
        
        if sys.executable != python_exe:
            os.execv(python_exe, [python_exe] + sys.argv)

    for dep in deps:
        try:
            if dep == "deep-translator": __import__("deep_translator")
            elif dep == "python-dotenv": __import__("dotenv")
            else: __import__(dep.replace("-", "_"))
        except ImportError:
            need_install.append(dep)
    
    if need_install:
        print(f"[*] Installing modules: {', '.join(need_install)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL)
            subprocess.check_call([sys.executable, "-m", "pip", "install", *need_install])
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            print(f"[!] Install error: {e}")
            sys.exit(1)

install_deps()

import json
import time
import random
import logging
import platform
import signal
import shutil
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from instagrapi import Client
from rich.console import Console
from rich.panel import Panel

from utils.language import LanguageManager
from modules.likes import LikeManager
from modules.comments import CommentManager
from modules.cleaner import CleanerBase

console = Console()

class InstagramActivityMaster(CleanerBase):
    def __init__(self):
        self.logs_yolu = Path("logs")
        super().__init__(self.logs_yolu)
        self.developer = "Muhammed Emir Çeliksu"
        self.calisiyor = True
        self.cl = Client()
        self.toplam_silinen = 0
        self.arsiv_dosyasi = self.logs_yolu / "arsiv_urller.log"
        self.lang = LanguageManager()
        self.ui = {}
        
        self._setup()
        signal.signal(signal.SIGINT, self._handle_exit)

    def _setup(self):
        if not self.logs_yolu.exists():
            self.logs_yolu.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_yolu / "app.log"
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=1, encoding='utf-8')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[handler])

    def _handle_exit(self, signum, frame):
        self.calisiyor = False
        sys.exit(0)

    def _archive(self, url):
        with open(self.arsiv_dosyasi, "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Removed: {url}\n")

    def _get_session(self):
        if not self.cl.user_id:
            browsers = self.tarayici_bul(self.ui['detect'])
            if not browsers: return False
            
            target = browsers[0]
            
            driver = None
            temp_dir = None
            try:
                driver, temp_dir = self.get_driver_and_profile(target)
                driver.get("https://www.instagram.com")
                time.sleep(6)
                cookies = driver.get_cookies()
                sid = next((c['value'] for c in cookies if c['name'] == 'sessionid'), None)
                if sid:
                    self.cl.login_by_sessionid(sid)
                    return True
            except:
                pass
            finally:
                if driver: driver.quit()
                if temp_dir and os.path.exists(temp_dir): shutil.rmtree(temp_dir)
        return self.cl.user_id is not None

    def _browser_opener_factory(self):
        browsers = self.tarayici_bul(self.ui['detect'])
        if not browsers: return lambda: (None, None)
        return lambda: self.get_driver_and_profile(browsers[0])

    def start(self):
        self.ui = self.lang.set_language()
        likes_mod = LikeManager(self.cl, self.ui, self._archive)
        comments_mod = CommentManager(self.ui, self._browser_opener_factory())
        
        while self.calisiyor:
            logo = r"""
   __  __ _   _ _   _   _   __  __ __  ____  
  |  \/  | | | | | | | / \ |  \/  |  \/  | ____| 
  | |\/| | | | | |_| |/ _ \| |\/| | |\/| |  _|   
  | |  | | |_| |  _  / ___ \ |  | | |  | | |___  
  |_|  |_|_|\___/|_| |_/_/   \_\_|  |_|  |_|_____| 

   _____ __  __ ___ ____  
  | ____|  \/  |_ _|  _ \ 
  |  _| | |\/| || || |_) |
  | |___| |  | || ||  _ < 
  |_____|_|  |_|___|_| \_\

    ____ _____ _     ___ _  ______  _   _ 
   / ___| ____| |   |_ _| |/ / ___|| | | |
  | |   |  _| | |    | || ' /\___ \| | | |
  | |___| |___| |___ | || . \ ___) | |_| |
   \____|_____|_____|___|_|\_\____/ \___/ 
    """
            console.print(Panel.fit(f"[bold magenta]{logo}[/bold magenta]\n[bold white]{self.ui['title']}[/bold white]\n[dim]Created by {self.developer}[/dim]", border_style="cyan"))
            
            print(f"1) {self.ui['menu_1']}")
            print(f"2) {self.ui['menu_2']}")
            print(f"3) {self.ui['menu_3']}")
            print(f"4) {self.ui['menu_4']}")
            print(f"0) {self.ui['menu_0']}")
            
            choice = console.input(f"\n[bold magenta]> [/bold magenta]")
            
            if choice == "0": break
            
            if choice in ["1", "2", "4"]:
                if not self._get_session():
                    console.print("[red]Could not fetch session.[/red]")
                    continue

            session_total = 0
            if choice == "1":
                session_total += likes_mod.sweep(mod="beğeni")
            elif choice == "2":
                session_total += likes_mod.sweep(mod="kaydedilen")
            elif choice == "3":
                session_total += comments_mod.sweep()
            elif choice == "4":
                session_total += likes_mod.sweep(mod="beğeni")
                session_total += likes_mod.sweep(mod="kaydedilen")
                session_total += comments_mod.sweep()
            
            self.toplam_silinen += session_total
            console.print(f"\n[bold green][✓] {self.ui['done']}\n[*] {self.ui['count']}: {session_total}")
            input("\nENTER...")

if __name__ == "__main__":
    app = InstagramActivityMaster()
    app.start()
