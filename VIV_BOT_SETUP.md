# 🏥 מדריך הגדרה - בוט פייסבוק לקליניקת VIV

## 📋 סקירה כללית

הבוט מטפל אוטומטית בהודעות ותגובות בפייסבוק העיסקי של קליניקת VIV:
- **מגיב להודעות פרטיות** במסנג'ר
- **מגיב לתגובות** בפוסטים
- **אוסף פרטי לקוחות** (שם, טלפון, נושא התעניינות)
- **שומר הכל ב-Google Sheets** לטיפול הנציגה

## 🔧 שלב 1: הגדרת Facebook App

### יצירת Facebook App
1. היכנס ל-[Facebook Developers](https://developers.facebook.com/)
2. לחץ על **"Create App"**
3. בחר **"Business"** כסוג האפליקציה
4. מלא פרטים:
   - **App Name**: VIV Clinic Bot
   - **Contact Email**: eli@viv.co.il

### הוספת Messenger Platform
1. בדף האפליקציה, לחץ **"Add Product"**
2. בחר **"Messenger"** ולחץ **"Set Up"**
3. ב-**"Access Tokens"**:
   - בחר את דף הפייסבוק של קליניקת VIV
   - העתק את ה-**Page Access Token**

### הגדרת Webhooks
1. ב-**"Webhooks"** לחץ **"Setup Webhooks"**
2. מלא:
   - **Callback URL**: `https://work-1-zfogegygfxxaveky.prod-runtime.all-hands.dev/webhook`
   - **Verify Token**: `VIV_CLINIC_2024`
3. בחר **Subscription Fields**:
   - ✅ `messages`
   - ✅ `messaging_postbacks`
   - ✅ `feed`
4. לחץ **"Verify and Save"**

## 📊 שלב 2: הגדרת Google Sheets

### יצירת Google Sheet
1. היכנס ל-[Google Sheets](https://sheets.google.com/)
2. צור גיליון חדש בשם **"VIV Clinic - פניות לקוחות"**
3. הוסף כותרות בשורה הראשונה:
   ```
   A1: תאריך ושעה
   B1: שם הלקוח
   C1: מספר טלפון
   D1: נושא התעניינות
   E1: מקור (פוסט)
   F1: Facebook User ID
   G1: סטטוס
   H1: הערות
   ```

### קבלת Sheet ID
1. מה-URL של הגיליון, העתק את ה-ID:
   ```
   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
   ```

### הגדרת Google API
1. היכנס ל-[Google Cloud Console](https://console.cloud.google.com/)
2. צור פרויקט חדש או בחר קיים
3. הפעל את **Google Sheets API**
4. צור **API Key** ב-**"Credentials"**

## 🔑 שלב 3: עדכון Credentials

ערוך את הקובץ `credentials.env`:

```env
# Facebook - עדכן עם הערכים האמיתיים
FACEBOOK_ACCESS_TOKEN=your_page_access_token_here
FACEBOOK_PAGE_ID=your_viv_clinic_page_id
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_VERIFY_TOKEN=VIV_CLINIC_2024

# Google Sheets
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SHEET_ID=your_sheet_id_here
```

## 🚀 שלב 4: הפעלת הבוט

### התקנת Dependencies
```bash
pip install flask requests
```

### הפעלה
```bash
python3 start_viv_bot.py
```

### בדיקת תקינות
1. **Health Check**: https://work-1-zfogegygfxxaveky.prod-runtime.all-hands.dev/health
2. **Test Endpoint**: POST לכתובת `/test` עם:
   ```json
   {
     "user_id": "test_user",
     "message": "שלום"
   }
   ```

## 💬 איך הבוט עובד

### תהליך השיחה
1. **לקוח שולח הודעה** → בוט מגיב בברכה ומבקש טלפון
2. **לקוח שולח טלפון** → בוט שואל על נושא ההתעניינות
3. **לקוח מציין נושא** → בוט שומר הכל ב-Google Sheets ושולח אישור

### דוגמת שיחה
```
👤 לקוח: שלום, אני מעוניין במידע על טיפולים
🤖 בוט: שלום יוסי! 👋
       תודה שפנית לקליניקת VIV.
       אשמח לעזור לך עם השאלה שלך.
       
       כדי שנציגה שלנו תוכל לחזור אליך עם כל הפרטים,
       אשמח אם תשאיר מספר טלפון לחזרה 📞

👤 לקוח: 0501234567
🤖 בוט: על איזה נושא תרצה לקבל מידע?
       (למשל: טיפולים, מחירים, זמינות וכו')

👤 לקוח: מחירי טיפולי פנים
🤖 בוט: תודה רבה יוסי! 🙏
       קיבלתי את הפרטים שלך:
       📞 טלפון: 0501234567
       📝 נושא: מחירי טיפולי פנים
       
       נציגה שלנו תחזור אליך בהקדם האפשרי ✨
```

## 📊 ניהול הנתונים

### Google Sheets
כל פנייה נשמרת עם:
- **תאריך ושעה** - מתי הלקוח פנה
- **שם הלקוח** - מתוך פרופיל הפייסבוק
- **מספר טלפון** - שהלקוח השאיר
- **נושא התעניינות** - מה הלקוח רוצה לדעת
- **מקור** - מאיזה פוסט הגיע (אם רלוונטי)
- **סטטוס** - ממתין לטיפול / טופל / וכו'

### עדכון סטטוס
הנציגה יכולה לעדכן בגיליון:
- **עמודה G (סטטוס)**: "ממתין לטיפול" → "נוצר קשר" → "טופל"
- **עמודה H (הערות)**: פרטים נוספים על השיחה

## 🔧 פתרון בעיות

### הבוט לא מגיב
1. בדוק שה-webhook פעיל ב-Facebook
2. ודא שה-Page Access Token תקין
3. בדוק logs בטרמינל

### לא נשמר ב-Google Sheets
1. ודא שה-Google API Key תקין
2. בדוק שה-Sheet ID נכון
3. ודא שהגיליון ציבורי או שיש הרשאות

### הודעות לא מגיעות
1. בדוק שהדף מחובר לאפליקציה
2. ודא שה-webhook מוגדר נכון
3. בדוק שהאפליקציה באישור Facebook

## 📞 תמיכה

לבעיות טכניות או שאלות:
- **אימייל**: eli@viv.co.il
- **טלפון**: [מספר הטלפון של הקליניקה]

## 🔄 עדכונים עתידיים

תכונות שניתן להוסיף:
- **שליחת SMS** אוטומטית ללקוחות
- **אינטגרציה עם CRM**
- **דוחות אוטומטיים**
- **בוט קולי** לטלפון
- **צ'אט בוט באתר**

---

**🏥 קליניקת VIV - שירות לקוחות מתקדם עם טכנולוגיה חכמה**