# 🤖 Telegram Bot & Mini App Setup Guide

## 📋 Quick Setup Checklist

### 1. 🤖 Configure Bot with @BotFather

1. **Find @BotFather** on Telegram
2. **Send `/newapp`** command
3. **Select your bot** (if you have multiple)
4. **Fill in the details:**
   - **Title:** `Expense Tracker`
   - **Description:** `Track your expenses with a modern, minimalist interface`
   - **Photo:** Upload an icon (optional)
   - **Web App URL:** `https://snake-olc6ureru-volodymyr-s-projects-9f0184a4.vercel.app`

### 2. 🔗 Webhook Configuration

Your webhook is automatically configured at:
- **Webhook URL:** `https://snake-olc6ureru-volodymyr-s-projects-9f0184a4.vercel.app/webhook`
- **Method:** POST
- **Content-Type:** application/json

### 3. 📱 Mini App Features

Your Mini App includes:
- ✅ **Automatic Telegram Authentication** - Users are automatically signed in
- ✅ **User Level Detection** - Guest/Registered/Premium/Admin levels
- ✅ **Multi-Storage System** - Different storage based on user level
- ✅ **Real-time Updates** - Instant expense tracking
- ✅ **Modern UI** - Black & white design with rounded corners

### 4. 🧪 Testing Your Bot

1. **Find your bot** on Telegram (search for @your_bot_username)
2. **Send `/start`** command
3. **Tap "📱 Open Expense Tracker"** button
4. **Verify automatic authentication** (should show your Telegram info)
5. **Test expense creation** and viewing

## 🔧 Environment Variables

Set these in your Vercel dashboard:

```
BOT_TOKEN=8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4
WEBAPP_URL=https://snake-olc6ureru-volodymyr-s-projects-9f0184a4.vercel.app
WEBHOOK_URL=https://snake-olc6ureru-volodymyr-s-projects-9f0184a4.vercel.app/webhook
```

## 📱 Bot Commands

Your bot supports these commands:

- `/start` - Open the Expense Tracker app
- `/help` - Show help and available commands  
- `/about` - About the application
- `/settings` - Bot and app settings
- `/stats` - Quick expense statistics

## 🎯 User Authentication Flow

1. **User opens Mini App** from bot
2. **Telegram provides user data** automatically
3. **App authenticates user** based on Telegram ID
4. **User level determined** (Guest/Registered/Premium/Admin)
5. **Storage backend selected** based on user level
6. **User can immediately** start tracking expenses

## 🔐 User Levels & Storage

| Level | Storage | Features |
|-------|---------|----------|
| 👤 **Guest** | Memory | Basic tracking, session only |
| 📝 **Registered** | File | Persistent storage, local files |
| ⭐ **Premium** | Database | SQLite, advanced features |
| 👑 **Admin** | Cloud | Enhanced DB, full access |

## 🚀 Deployment Commands

```bash
# Deploy to Vercel
vercel --prod

# Setup webhook (run once)
curl -X POST https://snake-olc6ureru-volodymyr-s-projects-9f0184a4.vercel.app/bot/setup

# Test webhook
curl -X GET https://snake-olc6ureru-volodymyr-s-projects-9f0184a4.vercel.app/bot/info
```

## 🔍 Troubleshooting

### Bot Not Responding
- Check if webhook is set: `GET /bot/info`
- Verify bot token is correct
- Check Vercel logs for errors

### Mini App Not Loading
- Verify Mini App URL in @BotFather
- Check if app is deployed and accessible
- Test URL in browser first

### Authentication Issues
- Check if user data is being passed correctly
- Verify Telegram WebApp data format
- Check browser console for errors

## 📞 Support

If you need help:
1. Check the logs in Vercel dashboard
2. Test individual endpoints
3. Verify environment variables
4. Contact support with error details

---

**🎉 Your Telegram Mini App is ready!**

Users can now:
- Open your bot and tap "📱 Open Expense Tracker"
- Automatically sign in with their Telegram account
- Track expenses with their appropriate storage level
- Enjoy a modern, clean interface

**Happy expense tracking!** 💰📱
