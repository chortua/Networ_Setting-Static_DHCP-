import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# --- Run command safely ---
def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            encoding="utf-8",  # avoids cp932 decode errors
            errors="ignore"
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

# --- Set static IP ---
def set_static():
    adapter = adapter_var.get()
    ip = ip_entry.get().strip()
    mask = mask_entry.get().strip()
    gateway = gw_entry.get().strip()
    dns = dns_entry.get().strip()

    if not adapter or not ip or not mask:
        messagebox.showerror("Error", "Adapter / IP / Subnet Mask are required.")
        return

    # Build netsh command
    if gateway in ["", "0.0.0.0"]:
        cmd_address = f'netsh interface ipv4 set address name="{adapter}" static {ip} {mask}'
    else:
        cmd_address = f'netsh interface ipv4 set address name="{adapter}" static {ip} {mask} {gateway}'

    output = run_cmd(cmd_address)

    # Set DNS only if not empty or 0.0.0.0
    if dns not in ["", "0.0.0.0"]:
        output += "\n" + run_cmd(f'netsh interface ipv4 set dns name="{adapter}" static {dns}')

    messagebox.showinfo("Done", f"✅ Static IP applied.\n\n{output}")

# --- Set DHCP ---
def set_dhcp():
    adapter = adapter_var.get()
    if not adapter:
        messagebox.showerror("Error", "Select an adapter")
        return

    cmds = [
        f'netsh interface ipv4 set address name="{adapter}" dhcp',
        f'netsh interface ipv4 set dns name="{adapter}" dhcp'
    ]
    output = "\n".join([run_cmd(c) for c in cmds])
    messagebox.showinfo("Done", f"✅ DHCP enabled.\n\n{output}")

# --- GUI ---
app = tk.Tk()
app.title("IP Switcher - Japanese Windows")

# Adapter dropdown
adapter_var = tk.StringVar()

# Use actual Japanese adapter names from your system
adapters = ["イーサネット", "Wi-Fi"]

ttk.Label(app, text="Adapter:").grid(row=0, column=0, sticky="e")
adapter_menu = ttk.Combobox(app, textvariable=adapter_var, values=adapters, width=20)
adapter_var.set("イーサネット")  # default LAN
adapter_menu.grid(row=0, column=1)

# IP Address
ttk.Label(app, text="IP Address:").grid(row=1, column=0, sticky="e")
ip_entry = tk.Entry(app)
ip_entry.insert(0, "192.168.")  # auto-fill
ip_entry.grid(row=1, column=1)

# Subnet Mask
ttk.Label(app, text="Subnet Mask:").grid(row=2, column=0, sticky="e")
mask_entry = tk.Entry(app)
mask_entry.insert(0, "255.255.255.0")
mask_entry.grid(row=2, column=1)

# Gateway (optional)
ttk.Label(app, text="Gateway (optional):").grid(row=3, column=0, sticky="e")
gw_entry = tk.Entry(app)
gw_entry.insert(0, "0.0.0.0")
gw_entry.grid(row=3, column=1)

# DNS (optional)
ttk.Label(app, text="DNS (optional):").grid(row=4, column=0, sticky="e")
dns_entry = tk.Entry(app)
dns_entry.insert(0, "0.0.0.0")
dns_entry.grid(row=4, column=1)

# Buttons
ttk.Button(app, text="Set STATIC IP", width=18, command=set_static).grid(row=5, column=0, pady=12)
ttk.Button(app, text="Set DHCP (AUTO)", width=18, command=set_dhcp).grid(row=5, column=1, pady=12)

app.mainloop()
