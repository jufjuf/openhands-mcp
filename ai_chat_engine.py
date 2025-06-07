#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Chat Engine for VIV Clinic Bot
Supports multiple AI providers: OpenAI, Google Gemini, Anthropic Claude
"""

import os
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class AIConfig:
    """Configuration for AI providers"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_URL = 'https://api.openai.com/v1/chat/completions'
    
    # Google Gemini Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-pro')
    GEMINI_URL = f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent'
    
    # Anthropic Claude Configuration
    CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
    CLAUDE_MODEL = os.environ.get('CLAUDE_MODEL', 'claude-3-haiku-20240307')
    CLAUDE_URL = 'https://api.anthropic.com/v1/messages'
    
    # Default provider priority
    DEFAULT_PROVIDER = os.environ.get('AI_PROVIDER', 'openai')  # openai, gemini, claude

class VIVClinicAI:
    """AI Chat Engine for VIV Clinic Bot"""
    
    def __init__(self):
        self.config = AIConfig()
        self.conversation_history = {}
        
        # VIV Clinic context and personality
        self.system_prompt = """
אתה בוט שירות לקוחות של VIV Clinic - מרפאת שיניים מתקדמת בתל אביב.

פרטי המרפאה:
- שם: VIV Clinic
- מיקום: רחוב הרופאים 123, תל אביב
- שעות פתיחה: א'-ה' 8:00-18:00, ו' 8:00-13:00, שבת סגור
- טלפון: 03-1234567
- שירותים: טיפולי שיניים כלליים, אורתודונטיה, השתלות, הלבנות, ניתוחים

האישיות שלך:
- מקצועי ואדיב
- מדבר עברית טבעית וחמה
- מסייע ללקוחות לקבוע תורים ולקבל מידע
- תמיד מציע לחזור עם שאלות נוספות
- משתמש באימוג'ים בצורה מתונה

המטרות שלך:
1. לעזור ללקוחות לקבוע תורים
2. לספק מידע על שירותים ומחירים
3. לענות על שאלות כלליות על המרפאה
4. לאסוף פרטי קשר של לקוחות פוטנציאליים
5. להפנות לצוות המרפאה במקרים מורכבים

חשוב: תמיד תענה בעברית, תהיה מועיל ומקצועי.
"""
        
        # Check which AI provider is available
        self.available_providers = self._check_available_providers()
        self.active_provider = self._select_provider()
        
        print(f"🤖 AI Engine initialized with provider: {self.active_provider}")
        print(f"📋 Available providers: {', '.join(self.available_providers)}")
    
    def _check_available_providers(self) -> List[str]:
        """Check which AI providers have valid API keys"""
        providers = []
        
        if self.config.OPENAI_API_KEY:
            providers.append('openai')
        if self.config.GEMINI_API_KEY:
            providers.append('gemini')
        if self.config.CLAUDE_API_KEY:
            providers.append('claude')
            
        return providers
    
    def _select_provider(self) -> str:
        """Select the best available AI provider"""
        if not self.available_providers:
            return 'fallback'
        
        # Try to use the preferred provider
        if self.config.DEFAULT_PROVIDER in self.available_providers:
            return self.config.DEFAULT_PROVIDER
        
        # Otherwise use the first available
        return self.available_providers[0]
    
    def _get_conversation_context(self, user_id: str) -> List[Dict]:
        """Get conversation history for context"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Keep only last 10 messages for context
        return self.conversation_history[user_id][-10:]
    
    def _save_message(self, user_id: str, role: str, content: str):
        """Save message to conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def _call_openai(self, messages: List[Dict]) -> str:
        """Call OpenAI GPT API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.config.OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.config.OPENAI_MODEL,
                'messages': [
                    {'role': 'system', 'content': self.system_prompt}
                ] + messages,
                'max_tokens': 500,
                'temperature': 0.7
            }
            
            response = requests.post(
                self.config.OPENAI_URL,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"❌ OpenAI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return None
    
    def _call_gemini(self, messages: List[Dict]) -> str:
        """Call Google Gemini API"""
        try:
            # Convert messages to Gemini format
            prompt_parts = [self.system_prompt]
            for msg in messages:
                role_prefix = "משתמש: " if msg['role'] == 'user' else "בוט: "
                prompt_parts.append(f"{role_prefix}{msg['content']}")
            
            full_prompt = "\n\n".join(prompt_parts)
            
            data = {
                'contents': [{
                    'parts': [{'text': full_prompt}]
                }],
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 500
                }
            }
            
            response = requests.post(
                f"{self.config.GEMINI_URL}?key={self.config.GEMINI_API_KEY}",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                print(f"❌ Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return None
    
    def _call_claude(self, messages: List[Dict]) -> str:
        """Call Anthropic Claude API"""
        try:
            headers = {
                'x-api-key': self.config.CLAUDE_API_KEY,
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
            
            # Convert messages to Claude format
            claude_messages = []
            for msg in messages:
                claude_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
            
            data = {
                'model': self.config.CLAUDE_MODEL,
                'max_tokens': 500,
                'system': self.system_prompt,
                'messages': claude_messages
            }
            
            response = requests.post(
                self.config.CLAUDE_URL,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['content'][0]['text'].strip()
            else:
                print(f"❌ Claude API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Claude error: {e}")
            return None
    
    def _fallback_response(self, message: str) -> str:
        """Fallback response when AI is not available"""
        message_lower = message.lower()
        
        # Smart fallback responses
        if any(word in message_lower for word in ['שלום', 'היי', 'בוקר', 'ערב']):
            return "שלום! ברוכים הבאים ל-VIV Clinic! 🏥 איך אני יכול לעזור לכם היום?"
        
        elif any(word in message_lower for word in ['תור', 'זמן', 'פגישה', 'לקבוע']):
            return "אשמח לעזור לכם לקבוע תור! 📅 אנא צרו קשר בטלפון 03-1234567 או ציינו את סוג הטיפול הרצוי."
        
        elif any(word in message_lower for word in ['מחיר', 'עלות', 'כמה', 'עולה']):
            return "המחירים שלנו תחרותיים ותלויים בסוג הטיפול. 💰 לפרטים מדויקים אנא צרו קשר: 03-1234567"
        
        elif any(word in message_lower for word in ['כתובת', 'איפה', 'מיקום', 'נמצא']):
            return "אנחנו נמצאים ברחוב הרופאים 123, תל אביב. 📍 קל להגיע אלינו בתחבורה ציבורית!"
        
        elif any(word in message_lower for word in ['שעות', 'פתוח', 'סגור', 'מתי']):
            return "שעות הפתיחה שלנו: א'-ה' 8:00-18:00, ו' 8:00-13:00. 🕐 בשבת אנחנו סגורים."
        
        elif any(word in message_lower for word in ['תודה', 'תנקיו', 'אסור']):
            return "בשמחה! 😊 אנחנו כאן בשבילכם. יום טוב!"
        
        else:
            return "תודה על פנייתכם ל-VIV Clinic! 🏥 נציג שלנו יחזור אליכם בהקדם. לשירות מיידי: 03-1234567"
    
    def generate_response(self, user_id: str, message: str) -> Tuple[str, bool]:
        """
        Generate AI response to user message
        Returns: (response_text, is_ai_generated)
        """
        try:
            # Save user message
            self._save_message(user_id, 'user', message)
            
            # Get conversation context
            context = self._get_conversation_context(user_id)
            
            # Convert to API format
            api_messages = []
            for msg in context:
                if msg['role'] in ['user', 'assistant']:
                    api_messages.append({
                        'role': msg['role'],
                        'content': msg['content']
                    })
            
            # Try AI providers
            response = None
            
            if self.active_provider == 'openai':
                response = self._call_openai(api_messages)
            elif self.active_provider == 'gemini':
                response = self._call_gemini(api_messages)
            elif self.active_provider == 'claude':
                response = self._call_claude(api_messages)
            
            # Use fallback if AI failed
            if not response:
                response = self._fallback_response(message)
                is_ai = False
            else:
                is_ai = True
            
            # Save bot response
            self._save_message(user_id, 'assistant', response)
            
            return response, is_ai
            
        except Exception as e:
            print(f"❌ Error generating AI response: {e}")
            return self._fallback_response(message), False
    
    def clear_conversation(self, user_id: str):
        """Clear conversation history for user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
    
    def get_conversation_summary(self, user_id: str) -> Dict:
        """Get conversation summary for analytics"""
        if user_id not in self.conversation_history:
            return {'message_count': 0, 'last_interaction': None}
        
        history = self.conversation_history[user_id]
        return {
            'message_count': len(history),
            'last_interaction': history[-1]['timestamp'] if history else None,
            'provider_used': self.active_provider
        }

# Global AI engine instance
ai_engine = None

def get_ai_engine():
    """Get or create AI engine instance"""
    global ai_engine
    if ai_engine is None:
        ai_engine = VIVClinicAI()
    return ai_engine

def test_ai_engine():
    """Test the AI engine with sample messages"""
    print("🧪 Testing AI Engine...")
    
    engine = get_ai_engine()
    
    test_messages = [
        "שלום, אני רוצה לקבוע תור",
        "כמה עולה טיפול שיניים?",
        "איפה אתם נמצאים?",
        "מתי אתם פתוחים?",
        "תודה רבה על העזרה!"
    ]
    
    for i, message in enumerate(test_messages):
        print(f"\n📨 Test {i+1}: {message}")
        response, is_ai = engine.generate_response(f"test_user_{i}", message)
        ai_status = "🤖 AI" if is_ai else "🔄 Fallback"
        print(f"🤖 Response ({ai_status}): {response}")

if __name__ == "__main__":
    test_ai_engine()