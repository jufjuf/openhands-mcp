#!/usr/bin/env python3
"""
Test AI Integration for VIV Clinic Bot
"""

import os
import sys

# Set environment variables for testing
os.environ['GEMINI_API_KEY'] = 'test_key_for_demo'
os.environ['AI_PROVIDER'] = 'gemini'

# Test the AI engine
from ai_chat_engine import get_ai_engine

def test_ai_responses():
    """Test AI responses with fallback"""
    print("🧪 Testing AI Integration...")
    
    engine = get_ai_engine()
    
    test_messages = [
        "שלום, אני רוצה לקבוע תור לטיפול שיניים",
        "כמה עולה הלבנת שיניים?", 
        "איפה המרפאה נמצאת?",
        "מתי אתם פתוחים בשבוע?",
        "יש לכם מקום חניה?",
        "תודה רבה על המידע!"
    ]
    
    print(f"🤖 AI Engine Status: {engine.active_provider}")
    print(f"📋 Available Providers: {', '.join(engine.available_providers)}")
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"📨 Test {i}: {message}")
        response, is_ai = engine.generate_response(f"test_user_{i}", message)
        ai_status = "🤖 AI Generated" if is_ai else "🔄 Fallback Response"
        print(f"🤖 Response ({ai_status}): {response}")
        print("-" * 80)

def test_facebook_bot():
    """Test Facebook bot with AI integration"""
    print("\n🤖 Testing Facebook Bot with AI...")
    
    from facebook_bot import FacebookBot
    
    bot = FacebookBot()
    
    test_scenarios = [
        ("user1", "שלום, אני רוצה לקבוע תור"),
        ("user2", "כמה עולה טיפול שורש?"),
        ("user3", "איפה אתם נמצאים? יש חניה?"),
        ("user4", "מתי אתם פתוחים? 0501234567"),  # With phone number
        ("user5", "תודה רבה על העזרה!")
    ]
    
    for user_id, message in test_scenarios:
        print(f"\n👤 User {user_id}: {message}")
        try:
            response = bot.process_message(user_id, message, "test")
            print(f"🤖 Bot Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 60)

def test_production_server():
    """Test production server AI integration"""
    print("\n🌐 Testing Production Server AI...")
    
    import requests
    import json
    
    # Test local server
    base_url = "http://localhost:12000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health Check: {response.json()}")
        
        # Test AI status
        response = requests.get(f"{base_url}/ai/status", timeout=5)
        print(f"🤖 AI Status: {response.json()}")
        
        # Test chat endpoint
        test_message = {
            "message": "שלום, אני רוצה לקבוע תור לטיפול שיניים",
            "sender_id": "test_user_ai"
        }
        
        response = requests.post(
            f"{base_url}/chat/send",
            json=test_message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"💬 Chat Response: {result.get('response', 'No response')}")
            print(f"🤖 AI Generated: {result.get('ai_generated', False)}")
        else:
            print(f"❌ Chat Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Server not running on localhost:12000")
    except Exception as e:
        print(f"❌ Server Test Error: {e}")

if __name__ == "__main__":
    print("🚀 VIV Clinic AI Integration Test Suite")
    print("=" * 80)
    
    # Test AI Engine
    test_ai_responses()
    
    # Test Facebook Bot
    test_facebook_bot()
    
    # Test Production Server
    test_production_server()
    
    print("\n✅ Test Suite Completed!")