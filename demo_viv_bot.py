#!/usr/bin/env python3
"""
Demo script for VIV Clinic Facebook Bot
Shows how the bot works with simulated conversations
"""

import time
from facebook_bot import FacebookBot
from google_sheets_manager import GoogleSheetsManager

def simulate_conversation():
    """Simulate a complete customer conversation"""
    print("🎭 VIV Clinic Bot Demo - Simulated Conversation")
    print("=" * 60)
    
    bot = FacebookBot()
    
    # Simulate customer conversation
    customer_id = "demo_customer_123"
    customer_name = "שרה לוי"
    
    print(f"👤 Customer: {customer_name} (ID: {customer_id})")
    print("📱 Platform: Facebook Messenger")
    print()
    
    # Step 1: Initial message
    print("💬 Step 1: Customer sends initial message")
    print("👤 Customer: שלום, אני מעוניינת במידע על טיפולי פנים")
    
    # Simulate bot processing (without actual Facebook API)
    print("🤖 Bot: Processing message...")
    
    # Mock the conversation state
    bot.conversations[customer_id] = {
        "stage": "greeting",
        "name": customer_name,
        "phone": None,
        "topic": None,
        "post_source": None
    }
    
    # Simulate greeting response
    greeting = f"שלום {customer_name}! 👋\nתודה שפנית לקליניקת VIV.\nאשמח לעזור לך עם השאלה שלך.\n\nכדי שנציגה שלנו תוכל לחזור אליך עם כל הפרטים, אשמח אם תשאיר מספר טלפון לחזרה 📞"
    
    print(f"🤖 Bot: {greeting}")
    print()
    
    # Update conversation state
    bot.conversations[customer_id]["stage"] = "waiting_phone"
    
    time.sleep(2)
    
    # Step 2: Customer provides phone
    print("💬 Step 2: Customer provides phone number")
    print("👤 Customer: 0501234567")
    
    phone = "0501234567"
    bot.conversations[customer_id]["phone"] = phone
    bot.conversations[customer_id]["stage"] = "waiting_topic"
    
    topic_request = "על איזה נושא תרצה לקבל מידע? (למשל: טיפולים, מחירים, זמינות וכו')"
    print(f"🤖 Bot: {topic_request}")
    print()
    
    time.sleep(2)
    
    # Step 3: Customer specifies topic
    print("💬 Step 3: Customer specifies inquiry topic")
    print("👤 Customer: מחירי טיפולי פנים ומתיחת עור")
    
    topic = "מחירי טיפולי פנים ומתיחת עור"
    bot.conversations[customer_id]["topic"] = topic
    bot.conversations[customer_id]["stage"] = "completed"
    
    # Simulate saving to Google Sheets
    print("📊 Bot: Saving to Google Sheets...")
    
    sheets = GoogleSheetsManager()
    customer_data = [
        "2025-06-07 14:20:00",  # timestamp
        customer_name,          # name
        phone,                  # phone
        topic,                  # topic
        "",                     # post source
        customer_id,            # facebook user id
        "ממתין לטיפול",         # status
        ""                      # notes
    ]
    
    sheets.add_customer_inquiry(customer_data)
    
    # Final confirmation
    confirmation = f"תודה רבה {customer_name}! 🙏\nקיבלתי את הפרטים שלך:\n📞 טלפון: {phone}\n📝 נושא: {topic}\n\nנציגה שלנו תחזור אליך בהקדם האפשרי ✨"
    
    print(f"🤖 Bot: {confirmation}")
    print()
    
    # Clear conversation
    del bot.conversations[customer_id]
    
    print("✅ Conversation completed successfully!")
    print("📋 Customer data saved to Google Sheets")
    print("🔔 Staff will be notified for follow-up")

def show_bot_features():
    """Show all bot features and capabilities"""
    print("\n🤖 VIV Clinic Bot Features")
    print("=" * 40)
    
    features = [
        "🔄 Auto-responds to Facebook messages and comments",
        "🇮🇱 Natural Hebrew conversation flow",
        "📞 Collects customer contact information",
        "📝 Records inquiry topics and interests",
        "📊 Saves all data to Google Sheets",
        "🔗 Real-time webhook integration",
        "⚡ Instant response to customer inquiries",
        "📱 Works on both Messenger and post comments",
        "🎯 Guides customers through information collection",
        "✅ Provides confirmation and next steps"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n📋 Conversation Flow:")
    print("  1. Customer sends message → Bot greets and asks for phone")
    print("  2. Customer provides phone → Bot asks for inquiry topic")
    print("  3. Customer specifies topic → Bot saves data and confirms")
    print("  4. Staff receives notification → Follow-up with customer")

def show_setup_summary():
    """Show setup requirements summary"""
    print("\n⚙️  Setup Requirements")
    print("=" * 30)
    
    print("📘 Facebook Setup:")
    print("  - Create Facebook App")
    print("  - Get Page Access Token")
    print("  - Configure webhook URL")
    print("  - Set verify token")
    
    print("\n📊 Google Sheets Setup:")
    print("  - Create Google Sheet")
    print("  - Get Google API key")
    print("  - Set up proper headers")
    print("  - Configure sheet permissions")
    
    print("\n🔑 Credentials Needed:")
    print("  - FACEBOOK_ACCESS_TOKEN")
    print("  - FACEBOOK_PAGE_ID")
    print("  - FACEBOOK_VERIFY_TOKEN")
    print("  - GOOGLE_API_KEY")
    print("  - GOOGLE_SHEET_ID")
    
    print("\n🚀 To Start:")
    print("  python3 start_viv_bot.py")

def main():
    """Main demo function"""
    print("🏥 VIV Clinic Facebook Bot - Demo")
    print("=" * 50)
    
    while True:
        print("\n📋 Demo Options:")
        print("1. Simulate customer conversation")
        print("2. Show bot features")
        print("3. Show setup summary")
        print("4. Exit")
        
        choice = input("\n💬 Choose option (1-4): ").strip()
        
        if choice == "1":
            simulate_conversation()
        elif choice == "2":
            show_bot_features()
        elif choice == "3":
            show_setup_summary()
        elif choice == "4":
            print("👋 Demo ended")
            break
        else:
            print("❌ Invalid choice, please try again")

if __name__ == "__main__":
    main()