import os
import sys
import time
import shutil
import threading
import subprocess
from datetime import datetime

# ================= COLORS =================
RED="\033[91m"
GREEN="\033[92m"
CYAN="\033[96m"
YELLOW="\033[93m"
RESET="\033[0m"

# ================= SAFE SLOW PRINT =================
def slow_print(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)

# ================= CHECK NMAP =================
def check_nmap():
    if shutil.which("nmap") is None:
        slow_print(f"{RED}[!] Nmap not installed\n{RESET}")
        slow_print("Termux : pkg install nmap -y\n")
        slow_print("Linux  : sudo apt install nmap -y\n")
        sys.exit(1)

# ================= CLEAR =================
def clear():
    os.system("clear")

# ================= BANNER STRING (NO PRINT HERE) =================
BANNER = f"""
{RED}
███╗   ██╗███╗   ███╗ █████╗ ██████╗
████╗  ██║████╗ ████║██╔══██╗██╔══██╗
██╔██╗ ██║██╔████╔██║███████║██████╔╝
██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝
██║ ╚████║██║ ╚═╝ ██║██║  ██║██║
╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝
{RESET}
{CYAN}ULTIMATE NMAP AI FRAMEWORK
Coded By:THE SILENT GHOST AREBAZ
Ethical Use Only ⚠️
{RESET}
"""

def show_banner():
    slow_print(BANNER)

# ================= LIVE PROGRESS =================
stop_spinner = False
def spinner():
    icons = "|/-\\"
    i = 0
    start = time.time()
    while not stop_spinner:
        t = int(time.time() - start)
        sys.stdout.write(f"\r{YELLOW}[Scanning] {icons[i%4]} Time: {t}s{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print()

# ================= AUTO VULN SUMMARY =================
def auto_vuln_summary(report):
    slow_print(f"\n{CYAN}[AI] Auto Vulnerability Summary:{RESET}\n")
    try:
        data = open(report, "r", errors="ignore").read().lower()
        found = False

        checks = {
            "ftp anonymous login": "FTP Anonymous Login Enabled",
            "ms17-010": "EternalBlue SMB Vulnerability",
            "vulnerable": "Generic Vulnerable Service",
            "cve-": "CVE Reference Found",
            "xss": "Possible XSS Indicator"
        }

        for k, v in checks.items():
            if k in data:
                slow_print(f"{YELLOW}- {v}{RESET}\n")
                found = True

        if not found:
            slow_print(f"{GREEN}- No critical vulnerability keyword found{RESET}\n")

    except:
        slow_print(f"{RED}- Unable to analyze report{RESET}\n")

# ================= RUN SCAN =================
def run_scan(cmd):
    global stop_spinner
    os.makedirs("reports", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt = f"reports/scan_{ts}.txt"
    xml = f"reports/scan_{ts}.xml"

    full_cmd = f"{cmd} -oN {txt} -oX {xml}"

    slow_print(f"\n{GREEN}[+] Running:\n{full_cmd}\n{RESET}")

    stop_spinner = False
    t = threading.Thread(target=spinner)
    t.start()

    try:
        p = subprocess.Popen(full_cmd, shell=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        p.wait()
    except KeyboardInterrupt:
        slow_print(f"\n{RED}[!] Scan Interrupted{RESET}\n")
    finally:
        stop_spinner = True
        t.join()

    slow_print(f"{GREEN}[✓] Scan Completed{RESET}\n")
    slow_print(f"{CYAN}[+] Report Saved:{RESET} {txt}, {xml}\n")

    auto_vuln_summary(txt)

# ================= AI SMART SCAN =================
def ai_smart_scan(target):
    slow_print(f"{CYAN}[AI] Smart Recon → Service → Vuln Scan{RESET}\n")
    run_scan(f"nmap -T4 -Pn -sC -sV --script vuln {target}")

# ================= MENU =================
def menu():
    slow_print(f"""
{YELLOW}[1] Quick Scan
[2] Service & Version Scan
[3] Full Port Scan
[4] OS Detection
[5] Aggressive Scan
[6] Stealth SYN Scan
[7] Vulnerability Scan
[8] UDP Scan
[9] AI Smart Scan (Auto)
[10] Multi Target Scan
[11] Fast Scan (T5)
[12] Custom Nmap Command
[0] Exit
{RESET}
""")

# ================= MAIN =================
def main():
    check_nmap()
    clear()
    show_banner()

    target = input(f"{CYAN}[+] Enter Target (IP/Domain): {RESET}").strip()
    if not target:
        slow_print(f"{RED}[!] Target cannot be empty{RESET}\n")
        return

    while True:
        menu()
        choice = input(f"{CYAN}Select Option: {RESET}").strip()

        if choice == "1":
            run_scan(f"nmap {target}")
        elif choice == "2":
            run_scan(f"nmap -sV {target}")
        elif choice == "3":
            run_scan(f"nmap -p 1-65535 {target}")
        elif choice == "4":
            run_scan(f"nmap -O {target}")
        elif choice == "5":
            run_scan(f"nmap -A {target}")
        elif choice == "6":
            run_scan(f"nmap -sS {target}")
        elif choice == "7":
            run_scan(f"nmap --script vuln {target}")
        elif choice == "8":
            run_scan(f"nmap -sU {target}")
        elif choice == "9":
            ai_smart_scan(target)
        elif choice == "10":
            t = input("Targets (comma separated): ")
            run_scan(f"nmap {t}")
        elif choice == "11":
            run_scan(f"nmap -T5 -F {target}")
        elif choice == "12":
            c = input("Enter nmap options (without nmap): ")
            run_scan(f"nmap {c}")
        elif choice == "0":
            slow_print(f"{GREEN}Stay Ethical 👋{RESET}\n")
            break
        else:
            slow_print(f"{RED}[!] Invalid Option{RESET}\n")

        input(f"{CYAN}\nPress Enter to continue...{RESET}")
        clear()
        show_banner()

# ================= START =================
if __name__ == "__main__":
    main()
