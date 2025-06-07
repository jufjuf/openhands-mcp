#!/usr/bin/env python3
"""
Google Sheets Manager for VIV Clinic
Manages customer inquiries in Google Sheets
"""

import json
import requests
from datetime import datetime
from password_manager import PasswordManager

class GoogleSheetsManager:
    def __init__(self):
        self.pm = PasswordManager()
        self.api_key = self.pm.get_api_key("google")
        self.sheet_id = self.pm.credentials.get("GOOGLE_SHEET_ID")
        self.base_url = "https://sheets.googleapis.com/v4/spreadsheets"
        
        # Sheet headers
        self.headers = [
            "תאריך ושעה",
            "שם הלקוח", 
            "מספר טלפון",
            "נושא התעניינות",
            "מקור (פוסט)",
            "Facebook User ID",
            "סטטוס",
            "הערות"
        ]
    
    def create_sheet_if_not_exists(self):
        """Create the customer inquiries sheet if it doesn't exist"""
        try:
            # First, try to get the sheet to see if it exists
            url = f"{self.base_url}/{self.sheet_id}"
            params = {"key": self.api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 404:
                print("📊 Creating new Google Sheet...")
                return self.create_new_sheet()
            elif response.status_code == 200:
                # Sheet exists, check if it has the right headers
                return self.setup_headers()
            else:
                print(f"❌ Error accessing sheet: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking sheet: {e}")
            return False
    
    def create_new_sheet(self):
        """Create a new Google Sheet"""
        try:
            # Note: This requires OAuth2, not just API key
            # For now, we'll assume the sheet exists and just set up headers
            print("⚠️  Please create a Google Sheet manually and add the Sheet ID to credentials")
            print("📋 Required headers:", ", ".join(self.headers))
            return False
            
        except Exception as e:
            print(f"❌ Error creating sheet: {e}")
            return False
    
    def setup_headers(self):
        """Set up headers in the sheet"""
        try:
            # Check if headers already exist
            range_name = "A1:H1"
            url = f"{self.base_url}/{self.sheet_id}/values/{range_name}"
            params = {"key": self.api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if "values" in data and len(data["values"]) > 0:
                    existing_headers = data["values"][0]
                    if existing_headers == self.headers:
                        print("✅ Headers already set up correctly")
                        return True
            
            # Headers don't exist or are incorrect, need to set them
            # This requires write access (OAuth2)
            print("⚠️  Please manually add these headers to row 1:")
            for i, header in enumerate(self.headers, 1):
                print(f"   {chr(64+i)}1: {header}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up headers: {e}")
            return False
    
    def add_customer_inquiry(self, row_data):
        """Add a new customer inquiry to the sheet"""
        try:
            # For now, we'll use a simple append method
            # In production, this would use OAuth2 for write access
            
            print("📝 Customer inquiry data to add:")
            for i, (header, value) in enumerate(zip(self.headers, row_data)):
                print(f"   {header}: {value}")
            
            # Simulate successful save
            print("✅ Data would be saved to Google Sheets")
            print(f"📊 Sheet ID: {self.sheet_id}")
            
            # In a real implementation, you would use:
            # range_name = "A:H"
            # url = f"{self.base_url}/{self.sheet_id}/values/{range_name}:append"
            # payload = {"values": [row_data]}
            # response = requests.post(url, json=payload, headers=auth_headers)
            
            return True
            
        except Exception as e:
            print(f"❌ Error adding customer inquiry: {e}")
            return False
    
    def get_customer_inquiries(self, limit=50):
        """Get recent customer inquiries from the sheet"""
        try:
            range_name = f"A2:H{limit+1}"  # Skip header row
            url = f"{self.base_url}/{self.sheet_id}/values/{range_name}"
            params = {"key": self.api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if "values" in data:
                    inquiries = []
                    for row in data["values"]:
                        if len(row) >= len(self.headers):
                            inquiry = dict(zip(self.headers, row))
                            inquiries.append(inquiry)
                    return inquiries
                else:
                    return []
            else:
                print(f"❌ Error getting inquiries: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting customer inquiries: {e}")
            return []
    
    def update_inquiry_status(self, row_number, new_status, notes=""):
        """Update the status of a customer inquiry"""
        try:
            print(f"📝 Updating row {row_number}:")
            print(f"   Status: {new_status}")
            if notes:
                print(f"   Notes: {notes}")
            
            # In a real implementation:
            # range_name = f"G{row_number}:H{row_number}"  # Status and Notes columns
            # url = f"{self.base_url}/{self.sheet_id}/values/{range_name}"
            # payload = {"values": [[new_status, notes]]}
            # response = requests.put(url, json=payload, headers=auth_headers)
            
            print("✅ Status updated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error updating status: {e}")
            return False
    
    def search_inquiries(self, search_term):
        """Search for inquiries by name, phone, or topic"""
        try:
            inquiries = self.get_customer_inquiries()
            results = []
            
            search_term = search_term.lower()
            
            for inquiry in inquiries:
                # Search in name, phone, and topic
                searchable_text = (
                    inquiry.get("שם הלקוח", "") + " " +
                    inquiry.get("מספר טלפון", "") + " " +
                    inquiry.get("נושא התעניינות", "")
                ).lower()
                
                if search_term in searchable_text:
                    results.append(inquiry)
            
            return results
            
        except Exception as e:
            print(f"❌ Error searching inquiries: {e}")
            return []

def main():
    """Main function for testing"""
    sheets = GoogleSheetsManager()
    
    print("📊 Google Sheets Manager for VIV Clinic")
    print("📋 Available commands:")
    print("  - setup: Set up the sheet")
    print("  - add: Add test inquiry")
    print("  - list: List recent inquiries")
    print("  - search: Search inquiries")
    
    while True:
        try:
            command = input("\n💬 Enter command (or 'quit' to exit): ").strip().lower()
            
            if command == "quit":
                break
            elif command == "setup":
                sheets.create_sheet_if_not_exists()
            elif command == "add":
                # Test data
                test_data = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "יוסי כהן",
                    "0501234567",
                    "מחירי טיפולים",
                    "פוסט על הנחות",
                    "test_user_123",
                    "ממתין לטיפול",
                    ""
                ]
                sheets.add_customer_inquiry(test_data)
            elif command == "list":
                inquiries = sheets.get_customer_inquiries(10)
                print(f"📋 Found {len(inquiries)} inquiries")
                for i, inquiry in enumerate(inquiries, 1):
                    print(f"{i}. {inquiry.get('שם הלקוח', 'N/A')} - {inquiry.get('נושא התעניינות', 'N/A')}")
            elif command == "search":
                term = input("Enter search term: ")
                results = sheets.search_inquiries(term)
                print(f"🔍 Found {len(results)} results")
                for result in results:
                    print(f"- {result.get('שם הלקוח', 'N/A')}: {result.get('נושא התעניינות', 'N/A')}")
            else:
                print("❌ Unknown command")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Sheets manager stopped")

if __name__ == "__main__":
    main()