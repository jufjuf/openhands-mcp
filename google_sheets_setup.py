#!/usr/bin/env python3
"""
Google Sheets Setup Guide for VIV Clinic
Instructions for connecting Google Sheets to the bot system
"""

import json
from csv_manager import CSVManager

def print_setup_instructions():
    """Print step-by-step instructions for Google Sheets setup"""
    
    print("🔧 Google Sheets Setup Instructions for VIV Clinic")
    print("=" * 60)
    
    print("\n📋 Step 1: Create Google Sheet")
    print("1. Go to https://docs.google.com/spreadsheets/")
    print("2. Create a new spreadsheet")
    print("3. Name it: 'VIV Clinic - Customer Data'")
    print("4. Add these headers in row 1:")
    print("   A1: תאריך")
    print("   B1: שם") 
    print("   C1: טלפון")
    print("   D1: נושא")
    print("   E1: מקור")
    print("   F1: סטטוס")
    print("   G1: הערות")
    
    print("\n🔑 Step 2: Get Google Sheets API Key")
    print("1. Go to https://console.developers.google.com/")
    print("2. Create a new project or select existing")
    print("3. Enable Google Sheets API")
    print("4. Create credentials (API Key)")
    print("5. Copy the API key")
    
    print("\n📊 Step 3: Make Sheet Public")
    print("1. In your Google Sheet, click 'Share'")
    print("2. Change permissions to 'Anyone with the link can edit'")
    print("3. Copy the sheet URL")
    print("4. Extract the Sheet ID from URL:")
    print("   URL: https://docs.google.com/spreadsheets/d/SHEET_ID/edit")
    print("   Copy the SHEET_ID part")
    
    print("\n⚙️  Step 4: Update credentials.env")
    print("Add these lines to your credentials.env file:")
    print("GOOGLE_API_KEY=your_api_key_here")
    print("GOOGLE_SHEET_ID=your_sheet_id_here")
    
    print("\n🔄 Step 5: Import Existing Data")
    print("Run this script with --import flag to import CSV data to Google Sheets")

def export_csv_for_google_sheets():
    """Export CSV data in Google Sheets format"""
    csv_manager = CSVManager()
    data = csv_manager.export_to_google_sheets_format()
    
    print("\n📤 CSV Data for Google Sheets Import:")
    print("=" * 40)
    
    for i, row in enumerate(data):
        if i == 0:
            print("Headers:", row)
        else:
            print(f"Row {i}:", row)
    
    # Save as JSON for easy import
    with open('google_sheets_import.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Data exported to: google_sheets_import.json")
    print("You can use this file to import data to Google Sheets")

def create_google_sheets_manager():
    """Create updated Google Sheets manager"""
    
    google_sheets_code = '''#!/usr/bin/env python3
"""
Google Sheets Manager for VIV Clinic
Updated version with API Key authentication
"""

import requests
import json
from password_manager import PasswordManager

class GoogleSheetsManager:
    def __init__(self):
        self.pm = PasswordManager()
        self.api_key = self.pm.get_api_key("google")
        self.sheet_id = self.pm.credentials.get("GOOGLE_SHEET_ID")
        self.base_url = "https://sheets.googleapis.com/v4/spreadsheets"
        
        if not self.api_key:
            print("⚠️  Google API key not found in credentials")
        if not self.sheet_id:
            print("⚠️  Google Sheet ID not found in credentials")
    
    def add_customer_inquiry(self, row_data):
        """Add customer inquiry to Google Sheets"""
        try:
            if not self.api_key or not self.sheet_id:
                print("❌ Missing Google credentials")
                return False
            
            # Prepare the request
            url = f"{self.base_url}/{self.sheet_id}/values/Sheet1:append"
            params = {
                "key": self.api_key,
                "valueInputOption": "RAW",
                "insertDataOption": "INSERT_ROWS"
            }
            
            payload = {
                "values": [row_data]
            }
            
            response = requests.post(url, params=params, json=payload)
            
            if response.status_code == 200:
                print("✅ Data added to Google Sheets")
                return True
            else:
                print(f"❌ Failed to add to Google Sheets: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error adding to Google Sheets: {e}")
            return False
    
    def get_all_customers(self):
        """Get all customers from Google Sheets"""
        try:
            if not self.api_key or not self.sheet_id:
                return []
            
            url = f"{self.base_url}/{self.sheet_id}/values/Sheet1"
            params = {"key": self.api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("values", [])
            else:
                print(f"❌ Failed to get data from Google Sheets: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting data from Google Sheets: {e}")
            return []
    
    def test_connection(self):
        """Test Google Sheets connection"""
        try:
            if not self.api_key or not self.sheet_id:
                return False
            
            url = f"{self.base_url}/{self.sheet_id}"
            params = {"key": self.api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Connected to Google Sheet: {data.get('properties', {}).get('title', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to connect to Google Sheets: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing Google Sheets connection: {e}")
            return False

if __name__ == "__main__":
    # Test the Google Sheets manager
    sheets = GoogleSheetsManager()
    
    if sheets.test_connection():
        print("🎉 Google Sheets integration is ready!")
    else:
        print("❌ Google Sheets integration needs setup")
'''
    
    with open('google_sheets_manager_updated.py', 'w', encoding='utf-8') as f:
        f.write(google_sheets_code)
    
    print("✅ Created updated Google Sheets manager: google_sheets_manager_updated.py")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_csv_for_google_sheets()
    elif len(sys.argv) > 1 and sys.argv[1] == "--create-manager":
        create_google_sheets_manager()
    else:
        print_setup_instructions()
        print("\n🚀 Quick Actions:")
        print("python google_sheets_setup.py --export     # Export CSV data")
        print("python google_sheets_setup.py --create-manager  # Create updated manager")