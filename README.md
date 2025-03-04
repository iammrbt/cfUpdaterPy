# Cloudflare DNS Updater

A Python-based GUI application for automatically updating Cloudflare DNS records with your current public IP address.

## Features

### Multiple Domain Support
- Support for multiple domains via comma-separated inputs
- Flexible Zone ID mapping:
  - Single Zone ID can be applied to multiple records
  - Multiple Zone IDs can be mapped 1:1 with record names
- Automatic validation of Zone ID and Record Name counts

### User Interface
- Clean, modern interface using ttk widgets
- API key masking for security
- Clear input field labels with usage instructions
- Real-time countdown display for auto-updates
- Detailed status messages in scrollable text area

### Dynamic Updates
- Non-blocking auto-update implementation
- Responsive UI during updates
- Live countdown timer
- Configurable update intervals
- Manual update option

### Configuration Management
- Save/Load configuration support
- Persistent settings between sessions
- Secure API key storage

## Usage

1. Enter your Cloudflare API credentials:
   - API Key
   - Email address

2. Configure your domains:
   - Zone ID(s): Single ID or comma-separated list
   - Record Name(s): Comma-separated list of domain names
   - Record Type: DNS record type (e.g., A, AAAA)

3. Set update interval in minutes

4. Choose update mode:
   - Click "Manual Update" for one-time update
   - Click "Start Auto Update" for scheduled updates
   - Use "Stop Auto Update" to halt automatic updates

## Requirements

- Python 3.x
- requests library
- tkinter (usually included with Python)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python cfUpdater.py
```
