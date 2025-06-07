#!/usr/bin/env python3
"""
Auto Login Helper for MCP Project
Helps automate login to various services using stored credentials
"""

import json
import sys
from password_manager import PasswordManager

class AutoLogin:
    def __init__(self):
        self.pm = PasswordManager()
    
    def facebook_login_data(self):
        """Get Facebook login data"""
        return {
            "email": self.pm.get_email("facebook"),
            "password": self.pm.get_password("facebook"),
            "access_token": self.pm.get_api_key("facebook")
        }
    
    def google_login_data(self):
        """Get Google login data"""
        return {
            "email": self.pm.get_email("google"),
            "password": self.pm.get_password("google"),
            "api_key": self.pm.get_api_key("google")
        }
    
    def zapier_login_data(self):
        """Get Zapier login data"""
        return {
            "email": self.pm.get_email("zapier"),
            "password": self.pm.get_password("zapier"),
            "api_key": self.pm.get_api_key("zapier")
        }
    
    def twilio_login_data(self):
        """Get Twilio login data"""
        return {
            "email": self.pm.get_email("twilio"),
            "password": self.pm.get_password("twilio"),
            "account_sid": self.pm.credentials.get("TWILIO_ACCOUNT_SID"),
            "auth_token": self.pm.credentials.get("TWILIO_AUTH_TOKEN")
        }
    
    def get_service_data(self, service):
        """Get login data for any service"""
        method_name = f"{service.lower()}_login_data"
        if hasattr(self, method_name):
            return getattr(self, method_name)()
        else:
            # Generic service data
            return {
                "email": self.pm.get_email(service),
                "password": self.pm.get_password(service),
                "api_key": self.pm.get_api_key(service)
            }

def main():
    auto_login = AutoLogin()
    
    if len(sys.argv) < 2:
        print("🔐 Auto Login Helper")
        print("\nUsage:")
        print("  python3 auto_login.py <service>")
        print("\nAvailable services:", ", ".join(auto_login.pm.list_services()))
        print("\nExample:")
        print("  python3 auto_login.py facebook")
        return
    
    service = sys.argv[1].lower()
    
    try:
        login_data = auto_login.get_service_data(service)
        
        # Remove None values
        login_data = {k: v for k, v in login_data.items() if v is not None}
        
        if login_data:
            print(json.dumps(login_data, indent=2))
        else:
            print(f"❌ No login data found for service: {service}")
    
    except Exception as e:
        print(f"❌ Error getting login data for {service}: {e}")

if __name__ == "__main__":
    main()