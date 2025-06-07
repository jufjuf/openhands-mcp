# ✅ VIV Clinic Bot - Post-Deployment Checklist

## 🎉 הבוט עלה לאוויר ב-Railway!

### 📋 צעדים אחרונים להשלמת ההגדרה:

## 1. 🔗 **קבל את ה-URL של הבוט**
- לך ל-Railway Dashboard
- העתק את ה-URL (משהו כמו: `https://your-app-name.railway.app`)

## 2. 🧪 **בדוק שהבוט עובד**
בדוק את הקישורים הבאים (החלף את YOUR_URL):
- ✅ `https://YOUR_URL.railway.app/` - דף הבית
- ✅ `https://YOUR_URL.railway.app/test` - בדיקת חיבור לפייסבוק
- ✅ `https://YOUR_URL.railway.app/messages` - הודעות מפייסבוק
- ✅ `https://YOUR_URL.railway.app/customers` - רשימת לקוחות

## 3. 🔧 **הגדר Webhook בפייסבוק**

### שלב א: לך לפייסבוק Developer Console
1. לך ל: https://developers.facebook.com/apps/557786413879136/webhooks/
2. לחץ "Edit" על ה-webhook הקיים או "Add Webhook"

### שלב ב: הגדר את ה-URL
- **Callback URL**: `https://YOUR_URL.railway.app/webhook`
- **Verify Token**: `VIV_CLINIC_VERIFY_TOKEN`
- **Subscription Fields**: בחר:
  - ✅ `messages`
  - ✅ `messaging_postbacks`
  - ✅ `messaging_optins`

### שלב ג: אמת את ה-Webhook
1. לחץ "Verify and Save"
2. אם הכל תקין, תראה ✅ ליד ה-webhook

## 4. 🧪 **בדיקה סופית**
1. שלח הודעה בפייסבוק לדף VIV Clinic
2. בדוק שהבוט מגיב
3. בדוק ב-`/customers` שהלקוח נשמר

## 5. 📊 **מעקב ובקרה**

### Railway Dashboard:
- **Logs**: לראות מה קורה בזמן אמת
- **Metrics**: שימוש במשאבים
- **Environment Variables**: עריכת המפתחות

### בוט Dashboard:
- **Statistics**: `https://YOUR_URL.railway.app/stats`
- **Health Check**: `https://YOUR_URL.railway.app/health`

## 🚨 **פתרון בעיות**

### אם הבוט לא מגיב:
1. בדוק Railway Logs
2. ודא שמשתני הסביבה נכונים
3. בדוק שה-webhook מוגדר נכון

### אם יש שגיאות:
1. בדוק ב-`/test` שהחיבור לפייסבוק תקין
2. ודא שה-Access Token לא פג
3. בדוק שה-Page ID נכון

## 📞 **מה קורה עכשיו?**

1. **לקוח שולח הודעה** בפייסבוק לדף VIV Clinic
2. **פייסבוק שולח** את ההודעה ל-webhook שלך
3. **הבוט מעבד** את ההודעה ושומר את הנתונים
4. **הבוט שולח תגובה** אוטומטית ללקוח
5. **הנתונים זמינים** בממשק הניהול

## 🎯 **הבוט פעיל ומוכן לקבל לקוחות!**

---

**מה ה-URL של הבוט שלך ב-Railway?**