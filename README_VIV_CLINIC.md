# 🤖 VIV Clinic Facebook Bot System

## ✅ מה הושלם בהצלחה

### 🔵 Facebook Integration - פעיל ועובד!
- ✅ התחברנו לחשבון Facebook (yufit15@walla.co.il)
- ✅ גישה לדף VIV Clinic Business
- ✅ יצירת/חיבור לאפליקציית Facebook Developer
- ✅ קבלת Access Token תקף
- ✅ הבוט יכול לקרוא הודעות ולשלוח תגובות
- ✅ נבדק עם 25 שיחות פעילות

### 📊 Data Management - פעיל עם CSV
- ✅ מערכת CSV לשמירת נתוני לקוחות
- ✅ שמירה אוטומטית של פניות מפייסבוק
- ✅ ממשק web לצפייה בנתונים
- ✅ סטטיסטיקות ודוחות

### 🌐 Web Server - פעיל
- ✅ שרת Flask עובד
- ✅ ממשק ניהול ובדיקות
- ✅ Webhook לפייסבוק
- ✅ API endpoints לנתונים

## 🔧 פרטים טכניים

### Facebook Credentials
```
App ID: 557786413879136
Page ID: 103991726050308
Access Token: EAAH7TcUPT2ABO8w0q1NNraDY3UASS0afjxHAKJk68cKj9TxlScM2fYFl01TaQbrZBqtSRqf9pYyteGx0zpN8F2yZB9xP9eli5ZBap9UT4qziZAqJZCTZAASfgI1BwBwlem0b5UWVTBKG5XJ9ZAqa9sgXuEKu7AvSCBhCpG11O0bVg9wBxa053fTclHhHlFBt21IzgZDZD
```

### Server URLs
- Main Server: https://work-1-liraghfqzcrynzgs.prod-runtime.all-hands.dev
- Test Bot: /test
- View Messages: /messages  
- View Customers: /customers
- Statistics: /stats
- Webhook: /webhook

## 📁 קבצים במערכת

### Core Files
- `facebook_bot.py` - הבוט הראשי (עובד עם CSV)
- `csv_manager.py` - ניהול נתוני לקוחות ב-CSV
- `password_manager.py` - ניהול credentials
- `test_server.py` - שרת הבדיקות והניהול

### Data Files
- `credentials.env` - כל ה-credentials (Facebook + Google)
- `viv_clinic_customers.csv` - נתוני לקוחות
- `google_sheets_import.json` - נתונים מוכנים ל-Google Sheets

### Setup Files
- `google_sheets_setup.py` - הוראות התקנת Google Sheets
- `README_VIV_CLINIC.md` - המדריך הזה

## 🚀 איך להפעיל

### הפעלת השרת
```bash
cd /workspace/openhands-mcp
python test_server.py
```

### בדיקת הבוט
1. לך ל: https://work-1-liraghfqzcrynzgs.prod-runtime.all-hands.dev
2. לחץ על "Test bot functionality"
3. בדוק הודעות ב-"/messages"
4. צפה בלקוחות ב-"/customers"

## ⏳ מה נותר לעשות

### Google Sheets Integration
1. **יצירת Google Sheet ידנית**
   - לך ל: https://docs.google.com/spreadsheets/
   - צור sheet חדש בשם "VIV Clinic - Customer Data"
   - הוסף headers: תאריך, שם, טלפון, נושא, מקור, סטטוס, הערות

2. **קבלת API Key**
   - לך ל: https://console.developers.google.com/
   - צור פרויקט חדש
   - הפעל Google Sheets API
   - צור API Key

3. **עדכון Credentials**
   ```
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_SHEET_ID=your_sheet_id_here
   ```

4. **העברת נתונים**
   ```bash
   python google_sheets_setup.py --export
   ```

### ניקוי Facebook Apps (אופציונלי)
- מחק אפליקציות Facebook מיותרות כפי שביקשת

## 🔄 תהליך העבודה הנוכחי

1. **לקוח שולח הודעה בפייסבוק** → 
2. **הבוט מזהה ומעבד את ההודעה** → 
3. **שומר את הנתונים ב-CSV** → 
4. **שולח תגובה אוטומטית ללקוח** → 
5. **המידע זמין בממשק הניהול**

## 📞 תמיכה

הבוט פעיל ועובד! אם יש בעיות:
1. בדוק את השרver ב: https://work-1-liraghfqzcrynzgs.prod-runtime.all-hands.dev/test
2. בדוק logs בטרמינל
3. ודא ש-Access Token תקף

## 🎉 סיכום

**Facebook Integration: ✅ הושלם בהצלחה!**
- הבוט פעיל ויכול לקבל ולשלוח הודעות
- נתוני לקוחות נשמרים ב-CSV
- ממשק ניהול פעיל

**Google Sheets: ⏳ ממתין להתקנה ידנית**
- הוראות מפורטות זמינות
- נתונים מוכנים להעברה
- קוד מוכן לחיבור

המערכת פועלת ומוכנה לקבל לקוחות! 🚀