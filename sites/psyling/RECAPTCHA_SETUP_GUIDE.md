# reCAPTCHA Setup Guide

## Quick Start (5 Minutes)

Follow these steps to activate reCAPTCHA v3 spam protection on the contact form.

---

## What You'll Get

- **90-95% spam reduction** (combined with honeypot)
- **Invisible to users** (no puzzles or challenges)
- **AI-powered bot detection**
- **Free** (Google provides 1M assessments/month free)

---

## Step-by-Step Setup

### Step 1: Register Your Site with Google (2 minutes)

1. **Visit:** https://www.google.com/recaptcha/admin/create

2. **Sign in** with Google account (use business/admin account)

3. **Fill out the form:**
   - **Label:** `Psyling Contact Form`
   - **reCAPTCHA type:** Select **"reCAPTCHA v3"**
   - **Domains:** Enter these (one per line):
     ```
     psyling.com
     www.psyling.com
     ```
   - **Owners:** (Optional) Add other admin emails
   - **Accept reCAPTCHA Terms of Service:** ✓ Check the box

4. **Click "Submit"**

5. **Save your keys** - You'll see two keys:
   ```
   Site Key: 6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   Secret Key: 6LcYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
   ```

   **IMPORTANT:** Keep the Secret Key private!

---

### Step 2: Add Keys to Environment File (1 minute)

1. **SSH into server** (if not already connected)

2. **Edit the .env file:**
   ```bash
   sudo nano /var/www/webgarden/sites/psyling/.env
   ```

3. **Add these lines at the end:**
   ```bash
   # reCAPTCHA v3 Spam Prevention
   RECAPTCHA_SITE_KEY=6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   RECAPTCHA_SECRET_KEY=6LcYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
   ```

   **Replace the X's and Y's with your actual keys!**

4. **Save and exit:**
   - Press `Ctrl + O` (save)
   - Press `Enter` (confirm)
   - Press `Ctrl + X` (exit)

---

### Step 3: Restart the Service (1 minute)

```bash
sudo systemctl restart psyling
```

**Verify it's running:**
```bash
sudo systemctl status psyling
```

You should see: `Active: active (running)`

---

### Step 4: Test It Works (1 minute)

1. **Visit contact page:**
   https://psyling.com/contact

2. **Look for reCAPTCHA badge:**
   - Should appear in bottom-right corner
   - Small gray badge that says "reCAPTCHA"

3. **Submit a test form:**
   - Fill out the contact form
   - Submit it
   - Should work normally (no puzzles!)

4. **Check the logs:**
   ```bash
   sudo journalctl -u psyling -n 50 | grep reCAPTCHA
   ```

   You should see something like:
   ```
   INFO: reCAPTCHA passed from IP 123.45.67.89: score=0.9
   ```

   **Score interpretation:**
   - 0.9-1.0 = Very likely human ✅
   - 0.7-0.9 = Likely human ✅
   - 0.5-0.7 = Possibly human ⚠️
   - 0.3-0.5 = Possibly bot ⚠️
   - 0.0-0.3 = Very likely bot ❌

---

## Verification Checklist

✅ reCAPTCHA badge appears on contact page
✅ Form submits successfully
✅ No JavaScript errors in browser console (F12)
✅ Logs show "reCAPTCHA passed" with score
✅ Score is above 0.5

---

## What If Something Goes Wrong?

### Problem: Badge Doesn't Appear

**Check 1:** Verify keys are set:
```bash
grep RECAPTCHA /var/www/webgarden/sites/psyling/.env
```

Should show two lines with your keys.

**Check 2:** Verify domain matches:
- Go to https://www.google.com/recaptcha/admin
- Click on your site
- Check "Domains" section
- Make sure `psyling.com` is listed

**Check 3:** Clear browser cache and reload

**Check 4:** Check browser console for errors (F12)

### Problem: Form Fails with "reCAPTCHA verification failed"

**Check 1:** Verify Secret Key is correct:
```bash
grep RECAPTCHA_SECRET_KEY /var/www/webgarden/sites/psyling/.env
```

**Check 2:** Make sure Site Key and Secret Key are from the same registration

**Check 3:** Check firewall allows outbound HTTPS:
```bash
curl -I https://www.google.com/recaptcha/api/siteverify
```

Should return: `HTTP/2 405` (method not allowed is OK - means connection works)

### Problem: All Users Get "Suspicious Submission"

**Cause:** Score threshold too strict

**Fix:** Lower the threshold temporarily:

1. Edit app.py:
   ```bash
   sudo nano /var/www/webgarden/sites/psyling/app.py
   ```

2. Find this line (around line 220):
   ```python
   if score < 0.5:
   ```

3. Change to:
   ```python
   if score < 0.3:  # More permissive
   ```

4. Save and restart:
   ```bash
   sudo systemctl restart psyling
   ```

---

## Monitoring & Maintenance

### View reCAPTCHA Scores (Daily/Weekly)

```bash
sudo journalctl -u psyling --since "1 day ago" | grep reCAPTCHA
```

### View Rejected Bots

```bash
sudo journalctl -u psyling --since "1 week ago" | grep "low score"
```

### View Honeypot Catches

```bash
sudo journalctl -u psyling --since "1 week ago" | grep Honeypot
```

### Check Total Spam Blocked

```bash
sudo journalctl -u psyling --since "1 week ago" | grep -E "(Honeypot|low score)" | wc -l
```

---

## reCAPTCHA Admin Console

**URL:** https://www.google.com/recaptcha/admin

**What you can see:**
- Request volume over time
- Score distribution
- Top domains/IPs
- Error rates

**Recommended:** Check monthly to:
- Verify it's working
- Review patterns
- Check for issues

---

## Costs

**Google reCAPTCHA v3:**
- **Free tier:** 1,000,000 assessments/month
- **Paid tier:** $1 per 1,000 assessments beyond free tier

**Your estimated usage:**
- Contact form submissions: ~100-500/month
- Well within free tier
- **Expected cost: $0/month**

---

## Security Notes

### DO NOT:
- ❌ Commit .env file to git
- ❌ Share Secret Key publicly
- ❌ Share Secret Key in emails/chat
- ❌ Use same keys across multiple sites

### DO:
- ✅ Keep Secret Key private
- ✅ Use environment variables (.env)
- ✅ Regenerate keys if compromised
- ✅ Monitor reCAPTCHA admin console
- ✅ Update keys if you change domains

### If Keys Are Compromised:

1. Go to https://www.google.com/recaptcha/admin
2. Click your site
3. Click "Regenerate keys"
4. Update .env file with new keys
5. Restart service

---

## Optional: Hide reCAPTCHA Badge

By default, the reCAPTCHA badge appears in bottom-right corner. You can hide it if you add a notice to your privacy policy.

### Step 1: Add CSS

Edit `templates/contact.html` and add:
```html
<style>
.grecaptcha-badge {
    visibility: hidden;
}
</style>
```

### Step 2: Add Privacy Notice

Add this text to your contact page or privacy policy:
```
This site is protected by reCAPTCHA and the Google
Privacy Policy and Terms of Service apply.
```

With links:
```html
This site is protected by reCAPTCHA and the Google
<a href="https://policies.google.com/privacy">Privacy Policy</a> and
<a href="https://policies.google.com/terms">Terms of Service</a> apply.
```

**Note:** This is optional. Most sites leave the badge visible.

---

## Summary

**Time to complete:** 5 minutes
**Difficulty:** Easy
**Cost:** $0
**Result:** 90%+ spam reduction

**Steps:**
1. ✅ Register at https://www.google.com/recaptcha/admin/create
2. ✅ Add keys to .env file
3. ✅ Restart service
4. ✅ Test on contact page
5. ✅ Monitor logs

**Need help?** Check the troubleshooting section above or review full documentation in `PHASE2_SPAM_PREVENTION_IMPLEMENTATION.md`.

---

**Created:** 2026-03-10
**Status:** Ready for setup
