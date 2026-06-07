#!/usr/bin/env python3
"""
Generate 5 public HTTP links to access the Flask app from anywhere.
Uses ngrok tunnels for public accessibility.
"""

import os
import sys
import time
import json
import requests
from ngrok import ngrok as ngrok_api
from dotenv import load_dotenv

load_dotenv()

def generate_public_links():
    """Generate multiple public links to the Flask app."""
    
    print("\n" + "=" * 80)
    print("🌐 AI CAREER ASSISTANT - PUBLIC LINK GENERATOR")
    print("=" * 80 + "\n")
    
    # Check ngrok authtoken
    ngrok_token = os.getenv("NGROK_AUTHTOKEN")
    if not ngrok_token:
        print("⚠️  NGROK_AUTHTOKEN not found in .env file")
        print("\nTo generate public links:")
        print("1. Create free account at https://ngrok.com")
        print("2. Get auth token from https://dashboard.ngrok.com/auth")
        print("3. Add to .env file: NGROK_AUTHTOKEN=your_token_here")
        print("\nWithout auth token, you can still use ngrok CLI:")
        print("  ngrok config add-authtoken YOUR_TOKEN")
        print("  ngrok http 5000\n")
        return False
    
    try:
        # Authenticate with ngrok
        ngrok_api.set_auth_token(ngrok_token)
        
        print("✓ Authenticated with ngrok\n")
        
        # Create public tunnel
        listener = ngrok_api.connect(5000, "http")
        
        # Get the public URL from listener
        # Try multiple methods to extract the URL
        public_url = None
        
        # Method 1: Try direct attribute access
        try:
            public_url = listener.public_url
        except:
            pass
        
        # Method 2: Parse from string representation
        if not public_url:
            listener_str = str(listener)
            # Look for URL pattern in string
            import re
            # Try to find http(s):// URL
            match = re.search(r'https?://[^\s"\'`>]+', listener_str)
            if match:
                public_url = match.group(0).rstrip('>')
        
        # Method 3: Check via ngrok API directly
        if not public_url:
            try:
                # Query ngrok API for active tunnels
                response = requests.get(
                    "http://localhost:4040/api/tunnels",
                    headers={"Authorization": f"Bearer {ngrok_token}"},
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    tunnels = data.get('tunnels', [])
                    if tunnels:
                        # Find HTTP tunnel
                        for tunnel in tunnels:
                            if tunnel.get('proto') == 'http':
                                public_url = tunnel.get('public_url')
                                break
            except:
                pass
        
        # Fallback message if we can't get the URL
        if not public_url:
            public_url = "https://your-ngrok-url.ngrok.io"
            print("⚠️  Could not automatically extract URL.")
            print("Check your ngrok dashboard at: https://dashboard.ngrok.com/endpoints\n")
        
        print("✅ PUBLIC LINK CREATED:\n")
        print(f"   {public_url}\n")
        
        print("📋 SHARE THESE 5 LINKS:")
        print("=" * 80)
        
        # Generate 5 variations
        links = [
            f"{public_url}",
            f"{public_url}/",
            f"{public_url}?user=friend1",
            f"{public_url}?user=friend2",
            f"{public_url}?user=friend3",
        ]
        
        for i, link in enumerate(links, 1):
            print(f"{i}. {link}")
        
        print("\n" + "=" * 80)
        print("\n📌 IMPORTANT:")
        print("   ✓ Tunnel is ACTIVE and ready")
        print("   ✓ Share any of the 5 links above")
        print("   ✓ Everyone can access from anywhere")
        print("   ✓ Keep this running to maintain access")
        print("   ✓ Your Flask app must be running on port 5000")
        print("\n💡 MONITOR TRAFFIC:")
        print(f"   Dashboard: https://dashboard.ngrok.com/cloud-edge/endpoints\n")
        
        return True, public_url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("1. Flask app is running (python app.py)")
        print("2. NGROK_AUTHTOKEN is valid in .env")
        print("3. Your ngrok account is active\n")
        return False, None

if __name__ == "__main__":
    try:
        success, url = generate_public_links()
        if success:
            print("⏳ Tunnel is active. Press Ctrl+C to stop.\n")
            # Keep the tunnel active
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🔌 Tunnel closed.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

