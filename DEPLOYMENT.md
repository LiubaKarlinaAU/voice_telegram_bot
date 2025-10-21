# Railway Deployment Guide

## 🚀 Deploying Telegram PDF to MP3 Bot on Railway

### Prerequisites
1. Railway account (sign up at [railway.app](https://railway.app))
2. GitHub repository with your bot code
3. Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
4. Groq API Token (from [console.groq.com](https://console.groq.com))

### Step 1: Prepare Your Repository

Your project structure should look like this:
```
telegram_bot/
├── bot.py              # Main bot file
├── config.py           # Configuration
├── handlers.py         # Bot handlers
├── utils.py           # Utility functions
├── requirements.txt    # Python dependencies
├── Procfile           # Railway process file
├── railway.json       # Railway configuration
├── runtime.txt        # Python version
└── .env               # Environment variables (local only)
```

### Step 2: Environment Variables

In Railway dashboard, add these environment variables:
- `BOT_TOKEN`: Your Telegram bot token
- `GROQ_TOKEN`: Your Groq API token

### Step 3: Deploy to Railway

#### Option A: Deploy from GitHub
1. Connect your GitHub repository to Railway
2. Railway will automatically detect it's a Python project
3. Set environment variables in Railway dashboard
4. Deploy!

#### Option B: Deploy via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Set environment variables
railway variables set BOT_TOKEN=your_bot_token_here
railway variables set GROQ_TOKEN=your_groq_token_here

# Deploy
railway up
```

### Step 4: Configure Railway Settings

1. **Build Command**: Railway will auto-detect Python
2. **Start Command**: `python bot.py`
3. **Port**: Railway handles this automatically
4. **Environment**: Production

### Step 5: Monitor Your Bot

- Check Railway logs for any errors
- Test your bot with `/start` command
- Monitor resource usage in Railway dashboard

### 🔧 Troubleshooting

#### Common Issues:

1. **Import Errors**: Make sure all files are in the same directory
2. **Environment Variables**: Double-check they're set in Railway dashboard
3. **Memory Issues**: Railway free tier has memory limits
4. **Timeout**: Bot might restart if idle for too long

#### Logs to Check:
```bash
# View Railway logs
railway logs
```

### 📊 Railway Configuration

The `railway.json` file configures:
- Build process
- Start command
- Restart policy
- Resource limits

### 🚨 Important Notes

1. **Free Tier Limits**: Railway free tier has usage limits
2. **Environment Variables**: Never commit `.env` files to Git
3. **Dependencies**: All dependencies are in `requirements.txt`
4. **Python Version**: Specified in `runtime.txt`

### 🔄 Updates

To update your bot:
1. Push changes to GitHub
2. Railway will auto-deploy
3. Or use `railway up` for manual deployment

### 📈 Scaling

For production use:
- Upgrade to Railway Pro plan
- Set up monitoring
- Configure auto-scaling
- Add health checks

### 🛡️ Security

- Keep API tokens secure
- Use Railway's environment variables
- Don't expose sensitive data in logs
- Regular security updates

### 📞 Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Telegram Bot API: [core.telegram.org/bots/api](https://core.telegram.org/bots/api)
