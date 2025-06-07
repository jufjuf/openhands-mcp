#!/usr/bin/env python3
"""
Facebook Webhook Server for VIV Clinic
Receives real-time notifications from Facebook
Handles messages and comments automatically
"""

import json
import hashlib
import hmac
from datetime import datetime
from flask import Flask, request, jsonify
from facebook_bot import FacebookBot
from password_manager import PasswordManager

app = Flask(__name__)

# Initialize bot and credentials
bot = FacebookBot()
pm = PasswordManager()
VERIFY_TOKEN = pm.credentials.get("FACEBOOK_VERIFY_TOKEN", "VIV_CLINIC_2024")
APP_SECRET = pm.credentials.get("FACEBOOK_APP_SECRET")

def verify_signature(payload, signature):
    """Verify that the payload was sent from Facebook"""
    if not APP_SECRET:
        print("⚠️  No app secret configured")
        return True  # Skip verification in development
    
    expected_signature = hmac.new(
        APP_SECRET.encode('utf-8'),
        payload,
        hashlib.sha1
    ).hexdigest()
    
    return hmac.compare_digest(f"sha1={expected_signature}", signature)

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """Verify webhook with Facebook"""
    try:
        # Facebook sends these parameters for verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        print(f"🔍 Webhook verification request:")
        print(f"   Mode: {mode}")
        print(f"   Token: {token}")
        print(f"   Challenge: {challenge}")
        
        # Check if the mode and token are correct
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("✅ Webhook verified successfully")
            return challenge
        else:
            print("❌ Webhook verification failed")
            return "Verification failed", 403
            
    except Exception as e:
        print(f"❌ Error in webhook verification: {e}")
        return "Error", 500

@app.route('/webhook', methods=['POST'])
def webhook_receive():
    """Receive webhook notifications from Facebook"""
    try:
        # Verify the signature
        signature = request.headers.get('X-Hub-Signature')
        if signature and not verify_signature(request.data, signature):
            print("❌ Invalid signature")
            return "Invalid signature", 403
        
        # Parse the JSON payload
        data = request.get_json()
        
        if not data:
            print("❌ No data received")
            return "No data", 400
        
        print(f"📨 Received webhook data: {json.dumps(data, indent=2)}")
        
        # Process the webhook data
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                process_page_entry(entry)
        
        return "OK", 200
        
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return "Error", 500

def process_page_entry(entry):
    """Process a page entry from the webhook"""
    try:
        page_id = entry.get('id')
        print(f"📄 Processing entry for page: {page_id}")
        
        # Handle messages
        if 'messaging' in entry:
            for messaging_event in entry['messaging']:
                process_messaging_event(messaging_event)
        
        # Handle comments
        if 'changes' in entry:
            for change in entry['changes']:
                if change.get('field') == 'feed':
                    process_feed_change(change)
                    
    except Exception as e:
        print(f"❌ Error processing page entry: {e}")

def process_messaging_event(messaging_event):
    """Process a messaging event (private message)"""
    try:
        sender_id = messaging_event.get('sender', {}).get('id')
        recipient_id = messaging_event.get('recipient', {}).get('id')
        
        print(f"💬 Message event - Sender: {sender_id}, Recipient: {recipient_id}")
        
        # Handle incoming messages
        if 'message' in messaging_event:
            message = messaging_event['message']
            message_text = message.get('text', '')
            
            if message_text and sender_id:
                print(f"📝 Received message: {message_text}")
                
                # Process the message with the bot
                bot.process_message(sender_id, message_text, source_type="messenger")
        
        # Handle postbacks (button clicks)
        elif 'postback' in messaging_event:
            postback = messaging_event['postback']
            payload = postback.get('payload', '')
            
            print(f"🔘 Received postback: {payload}")
            
            # Handle postback as a message
            if payload and sender_id:
                bot.process_message(sender_id, payload, source_type="messenger")
                
    except Exception as e:
        print(f"❌ Error processing messaging event: {e}")

def process_feed_change(change):
    """Process a feed change (comment on post)"""
    try:
        value = change.get('value', {})
        
        # Handle new comments
        if value.get('verb') == 'add' and value.get('item') == 'comment':
            comment_id = value.get('comment_id')
            post_id = value.get('post_id')
            sender_id = value.get('sender_id')
            message = value.get('message', '')
            
            print(f"💬 New comment - Post: {post_id}, Comment: {comment_id}")
            print(f"📝 Comment text: {message}")
            
            if sender_id and message:
                # Process the comment with the bot
                response = bot.process_message(
                    sender_id, 
                    message, 
                    source_type="comment", 
                    post_id=post_id
                )
                
                # Reply to the comment if we got a response
                if response:
                    bot.reply_to_comment(comment_id, response)
                    
    except Exception as e:
        print(f"❌ Error processing feed change: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "VIV Clinic Facebook Bot",
        "timestamp": str(datetime.now())
    })

@app.route('/test', methods=['POST'])
def test_bot():
    """Test endpoint for manual testing"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'test_user')
        message = data.get('message', 'שלום')
        
        print(f"🧪 Test message from {user_id}: {message}")
        
        # Process with bot
        bot.process_message(user_id, message)
        
        return jsonify({"status": "success", "message": "Test completed"})
        
    except Exception as e:
        print(f"❌ Error in test: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Get current active conversations"""
    try:
        conversations = bot.conversations
        return jsonify({
            "active_conversations": len(conversations),
            "conversations": conversations
        })
        
    except Exception as e:
        print(f"❌ Error getting conversations: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🤖 Starting VIV Clinic Facebook Webhook Server")
    print(f"🔑 Verify Token: {VERIFY_TOKEN}")
    print("📡 Webhook URL: http://your-domain.com/webhook")
    print("🏥 Health Check: http://your-domain.com/health")
    print("🧪 Test Endpoint: http://your-domain.com/test")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=12000,
        debug=True
    )