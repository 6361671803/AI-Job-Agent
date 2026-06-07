#!/usr/bin/env python3
"""
Create public ngrok tunnels to expose the Flask app to the internet.
Run this script while app.py is running on port 5000.
"""

import time
import subprocess
import sys

# You need to create a free account at https://ngrok.com and get an auth token
# Then run: ngrok config add-authtoken YOUR_TOKEN

print("=" * 80)
print("AI CAREER ASSISTANT - PUBLIC ACCESS SETUP")
print("=" * 80)
print()
print("Prerequisites:")
print("1. Create a free ngrok account at https://ngrok.com")
print("2. Get your auth token from https://dashboard.ngrok.com/auth")
print("3. Run: ngrok config add-authtoken YOUR_AUTH_TOKEN")
print("4. Make sure Flask app is running on http://127.0.0.1:5000")
print()
print("=" * 80)
print()

# Check if ngrok is available
try:
    result = subprocess.run(["ngrok", "--version"], capture_output=True, text=True)
    print(f"✓ ngrok is installed: {result.stdout.strip()}")
except FileNotFoundError:
    print("✗ ngrok CLI not found. Install from https://ngrok.com/download")
    sys.exit(1)

print()
print("Starting ngrok tunnel on port 5000...")
print("(Keep this terminal open while using the app)")
print()
print("=" * 80)
print()

# Start ngrok tunnel
try:
    subprocess.run(["ngrok", "http", "5000"])
except KeyboardInterrupt:
    print("\nTunnel closed.")
