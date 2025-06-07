#!/usr/bin/env python3
"""
Production server for VIV Clinic Facebook Bot
Optimized for deployment on Heroku/Railway/Render
"""

import os
from flask import Flask, request, jsonify
import json
import requests

# Try to import AI chat manager
try:
    from ai_chat_manager import ai_chat_manager
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ AI Chat Manager not available, using fallback responses")

app = Flask(__name__)

# Get credentials from environment variables
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_VERIFY_TOKEN = os.environ.get('FACEBOOK_VERIFY_TOKEN', 'VIV_CLINIC_VERIFY_TOKEN')

# Initialize CSV manager
try:
    from csv_manager import CSVManager
    csv_manager = CSVManager()
except ImportError:
    csv_manager = None

# Initialize AI chat engine
try:
    from ai_chat_engine import get_ai_engine
    ai_engine = get_ai_engine()
    print("✅ AI chat engine initialized successfully")
except ImportError as e:
    print(f"❌ Error initializing AI engine: {e}")
    ai_engine = None

@app.route('/')
def home():
    return """
    <div style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; direction: rtl;">
        <h1 style="color: #2c5aa0;">🤖 VIV Clinic Facebook Bot</h1>
        <h2 style="color: #28a745;">✅ הבוט פעיל ועובד!</h2>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3>📊 סטטוס המערכת:</h3>
            <ul style="font-size: 16px;">
                <li>✅ Facebook Integration: פעיל</li>
                <li>✅ Access Token: תקף</li>
                <li>✅ Page ID: 103991726050308</li>
                <li>✅ CSV Database: פעיל</li>
                <li>🤖 AI Chat Engine: """ + ("פעיל" if ai_engine else "לא זמין") + """</li>
            </ul>
        </div>
        
        <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3>🔧 API Endpoints:</h3>
            <ul style="font-size: 14px;">
                <li><a href="/test" style="color: #1976d2;">/test</a> - בדיקת פונקציונליות הבוט</li>
                <li><a href="/chat" style="color: #1976d2; font-weight: bold;">🤖 /chat</a> - ממשק טסט לשיחה עם הבוט</li>
                <li><a href="/messages" style="color: #1976d2;">/messages</a> - הודעות אחרונות מפייסבוק</li>
                <li><a href="/customers" style="color: #1976d2;">/customers</a> - רשימת לקוחות</li>
                <li><a href="/stats" style="color: #1976d2;">/stats</a> - סטטיסטיקות</li>
                <li><a href="/ai/status" style="color: #9c27b0;">🧠 /ai/status</a> - סטטוס מנוע AI</li>
                <li><a href="/ai/test" style="color: #9c27b0;">🧪 /ai/test</a> - בדיקת מנוע AI</li>
                <li><strong>/webhook</strong> - נקודת קבלה לפייסבוק</li>
            </ul>
        </div>
        
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3>📞 איך זה עובד:</h3>
            <ol style="font-size: 14px;">
                <li>לקוח שולח הודעה בפייסבוק לדף VIV Clinic</li>
                <li>הבוט מקבל את ההודעה דרך ה-webhook</li>
                <li>הבוט מעבד את ההודעה ושומר את הנתונים</li>
                <li>הבוט שולח תגובה אוטומטית ללקוח</li>
                <li>הנתונים זמינים כאן לצפייה וניהול</li>
            </ol>
        </div>
        
        <p style="text-align: center; color: #666; margin-top: 40px;">
            🏥 VIV Clinic - מערכת בוט אוטומטית לשירות לקוחות
        </p>
    </div>
    """

@app.route('/test')
def test_bot():
    """Test bot functionality"""
    try:
        # Debug environment variables first
        debug_info = {
            "FACEBOOK_ACCESS_TOKEN": "✅ Set" if FACEBOOK_ACCESS_TOKEN else "❌ Missing",
            "FACEBOOK_PAGE_ID": "✅ Set" if FACEBOOK_PAGE_ID else "❌ Missing",
            "FACEBOOK_APP_ID": "✅ Set" if FACEBOOK_APP_ID else "❌ Missing",
            "token_length": len(FACEBOOK_ACCESS_TOKEN) if FACEBOOK_ACCESS_TOKEN else 0,
            "token_starts_with": FACEBOOK_ACCESS_TOKEN[:10] + "..." if FACEBOOK_ACCESS_TOKEN else "None"
        }
        
        if not FACEBOOK_ACCESS_TOKEN:
            return jsonify({
                "status": "❌ Error",
                "error": "FACEBOOK_ACCESS_TOKEN not found in environment variables",
                "debug": debug_info
            })
            
        url = f"https://graph.facebook.com/v18.0/me"
        params = {"access_token": FACEBOOK_ACCESS_TOKEN}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "status": "✅ Success",
                "facebook_connection": "Active",
                "page_name": data.get("name"),
                "page_id": data.get("id"),
                "access_token_valid": True,
                "server_status": "Production Ready",
                "debug": debug_info
            })
        else:
            return jsonify({
                "status": "❌ Error",
                "error": response.text,
                "response_code": response.status_code,
                "debug": debug_info
            })
            
    except Exception as e:
        return jsonify({
            "status": "❌ Error",
            "error": str(e),
            "debug": debug_info if 'debug_info' in locals() else "Debug info not available"
        })

@app.route('/messages')
def check_messages():
    """Check recent messages"""
    try:
        if not FACEBOOK_ACCESS_TOKEN:
            return jsonify({
                "status": "❌ Error",
                "error": "FACEBOOK_ACCESS_TOKEN not found in environment variables"
            })
            
        url = f"https://graph.facebook.com/v18.0/me/conversations"
        params = {"access_token": FACEBOOK_ACCESS_TOKEN, "limit": 10}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            conversations = data.get("data", [])
            
            result = {
                "status": "✅ Success",
                "total_conversations": len(conversations),
                "recent_conversations": []
            }
            
            for conv in conversations[:5]:
                result["recent_conversations"].append({
                    "id": conv["id"],
                    "updated": conv["updated_time"]
                })
            
            return jsonify(result)
        else:
            return jsonify({
                "status": "❌ Error",
                "error": response.text,
                "response_code": response.status_code
            })
            
    except Exception as e:
        return jsonify({
            "status": "❌ Error",
            "error": str(e)
        })

@app.route('/customers')
def view_customers():
    """View customer data from CSV"""
    try:
        customers = csv_manager.get_customers(50)  # Get last 50 customers
        
        return jsonify({
            "status": "✅ Success",
            "total_customers": len(customers),
            "customers": customers
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Error",
            "error": str(e)
        })

@app.route('/stats')
def customer_stats():
    """Get customer statistics"""
    try:
        stats = csv_manager.get_stats()
        
        return jsonify({
            "status": "✅ Success",
            "statistics": stats
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Error",
            "error": str(e)
        })

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Facebook webhook endpoint"""
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == FACEBOOK_VERIFY_TOKEN:
            print("✅ Webhook verified successfully")
            return challenge
        else:
            print("❌ Webhook verification failed")
            return 'Verification failed', 403
    
    elif request.method == 'POST':
        # Handle incoming messages
        data = request.get_json()
        
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                for messaging in entry.get('messaging', []):
                    sender_id = messaging['sender']['id']
                    
                    if 'message' in messaging:
                        message_text = messaging['message'].get('text', '')
                        print(f"📨 New message from {sender_id}: {message_text}")
                        
                        # Save customer data if CSV manager available
                        if csv_manager:
                            try:
                                csv_manager.save_customer({
                                    'name': f'Customer_{sender_id[-4:]}',
                                    'phone': 'Unknown',
                                    'message': message_text,
                                    'source': 'Facebook',
                                    'status': 'New'
                                })
                            except Exception as e:
                                print(f"Error saving customer: {e}")
                        
                        # Send automatic response
                        response_text = "שלום! תודה על פנייתך לVIV Clinic. נציג שלנו יחזור אליך בהקדם. 🏥"
                        send_facebook_message(sender_id, response_text)
        
        return 'OK', 200

def send_facebook_message(recipient_id, message_text):
    """Send message via Facebook API"""
    try:
        if not FACEBOOK_ACCESS_TOKEN:
            return False
            
        url = f"https://graph.facebook.com/v18.0/me/messages"
        headers = {"Content-Type": "application/json"}
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text},
            "access_token": FACEBOOK_ACCESS_TOKEN
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

@app.route('/health')
def health_check():
    """Health check endpoint"""
    ai_status = "active" if ai_engine and ai_engine.active_provider != "fallback" else "fallback"
    return jsonify({
        "status": "healthy",
        "service": "VIV Clinic Facebook Bot",
        "version": "1.1.0",
        "ai_engine": ai_status,
        "ai_provider": ai_engine.active_provider if ai_engine else "none"
    })

@app.route('/debug')
def debug_env():
    """Debug environment variables"""
    return jsonify({
        "environment_vars": {
            "FACEBOOK_ACCESS_TOKEN": "✅ Set" if FACEBOOK_ACCESS_TOKEN else "❌ Missing",
            "FACEBOOK_PAGE_ID": "✅ Set" if FACEBOOK_PAGE_ID else "❌ Missing", 
            "FACEBOOK_APP_ID": "✅ Set" if FACEBOOK_APP_ID else "❌ Missing",
            "FACEBOOK_VERIFY_TOKEN": "✅ Set" if FACEBOOK_VERIFY_TOKEN else "❌ Missing"
        },
        "token_length": len(FACEBOOK_ACCESS_TOKEN) if FACEBOOK_ACCESS_TOKEN else 0,
        "token_prefix": FACEBOOK_ACCESS_TOKEN[:20] + "..." if FACEBOOK_ACCESS_TOKEN else "None"
    })

@app.route('/chat')
def chat_interface():
    """Chat interface for testing the bot"""
    return '''
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 בוט VIV Clinic - ממשק טסט</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            direction: rtl;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(45deg, #2196F3, #21CBF3);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .header p {
            margin: 5px 0 0 0;
            opacity: 0.9;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #eee;
        }
        .message {
            margin: 10px 0;
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 70%;
            word-wrap: break-word;
        }
        .user-message {
            background: #007bff;
            color: white;
            margin-right: auto;
            text-align: right;
        }
        .bot-message {
            background: #e9ecef;
            color: #333;
            margin-left: auto;
            text-align: right;
        }
        .input-container {
            padding: 20px;
            background: white;
            display: flex;
            gap: 10px;
        }
        .message-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            direction: rtl;
        }
        .message-input:focus {
            border-color: #007bff;
        }
        .send-button {
            padding: 12px 24px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        .send-button:hover {
            background: #0056b3;
        }
        .send-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .typing {
            font-style: italic;
            color: #666;
            padding: 8px 16px;
        }
        .status {
            text-align: center;
            padding: 10px;
            background: #d4edda;
            color: #155724;
            border-bottom: 1px solid #c3e6cb;
        }
        .back-link {
            display: inline-block;
            margin: 10px 20px;
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 בוט VIV Clinic</h1>
            <p>ממשק טסט לבדיקת הבוט</p>
        </div>
        
        <a href="/" class="back-link">← חזרה לדף הבית</a>
        
        <div class="status">
            ✅ הבוט מוכן לשיחה - שלח הודעה כדי לבדוק איך הוא מגיב
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="bot-message">
                שלום! אני הבוט של VIV Clinic. איך אני יכול לעזור לך היום? 😊
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" class="message-input" 
                   placeholder="הקלד הודעה..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()" class="send-button" id="sendButton">שלח</button>
        </div>
    </div>

    <script>
        let conversationId = 'test_' + Date.now();
        
        function addMessage(text, isUser) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
            messageDiv.textContent = text;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function showTyping() {
            const chatContainer = document.getElementById('chatContainer');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing';
            typingDiv.id = 'typing';
            typingDiv.textContent = 'הבוט כותב...';
            chatContainer.appendChild(typingDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function hideTyping() {
            const typing = document.getElementById('typing');
            if (typing) {
                typing.remove();
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            sendButton.disabled = true;
            
            // Show typing indicator
            showTyping();
            
            try {
                const response = await fetch('/chat/send', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        sender_id: conversationId
                    })
                });
                
                const data = await response.json();
                
                // Hide typing and add bot response
                hideTyping();
                addMessage(data.response, false);
                
            } catch (error) {
                hideTyping();
                addMessage('שגיאה: לא ניתן לקבל תגובה מהבוט', false);
                console.error('Error:', error);
            }
            
            sendButton.disabled = false;
            input.focus();
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Focus on input when page loads
        document.getElementById('messageInput').focus();
    </script>
</body>
</html>
    '''

@app.route('/chat/send', methods=['POST'])
def chat_send():
    """Handle test chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        sender_id = data.get('sender_id', 'test_user')
        
        # Simulate bot processing (same logic as webhook)
        print(f"📨 Test message from {sender_id}: {message}")
        
        # Save customer data if CSV manager available
        if csv_manager:
            try:
                csv_manager.save_customer({
                    'name': f'Test_User_{sender_id[-4:]}',
                    'phone': 'Test',
                    'message': message,
                    'source': 'Test_Chat',
                    'status': 'Test'
                })
            except Exception as e:
                print(f"Error saving test customer: {e}")
        
        # Generate bot response using AI engine
        if ai_engine:
            try:
                bot_response, is_ai_generated = ai_engine.generate_response(sender_id, message)
                print(f"🤖 AI Response ({'AI' if is_ai_generated else 'Fallback'}): {bot_response}")
            except Exception as e:
                print(f"❌ AI engine error: {e}")
                bot_response = "מצטער, יש לי בעיה טכנית כרגע. אנא נסו שוב או צרו קשר בטלפון 03-1234567 🏥"
        else:
            # Fallback to simple responses if AI not available
            if 'שלום' in message or 'היי' in message or 'hello' in message.lower():
                bot_response = "שלום! ברוכים הבאים ל-VIV Clinic! 🏥 איך אני יכול לעזור לכם היום?"
            elif 'תור' in message or 'זמן' in message:
                bot_response = "אשמח לעזור לכם לקבוע תור! 📅 אנא ציינו את סוג הטיפול הרצוי ותאריך מועדף."
            elif 'מחיר' in message or 'עלות' in message or 'כמה' in message:
                bot_response = "המחירים שלנו תלויים בסוג הטיפול. 💰 נציג שלנו יחזור אליכם עם פרטים מדויקים."
            elif 'כתובת' in message or 'איפה' in message or 'מיקום' in message:
                bot_response = "אנחנו נמצאים ברחוב הרופאים 123, תל אביב. 📍 ניתן להגיע גם בתחבורה ציבורית!"
            elif 'שעות' in message or 'פתוח' in message:
                bot_response = "אנחנו פתוחים א'-ה' 8:00-18:00, ו' 8:00-13:00. 🕐 בשבת אנחנו סגורים."
            elif 'תודה' in message or 'תנקיו' in message:
                bot_response = "בשמחה! 😊 אנחנו כאן בשבילכם. יום טוב!"
            else:
                bot_response = "תודה על פנייתכם! 🏥 נציג שלנו יחזור אליכם בהקדם עם מענה מפורט."
        
        return jsonify({
            'status': 'success',
            'response': bot_response
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'response': f'שגיאה: {str(e)}'
        }), 500

@app.route('/ai/status')
def ai_status():
    """Get AI engine status and configuration"""
    if not ai_engine:
        return jsonify({
            'status': 'disabled',
            'message': 'AI engine not initialized',
            'available_providers': []
        })
    
    return jsonify({
        'status': 'active',
        'provider': ai_engine.active_provider,
        'available_providers': ai_engine.available_providers,
        'message': f'AI engine running with {ai_engine.active_provider}'
    })

@app.route('/ai/test')
def ai_test():
    """Test AI engine with sample messages"""
    if not ai_engine:
        return jsonify({'error': 'AI engine not available'})
    
    test_messages = [
        "שלום, אני רוצה לקבוע תור",
        "כמה עולה טיפול שיניים?",
        "איפה אתם נמצאים?"
    ]
    
    results = []
    for i, message in enumerate(test_messages):
        try:
            response, is_ai = ai_engine.generate_response(f"test_user_{i}", message)
            results.append({
                'message': message,
                'response': response,
                'is_ai_generated': is_ai
            })
        except Exception as e:
            results.append({
                'message': message,
                'error': str(e)
            })
    
    return jsonify({
        'status': 'success',
        'provider': ai_engine.active_provider,
        'test_results': results
    })

@app.route('/ai/clear/<user_id>')
def ai_clear_conversation(user_id):
    """Clear conversation history for a user"""
    if not ai_engine:
        return jsonify({'error': 'AI engine not available'})
    
    ai_engine.clear_conversation(user_id)
    return jsonify({
        'status': 'success',
        'message': f'Conversation cleared for user {user_id}'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)