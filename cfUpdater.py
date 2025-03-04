import requests
import tkinter as tk
from tkinter import messagebox, ttk  # Import ttk for themed widgets
import configparser
import os
import time
import logging

# Global variables for auto update scheduling
auto_update_running = False
auto_update_id = None

# Configure logging
logging.basicConfig(filename='cfUpdater.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def get_public_ip() -> str | None:
    """Fetches the current public IP address.

    Returns:
        str: The public IP address, or None if an error occurred.
    """
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to get public IP: {e}")
        logging.error(f"Failed to get public IP: {e}")
        return None
    except requests.exceptions.Timeout as e:
        messagebox.showerror("Error", f"Request timed out: {e}")
        logging.error(f"Request timed out: {e}")
        return None

# Save and load configuration
def save_config():
    """Saves the user's configuration to a file."""
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'ApiKey': api_key_entry.get(),
        'Email': email_entry.get(),
        'ZoneIDs': zone_id_entry.get(),
        'RecordNames': record_name_entry.get(),
        'RecordType': record_type_entry.get(),
        'Interval': interval_entry.get()
    }
    try:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        messagebox.showinfo("Info", "Configuration saved successfully.")
    except OSError as e:
        messagebox.showerror("Error", f"Failed to save config: {e}")
        logging.error(f"Failed to save config: {e}")


def load_config():
    """Loads the user's configuration from a file."""
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        if 'DEFAULT' in config:
            api_key_entry.delete(0, tk.END)
            api_key_entry.insert(0, config['DEFAULT'].get('ApiKey', ''))

            email_entry.delete(0, tk.END)
            email_entry.insert(0, config['DEFAULT'].get('Email', ''))

            zone_id_entry.delete(0, tk.END)
            zone_id_entry.insert(0, config['DEFAULT'].get('ZoneIDs', ''))

            record_name_entry.delete(0, tk.END)
            record_name_entry.insert(0, config['DEFAULT'].get('RecordNames', ''))

            record_type_entry.delete(0, tk.END)
            record_type_entry.insert(0, config['DEFAULT'].get('RecordType', ''))

            interval_entry.delete(0, tk.END)
            interval_entry.insert(0, config['DEFAULT'].get('Interval', ''))
    except OSError as e:
        messagebox.showerror("Error",f"Failed to load config file: {e}")
        logging.error(f"Failed to load config file: {e}")


# Get the DNS record ID for a given domain record
def get_dns_record_id(api_key: str, email: str, zone_id: str, record_name: str, record_type: str) -> str | None:
    """Retrieves the DNS record ID from Cloudflare.

    Args:
        api_key: The Cloudflare API key.
        email: The Cloudflare account email.
        zone_id: The Cloudflare zone ID.
        record_name: The DNS record name.
        record_type: The DNS record type.

    Returns:
        The DNS record ID, or None if an error occurred.
    """
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type={record_type}&name={record_name}",
            headers=headers, timeout=10
        )
        response.raise_for_status()
        records = response.json()["result"]
        if records:
            return records[0]["id"]
        else:
            messagebox.showinfo("Info", f"No matching DNS record found for {record_name}")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API request failed: {e}")
        logging.error(f"API request failed: {e}")
        return None
    except requests.exceptions.Timeout as e:
        messagebox.showerror("Error", f"API request timed out: {e}")
        logging.error(f"API request timed out: {e}")
        return None

# Check the current IP content of a DNS record
def check_dns_record(api_key: str, email: str, zone_id: str, record_name: str, record_type: str) -> str | None:
    """Checks the current IP address of a DNS record.

    Args:
        api_key: The Cloudflare API key.
        email: The Cloudflare account email.
        zone_id: The Cloudflare zone ID.
        record_name: The DNS record name.
        record_type: The DNS record type.

    Returns:
        The current IP address of the DNS record, or None if not found.
    """
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type={record_type}&name={record_name}",
            headers=headers, timeout=10
        )
        response.raise_for_status()
        records = response.json()["result"]
        if records:
            return records[0]['content']  # Return the IP address of the DNS record
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to check DNS record: {e}")
        return None
    except requests.exceptions.Timeout as e:
        logging.error(f"Failed to check DNS record, request timed out: {e}")
        return None


# Update a single DNS record and return True if successful
def update_dns_record_for_domain(api_key: str, email: str, zone_id: str, record_name: str, record_type: str, ip: str) -> bool:
    """Updates a single DNS record on Cloudflare.

    Args:
        api_key: The Cloudflare API key.
        email: The Cloudflare account email.
        zone_id: The Cloudflare zone ID.
        record_name: The DNS record name.
        record_type: The DNS record type.
        ip: The new IP address.

    Returns:
        True if the update was successful, False otherwise.
    """
    record_id = get_dns_record_id(api_key, email, zone_id, record_name, record_type)
    if not record_id:
        return False

    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "type": record_type,
        "name": record_name,
        "content": ip,
        "ttl": 1,  # Automatic TTL
        "proxied": False  # Adjust as needed
    }

    try:
        response = requests.put(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            json=data, headers=headers, timeout=10
        )
        response.raise_for_status()
        return True  # Successful update

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error",f"Failed to update {record_name}: {e}")
        logging.error(f"Failed to update {record_name}: {e}")
        return False
    except requests.exceptions.Timeout as e:
        messagebox.showerror("Error",f"Failed to update {record_name}, request timed out: {e}")
        logging.error(f"Failed to update {record_name}, request timed out: {e}")
        return False

# Manual update triggered by the button
def manual_update():
    """Performs a manual DNS update."""
    current_ip = get_public_ip()
    if not current_ip:
        return

    ip_label.config(text=current_ip)
    record_names = [r.strip() for r in record_name_entry.get().split(",") if r.strip()]
    zone_ids = [z.strip() for z in zone_id_entry.get().split(",") if z.strip()]

    # If only one zone ID is provided, use it for all record names.
    if len(zone_ids) == 1 and len(record_names) > 1:
        zone_ids = zone_ids * len(record_names)
    elif len(zone_ids) != len(record_names):
        messagebox.showerror("Error", "Number of Zone IDs must be either 1 or match the number of Record Names.")
        return

    for record_name, zone_id in zip(record_names, zone_ids):
        dns_record_ip = check_dns_record(api_key_entry.get(), email_entry.get(), zone_id, record_name, record_type_entry.get())
        if dns_record_ip == current_ip:
            result_text.insert(tk.END, f"Info: {record_name} is already up-to-date.\n")
            continue
        elif dns_record_ip is None:
            result_text.insert(tk.END, f"Error: Could not retrieve DNS record for {record_name}.\n")
            continue

        if update_dns_record_for_domain(api_key_entry.get(), email_entry.get(), zone_id, record_name, record_type_entry.get(), current_ip):
            result_text.insert(tk.END, f"Success: Updated {record_name} to {current_ip}.\n")
        else:
            result_text.insert(tk.END, f"Error: Failed to update {record_name}.\n")


# Dynamic auto update using tkinter's after() for non-blocking scheduling
def schedule_next_update(seconds: int):
    """Schedules the next automatic update.

    Args:
        seconds: The number of seconds until the next update.
    """
    global auto_update_running, auto_update_id
    if not auto_update_running:
        countdown_label.config(text="Auto update stopped.")
        return

    if seconds > 0:
        mins, secs = divmod(seconds, 60)
        countdown_label.config(text=f"Next check in: {mins:02d}:{secs:02d}")
        auto_update_id = root.after(1000, schedule_next_update, seconds - 1)
    else:
        perform_update()

def perform_update():
    """Performs the automatic DNS update."""
    global auto_update_running
    if not auto_update_running:
        return

    current_ip = get_public_ip()
    if not current_ip:
        # If the IP could not be fetched, reschedule the next check
        schedule_next_update(int(float(interval_entry.get()) * 60))
        return

    ip_label.config(text=current_ip)
    record_names = [r.strip() for r in record_name_entry.get().split(",") if r.strip()]
    zone_ids = [z.strip() for z in zone_id_entry.get().split(",") if z.strip()]

    if len(zone_ids) == 1 and len(record_names) > 1:
        zone_ids = zone_ids * len(record_names)
    elif len(zone_ids) != len(record_names):
        result_text.insert(tk.END, "Error: Number of Zone IDs must be either 1 or match the number of Record Names.\n")
        schedule_next_update(int(float(interval_entry.get()) * 60))
        return

    update_performed = False
    for record_name, zone_id in zip(record_names, zone_ids):
        dns_record_ip = check_dns_record(api_key_entry.get(), email_entry.get(), zone_id, record_name, record_type_entry.get())
        if dns_record_ip == current_ip:
            result_text.insert(tk.END, f"Info: {record_name} is already up-to-date.\n")
            continue
        elif dns_record_ip is None:
            result_text.insert(tk.END, f"Error: Could not retrieve DNS record for {record_name}.\n")
            continue

        if update_dns_record_for_domain(api_key_entry.get(), email_entry.get(), zone_id, record_name, record_type_entry.get(), current_ip):
            result_text.insert(tk.END, f"Success: Updated {record_name} to {current_ip}.\n")
            update_performed = True
        else:
            result_text.insert(tk.END, f"Error: Failed to update {record_name}.\n")

    if not update_performed:
        result_text.insert(tk.END, f"No update necessary at {time.strftime('%Y-%m-%d %H:%M:%S')}.\n")

    # Reschedule next update using the specified interval (in minutes)
    interval_sec = int(float(interval_entry.get()) * 60)
    schedule_next_update(interval_sec)

def start_auto_update():
    """Starts the automatic update process."""
    global auto_update_running
    auto_update_running = True
    try:
        interval_sec = int(float(interval_entry.get()) * 60)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the update interval.")
        return
    schedule_next_update(interval_sec)

def stop_auto_update():
    """Stops the automatic update process."""
    global auto_update_running, auto_update_id
    auto_update_running = False
    if auto_update_id:
        root.after_cancel(auto_update_id)
        auto_update_id = None
    countdown_label.config(text="Auto update stopped.")

# Move this function before the GUI Setup section, after the other function definitions
def toggle_api_key_visibility():
    """Toggles the visibility of the API key."""
    current = api_key_entry.cget("show")
    if current == "*":
        api_key_entry.config(show="")
        toggle_api_key_button.config(text="Hide API Key")
    else:
        api_key_entry.config(show="*")
        toggle_api_key_button.config(text="Show API Key")

# --- GUI Setup ---
root = tk.Tk()
root.title("DNS Updater")

# Use ttk for a more modern look
style = ttk.Style()
style.theme_use("clam")  # You can choose other themes like "default", "alt", "classic"

# Display Public IP
ttk.Label(root, text="Your Public IP:").pack(pady=5)
ip_label = ttk.Label(root, text=get_public_ip())
ip_label.pack()

# Save and Load Buttons
save_config_button = ttk.Button(root, text="Save Config", command=save_config)
save_config_button.pack(pady=2)

load_config_button = ttk.Button(root, text="Load Config", command=load_config)
load_config_button.pack(pady=2)

# Input Fields with clear directions
ttk.Label(root, text="API Key:").pack()
api_key_entry = ttk.Entry(root, width=50, show="*")  # Add show="*" parameter
api_key_entry.pack()
toggle_api_key_button = ttk.Button(root, text="Show API Key", command=toggle_api_key_visibility)
toggle_api_key_button.pack(pady=2)

ttk.Label(root, text="Email:").pack()
email_entry = ttk.Entry(root, width=50)
email_entry.pack()

ttk.Label(root, text="Zone ID(s): (For multiple domains, separate by commas)").pack()
zone_id_entry = ttk.Entry(root, width=50)
zone_id_entry.pack()

ttk.Label(root, text="Record Name(s): (For multiple domains, separate by commas)").pack()
record_name_entry = ttk.Entry(root, width=50)
record_name_entry.pack()

ttk.Label(root, text="Record Type:").pack()
record_type_entry = ttk.Entry(root, width=50)
record_type_entry.pack()

ttk.Label(root, text="Update Interval (minutes):").pack()
interval_entry = ttk.Entry(root, width=20)
interval_entry.pack()

# Buttons for manual and automatic updates
update_button = ttk.Button(root, text="Manual Update", command=manual_update)
update_button.pack(pady=5)

start_button = ttk.Button(root, text="Start Auto Update", command=start_auto_update)
start_button.pack(pady=5)

stop_button = ttk.Button(root, text="Stop Auto Update", command=stop_auto_update)
stop_button.pack(pady=5)

# Countdown label for auto update
countdown_label = ttk.Label(root, text="Auto update stopped.")
countdown_label.pack(pady=5)

# Result text box
result_text = tk.Text(root, height=10, width=80)
result_text.pack(pady=5)

# Load configuration on startup
load_config()

root.mainloop()
