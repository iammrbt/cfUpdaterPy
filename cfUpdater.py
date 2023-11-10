import requests
import tkinter as tk
from tkinter import messagebox

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to get public IP: {e}")
        return None

def update_dns_record():
    api_key = api_key_entry.get()
    email = email_entry.get()
    zone_id = zone_id_entry.get()
    record_name = record_name_entry.get()
    record_type = record_type_entry.get()
    content = ip_label.cget("text")

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
            result_text.insert(tk.END, "Success: DNS record updated successfully\n")
        else:
            result_text.insert(tk.END, f"Error: Failed to update DNS record: {response.text}\n")
    except requests.RequestException as e:
        result_text.insert(tk.END, f"API request failed: {e}\n")

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

tk.Label(root, text="Record Name:").pack()
record_name_entry = tk.Entry(root)
record_name_entry.pack()

tk.Label(root, text="Record Type:").pack()
record_type_entry = tk.Entry(root)
record_type_entry.pack()

# Update Button
update_button = tk.Button(root, text="Update DNS Record", command=update_dns_record)
update_button.pack()

# Result Text Widget
result_text = tk.Text(root, height=5, width=50)
result_text.pack()

root.mainloop()
