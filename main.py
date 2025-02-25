import tkinter as tk
from tkinter import messagebox
import subprocess
import ctypes
import sys
import os

RULE_NAME = "123456"
REMOTE_IP = "192.81.241.171"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_command(command_list):
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            encoding="cp866",
            errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.stdout or "", result.stderr or ""
    except Exception as e:
        return "", str(e)

def enable_rule():
    command = [
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name={RULE_NAME}",
        "dir=out",
        "action=block",
        f"remoteip={REMOTE_IP}"
    ]
    stdout, stderr = run_command(command)
    if stderr:
        messagebox.showerror("Error", f"Failed to enable the rule:\n{stderr}")
    else:
        status_label.config(text="Enabled")

def disable_rule():
    command = [
        "netsh", "advfirewall", "firewall", "delete", "rule",
        f"name={RULE_NAME}"
    ]
    stdout, stderr = run_command(command)
    if stderr:
        messagebox.showerror("Error", f"Failed to disable the rule:\n{stderr}")
    else:
        status_label.config(text="Disabled")

def check_rule_status():
    command = [
        "netsh", "advfirewall", "firewall", "show", "rule",
        f"name={RULE_NAME}"
    ]
    stdout, stderr = run_command(command)
    return RULE_NAME in stdout

def update_status():
    if check_rule_status():
        status_label.config(text="Enabled")
    else:
        status_label.config(text="Disabled")

def on_closing():
    disable_rule()
    root.destroy()

if not is_admin():
    script = os.path.abspath(__file__)
    ret = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}"', None, 1
    )
    if int(ret) <= 32:
        messagebox.showerror("Error", "Failed to obtain administrator privileges.")
    sys.exit(0)

root = tk.Tk()
root.title("By your favorite kitty")
root.geometry("300x150")
root.resizable(False, False)

status_label = tk.Label(root, text="Checking...", font=("Arial", 14))
status_label.pack(pady=10)

enable_button = tk.Button(root, text="Enable", font=("Arial", 12), command=lambda: [enable_rule(), update_status()])
enable_button.pack(pady=5)

disable_button = tk.Button(root, text="Disable", font=("Arial", 12), command=lambda: [disable_rule(), update_status()])
disable_button.pack(pady=5)

update_status()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
