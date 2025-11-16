# WebGarden Site Deployment - Quick Start

Deploy a complete new site in **15 minutes** with just 2 commands!

## Prerequisites Check

```bash
# Verify you have everything:
which psql nginx systemctl certbot python3 pip3
# All should return paths - if not, see deploy/README.md for installation
```

## Deploy in 2 Steps

### Step 1: Run Infrastructure Deployment (5 minutes)

```bash
cd /var/www/webgarden/webgarden/deploy

# Template:
sudo ./new_site.sh <site_id> <domain> <port> <db_password> "<site_name>"

# Example:
sudo ./new_site.sh dentist dentist.mywebgarden.com 8003 "SecurePass2024!" "Smile Dental Clinic"
```

**What this does:**
- Creates PostgreSQL database
- Sets up Python virtual environment
- Configures Nginx reverse proxy
- Creates systemd service
- Installs all dependencies
- Prompts for admin user creation
- Optionally sets up SSL

### Step 2: Build Site with Claude Code (10 minutes)

```bash
# 1. Open the prompt template
cat deploy/SITE_CREATION_PROMPT.md

# 2. Fill in all [BRACKETED] sections with your business info

# 3. Copy the filled prompt and paste into Claude Code

# 4. Wait for Claude to build your complete site

# 5. Restart the service
sudo systemctl restart dentist.service

# 6. Visit your site!
```

## Port Reference

Use the next available port:

- 8001: psyling (therapist site)
- 8002: keystone (landscaping site)
- **8003: NEXT AVAILABLE**
- 8004+: Future sites

## Quick Commands

```bash
# Check what's running
sudo systemctl status dentist.service

# View logs
sudo journalctl -u dentist.service -f

# Restart site
sudo systemctl restart dentist.service

# Create admin (if skipped during deployment)
cd /var/www/webgarden/webgarden/sites/dentist
venv/bin/flask create-admin

# Set up SSL (if skipped during deployment)
sudo certbot --nginx -d dentist.mywebgarden.com
```

## Troubleshooting

**Service won't start?**
```bash
sudo journalctl -u dentist.service -n 50
```

**502 Bad Gateway?**
```bash
# Check if app is running
sudo systemctl status dentist.service

# Check port is correct
sudo netstat -tuln | grep 8003
```

**Need to start over?**
```bash
# Delete everything and redeploy
sudo systemctl stop dentist.service
sudo rm -rf /var/www/webgarden/webgarden/sites/dentist
sudo -u postgres psql -c "DROP DATABASE dentist_db;"
sudo -u postgres psql -c "DROP USER dentist_user;"
sudo rm /etc/webgarden/dentist.env
sudo rm /etc/nginx/sites-enabled/dentist
sudo rm /etc/systemd/system/dentist.service
sudo systemctl daemon-reload
```

## Next Steps After Deployment

1. ✓ Infrastructure deployed (Step 1)
2. ✓ Site built with Claude Code (Step 2)
3. **Test everything:**
   - Visit homepage
   - Test contact form
   - Log into admin panel
   - Create test blog post
4. **Add real content:**
   - Upload photos
   - Replace placeholder text
   - Add testimonials
5. **Configure email:**
   - Update Mailgun credentials in `/etc/webgarden/dentist.env`
   - Restart service
6. **Monitor:**
   - Check logs regularly
   - Set up backups
   - Monitor performance

## Full Documentation

- **Complete guide:** `deploy/README.md`
- **Prompt template:** `deploy/SITE_CREATION_PROMPT.md`
- **Troubleshooting:** See README.md "Troubleshooting" section

---

**Ready?** Run Step 1 now! 🚀
