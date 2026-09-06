# 🚀 Deploy to Vercel (5 Minutes)

Vercel provides **free, serverless deployment** with auto-scaling. Your app runs instantly with zero configuration.

---

## Prerequisites

- GitHub account with this repo forked
- Vercel account (free at https://vercel.com)
- A Locket account (for seeding, optional)
- RevenueCat tokens JSON (optional, can use gist)

---

## Step-by-Step Guide

### 1. Fork Repository

Go to https://github.com/hi0961akk/LocketGolocker and click **Fork**.

This creates a copy under your GitHub account.

### 2. Create Vercel Project

1. Visit https://vercel.com/new
2. Click **Continue with GitHub**
3. Select the forked `LocketGolocker` repository
4. Vercel auto-detects Python + reads `vercel.json`
5. Click **Deploy**

Vercel will start building immediately.

### 3. Set Environment Variables

While deploying (or after), go to **Settings → Environment Variables** and add:

#### Required
```env
ADMIN_PASSWORD=YourSecurePassword123!
```

#### Optional (Recommended)
```env
FLASK_SECRET_KEY=<generate via: openssl rand -hex 32>
BEHIND_HTTPS=1
EMAIL=your_locket_email@gmail.com
PASSWORD=your_locket_password
gist_token_url=https://gist.githubusercontent.com/.../raw/tokens.json
TELEGRAM_BOT_TOKEN=<your_bot_token>
TELEGRAM_CHAT_ID=<your_chat_id>
```

**How to generate `FLASK_SECRET_KEY`:**
```bash
openssl rand -hex 32
```
Output: `a1b2c3d4e5f6...` — paste this value.

### 4. Deployment Complete ✅

Your app is live at: **https://[project-name].vercel.app**

- **Frontend**: https://[project-name].vercel.app/
- **Admin**: https://[project-name].vercel.app/admin/login

---

## Post-Deployment

### First Time Setup

1. Open **https://[project-name].vercel.app/admin/login**
2. Login with:
   - **Username**: (if `ADMIN_USERNAME` was set, otherwise use default)
   - **Password**: Your `ADMIN_PASSWORD` from env vars

3. **Accounts** tab:
   - If you seeded with `EMAIL`/`PASSWORD`, one account auto-created
   - Otherwise, manually add Locket credentials:
     - Email
     - Password
     - Click **Test Login** first
     - Then **Save**

4. **Tokens** tab (if not using gist):
   - Add RevenueCat subscription payloads
   - Format: JSON array of receipt objects

5. Test the frontend:
   - Open https://[project-name].vercel.app/
   - Enter a Locket username
   - Click **Unlock Gold**

### Auto-Deploy on Push

Every push to your `main` branch auto-deploys:
```bash
git add .
git commit -m "Update configuration"
git push origin main
```

Vercel rebuilds and redeploys automatically (watch at https://vercel.com/dashboard).

---

## Important Notes

### ⚠️ Vercel Limitations

Vercel is **serverless**, meaning:

1. **No persistent filesystem** — SQLite resets on deployment
   - ✅ Works fine for **demo/testing**
   - ❌ Not ideal for **production with persistent data**

2. **Max 15 minutes per request** — queue jobs must complete within this window
   - ✅ Works for **typical restore requests** (1-5 min each)
   - ❌ May fail for **very long jobs** (rare)

3. **No background workers** — threads don't run between HTTP requests
   - ✅ Still works because QueueManager polls SQLite every 0.5s
   - ✅ Each request triggers at least one poll cycle

### ✅ Workarounds for Production

**Option A: Use Vercel Blob Storage** (Paid)
- Store SQLite in Vercel Blob instead of `/tmp`
- Requires Vercel Pro ($20/month)
- Modify `locket/db.py` to sync with Blob

**Option B: Deploy to VPS Instead** (Recommended for Production)
- Use Ubuntu VPS ($5-10/month)
- Full persistent background workers
- See [deploy.md](./deploy.md) for instructions

**Option C: Accept Reset on Deploy** (Development)
- Database resets when you deploy
- Seed accounts via `EMAIL`/`PASSWORD` on each boot
- Good for testing and demos

---

## Configuration Reference

### Environment Variables in Vercel

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `ADMIN_PASSWORD` | ✅ Yes | — | Session password for `/admin` |
| `ADMIN_USERNAME` | ❌ No | `admin` | Login username (if you want to change it) |
| `FLASK_SECRET_KEY` | ❌ No | Random | If set, preserves admin sessions across restarts |
| `BEHIND_HTTPS` | ❌ No | `0` | Set to `1` when behind reverse proxy |
| `EMAIL` | ❌ No | — | Seed Locket account email (auto-added on boot) |
| `PASSWORD` | ❌ No | — | Seed Locket account password |
| `gist_token_url` | ❌ No | — | JSON array URL of RevenueCat payloads (fallback) |
| `TELEGRAM_BOT_TOKEN` | ❌ No | — | Bot token for success notifications |
| `TELEGRAM_CHAT_ID` | ❌ No | — | Chat ID for Telegram alerts |
| `LOCKET_DB` | ❌ No | `locket.db` | SQLite path (only `/tmp` is writable on Vercel) |

### Vercel Build Config

[vercel.json](./vercel.json) is pre-configured:
```json
{
    "version": 2,
    "builds": [
        {
            "src": "app.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "app.py"
        }
    ]
}
```

**Do NOT modify** unless you know what you're doing.

---

## Monitoring & Logs

### View Logs in Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Select your project
3. Click **Deployments**
4. Click the latest deployment
5. Scroll to **Logs** tab

### Download Logs via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# View logs
vercel logs --project=locket-golocker --follow
```

### Common Errors

| Error | Fix |
|-------|-----|
| `ADMIN_PASSWORD not set` | Add `ADMIN_PASSWORD` to Vercel env vars |
| `ModuleNotFoundError: locket` | `vercel.json` points to wrong file (should be `app.py`) |
| 502 Bad Gateway | App crashed — check logs via Vercel dashboard |
| 503 Service Unavailable | No accounts in DB — seed via `EMAIL`/`PASSWORD` env vars |

---

## Updating Your App

### Pull Latest Changes

```bash
cd your-fork-dir
git pull origin main
git push origin main
```

Vercel auto-redeploys immediately.

### Modify Code Locally

```bash
git clone https://github.com/YOUR-USERNAME/LocketGolocker.git
cd LocketGolocker

# Make your changes
nano locket/some_file.py

# Commit & push
git add .
git commit -m "My changes"
git push origin main
```

Vercel sees the push and redeploys.

---

## Scaling on Vercel

Vercel automatically scales your app:

- **Load spikes** → Automatically spawn additional serverless instances
- **No usage** → Functions sleep (you pay only for execution time)
- **Concurrent requests** → Each spawns its own Python runtime

### Cost Estimate

- **Free Tier**: Up to 100GB bandwidth/month, 1 deployment/day
- **Pro Tier**: $20/month — unlimited deployments, priority support
- **Pay as you go**: Only charged for extra compute beyond free tier

For moderate usage (1000 restores/month), **Free Tier is sufficient**.

---

## Rollback to Previous Version

If a deployment breaks:

1. Go to https://vercel.com/dashboard
2. Select your project → **Deployments**
3. Find the last working version
4. Click the three-dot menu → **Promote to Production**

Your app rolls back to that version instantly.

---

## Need Help?

- **Deployment stuck?** Check Vercel build logs in dashboard
- **App crashing?** Look for env var typos (Vercel is case-sensitive)
- **Database reset on deploy?** This is expected on serverless — use VPS for persistence
- **Questions?** Open an issue on GitHub or check [README.md](./README.md)

---

## Next Steps

### For Production (Persistent Data)

Follow [deploy.md](./deploy.md) instead for **VPS deployment** with:
- ✅ Persistent SQLite database
- ✅ Always-on background workers
- ✅ Better performance for high volume
- ✅ Custom domain & SSL

### For Scaling on Vercel

If you need persistent data on Vercel:
1. Upgrade to **Vercel Pro** ($20/month)
2. Use **Vercel Blob Storage** for SQLite
3. Modify `locket/db.py` to read/write from Blob

---

**Your app is live! 🎉**

Share your link: https://[project-name].vercel.app

Next: Add Locket accounts via `/admin/login` and test the restore workflow.
