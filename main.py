#!/usr/bin/env python3
import os
import sys
import requests
import subprocess
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

banner = '''
🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙
🐙   ___             _               ___      _                            🐙🐙🐙
🐙  / _ \\    __     | |_     ___    / __|    | |     ___    _ _      ___   🐙🐙🐙🐙🐙
🐙 | (_) |  / _|    |  _|   / _ \\  | (__     | |    / _ \\  | ' \\    / -_)  🐙🐙🐙🐙🐙🐙🐙🐙🐙
🐙  \\___/   \\__|_   _\\__|   \\___/   \\___|   _|_|_   \\___/  |_||_|   \\___|  🐙🐙🐙🐙🐙🐙🐙🐙🐙
🐙_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 🐙🐙🐙🐙🐙
🐙"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 🐙🐙🐙
🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙🐙
'''

version = 'v2025.08.13.GK0827 - Created By MrSquidward'

config = {
    "target": None,
    "project": None,
    "verbose": False
}

def show_help():
    print(Fore.CYAN + """
Available Commands:
    set url <target>       - Set target URL
    set project <path>     - Set project folder path
    clone                  - Clone the full website
    verbose on/off         - Enable/disable verbose mode
    subdomains             - Find subdomains (via crt.sh)
    subdirs                - Find hidden directories (wordlist based)
    download <.ext>        - Download specific file type
    show config            - Show current settings
    save config            - Save current config to file
    load config            - Load config from file
    cd <folder>            - Change working directory
    help                   - Show this help
    exit                   - Exit the tool
    Any other Linux command is executed in shell
""")

def show_config():
    print(Fore.CYAN + "[*] Current Configuration:")
    for key, value in config.items():
        print(f"    {key}: {value}")

def save_config(filename="octoclone_config.json"):
    try:
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)
        print(Fore.GREEN + f"[+] Config saved to {filename}")
    except Exception as e:
        print(Fore.RED + f"[!] Error saving config: {e}")

def load_config(filename="octoclone_config.json"):
    global config
    try:
        with open(filename, "r") as f:
            config = json.load(f)
        print(Fore.GREEN + f"[+] Config loaded from {filename}")
    except Exception as e:
        print(Fore.RED + f"[!] Error loading config: {e}")

def fetch_html(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(Fore.RED + f"[!] Error fetching page: {e}")
        return None

def download_resource(url, folder, verbose=False):
    try:
        parsed_url = urlparse(url)
        local_path = os.path.join(folder, parsed_url.path.lstrip('/'))
        if local_path.endswith('/') or local_path == folder:
            local_path = os.path.join(local_path, 'index.html')
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            if verbose:
                print(Fore.GREEN + f"[+] Downloaded: {url}")
            return os.path.relpath(local_path, folder)
        else:
            if verbose:
                print(Fore.RED + f"[-] Failed ({r.status_code}): {url}")
    except Exception as e:
        if verbose:
            print(Fore.RED + f"[!] Error downloading {url}: {e}")
    return None

def clone_website(target, project, verbose=False):
    if not target or not project:
        print(Fore.RED + "[!] Set target URL and project first.")
        return
    html = fetch_html(target)
    if not html:
        return
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(['link', 'script', 'img']):
        attr = 'href' if tag.name == 'link' else 'src'
        if tag.has_attr(attr):
            src = tag[attr]
            full_url = urljoin(target, src)
            local_path = download_resource(full_url, project, verbose=verbose)
            if local_path:
                tag[attr] = local_path
    os.makedirs(project, exist_ok=True)
    with open(os.path.join(project, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    print(Fore.GREEN + f"[+] Website cloned successfully at {project}")

def find_subdomains(domain):
    print(Fore.YELLOW + f"[*] Finding subdomains for {domain}...")
    try:
        response = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
        data = response.json()
        subs = set()
        for entry in data:
            for name in entry['name_value'].split('\n'):
                if domain in name:
                    subs.add(name.strip())
        for sub in sorted(subs):
            print(" -", sub)
    except Exception as e:
        print(Fore.RED + f"[!] Error fetching subdomains: {e}")

def scan_subdirs(url, wordlist='common.txt'):
    print(Fore.YELLOW + f"[*] Scanning hidden directories at {url}...")
    try:
        with open(wordlist, 'r') as f:
            for path in f:
                path = path.strip()
                full_url = urljoin(url, path)
                r = requests.get(full_url, timeout=5)
                if r.status_code == 200:
                    print(Fore.GREEN + f"[+] Found: {full_url}")
    except Exception as e:
        print(Fore.RED + f"[!] Error scanning directories: {e}")

def download_by_extension(url, ext, project):
    html = fetch_html(url)
    if not html:
        return
    soup = BeautifulSoup(html, 'html.parser')
    found = False
    for tag in soup.find_all(['a', 'script', 'link']):
        for attr in ['href', 'src']:
            if tag.has_attr(attr) and tag[attr].endswith(ext):
                full_url = urljoin(url, tag[attr])
                if download_resource(full_url, project, verbose=config["verbose"]):
                    found = True
    if not found:
        print(Fore.YELLOW + "[*] No matching files found.")

def set_project(path):
    full_path = os.path.abspath(os.path.expanduser(path))
    try:
        os.makedirs(full_path, exist_ok=True)
        config["project"] = full_path
        print(Fore.GREEN + f"[+] Project folder set to: {full_path}")
    except Exception as e:
        print(Fore.RED + f"[!] Could not create project folder: {e}")

def shell():
    while True:
        try:
            command = input(Fore.LIGHTMAGENTA_EX + "octoclone> ").strip()
            if not command:
                continue
            if command == "help":
                show_help()
            elif command == "exit":
                print(Fore.YELLOW + "[*] Exiting OctoClone...")
                break
            elif command.startswith("set url "):
                config["target"] = command[8:].strip()
                print(Fore.GREEN + f"[+] Target set: {config['target']}")
            elif command.startswith("set project "):
                set_project(command[12:].strip())
            elif command == "clone":
                clone_website(config["target"], config["project"], verbose=config["verbose"])
            elif command.startswith("verbose "):
                value = command.split()[1].lower()
                config["verbose"] = value == "on"
                print(Fore.GREEN + "[+] Verbose mode enabled" if config["verbose"] else Fore.YELLOW + "[-] Verbose mode disabled")
            elif command == "subdomains":
                if config["target"]:
                    domain = urlparse(config["target"]).netloc
                    find_subdomains(domain)
                else:
                    print(Fore.RED + "[!] Set target first.")
            elif command == "subdirs":
                if config["target"]:
                    scan_subdirs(config["target"])
                else:
                    print(Fore.RED + "[!] Set target first.")
            elif command.startswith("download "):
                if config["target"] and config["project"]:
                    download_by_extension(config["target"], command.split()[1], config["project"])
                else:
                    print(Fore.RED + "[!] Set target URL and project folder first.")
            elif command == "show config":
                show_config()
            elif command == "save config":
                save_config()
            elif command == "load config":
                load_config()
            elif command.startswith("cd "):
                try:
                    os.chdir(command[3:].strip())
                    print(Fore.GREEN + f"[+] Changed directory to {os.getcwd()}")
                except Exception as e:
                    print(Fore.RED + f"[!] {e}")
            else:
                try:
                    subprocess.run(command, shell=True)
                except Exception as e:
                    print(Fore.RED + f"[!] Command error: {e}")
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[*] Use 'exit' to quit.")
        except EOFError:
            print()
            break

def main():
    os.system('clear')
    print(Fore.GREEN + banner)
    print(Fore.RED + version)
    print(Fore.YELLOW + "Type 'help' for commands.\n")
    shell()

if __name__ == "__main__":
    main()
