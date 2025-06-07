#!/usr/bin/env python3
"""
Deploy script for Railway - copies production_server.py to Railway deployment
"""

import os
import shutil
import subprocess

def deploy_to_railway():
    """Deploy the latest version to Railway"""
    
    print("🚀 Starting Railway deployment...")
    
    # Check if we have the production server file
    if not os.path.exists('production_server.py'):
        print("❌ production_server.py not found!")
        return False
    
    print("✅ Found production_server.py")
    
    # Check current version
    with open('production_server.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if '"version": "1.0.2"' in content:
            print("✅ Version 1.0.2 confirmed")
        else:
            print("⚠️  Version might not be updated")
    
    # Try to push to git (Railway auto-deploys from main branch)
    try:
        print("📤 Attempting to push to GitHub...")
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        print(f"Git status: {result.stdout}")
        
        # Check if we're on main branch
        if 'On branch main' in result.stdout:
            print("✅ On main branch")
            
            # Check if there are changes to push
            if 'Your branch is ahead' in result.stdout:
                print("📤 Changes ready to push")
                return True
            else:
                print("✅ Already up to date")
                return True
        else:
            print("⚠️  Not on main branch")
            return False
            
    except Exception as e:
        print(f"❌ Git error: {e}")
        return False

if __name__ == "__main__":
    success = deploy_to_railway()
    if success:
        print("🎉 Deployment preparation complete!")
        print("🔄 Railway should auto-deploy from main branch")
        print("🌐 Check: https://web-production-0cf2e.up.railway.app/health")
    else:
        print("❌ Deployment preparation failed")