#!/usr/bin/env python3
"""
CSV Manager for VIV Clinic - Temporary solution until Google Sheets is connected
"""

import csv
import os
from datetime import datetime
from pathlib import Path

class CSVManager:
    def __init__(self, csv_file="viv_clinic_customers.csv"):
        self.csv_file = Path(__file__).parent / csv_file
        self.headers = [
            "תאריך",
            "שם",
            "טלפון", 
            "נושא",
            "מקור",
            "סטטוס",
            "הערות"
        ]
        self.init_csv()
    
    def init_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not self.csv_file.exists():
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
            print(f"✅ Created CSV file: {self.csv_file}")
        else:
            print(f"✅ CSV file exists: {self.csv_file}")
    
    def add_customer(self, name, phone, topic, source="Facebook", status="חדש", notes=""):
        """Add new customer to CSV"""
        try:
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([date, name, phone, topic, source, status, notes])
            
            print(f"✅ Added customer: {name} - {phone}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding customer: {e}")
            return False
    
    def get_customers(self, limit=10):
        """Get recent customers from CSV"""
        try:
            customers = []
            
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    customers.append(row)
            
            # Return most recent customers
            return customers[-limit:] if len(customers) > limit else customers
            
        except Exception as e:
            print(f"❌ Error reading customers: {e}")
            return []
    
    def search_customer(self, phone):
        """Search for customer by phone number"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['טלפון'] == phone:
                        return row
            return None
            
        except Exception as e:
            print(f"❌ Error searching customer: {e}")
            return None
    
    def update_customer_status(self, phone, new_status, notes=""):
        """Update customer status"""
        try:
            customers = []
            updated = False
            
            # Read all customers
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['טלפון'] == phone:
                        row['סטטוס'] = new_status
                        if notes:
                            row['הערות'] = notes
                        updated = True
                    customers.append(row)
            
            if updated:
                # Write back all customers
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.headers)
                    writer.writeheader()
                    writer.writerows(customers)
                
                print(f"✅ Updated customer {phone} status to: {new_status}")
                return True
            else:
                print(f"⚠️  Customer {phone} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error updating customer: {e}")
            return False
    
    def export_to_google_sheets_format(self):
        """Export CSV in format ready for Google Sheets import"""
        try:
            customers = self.get_customers(limit=1000)  # Get all customers
            
            # Create formatted data for Google Sheets
            sheets_data = []
            sheets_data.append(self.headers)  # Headers
            
            for customer in customers:
                row = [
                    customer.get('תאריך', ''),
                    customer.get('שם', ''),
                    customer.get('טלפון', ''),
                    customer.get('נושא', ''),
                    customer.get('מקור', ''),
                    customer.get('סטטוס', ''),
                    customer.get('הערות', '')
                ]
                sheets_data.append(row)
            
            return sheets_data
            
        except Exception as e:
            print(f"❌ Error exporting to Google Sheets format: {e}")
            return []
    
    def get_stats(self):
        """Get customer statistics"""
        try:
            customers = self.get_customers(limit=1000)
            
            stats = {
                "total_customers": len(customers),
                "sources": {},
                "statuses": {},
                "recent_customers": len([c for c in customers if datetime.now().strftime("%Y-%m-%d") in c.get('תאריך', '')])
            }
            
            for customer in customers:
                source = customer.get('מקור', 'Unknown')
                status = customer.get('סטטוס', 'Unknown')
                
                stats["sources"][source] = stats["sources"].get(source, 0) + 1
                stats["statuses"][status] = stats["statuses"].get(status, 0) + 1
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}

if __name__ == "__main__":
    # Test the CSV manager
    csv_manager = CSVManager()
    
    # Add test customer
    csv_manager.add_customer(
        name="יוסי כהן",
        phone="0501234567",
        topic="טיפול שיניים",
        notes="לקוח חדש מפייסבוק"
    )
    
    # Get recent customers
    customers = csv_manager.get_customers(5)
    print(f"\n📋 Recent customers ({len(customers)}):")
    for customer in customers:
        print(f"  - {customer['שם']} ({customer['טלפון']}) - {customer['נושא']}")
    
    # Get stats
    stats = csv_manager.get_stats()
    print(f"\n📊 Statistics:")
    print(f"  Total customers: {stats['total_customers']}")
    print(f"  Today's customers: {stats['recent_customers']}")
    print(f"  Sources: {stats['sources']}")
    print(f"  Statuses: {stats['statuses']}")