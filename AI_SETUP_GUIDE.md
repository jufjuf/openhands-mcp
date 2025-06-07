# 🤖 מדריך הגדרת מנוע AI לבוט VIV Clinic

## 🎯 סקירה כללית

הבוט תומך במספר ספקי AI:
- **Google Gemini** (מומלץ - חינמי עד 60 בקשות לדקה)
- **OpenAI GPT** (בתשלום - הכי חכם)
- **Anthropic Claude** (בתשלום - בטוח מאוד)

## ✅ מצב נוכחי
הבוט כבר מוכן לעבודה עם מנוע AI! כרגע הוא עובד במצב fallback עם תגובות חכמות מוגדרות מראש.

## 🎯 ספקי AI נתמכים

### 1. OpenAI GPT (מומלץ)
- **מודל**: GPT-3.5-turbo או GPT-4
- **יתרונות**: תמיכה מעולה בעברית, מהיר ויציב
- **עלות**: ~$0.002 לכל 1K tokens
- **הגדרה**: https://platform.openai.com/api-keys

### 2. Google Gemini
- **מודל**: gemini-pro
- **יתרונות**: חינמי עד 60 בקשות לדקה
- **תמיכה בעברית**: טובה
- **הגדרה**: https://makersuite.google.com/app/apikey

### 3. Anthropic Claude
- **מודל**: claude-3-haiku-20240307
- **יתרונות**: מהיר וחסכוני
- **תמיכה בעברית**: טובה
- **הגדרה**: https://console.anthropic.com/

## 🔧 הגדרת משתני סביבה

### Railway/Heroku/Render:
```bash
# OpenAI (מומלץ)
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo
AI_PROVIDER=openai

# Google Gemini (חלופה חינמית)
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-pro
AI_PROVIDER=gemini

# Anthropic Claude (חלופה מתקדמת)
CLAUDE_API_KEY=your-claude-api-key
CLAUDE_MODEL=claude-3-haiku-20240307
AI_PROVIDER=claude
```

### קובץ .env מקומי:
```bash
cp .env.example .env
# ערוך את הקובץ והוסף את המפתחות שלך
```

## 📝 הוראות הגדרה מפורטות

### OpenAI (מומלץ למתחילים)

1. **צור חשבון**: https://platform.openai.com/signup
2. **קבל API Key**: https://platform.openai.com/api-keys
3. **הוסף credit**: מינימום $5 לתחילת עבודה
4. **הגדר משתנים**:
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   AI_PROVIDER=openai
   ```

### Google Gemini (חינמי)

1. **צור פרויקט**: https://console.cloud.google.com/
2. **הפעל Gemini API**: https://makersuite.google.com/
3. **קבל API Key**: https://makersuite.google.com/app/apikey
4. **הגדר משתנים**:
   ```bash
   GEMINI_API_KEY=your-gemini-key-here
   GEMINI_MODEL=gemini-pro
   AI_PROVIDER=gemini
   ```

### Anthropic Claude

1. **צור חשבון**: https://console.anthropic.com/
2. **קבל API Key**: https://console.anthropic.com/account/keys
3. **הוסף credit**: מינימום $5
4. **הגדר משתנים**:
   ```bash
   CLAUDE_API_KEY=sk-ant-your-key-here
   CLAUDE_MODEL=claude-3-haiku-20240307
   AI_PROVIDER=claude
   ```

## 🚀 פריסה לפרודקשן

### Railway:
```bash
# הוסף משתני סביבה ב-Railway Dashboard
railway variables set OPENAI_API_KEY=sk-your-key
railway variables set AI_PROVIDER=openai
railway deploy
```

### Heroku:
```bash
heroku config:set OPENAI_API_KEY=sk-your-key
heroku config:set AI_PROVIDER=openai
git push heroku main
```

### Render:
1. עבור ל-Dashboard
2. הוסף Environment Variables
3. Deploy מחדש

## 🧪 בדיקת התקנה

### בדיקה מקומית:
```bash
python ai_chat_engine.py
```

### בדיקה בפרודקשן:
1. עבור ל: `https://your-app.railway.app/ai/status`
2. בדוק שהסטטוס הוא "active"
3. נסה: `https://your-app.railway.app/ai/test`

### בדיקה בממשק הצ'אט:
1. עבור ל: `https://your-app.railway.app/chat`
2. שלח הודעה: "שלום, אני רוצה לקבוע תור לטיפול שיניים"
3. בדוק שהתגובה טבעית ומותאמת

## 📊 ניטור ועלויות

### OpenAI:
- **עלות**: ~$0.002 לכל 1K tokens
- **ניטור**: https://platform.openai.com/usage
- **הגבלות**: 3 RPM (Requests Per Minute) בחשבון חינמי

### Google Gemini:
- **עלות**: חינמי עד 60 RPM
- **ניטור**: https://console.cloud.google.com/
- **הגבלות**: 60 בקשות לדקה

### Anthropic Claude:
- **עלות**: ~$0.00025 לכל 1K tokens
- **ניטור**: https://console.anthropic.com/
- **הגבלות**: תלוי בתוכנית

## 🔧 התאמות מתקדמות

### שינוי אישיות הבוט:
ערוך את `system_prompt` בקובץ `ai_chat_engine.py`:

```python
self.system_prompt = """
אתה בוט שירות לקוחות של VIV Clinic...
[התאם את האישיות והסגנון כאן]
"""
```

### הגדרת מודלים שונים:
```bash
# GPT-4 (יקר יותר, איכות גבוהה יותר)
OPENAI_MODEL=gpt-4

# GPT-3.5-turbo (מומלץ - איזון טוב)
OPENAI_MODEL=gpt-3.5-turbo

# Claude Sonnet (איכות גבוהה)
CLAUDE_MODEL=claude-3-sonnet-20240229
```

## 🛠️ פתרון בעיות

### בעיה: "AI engine not initialized"
**פתרון**: בדוק שמשתני הסביבה מוגדרים נכון

### בעיה: "API key invalid"
**פתרון**: 
1. בדוק שה-API key נכון
2. בדוק שיש credit בחשבון
3. בדוק שה-API מופעל

### בעיה: תגובות באנגלית
**פתרון**: עדכן את ה-system_prompt לדגיש עברית

### בעיה: תגובות איטיות
**פתרון**: 
1. עבור ל-GPT-3.5-turbo במקום GPT-4
2. נסה Gemini או Claude
3. בדוק את חיבור האינטרנט

## 📈 אופטימיזציה

### חיסכון בעלויות:
1. השתמש ב-GPT-3.5-turbo במקום GPT-4
2. הגבל את אורך ההיסטוריה (כרגע 10 הודעות)
3. השתמש ב-Gemini לבדיקות

### שיפור איכות:
1. עבור ל-GPT-4 לתגובות מורכבות
2. התאם את ה-system_prompt
3. הוסף דוגמאות ספציפיות

## 🔄 גיבוי ו-Fallback

המערכת כוללת מנגנון fallback אוטומטי:
1. אם ה-AI לא זמין - תגובות קבועות מראש
2. אם יש שגיאה - הודעת שגיאה ידידותית
3. אם אין API key - מצב fallback מלא

## 📞 תמיכה

לעזרה נוספת:
1. בדוק את הלוגים: `railway logs` או `heroku logs`
2. נסה את endpoint הבדיקה: `/ai/test`
3. בדוק את הסטטוס: `/ai/status`

---

**🎯 המלצה**: התחל עם Google Gemini (חינמי) לבדיקות, ועבור ל-OpenAI GPT-3.5-turbo לפרודקשן.