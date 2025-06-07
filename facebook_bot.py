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
    
    def process_message(self, user_id, message_text, source_type="messenger", post_id=None):
        """Process incoming message and respond appropriately"""
        try:
            # Get user info
            user_name = self.extract_name_from_profile(user_id)
            conversation = self.get_conversation_state(user_id)
            
            # Update name if not set
            if not conversation["name"]:
                conversation["name"] = user_name
                self.update_conversation_state(user_id, {"name": user_name})
            
            # Set post source if from comment
            if source_type == "comment" and post_id:
                conversation["post_source"] = post_id
                self.update_conversation_state(user_id, {"post_source": post_id})
            
            # Process based on conversation stage
            if conversation["stage"] == "greeting":
                # Send greeting and ask for phone
                response = self.responses["greeting"].format(name=user_name)
                response += "\n\n" + self.responses["ask_phone"]
                
                if source_type == "messenger":
                    self.send_message(user_id, response)
                else:
                    return response
                
                self.update_conversation_state(user_id, {"stage": "waiting_phone"})
                
            elif conversation["stage"] == "waiting_phone":
                # Check if message contains phone number
                phone = self.extract_phone_number(message_text)
                
                if phone:
                    self.update_conversation_state(user_id, {
                        "phone": phone,
                        "stage": "waiting_topic"
                    })
                    
                    response = self.responses["ask_topic"]
                    
                    if source_type == "messenger":
                        self.send_message(user_id, response)
                    else:
                        return response
                else:
                    # Ask for phone again
                    response = "לא זיהיתי מספר טלפון בהודעה. " + self.responses["ask_phone"]
                    
                    if source_type == "messenger":
                        self.send_message(user_id, response)
                    else:
                        return response
                        
            elif conversation["stage"] == "waiting_topic":
                # Save topic and complete conversation
                self.update_conversation_state(user_id, {
                    "topic": message_text,
                    "stage": "completed"
                })
                
                # Save to Google Sheets
                self.save_to_csv(user_id, conversation)
                
                # Send confirmation
                response = self.responses["confirmation"].format(
                    name=conversation["name"],
                    phone=conversation["phone"],
                    topic=message_text
                )
                
                if source_type == "messenger":
                    self.send_message(user_id, response)
                else:
                    return response
                
                # Reset conversation
                del self.conversations[user_id]
                
            else:
                # Conversation completed, start new one
                self.conversations[user_id] = {
                    "stage": "greeting",
                    "name": user_name,
                    "phone": None,
                    "topic": None,
                    "post_source": post_id
                }
                return self.process_message(user_id, message_text, source_type, post_id)
                
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