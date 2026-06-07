#!/usr/bin/env python3
import os
import sys
import time
sys.path.insert(0, r'C:\Users\kmdri\AppData\Local\Programs\Python\Python310\lib\site-packages')

from ngrok import ngrok as ngrok_sdk
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('NGROK_AUTHTOKEN')

if not token:
    print("ERROR: NGROK_AUTHTOKEN not in .env")
    sys.exit(1)

try:
    print("Starting ngrok...")
    ngrok_sdk.set_auth_token(token)
    listener = ngrok_sdk.connect(5000, "http")
    
    # Get URL
    url = None
    listener_str = str(listener)
    import re
    m = re.search(r'(https?://[a-zA-Z0-9\-]+\.ngrok[^"\'>`\s]+)', listener_str)
    if m:
        url = m.group(1)
    
    if not url and hasattr(listener, 'public_url'):
        url = listener.public_url
    
    if not url:
        print(f"Listener string: {listener_str}")
        url = "CHECK DASHBOARD"
    
    print("\n" + "="*80)
    print("✅ TUNNEL ACTIVE!")
    print("="*80)
    print(f"\nPublic URL: {url}\n")
    print("Share these 5 links:\n")
    for i in range(1, 6):
        if i == 1:
            print(f"{i}. {url}")
        elif i == 2:
            print(f"{i}. {url}/")
        else:
            print(f"{i}. {url}?user=friend{i-2}")
    print("\n" + "="*80)
    print("Keep this running! Press Ctrl+C to stop.\n")
    
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nStopped.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
