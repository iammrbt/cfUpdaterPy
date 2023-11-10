import requests
import tkinter as tk
from tkinter import messagebox
import threading
import time

auto_update_flag = False

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to get public IP: {e}")
        return None

def get_dns_record_id(api_key, email, zone_id, record_name, record_type):
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type={record_type}&name={record_name}", headers=headers)
        if response.status_code == 200:
            records = response.json()["result"]
            if records:
                return records[0]["id"]
            else:
                messagebox.showinfo("Info", "No matching DNS record found")
                return None
        else:
            messagebox.showerror("Error", f"Failed to fetch DNS records: {response.text}")
            return None
    except requests.RequestException as e:
        messagebox.showerror("Error", f"API request failed: {e}")
        return None

def check_dns_record(api_key, email, zone_id, record_name, record_type, current_ip):
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type={record_type}&name={record_name}", headers=headers)
    if response.status_code == 200:
        records = response.json()["result"]
        if records and records[0]['content'] == current_ip:
            return True
    return False

def update_dns_record():
    api_key = api_key_entry.get()
    email = email_entry.get()
    zone_id = zone_id_entry.get()
    record_names = record_name_entry.get().split(",")  # Splitting by comma for multiple record names
    record_type = record_type_entry.get()
    content = ip_label.cget("text")

    for record_name in record_names:
        record_name = record_name.strip()  # Removing leading/trailing whitespace
        if check_dns_record(api_key, email, zone_id, record_name, record_type, content):
            result_text.insert(tk.END, f"Info: DNS record for {record_name} already matches the current IP.\n")
            continue
        record_id = get_dns_record_id(api_key, email, zone_id, record_name, record_type)
        if not record_id:
            continue

        headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": api_key,
            "Content-Type": "application/json"
        }

        data = {
            "type": record_type,
            "name": record_name,
            "content": content,
            "ttl": 1,
            "proxied": False
        }

        try:
            response = requests.put(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}", json=data, headers=headers)
            if response.status_code == 200:
                result_text.insert(tk.END, f"Success: DNS record for {record_name} updated successfully\n")
            else:
                result_text.insert(tk.END, f"Error: Failed to update DNS record for {record_name}: {response.text}\n")
        except requests.RequestException as e:
            result_text.insert(tk.END, f"API request failed for {record_name}: {e}\n")

def auto_update():
    global auto_update_flag
    auto_update_flag = True
    interval = float(interval_entry.get()) * 60  # Convert minutes to seconds
    while auto_update_flag:
        current_ip = get_public_ip()
        if current_ip != ip_label.cget("text"):
            ip_label.config(text=current_ip)
            update_dns_record()
        time.sleep(interval)

def stop_auto_update():
    global auto_update_flag
    auto_update_flag = False

# GUI Setup
root = tk.Tk()
root.title("DNS Updater")

# Public IP Display
tk.Label(root, text="Your Public IP:").pack()
ip_label = tk.Label(root, text=get_public_ip())
ip_label.pack()

# Input Fields with Labels
tk.Label(root, text="API Key:").pack()
api_key_entry = tk.Entry(root)
api_key_entry.pack()

tk.Label(root, text="Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Zone ID:").pack()
zone_id_entry = tk.Entry(root)
zone_id_entry.pack()

tk.Label(root, text="Record Name(s):").pack()
record_name_entry = tk.Entry(root)
record_name_entry.pack()

tk.Label(root, text="Record Type:").pack()
record_type_entry = tk.Entry(root)
record_type_entry.pack()

# Update Button
update_button = tk.Button(root, text="Update DNS Record", command=update_dns_record)
update_button.pack()

# Interval Input Field
tk.Label(root, text="Update Interval (minutes):").pack()
interval_entry = tk.Entry(root)
interval_entry.pack()

# Start and Stop Auto-Update Buttons
start_auto_update_button = tk.Button(root, text="Start Auto Update", command=lambda: threading.Thread(target=auto_update, daemon=True).start())
start_auto_update_button.pack()

stop_auto_update_button = tk.Button(root, text="Stop Auto Update", command=stop_auto_update)
stop_auto_update_button.pack()

# Result Text Widget
result_text = tk.Text(root, height=5, width=50)
result_text.pack()

root.mainloop()
