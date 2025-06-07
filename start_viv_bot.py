#!/usr/bin/env python3
"""
VIV Clinic Facebook Bot Launcher
Starts the Facebook bot with all necessary components
"""

import os
import sys
import time
import threading
from datetime import datetime
from facebook_webhook import app
from facebook_bot import FacebookBot
from google_sheets_manager import GoogleSheetsManager

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import flask
        print("✅ Flask available")
    except ImportError:
        print("❌ Flask not found. Installing...")
        os.system("pip install flask")
    
    try:
        import requests
        print("✅ Requests available")
    except ImportError:
        print("❌ Requests not found. Installing...")
        os.system("pip install requests")

def check_credentials():
    """Check if all required credentials are configured"""
    from password_manager import PasswordManager
    
    pm = PasswordManager()
    required_creds = [
        "FACEBOOK_ACCESS_TOKEN",
        "FACEBOOK_PAGE_ID", 
        "FACEBOOK_VERIFY_TOKEN",
        "GOOGLE_SHEET_ID"
    ]
    
    missing = []
    for cred in required_creds:
        if not pm.credentials.get(cred) or pm.credentials.get(cred).startswith("your_"):
            missing.append(cred)
    
    if missing:
        print("⚠️  Missing or incomplete credentials:")
        for cred in missing:
            print(f"   - {cred}")
        print("\n📝 Please update credentials.env with your actual values")
        return False
    
    print("✅ All credentials configured")
    return True

def setup_google_sheets():
    """Set up Google Sheets for customer data"""
    try:
        sheets = GoogleSheetsManager()
        sheets.create_sheet_if_not_exists()
        print("✅ Google Sheets ready")
        return True
    except Exception as e:
        print(f"⚠️  Google Sheets setup issue: {e}")
        return False

def test_facebook_connection():
    """Test Facebook API connection"""
    try:
        bot = FacebookBot()
        # Try to get page info
        page_token = bot.get_page_access_token()
        if page_token:
            print("✅ Facebook connection successful")
            return True
        else:
            print("⚠️  Facebook connection issue")
            return False
    except Exception as e:
        print(f"⚠️  Facebook connection error: {e}")
        return False

def start_webhook_server():
    """Start the webhook server"""
    print("🚀 Starting webhook server...")
    print("📡 Webhook URL: https://work-1-zfogegygfxxaveky.prod-runtime.all-hands.dev/webhook")
    print("🏥 Health Check: https://work-1-zfogegygfxxaveky.prod-runtime.all-hands.dev/health")
    
    app.run(
        host='0.0.0.0',
        port=12000,
        debug=False,
        use_reloader=False
    )

def monitor_conversations():
    """Monitor and log active conversations"""
    bot = FacebookBot()
    
    while True:
        try:
            active_count = len(bot.conversations)
            if active_count > 0:
                print(f"💬 Active conversations: {active_count}")
                for user_id, conv in bot.conversations.items():
                    print(f"   - {conv.get('name', 'Unknown')}: {conv.get('stage', 'unknown')}")
            
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            time.sleep(60)

def main():
    """Main function"""
    print("🏥 VIV Clinic Facebook Bot")
    print("=" * 50)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    check_dependencies()
    
    # Check credentials
    print("\n🔑 Checking credentials...")
    if not check_credentials():
        print("\n❌ Cannot start bot without proper credentials")
        print("📝 Please configure credentials.env and try again")
        return
    
    # Setup Google Sheets
    print("\n📊 Setting up Google Sheets...")
    setup_google_sheets()
    
    # Test Facebook connection
    print("\n📘 Testing Facebook connection...")
    test_facebook_connection()
    
    print("\n" + "=" * 50)
    print("🤖 VIV CLINIC BOT READY")
    print("=" * 50)
    
    print("\n📋 Bot Features:")
    print("✅ Responds to Facebook Messenger messages")
    print("✅ Replies to Facebook post comments") 
    print("✅ Collects customer information (name, phone, topic)")
    print("✅ Saves data to Google Sheets")
    print("✅ Hebrew language support")
    
    print("\n🔧 Setup Instructions:")
    print("1. Configure Facebook App webhook URL:")
    print("   https://work-1-zfogegygfxxaveky.prod-runtime.all-hands.dev/webhook")
    print("2. Set verify token: VIV_CLINIC_2024")
    print("3. Subscribe to: messages, messaging_postbacks, feed")
    
    try:
        # Start monitoring in background
        monitor_thread = threading.Thread(target=monitor_conversations, daemon=True)
        monitor_thread.start()
        
        # Start webhook server (this blocks)
        start_webhook_server()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")

if __name__ == "__main__":
    main()