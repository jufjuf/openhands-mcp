#!/usr/bin/env python3
"""
AI Chat Manager for VIV Clinic Bot
Handles intelligent conversation using Google Gemini API
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

class AIChatManager:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
        # Conversation history storage (in production, use database)
        self.conversations = {}
        
        # VIV Clinic context and personality
        self.system_prompt = """
אתה עוזר וירטואלי של VIV Clinic - מרפאת שיניים מתקדמת.

פרטי המרפאה:
- שם: VIV Clinic
- כתובת: רחוב הרצל 45, תל אביב
- טלפון: 03-1234567
- שעות פתיחה: ראשון-חמישי 8:00-18:00, שישי 8:00-13:00
- שירותים: טיפולי שיניים כלליים, השתלות, יישור שיניים, הלבנה

האישיות שלך:
- מקצועי ואדיב
- מסביר בפשטות
- עוזר לקבוע תורים
- מספק מידע על טיפולים
- תמיד מנסה לעזור

הנחיות:
1. תמיד ענה בעברית
2. היה קצר ולעניין
3. אם לא יודע משהו, הפנה ליצירת קשר עם המרפאה
4. עודד לקבוע תור אם מתאים
5. תמיד היה חיובי ומועיל
"""

    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history for a user"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        return self.conversations[user_id]

    def add_to_history(self, user_id: str, role: str, content: str):
        """Add message to conversation history"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 messages to avoid token limits
        if len(self.conversations[user_id]) > 10:
            self.conversations[user_id] = self.conversations[user_id][-10:]

    def generate_response(self, user_message: str, user_id: str = "default") -> str:
        """Generate AI response using Google Gemini"""
        
        if not self.api_key:
            return self._fallback_response(user_message)
        
        try:
            # Get conversation history
            history = self.get_conversation_history(user_id)
            
            # Build conversation context
            conversation_text = self.system_prompt + "\n\nהיסטוריית השיחה:\n"
            
            for msg in history[-5:]:  # Last 5 messages for context
                role_hebrew = "לקוח" if msg["role"] == "user" else "עוזר"
                conversation_text += f"{role_hebrew}: {msg['content']}\n"
            
            conversation_text += f"לקוח: {user_message}\nעוזר:"
            
            # Prepare API request
            payload = {
                "contents": [{
                    "parts": [{
                        "text": conversation_text
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 200,
                    "stopSequences": ["לקוח:", "עוזר:"]
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    ai_response = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    
                    # Add to conversation history
                    self.add_to_history(user_id, "user", user_message)
                    self.add_to_history(user_id, "assistant", ai_response)
                    
                    return ai_response
                else:
                    return self._fallback_response(user_message)
            else:
                print(f"Gemini API Error: {response.status_code} - {response.text}")
                return self._fallback_response(user_message)
                
        except Exception as e:
            print(f"AI Chat Error: {str(e)}")
            return self._fallback_response(user_message)

    def _fallback_response(self, user_message: str) -> str:
        """Fallback responses when AI is not available"""
        
        message_lower = user_message.lower()
        
        # Greeting responses
        if any(word in message_lower for word in ['שלום', 'היי', 'בוקר טוב', 'ערב טוב']):
            return "שלום! ברוכים הבאים ל-VIV Clinic 🦷\nאיך אני יכול לעזור לכם היום?"
        
        # Appointment requests
        elif any(word in message_lower for word in ['תור', 'לקבוע', 'פגישה', 'מועד']):
            return "אשמח לעזור לכם לקבוע תור! 📅\nאנא צרו קשר:\n📞 03-1234567\nאו בקרו אותנו ברחוב הרצל 45, תל אביב"
        
        # Price inquiries
        elif any(word in message_lower for word in ['מחיר', 'עולה', 'כמה', 'עלות']):
            return "המחירים שלנו תלויים בסוג הטיפול 💰\nלמידע מדויק על מחירים, אנא צרו קשר:\n📞 03-1234567"
        
        # Location questions
        elif any(word in message_lower for word in ['איפה', 'כתובת', 'מיקום', 'נמצא']):
            return "🏥 VIV Clinic נמצאת ב:\nרחוב הרצל 45, תל אביב\n📞 03-1234567"
        
        # Opening hours
        elif any(word in message_lower for word in ['שעות', 'פתוח', 'סגור', 'מתי']):
            return "🕐 שעות הפתיחה שלנו:\nראשון-חמישי: 8:00-18:00\nשישי: 8:00-13:00\nשבת: סגור"
        
        # Thank you
        elif any(word in message_lower for word in ['תודה', 'תנקיו', 'אחלה']):
            return "בשמחה! 😊\nVIV Clinic תמיד כאן בשבילכם\nבריאות השיניים שלכם חשובה לנו! 🦷"
        
        # Default response
        else:
            return "תודה על הפנייה! 😊\nלמידע נוסף או לקביעת תור:\n📞 03-1234567\nרחוב הרצל 45, תל אביב"

    def clear_conversation(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            del self.conversations[user_id]

    def get_conversation_summary(self, user_id: str) -> Dict:
        """Get conversation summary and statistics"""
        history = self.get_conversation_history(user_id)
        
        return {
            "user_id": user_id,
            "message_count": len(history),
            "last_message": history[-1]["timestamp"] if history else None,
            "conversation_started": history[0]["timestamp"] if history else None
        }

# Global instance
ai_chat_manager = AIChatManager()