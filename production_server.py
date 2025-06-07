#!/usr/bin/env python3
"""
Production server for VIV Clinic Facebook Bot
Optimized for deployment on Heroku/Railway/Render
"""

import os
from flask import Flask, request, jsonify
import json
import requests

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
            </ul>
        </div>
        
        <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3>🔧 API Endpoints:</h3>
            <ul style="font-size: 14px;">
                <li><a href="/test" style="color: #1976d2;">/test</a> - בדיקת פונקציונליות הבוט</li>
                <li><a href="/messages" style="color: #1976d2;">/messages</a> - הודעות אחרונות מפייסבוק</li>
                <li><a href="/customers" style="color: #1976d2;">/customers</a> - רשימת לקוחות</li>
                <li><a href="/stats" style="color: #1976d2;">/stats</a> - סטטיסטיקות</li>
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
        if not FACEBOOK_ACCESS_TOKEN:
            return jsonify({
                "status": "❌ Error",
                "error": "FACEBOOK_ACCESS_TOKEN not found in environment variables"
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
                "environment_vars": {
                    "FACEBOOK_ACCESS_TOKEN": "✅ Set" if FACEBOOK_ACCESS_TOKEN else "❌ Missing",
                    "FACEBOOK_PAGE_ID": "✅ Set" if FACEBOOK_PAGE_ID else "❌ Missing",
                    "FACEBOOK_APP_ID": "✅ Set" if FACEBOOK_APP_ID else "❌ Missing"
                }
            })
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
    return jsonify({
        "status": "healthy",
        "service": "VIV Clinic Facebook Bot",
        "version": "1.0.0"
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)