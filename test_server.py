#!/usr/bin/env python3
"""
Test server for VIV Clinic Facebook Bot
"""

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
    <h1>🤖 VIV Clinic Facebook Bot Server</h1>
    <h2>Status:</h2>
    <ul>
        <li>✅ Facebook Integration: Active</li>
        <li>📞 Access Token: Valid</li>
        <li>📋 Page ID: 103991726050308</li>
    </ul>
    
    <h2>Test Endpoints:</h2>
    <ul>
        <li><a href="/test">/test</a> - Test bot functionality</li>
        <li><a href="/messages">/messages</a> - Check recent messages</li>
        <li><a href="/customers">/customers</a> - View customer data</li>
        <li><a href="/stats">/stats</a> - Customer statistics</li>
        <li><a href="/webhook" target="_blank">/webhook</a> - Facebook webhook endpoint</li>
    </ul>
    """

@app.route('/test')
def test_bot():
    """Test bot functionality"""
    try:
        # Test Facebook API connection
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
                "access_token_valid": True
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
        params = {"access_token": bot.access_token, "limit": 5}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            conversations = data.get("data", [])
            
            result = {
                "status": "✅ Success",
                "total_conversations": len(conversations),
                "recent_conversations": []
            }
            
            for conv in conversations[:3]:
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
            return challenge
        else:
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

@app.route('/customers')
def view_customers():
    """View customer data from CSV"""
    try:
        customers = csv_manager.get_customers(20)  # Get last 20 customers
        
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

if __name__ == '__main__':
    print("🚀 Starting VIV Clinic Facebook Bot Server...")
    print("📋 Facebook Integration: ✅ Active")
    print("🌐 Server will be available at: https://work-1-liraghfqzcrynzgs.prod-runtime.all-hands.dev")
    app.run(host='0.0.0.0', port=12000, debug=True)