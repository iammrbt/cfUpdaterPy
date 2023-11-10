# Cloudflare DNS Updater

## Overview
This Python script provides a graphical user interface (GUI) to update DNS records in Cloudflare. It retrieves the public IP address of the user's machine using the ipify service and updates a specified DNS record in Cloudflare with this IP address.

## Features
- Retrieves the current public IP address.
- Updates a specified DNS record in Cloudflare with the current IP.
- GUI for easy interaction.

## Prerequisites
- Python 3.x
- `requests` library (Install using `pip install requests`)

## Setup
1. Clone or download this repository to your local machine.
2. Install the required Python packages: `pip install requests`.

## Configuration
Before running the script, ensure you have the following Cloudflare account details:
- API Key
- Email associated with Cloudflare account
- Zone ID of the domain
- Record Name and Record Type you wish to update

## Usage
1. Run the script using Python: `python cf_dns_updater.py`.
2. Enter your Cloudflare API Key, Email, Zone ID, Record Name, and Record Type in the respective fields in the GUI.
3. The script will display your current public IP. If you want to update the specified DNS record to this IP, click on the "Update DNS Record" button.
4. Results of the operation will be displayed in the GUI.

## Troubleshooting
- Ensure all entered credentials and information are correct.
- Make sure your Cloudflare API key has the necessary permissions.
- Check your internet connection if the script fails to retrieve the public IP.

## License
[MIT License](LICENSE.md)
