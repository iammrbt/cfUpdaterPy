# Cloudflare DNS Updater

## Overview
This Python script provides a graphical user interface (GUI) to update DNS records in Cloudflare. It retrieves the public IP address of the user's machine using the ipify service and updates one or more DNS records in Cloudflare with this IP address.

## Features
- Retrieves the current public IP address
- Updates multiple DNS records simultaneously
- Supports different Zone IDs for different domains
- Dynamic auto-update with countdown display
- Configuration save/load functionality
- User-friendly GUI with clear instructions
- Responsive interface during auto-updates
- Detailed status updates and error reporting
- Secure API key entry with show/hide toggle

## Prerequisites
- Python 3.x
- `requests` library (Install using `pip install requests`)
- `tkinter` library (usually included with Python)

## Setup
1. Clone or download this repository to your local machine
2. Install the required Python packages: `pip install requests`

## Configuration
Before running the script, ensure you have the following Cloudflare account details:
- API Key
- Email associated with Cloudflare account
- Zone ID(s) for your domain(s)
- Record Name(s) and Record Type you wish to update

### Multiple Domain Support
You can update multiple domains by:
- Entering multiple record names separated by commas (e.g., "test1.example.com, test2.example.com")
- Either:
  - Using a single Zone ID that applies to all records, or
  - Entering multiple Zone IDs (comma-separated) that match the number of record names

## Usage
1. Run the script using Python: `python cfUpdater.py`
2. Enter your configuration details in the GUI:
   - Cloudflare API Key (can be toggled visible/hidden)
   - Email address
   - Zone ID(s) (comma-separated for multiple domains)
   - Record Name(s) (comma-separated for multiple domains)
   - Record Type
   - Update interval (in minutes)
3. Choose your update method:
   - Click "Manual Update" for a one-time update
   - Click "Start Auto Update" to begin automatic updates at the specified interval
   - Click "Stop Auto Update" to halt automatic updates
4. The GUI will display:
   - Your current public IP
   - A countdown to the next auto-update
   - Results of update operations in the text area

## Troubleshooting
- Ensure all entered credentials and information are correct
- Make sure your Cloudflare API key has the necessary permissions
- For Zone-specific issues, try using a Global API key
- Check your internet connection if the script fails to retrieve the public IP
- Review the cfUpdater.log file for detailed error messages

## License
[MIT License](LICENSE.md)
