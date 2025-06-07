#!/usr/bin/env python3
"""
Production server for VIV Clinic Facebook Bot
Optimized for deployment on Heroku/Railway/Render
"""

import os
from flask import Flask, request, jsonify
from facebook_bot import FacebookBot
from csv_manager import CSVManager
import json

app = Flask(__name__)
bot = FacebookBot()
csv_manager = CSVManager()

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
        import requests
        url = f"https://graph.facebook.com/v18.0/me"
        params = {"access_token": bot.access_token}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "status": "✅ Success",
                "facebook_connection": "Active",
                "page_name": data.get("name"),
                "page_id": data.get("id"),
                "access_token_valid": True,
                "server_status": "Production Ready"
            })
        else:
            return jsonify({
                "status": "❌ Error",
                "error": response.text
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
        import requests
        url = f"https://graph.facebook.com/v18.0/me/conversations"
        params = {"access_token": bot.access_token, "limit": 10}
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
                "error": response.text
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
        verify_token = "VIV_CLINIC_VERIFY_TOKEN"
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == verify_token:
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
                        
                        # Process message with bot
                        response = bot.process_message(sender_id, message_text)
                        if response:
                            bot.send_message(sender_id, response)
        
        return 'OK', 200

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "VIV Clinic Facebook Bot",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)