#!/usr/bin/env python3
"""
Facebook Business Bot for VIV Clinic
Handles customer inquiries on Facebook Messenger and post comments
Collects customer information and updates Google Sheets
"""

import json
import time
import requests
import re
from datetime import datetime
from password_manager import PasswordManager
from csv_manager import CSVManager
try:
    from ai_chat_engine import get_ai_engine
    ai_engine = get_ai_engine()
    AI_AVAILABLE = True
except ImportError:
    ai_engine = None
    AI_AVAILABLE = False
    print("⚠️ AI Chat Engine not available, using fallback responses")

class FacebookBot:
    def __init__(self):
        self.pm = PasswordManager()
        self.csv_manager = CSVManager()
        self.access_token = self.pm.get_api_key("facebook")
        self.page_id = self.pm.credentials.get("FACEBOOK_PAGE_ID")
        self.base_url = "https://graph.facebook.com/v18.0"
        
        # Bot responses in Hebrew
        self.responses = {
            "greeting": "שלום {name}! 👋\nתודה שפנית לקליניקת VIV.\nאשמח לעזור לך עם השאלה שלך.",
            "ask_phone": "כדי שנציגה שלנו תוכל לחזור אליך עם כל הפרטים, אשמח אם תשאיר מספר טלפון לחזרה 📞",
            "ask_topic": "על איזה נושא תרצה לקבל מידע? (למשל: טיפולים, מחירים, זמינות וכו')",
            "confirmation": "תודה רבה {name}! 🙏\nקיבלתי את הפרטים שלך:\n📞 טלפון: {phone}\n📝 נושא: {topic}\n\nנציגה שלנו תחזור אליך בהקדם האפשרי ✨",
            "error": "מצטער, נתקלתי בבעיה טכנית. אנא נסה שוב או צור קשר ישירות בטלפון 📞"
        }
        
        # Conversation states
        self.conversations = {}
        
    def get_page_access_token(self):
        """Get page access token - we already have it"""
        # הטוקן שיש לנו כבר הוא Page Access Token
        return self.access_token
    
    def send_message(self, recipient_id, message):
        """Send message via Facebook Messenger"""
        try:
            url = f"{self.base_url}/me/messages"
            
            payload = {
                "recipient": {"id": recipient_id},
                "message": {"text": message},
                "access_token": self.access_token
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"✅ Message sent to {recipient_id}")
                return True
            else:
                print(f"❌ Failed to send message: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def reply_to_comment(self, comment_id, message):
        """Reply to a Facebook post comment"""
        try:
            page_token = self.get_page_access_token()
            url = f"{self.base_url}/{comment_id}/comments"
            
            payload = {
                "message": message,
                "access_token": page_token
            }
            
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                print(f"✅ Reply sent to comment {comment_id}")
                return True
            else:
                print(f"❌ Failed to reply to comment: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error replying to comment: {e}")
            return False
    
    def extract_phone_number(self, text):
        """Extract phone number from text"""
        # Hebrew phone number patterns
        patterns = [
            r'0\d{1,2}-?\d{7}',  # Israeli format
            r'\+972-?\d{1,2}-?\d{7}',  # International format
            r'05\d-?\d{7}',  # Mobile format
            r'\d{10}',  # 10 digits
            r'\d{3}-?\d{7}'  # 3-7 format
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group().replace('-', '').replace(' ', '')
        
        return None
    
    def extract_name_from_profile(self, user_id):
        """Get user's name from Facebook profile"""
        try:
            url = f"{self.base_url}/{user_id}"
            params = {
                "fields": "first_name,last_name",
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "first_name" in data:
                name = data["first_name"]
                if "last_name" in data:
                    name += f" {data['last_name']}"
                return name
            
            return "לקוח"
            
        except Exception as e:
            print(f"❌ Error getting user name: {e}")
            return "לקוח"
    
    def get_conversation_state(self, user_id):
        """Get current conversation state for user"""
        return self.conversations.get(user_id, {
            "stage": "greeting",
            "name": None,
            "phone": None,
            "topic": None,
            "post_source": None
        })
    
    def update_conversation_state(self, user_id, updates):
        """Update conversation state for user"""
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                "stage": "greeting",
                "name": None,
                "phone": None,
                "topic": None,
                "post_source": None
            }
        
        self.conversations[user_id].update(updates)
    
    def _fallback_response(self, message_text):
        """Fallback response when AI is not available"""
        message_lower = message_text.lower()
        
        # Smart fallback responses
        if any(word in message_lower for word in ['שלום', 'היי', 'בוקר', 'ערב']):
            return "שלום! ברוכים הבאים ל-VIV Clinic! 🏥 איך אני יכול לעזור לכם היום?"
        
        elif any(word in message_lower for word in ['תור', 'זמן', 'פגישה', 'לקבוע']):
            return "אשמח לעזור לכם לקבוע תור! 📅 אנא צרו קשר בטלפון 03-1234567 או ציינו את סוג הטיפול הרצוי."
        
        elif any(word in message_lower for word in ['מחיר', 'עלות', 'כמה', 'עולה']):
            return "המחירים שלנו תחרותיים ותלויים בסוג הטיפול. 💰 לפרטים מדויקים אנא צרו קשר: 03-1234567"
        
        elif any(word in message_lower for word in ['כתובת', 'איפה', 'מיקום', 'נמצא']):
            return "🏥 VIV Clinic נמצאת ב:\nרחוב הרצל 45, תל אביב\n📞 03-1234567"
        
        elif any(word in message_lower for word in ['שעות', 'פתוח', 'סגור', 'מתי']):
            return "🕐 שעות הפתיחה שלנו:\nראשון-חמישי: 8:00-18:00\nשישי: 8:00-13:00\nשבת: סגור"
        
        elif any(word in message_lower for word in ['תודה', 'תנקיו', 'אסור']):
            return "בשמחה! 😊 VIV Clinic תמיד כאן בשבילכם!"
        
        else:
            return "תודה על פנייתכם ל-VIV Clinic! 🏥 נציג שלנו יחזור אליכם בהקדם. לשירות מיידי: 03-1234567"
    
    def process_message(self, user_id, message_text, source_type="messenger", post_id=None):
        """Process incoming message and respond appropriately using AI"""
        try:
            # Get user info
            user_name = self.extract_name_from_profile(user_id)
            
            # Generate AI response
            if AI_AVAILABLE and ai_engine:
                ai_response, is_ai_generated = ai_engine.generate_response(user_id, message_text)
                print(f"🤖 AI Response ({'AI' if is_ai_generated else 'Fallback'}): {ai_response}")
            else:
                ai_response = self._fallback_response(message_text)
            
            # Check if user provided contact info during conversation
            phone = self.extract_phone_number(message_text)
            
            # Save conversation data if we have contact info
            if phone or any(keyword in message_text.lower() for keyword in ['תור', 'לקבוע', 'פגישה']):
                customer_data = {
                    "name": user_name,
                    "phone": phone if phone else "לא סופק",
                    "topic": message_text[:100],  # First 100 chars as topic
                    "source": f"Facebook_{source_type}",
                    "post_id": post_id if post_id else "N/A",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Save to CSV
                self.save_to_csv(user_id, customer_data)
                
                # Add contact collection message if no phone provided
                if not phone and any(keyword in message_text.lower() for keyword in ['תור', 'לקבוע', 'פגישה']):
                    ai_response += "\n\n📞 כדי לקבוע תור, אשמח אם תשאיר מספר טלפון לחזרה או תתקשר ישירות: 03-1234567"
            
            # Send response
            if source_type == "messenger":
                self.send_message(user_id, ai_response)
            else:
                return ai_response
                
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            error_response = self.responses["error"]
            
            if source_type == "messenger":
                self.send_message(user_id, error_response)
            else:
                return error_response
    
    def save_to_csv(self, user_id, conversation):
        """Save conversation data to CSV file"""
        try:
            # Add customer to CSV
            success = self.csv_manager.add_customer(
                name=conversation.get("name", ""),
                phone=conversation.get("phone", ""),
                topic=conversation.get("topic", ""),
                source="Facebook",
                status="ממתין לטיפול",
                notes=f"Facebook User ID: {user_id}"
            )
            
            if success:
                print(f"✅ Data saved to CSV for {conversation['name']}")
            else:
                print(f"❌ Failed to save data to CSV")
                
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
    
    def get_recent_messages(self):
        """Get recent messages from Facebook page"""
        try:
            page_token = self.get_page_access_token()
            url = f"{self.base_url}/me/conversations"
            
            params = {
                "fields": "participants,updated_time,message_count",
                "access_token": page_token
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "data" in data:
                return data["data"]
            
            return []
            
        except Exception as e:
            print(f"❌ Error getting messages: {e}")
            return []
    
    def get_recent_comments(self):
        """Get recent comments on page posts"""
        try:
            page_token = self.get_page_access_token()
            url = f"{self.base_url}/me/posts"
            
            params = {
                "fields": "comments{from,message,created_time,id}",
                "access_token": page_token
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            comments = []
            if "data" in data:
                for post in data["data"]:
                    if "comments" in post and "data" in post["comments"]:
                        for comment in post["comments"]["data"]:
                            comment["post_id"] = post["id"]
                            comments.append(comment)
            
            return comments
            
        except Exception as e:
            print(f"❌ Error getting comments: {e}")
            return []

def main():
    """Main function for testing"""
    bot = FacebookBot()
    
    print("🤖 VIV Clinic Facebook Bot Started")
    print("📋 Available commands:")
    print("  - test_message: Test message processing")
    print("  - check_messages: Check for new messages")
    print("  - check_comments: Check for new comments")
    
    while True:
        try:
            command = input("\n💬 Enter command (or 'quit' to exit): ").strip().lower()
            
            if command == "quit":
                break
            elif command == "test_message":
                user_id = input("Enter user ID: ")
                message = input("Enter message: ")
                bot.process_message(user_id, message)
            elif command == "check_messages":
                messages = bot.get_recent_messages()
                print(f"📨 Found {len(messages)} conversations")
            elif command == "check_comments":
                comments = bot.get_recent_comments()
                print(f"💬 Found {len(comments)} comments")
            else:
                print("❌ Unknown command")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Bot stopped")

if __name__ == "__main__":
    main()