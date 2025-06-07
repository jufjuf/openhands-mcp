#!/usr/bin/env python3
"""
Simple Password Manager for MCP Project
Safely loads and manages credentials from .env file
"""

import os
import sys
from pathlib import Path

class PasswordManager:
    def __init__(self, env_file="credentials.env"):
        self.env_file = env_file
        self.credentials = {}
        self.load_credentials()
    
    def load_credentials(self):
        """Load credentials from env file"""
        env_path = Path(__file__).parent / self.env_file
        
        if not env_path.exists():
            print(f"❌ Error: {self.env_file} not found!")
            return
        
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        self.credentials[key] = value
                        os.environ[key] = value
            print(f"✅ Loaded {len(self.credentials)} credentials from {self.env_file}")
        except Exception as e:
            print(f"❌ Error loading {self.env_file}: {e}")
    
    def get_password(self, service):
        """Get password for a specific service"""
        service_upper = service.upper()
        
        # Try different password key formats
        possible_keys = [
            f"{service_upper}_PASSWORD",
            f"{service_upper}_PASS",
            f"{service}_PASSWORD",
            f"{service}_PASS"
        ]
        
        for key in possible_keys:
            if key in self.credentials:
                return self.credentials[key]
        
        print(f"⚠️  Password not found for service: {service}")
        return None
    
    def get_email(self, service):
        """Get email for a specific service"""
        service_upper = service.upper()
        
        possible_keys = [
            f"{service_upper}_EMAIL",
            f"{service}_EMAIL",
            f"{service_upper}_USER",
            f"{service}_USER"
        ]
        
        for key in possible_keys:
            if key in self.credentials:
                return self.credentials[key]
        
        print(f"⚠️  Email not found for service: {service}")
        return None
    
    def get_api_key(self, service):
        """Get API key for a specific service"""
        service_upper = service.upper()
        
        possible_keys = [
            f"{service_upper}_API_KEY",
            f"{service_upper}_ACCESS_TOKEN",
            f"{service_upper}_AUTH_TOKEN",
            f"{service_upper}_TOKEN",
            f"{service}_API_KEY",
            f"{service}_ACCESS_TOKEN"
        ]
        
        for key in possible_keys:
            if key in self.credentials:
                return self.credentials[key]
        
        print(f"⚠️  API key not found for service: {service}")
        return None
    
    def list_services(self):
        """List all available services"""
        services = set()
        for key in self.credentials.keys():
            if '_' in key:
                service = key.split('_')[0].lower()
                services.add(service)
        return sorted(services)
    
    def show_service_info(self, service):
        """Show all info for a specific service"""
        service_upper = service.upper()
        service_lower = service.lower()
        
        print(f"\n🔍 {service.title()} Credentials:")
        print("-" * 30)
        
        # Find all keys for this service
        service_keys = [key for key in self.credentials.keys() 
                       if key.startswith(service_upper + '_') or key.startswith(service_lower + '_')]
        
        if not service_keys:
            print(f"❌ No credentials found for {service}")
            return
        
        for key in sorted(service_keys):
            value = self.credentials[key]
            # Hide passwords partially for security
            if 'PASSWORD' in key or 'SECRET' in key or 'TOKEN' in key:
                if len(value) > 4:
                    display_value = value[:2] + '*' * (len(value) - 4) + value[-2:]
                else:
                    display_value = '*' * len(value)
            else:
                display_value = value
            
            print(f"  {key}: {display_value}")

def main():
    pm = PasswordManager()
    
    if len(sys.argv) < 2:
        print("🔐 Password Manager for MCP Project")
        print("\nUsage:")
        print("  python3 password_manager.py list                    # List all services")
        print("  python3 password_manager.py show <service>          # Show service info")
        print("  python3 password_manager.py password <service>      # Get password")
        print("  python3 password_manager.py email <service>         # Get email")
        print("  python3 password_manager.py api <service>           # Get API key")
        print("\nAvailable services:", ", ".join(pm.list_services()))
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        services = pm.list_services()
        print("📋 Available services:")
        for service in services:
            print(f"  • {service}")
    
    elif command == "show" and len(sys.argv) > 2:
        service = sys.argv[2]
        pm.show_service_info(service)
    
    elif command == "password" and len(sys.argv) > 2:
        service = sys.argv[2]
        password = pm.get_password(service)
        if password:
            print(f"🔑 {service} password: {password}")
    
    elif command == "email" and len(sys.argv) > 2:
        service = sys.argv[2]
        email = pm.get_email(service)
        if email:
            print(f"📧 {service} email: {email}")
    
    elif command == "api" and len(sys.argv) > 2:
        service = sys.argv[2]
        api_key = pm.get_api_key(service)
        if api_key:
            print(f"🔐 {service} API key: {api_key}")
    
    else:
        print("❌ Invalid command or missing service name")

if __name__ == "__main__":
    main()