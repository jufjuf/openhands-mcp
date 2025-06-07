#!/usr/bin/env python3
"""
Environment loader for MCP Server
Loads credentials from .env file safely
"""

import os
from pathlib import Path

def load_env_file(env_file=".env"):
    """Load environment variables from file"""
    env_path = Path(__file__).parent / env_file
    
    if not env_path.exists():
        print(f"Warning: {env_file} not found. Using environment variables only.")
        return
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
        print(f"✅ Loaded environment variables from {env_file}")
    except Exception as e:
        print(f"❌ Error loading {env_file}: {e}")

def get_credential(key, default=None):
    """Get credential with fallback"""
    value = os.environ.get(key, default)
    if not value:
        print(f"⚠️  Warning: {key} not found in environment")
    return value

if __name__ == "__main__":
    # Load environment variables
    load_env_file()
    
    # Test some credentials
    print("\n🔍 Testing credentials:")
    print(f"EMAIL_ADDRESS: {'✅' if get_credential('EMAIL_ADDRESS') else '❌'}")
    print(f"FACEBOOK_ACCESS_TOKEN: {'✅' if get_credential('FACEBOOK_ACCESS_TOKEN') else '❌'}")
    print(f"OPENAI_API_KEY: {'✅' if get_credential('OPENAI_API_KEY') else '❌'}")