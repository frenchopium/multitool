import os
import sys
import time
import socket
import subprocess
import ctypes
import shutil
import requests
import webbrowser
from datetime import datetime
import winreg
import psutil

def print_ascii_art():
    # Code ANSI pour le rouge
    RED = '\033[91m'
    RESET = '\033[0m'
    
    ascii_art = f"""{RED}
    ██╗███╗   ██╗████████╗███████╗██████╗ ██╗   ██╗██████╗ ████████╗██╗
    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██║   ██║██╔══██╗╚══██╔══╝██║
    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██║   ██║██████╔╝   ██║   ██║
    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██║   ██║██╔══██╗   ██║   ██║
    ██║██║ ╚████║   ██║   ███████╗██║  ██║╚██████╔╝██║  ██║   ██║   ██║
    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝
    {RESET}"""
    print(ascii_art)

def ping_ip(ip):
    try:
        start_time = time.time()
        subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()
        ms = round((end_time - start_time) * 1000, 2)
        print(f"Ping vers {ip}: {ms}ms")
    except Exception as e:
        print(f"Erreur lors du ping: {str(e)}")

def lookup_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"IP de {domain}: {ip}")
    except Exception as e:
        print(f"Erreur lors du lookup: {str(e)}")

def clean_windows_files():
    temp_folders = [
        os.path.join(os.environ['TEMP']),
        os.path.join(os.environ['WINDIR'], 'Temp'),
        os.path.join(os.environ['WINDIR'], 'Prefetch')
    ]
    
    for folder in temp_folders:
        try:
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Impossible de supprimer {item_path}: {str(e)}")
            print(f"Nettoyage de {folder} terminé")
        except Exception as e:
            print(f"Erreur lors du nettoyage de {folder}: {str(e)}")

def toggle_windows_defender(enable=True):
    try:
        if enable:
            subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $false'], shell=True)
            subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableIOAVProtection $false'], shell=True)
            print("Windows Defender activé")
        else:
            subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'], shell=True)
            subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableIOAVProtection $true'], shell=True)
            print("Windows Defender désactivé")
    except Exception as e:
        print(f"Erreur lors de la modification de Windows Defender: {str(e)}")

def repair_windows():
    try:
        print("Démarrage de la réparation Windows...")
        subprocess.run(['sfc', '/scannow'], shell=True)
        subprocess.run(['DISM', '/Online', '/Cleanup-Image', '/RestoreHealth'], shell=True)
        print("Réparation Windows terminée")
    except Exception as e:
        print(f"Erreur lors de la réparation Windows: {str(e)}")

def join_discord():
    discord_url = "https://discord.gg/lbxmb"
    webbrowser.open(discord_url)

def main_menu():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Ping IP")
        print("2. Lookup Domain")
        print("3. Nettoyer fichiers Windows")
        print("4. Désactiver Windows Defender")
        print("5. Activer Windows Defender")
        print("6. Réparer Windows")
        print("7. Rejoindre Discord")
        print("8. Quitter")
        
        choice = input("\nChoisissez une option (1-8): ")
        
        if choice == "1":
            ip = input("Entrez l'IP à pinger: ")
            ping_ip(ip)
        elif choice == "2":
            domain = input("Entrez le domaine à rechercher: ")
            lookup_domain(domain)
        elif choice == "3":
            clean_windows_files()
        elif choice == "4":
            toggle_windows_defender(False)
        elif choice == "5":
            toggle_windows_defender(True)
        elif choice == "6":
            repair_windows()
        elif choice == "7":
            join_discord()
        elif choice == "8":
            print("Au revoir!")
            sys.exit()
        else:
            print("Option invalide!")

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print("Ce programme nécessite des droits administrateur!")
        sys.exit(1)
    
    print_ascii_art()
    main_menu() 