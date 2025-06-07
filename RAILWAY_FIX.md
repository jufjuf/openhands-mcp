# 🔧 Railway - תיקון Access Token

## ❌ הבעיה: 
ה-Access Token לא עובד ב-production

## ✅ הפתרון:

### שלב 1: הגדר משתני סביבה ב-Railway
1. לך ל-Railway Dashboard
2. בחר את הפרויקט שלך
3. לחץ על "Variables" 
4. הוסף את המשתנים הבאים:

```
FACEBOOK_ACCESS_TOKEN=EAAH7TcUPT2ABO8w0q1NNraDY3UASS0afjxHAKJk68cKj9TxlScM2fYFl01TaQbrZBqtSRqf9pYyteGx0zpN8F2yZB9xP9eli5ZBap9UT4qziZAqJZCTZAASfgI1BwBwlem0b5UWVTBKG5XJ9ZAqa9sgXuEKu7AvSCBhCpG11O0bVg9wBxa053fTclHhHlFBt21IzgZDZD

FACEBOOK_PAGE_ID=103991726050308

FACEBOOK_APP_ID=557786413879136

FACEBOOK_VERIFY_TOKEN=VIV_CLINIC_VERIFY_TOKEN
```

### שלב 2: Redeploy
לאחר הוספת המשתנים, Railway יעשה redeploy אוטומטי

### שלב 3: בדוק שוב
לך ל: https://web-production-0cf2e.up.railway.app/test

## 🔄 אם עדיין לא עובד:

### אפשרות 1: Access Token פג
נצטרך ליצור token חדש:
1. לך ל: https://developers.facebook.com/tools/explorer/
2. בחר את האפליקציה: VIV Clinic Bot
3. בחר Page Access Token
4. העתק את הtoken החדש

### אפשרות 2: בעיה בקוד
נבדוק את הlogs ב-Railway Dashboard

---

**תוכל לבדוק אם הוספת את משתני הסביבה ב-Railway?**