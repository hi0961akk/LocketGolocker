# 🔓 Locket Gold Premium Unlocker

**Unlock Locket Gold premium features with just a username — no password required!**

A Flask-based service that automatically restores purchased Locket Gold subscriptions for any username. Features an admin panel for account management, real-time queue processing, and seamless Vercel deployment.

---

## ✨ Features

- 🚀 **Quick Restore** — Enter any Locket username to unlock Gold features instantly
- 👤 **No Password Needed** — Uses temporary email accounts for silent verification
- ⚙️ **Admin Panel** — Manage accounts, tokens, and monitor queue status in real-time
- 🌐 **Multi-Account Rotation** — Automatically rotates through multiple Locket accounts
- 📊 **Queue Management** — Handles concurrent restore requests with fair scheduling
- 🔐 **RevenueCat Integration** — Forges premium subscription receipts with custom tokens
- 📝 **Account Bulk Creator** — `create_accounts.py` script to auto-generate accounts via Foxycrown temp mail
- 🚁 **Serverless Deployment** — Optimized for Vercel with SQLite persistence
- 🔔 **Telegram Notifications** — Optional success alerts to your Telegram chat
- 📱 **Mobile-Friendly** — Responsive UI with SweetAlert2 and reCAPTCHA

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (index.html)                   │
│  Vanilla JS + SweetAlert2 + reCAPTCHA                      │
│  Polls /api/restore → /api/queue/status every 1s          │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Flask Routes Layer                         │
│  ┌─────────────────────────────────────────────────────────┐
│  │ Public:  /api/restore, /api/queue/status               │
│  │ Admin:   /admin/login, /admin/api/*                    │
│  └─────────────────────────────────────────────────────────┘
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│          QueueManager (Daemon Thread Pool)                   │
│  ┌─────────────────────────────────────────────────────────┐
│  │ Polls SQLite queue_requests every 0.5s                 │
│  │ 1 worker thread per Locket account (slots)             │
│  │ Processes restore requests atomically                  │
│  └─────────────────────────────────────────────────────────┘
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              AccountRotator (In-Memory Cache)                │
│  ┌─────────────────────────────────────────────────────────┐
│  │ Keys: stable UUIDs (slot_id)                            │
│  │ Values: Auth + LocketAPI instances per account         │
│  │ Sources: accounts table + environment seed              │
│  └─────────────────────────────────────────────────────────┘
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              SQLite Database (locket.db)                     │
│  ┌─────────────────────────────────────────────────────────┐
│  │ Tables:                                                 │
│  │  • accounts — Locket credentials + status               │
│  │  • queue_requests — User restore requests              │
│  │  • queue_claims — Atomic claim tracking                │
│  │  • processing_times — Performance history              │
│  │  • recent_log — Latest 30 completions                  │
│  │  • tokens — RevenueCat receipts (alt: gist_token_url)  │
│  └─────────────────────────────────────────────────────────┘
└──────────────────────────────────────────────────────────────┘
```

### Key Modules

| Module | Purpose |
|--------|---------|
| `locket/__init__.py` | Flask app factory — bootstraps config, DB, rotator, queue, blueprints |
| `locket/db.py` | SQLite schema creation + thread-local connections |
| `locket/rotator.py` | AccountRotator — in-memory cache of Auth + LocketAPI instances |
| `locket/queue_manager.py` | QueueManager + worker threads — polls DB every 0.5s, processes requests |
| `locket/locket_auth.py` | Auth class — posts to Firebase identitytoolkit verifyPassword |
| `locket/locket_api.py` | LocketAPI class — getUserByUsername, getLastMoment, restorePurchase |
| `locket/tokens.py` | TokensStore — manages RevenueCat receipts (DB or gist fallback) |
| `locket/admin/` | Admin panel — login, account/token CRUD, queue monitoring |
| `locket/public/` | Public routes — /api/restore, /api/queue/status, /, /api/get-user-info |
| `create_accounts.py` | Bulk account creator — spawns temp mail accounts via Foxycrown |
| `app.py` | Entry point — Flask dev server & Vercel/Gunicorn compatibility |
| `wsgi.py` | WSGI entry for gunicorn (production VPS deployments) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- SQLite 3.35+ (pre-installed on most systems)
- pip or venv

### Local Development

1. **Clone & Install**
   ```bash
   git clone https://github.com/hi0961akk/LocketGolocker.git
   cd LocketGolocker
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and set:
   #   ADMIN_PASSWORD=<your_admin_password>
   #   EMAIL=<locket_email> (optional seed account)
   #   PASSWORD=<locket_password>
   nano .env
   ```

3. **Run**
   ```bash
   python app.py
   ```
   
   Open: **http://localhost:5001**
   - Frontend: http://localhost:5001/
   - Admin: http://localhost:5001/admin/login

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `ADMIN_PASSWORD` | ✅ Yes | Password for `/admin` panel |
| `EMAIL` | ❌ No | Seed Locket account email (for first boot) |
| `PASSWORD` | ❌ No | Seed Locket account password |
| `FLASK_SECRET_KEY` | ❌ No | Session cookie encryption (random if unset) |
| `BEHIND_HTTPS` | ❌ No | Set to `1` if behind nginx/reverse proxy with TLS |
| `gist_token_url` | ❌ No | JSON array URL of RevenueCat payloads (fallback) |
| `TELEGRAM_BOT_TOKEN` | ❌ No | Telegram bot token for success notifications |
| `TELEGRAM_CHAT_ID` | ❌ No | Telegram chat ID for notifications |
| `LOCKET_DB` | ❌ No | SQLite path (default: `locket.db` in cwd) |

### App Startup Behavior

- **With seed account** (`EMAIL` + `PASSWORD` set):
  - Creates one initial account in the database on first boot
  - QueueManager spawns 1 worker thread
  
- **Without seed account**:
  - Boots with 0 accounts (gracefully)
  - Public endpoints return HTTP 503 until accounts are added
  - Admin panel remains accessible to add accounts manually

---

## 📋 Creating Accounts (Bulk)

The `create_accounts.py` script auto-generates Locket accounts via Foxycrown temporary email:

```bash
# Basic: 5 accounts, sequential pattern, no proxy
python create_accounts.py --count 5 \
  --password 'StrongPwd123!' \
  --email-pattern 'locket_{i}@crxmail.com'

# Advanced: 100 accounts, 10 parallel workers, rotating proxies
python create_accounts.py --count 100 \
  --workers 10 \
  --password 'StrongPwd123!' \
  --email-pattern 'locket_{i}@crxmail.com' \
  --proxy-file proxies.txt

# Random Foxycrown email, no pattern
python create_accounts.py --count 5 \
  --password 'StrongPwd123!' \
  --domain crxmail.com
```

Output: `created_accounts.json` (progress saved after each success)
Automatically adds accounts to the DB (unless `--no-add` is passed).

For full details: `python create_accounts.py --help`

---

## 🔐 Admin Panel

Access: **http://localhost:5001/admin/login**

### Dashboard Sections

**Accounts**
- Add new Locket credentials (Test Login before saving)
- View all registered accounts + status
- Remove accounts (preserves history)
- Spawn new worker threads instantly

**Tokens**
- Paste RevenueCat subscription payloads
- Override the gist fallback
- Manage multiple token sets

**Queue**
- Real-time view of waiting/processing/completed requests
- Worker performance metrics
- Historical logs (last 30 entries)

**Site Settings** *(future)*
- Theme customization
- Maintenance mode (blocks users, bypasses admin)

---

## 📡 API Reference

### Public Endpoints

#### `POST /api/get-user-info`
Preview a Locket user profile (no queue).

**Request:**
```json
{ "username": "john.doe" }
```

**Response:**
```json
{
  "username": "john.doe",
  "display_name": "John Doe",
  "avatar_url": "https://...",
  "profile_data": {...}
}
```

#### `POST /api/restore`
Request premium restore for a username.

**Request:**
```json
{ "username": "john.doe" }
```

**Response (Success):**
```json
{
  "client_id": "abc123def456",
  "position": 3,
  "total_queue": 12,
  "estimated_time": 45
}
```

**Response (Queue Full):**
```json
{ "error": "Service temporarily unavailable", "code": 503 }
```

#### `POST /api/queue/status`
Poll restore request status.

**Request:**
```json
{ "client_id": "abc123def456" }
```

**Response (Processing):**
```json
{
  "status": "processing",
  "position": 1,
  "total_queue": 10,
  "estimated_time": 30
}
```

**Response (Completed):**
```json
{
  "status": "completed",
  "locket_username": "john.doe",
  "gold_until": "2026-12-31"
}
```

**Response (Expired):**
```json
{
  "status": "not_found"
}
```

#### `GET /api/queue/global-status`
Aggregate queue statistics.

**Response:**
```json
{
  "workers_active": 5,
  "waiting": 12,
  "processing": 5,
  "completed_today": 234
}
```

### Admin Endpoints (Protected)

All require session cookie (`/admin/login`).

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/admin` | GET | Dashboard HTML |
| `/admin/login` | GET/POST | Login form |
| `/admin/logout` | POST | Clear session |
| `/admin/api/accounts` | GET/POST/DELETE | CRUD accounts |
| `/admin/api/accounts/test` | POST | Test login for email |
| `/admin/api/tokens/<index>` | GET/POST/DELETE | CRUD RevenueCat payloads |
| `/admin/api/queue` | GET | Snapshot of queue state |

---

## 🌐 Deployment

### Option 1: Vercel (Recommended)

Vercel provides **free serverless deployment** with auto-scaling. SQLite persists using Vercel's Blob Storage.

#### Setup Steps

1. **Fork this repository** to your GitHub account

2. **Create Vercel project:**
   - Go to https://vercel.com/new
   - Connect your GitHub fork
   - Vercel auto-detects Python + `vercel.json` config

3. **Set environment variables** in Vercel dashboard:
   ```
   ADMIN_PASSWORD=<random_password>
   EMAIL=<your_locket_email> (optional)
   PASSWORD=<your_locket_password> (optional)
   FLASK_SECRET_KEY=<openssl rand -hex 32>
   BEHIND_HTTPS=1
   gist_token_url=https://gist.githubusercontent.com/.../raw
   TELEGRAM_BOT_TOKEN=<your_bot_token> (optional)
   TELEGRAM_CHAT_ID=<your_chat_id> (optional)
   ```

4. **Deploy:**
   - Vercel automatically deploys on each push to `main`
   - Access at: `https://your-project.vercel.app`
   - Admin: `https://your-project.vercel.app/admin/login`

#### Vercel Limitations & Workarounds

⚠️ **Serverless constraints:**
- **No persistent filesystem** — SQLite lives in `/tmp` and resets on each deployment
- **15-min max execution time** — long-running queue jobs must complete within this window
- **No background workers** — the QueueManager thread pool doesn't survive between requests

✅ **Workarounds:**
- Use **Vercel Blob Storage** to persist `locket.db` (requires paid plan or custom setup)
- Alternative: **Deploy to VPS** (see below) for persistent background processing
- For demo/testing: SQLite auto-seeds from `created_accounts.json` on each boot

#### To Add Blob Storage (Advanced)

```bash
npm install @vercel/blob
```

Modify `locket/db.py` to sync SQLite to Blob on write.

### Option 2: VPS Deployment (Ubuntu/Debian)

For **production with persistent background workers**.

#### Prerequisites
- Ubuntu 22.04+ or Debian 12+
- ≥ 512 MB RAM
- Domain with A-record pointing to VPS IP
- Cloudflare account (optional but recommended for protection)

#### Quick Install

```bash
# 1. SSH to VPS as root
ssh root@<your_ip>

# 2. Update system & install dependencies
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git nginx

# 3. Create app user
sudo adduser --system --group --shell /bin/bash --home /home/locket locket

# 4. Clone repo
sudo -u locket -i
cd ~
git clone https://github.com/hi0961akk/LocketGolocker.git
cd LocketGolocker
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
exit

# 5. Create .env
sudo nano /home/locket/LocketGolocker/.env
```

Minimum `.env`:
```env
ADMIN_PASSWORD=<random_password>
FLASK_SECRET_KEY=<openssl rand -hex 32>
BEHIND_HTTPS=1
EMAIL=<optional_seed_email>
PASSWORD=<optional_seed_password>
```

```bash
# 6. Setup systemd service
sudo cp /home/locket/LocketGolocker/deploy/locket.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now locket
sudo systemctl status locket

# 7. Setup nginx (Cloudflare-fronted)
sudo cp /home/locket/LocketGolocker/deploy/nginx-cloudflare.conf /etc/nginx/sites-available/locket
sudo sed -i 's/YOUR_DOMAIN/your-domain.com/g' /etc/nginx/sites-available/locket
sudo ln -sf /etc/nginx/sites-available/locket /etc/nginx/sites-enabled/locket
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# 8. Setup Cloudflare (dashboard)
# - DNS: A record → VPS IP, Orange cloud (Proxied)
# - SSL/TLS: Flexible (simplest) or Full (strict) with Origin Certificate

# 9. Firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

Access: **https://your-domain.com**

#### VPS Management

```bash
# View logs
sudo journalctl -u locket -f

# Restart app
sudo systemctl restart locket

# Pull updates
sudo -u locket -i
cd LocketGolocker
git pull
.venv/bin/pip install -r requirements.txt
exit
sudo systemctl restart locket

# Backup database
sudo -u locket sqlite3 /home/locket/LocketGolocker/locket.db \
  ".backup /home/locket/backups/locket-$(date +%F).db"

# Auto-backup via cron (daily at 3 AM)
# sudo crontab -e
# 0 3 * * * sudo -u locket sqlite3 /home/locket/LocketGolocker/locket.db \
#   ".backup /home/locket/backups/locket-$(date +\%F).db"
```

### Option 3: Docker (Custom Setup)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
```

```bash
docker build -t locket-gold .
docker run -p 5001:5001 \
  -e ADMIN_PASSWORD=<password> \
  -e FLASK_SECRET_KEY=<key> \
  -v locket_data:/app \
  locket-gold
```

---

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 503 on `/api/restore` | No accounts in DB | Add account via `/admin/api/accounts` |
| Admin login redirect loop | `BEHIND_HTTPS=1` but accessing via HTTP | Set `BEHIND_HTTPS=0` for local dev, or use HTTPS proxy |
| `ADMIN_PASSWORD not set` error | `.env` not loaded or missing var | Check `.env` path and required vars |
| Worker threads not processing | Account login failed (401 from Locket) | Test account credentials in admin panel |
| Port 5001 in use | Another process on same port | `lsof -ti:5001 \| xargs kill -9` |
| Database locked error | SQLite contention (WAL issue) | Restart app: `sudo systemctl restart locket` |

---

## 📝 License

MIT License — see [LICENSE](./LICENSE)

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. The author assumes no responsibility for misuse or violations of terms of service. Use at your own risk.

- Locket is a trademark of Locket, Inc.
- This tool is not affiliated with or endorsed by Locket.
- Unauthorized account access or service manipulation may violate local laws.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or suggestions:
- Open a GitHub Issue
- Check [CLAUDE.md](./CLAUDE.md) for architecture deep-dive
- Check [deploy.md](./deploy.md) for VPS deployment details

---

## 📚 Additional Resources

- **[CLAUDE.md](./CLAUDE.md)** — Detailed architecture, module breakdown, gotchas
- **[deploy.md](./deploy.md)** — VPS deployment guide (Ubuntu/Debian + Cloudflare)
- **[create_accounts.py](./create_accounts.py)** — Bulk account creation via Foxycrown
- **Requirements**: [requirements.txt](./requirements.txt)
- **Vercel Config**: [vercel.json](./vercel.json)
- **Gunicorn Config**: [gunicorn.conf.py](./gunicorn.conf.py)

---

**Made with ❤️ by the Locket Gold Unlocker community**
