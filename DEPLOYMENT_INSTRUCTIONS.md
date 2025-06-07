# 🚀 VIV Clinic Bot - הוראות דיפלויימנט

## 🎯 אפשרות 1: Heroku (מומלץ)

### שלב 1: הכנה
1. **צור חשבון Heroku**: https://signup.heroku.com/
2. **התקן Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

### שלב 2: יצירת אפליקציה
```bash
# התחבר ל-Heroku
heroku login

# צור אפליקציה חדשה
heroku create viv-clinic-bot

# הוסף את ה-remote
git remote add heroku https://git.heroku.com/viv-clinic-bot.git
```

### שלב 3: הגדרת משתני סביבה
```bash
# Facebook credentials
heroku config:set FACEBOOK_ACCESS_TOKEN="EAAH7TcUPT2ABO8w0q1NNraDY3UASS0afjxHAKJk68cKj9TxlScM2fYFl01TaQbrZBqtSRqf9pYyteGx0zpN8F2yZB9xP9eli5ZBap9UT4qziZAqJZCTZAASfgI1BwBwlem0b5UWVTBKG5XJ9ZAqa9sgXuEKu7AvSCBhCpG11O0bVg9wBxa053fTclHhHlFBt21IzgZDZD"

heroku config:set FACEBOOK_PAGE_ID="103991726050308"

heroku config:set FACEBOOK_APP_ID="557786413879136"

heroku config:set FACEBOOK_VERIFY_TOKEN="VIV_CLINIC_VERIFY_TOKEN"
```

### שלב 4: דיפלויימנט
```bash
# דחף לHeroku
git push heroku main

# פתח את האפליקציה
heroku open
```

### שלב 5: הגדרת Webhook בפייסבוק
1. לך ל: https://developers.facebook.com/apps/557786413879136/webhooks/
2. הוסף webhook URL: `https://your-app-name.herokuapp.com/webhook`
3. Verify Token: `VIV_CLINIC_VERIFY_TOKEN`
4. Subscribe to: `messages`, `messaging_postbacks`

---

## 🎯 אפשרות 2: Railway (קל מאוד)

### שלב 1: הכנה
1. **צור חשבון Railway**: https://railway.app/
2. **חבר את GitHub**: התחבר עם חשבון GitHub שלך

### שלב 2: דיפלויימנט
1. לחץ "New Project"
2. בחר "Deploy from GitHub repo"
3. בחר את הrepository: `jufjuf/openhands-mcp`
4. בחר branch: `viv-clinic-facebook-bot-integration`

### שלב 3: הגדרת משתני סביבה
ב-Railway Dashboard, לך ל-Variables והוסף:
```
FACEBOOK_ACCESS_TOKEN=EAAH7TcUPT2ABO8w0q1NNraDY3UASS0afjxHAKJk68cKj9TxlScM2fYFl01TaQbrZBqtSRqf9pYyteGx0zpN8F2yZB9xP9eli5ZBap9UT4qziZAqJZCTZAASfgI1BwBwlem0b5UWVTBKG5XJ9ZAqa9sgXuEKu7AvSCBhCpG11O0bVg9wBxa053fTclHhHlFBt21IzgZDZD
FACEBOOK_PAGE_ID=103991726050308
FACEBOOK_APP_ID=557786413879136
FACEBOOK_VERIFY_TOKEN=VIV_CLINIC_VERIFY_TOKEN
```

### שלב 4: הגדרת Webhook
1. קבל את ה-URL מRailway (משהו כמו: `https://your-app.railway.app`)
2. הגדר webhook בפייסבוק: `https://your-app.railway.app/webhook`

---

## 🎯 אפשרות 3: Render

### שלב 1: הכנה
1. **צור חשבון Render**: https://render.com/
2. **חבר GitHub**: התחבר עם GitHub

### שלב 2: יצירת Web Service
1. לחץ "New +"
2. בחר "Web Service"
3. חבר את הrepository
4. הגדרות:
   - **Name**: `viv-clinic-bot`
   - **Branch**: `viv-clinic-facebook-bot-integration`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn production_server:app`

### שלב 3: משתני סביבה
הוסף ב-Environment Variables:
```
FACEBOOK_ACCESS_TOKEN=EAAH7TcUPT2ABO8w0q1NNraDY3UASS0afjxHAKJk68cKj9TxlScM2fYFl01TaQbrZBqtSRqf9pYyteGx0zpN8F2yZB9xP9eli5ZBap9UT4qziZAqJZCTZAASfgI1BwBwlem0b5UWVTBKG5XJ9ZAqa9sgXuEKu7AvSCBhCpG11O0bVg9wBxa053fTclHhHlFBt21IzgZDZD
FACEBOOK_PAGE_ID=103991726050308
FACEBOOK_APP_ID=557786413879136
FACEBOOK_VERIFY_TOKEN=VIV_CLINIC_VERIFY_TOKEN
```

---

## ✅ בדיקה שהכל עובד

לאחר הדיפלויימנט:

1. **בדוק את הבוט**: `https://your-app-url.com/test`
2. **בדוק הודעות**: `https://your-app-url.com/messages`
3. **בדוק webhook**: שלח הודעה בפייסבוק לדף VIV Clinic

## 🔧 פתרון בעיות

### אם הבוט לא עובד:
1. בדוק logs: `heroku logs --tail` (או ב-Railway/Render dashboard)
2. ודא שמשתני הסביבה נקלטו נכון
3. בדוק שה-webhook מוגדר נכון בפייסבוק

### אם יש שגיאות:
1. בדוק שכל הקבצים נדחפו ל-GitHub
2. ודא ש-requirements.txt מעודכן
3. בדוק שה-Procfile נכון

## 🎉 סיום

ברגע שהדיפלויימנט מושלם, הבוט יהיה זמין 24/7 ויוכל לקבל הודעות מלקוחות בפייסבוק!

**איזה פלטפורמה תרצה להשתמש? Heroku, Railway או Render?**