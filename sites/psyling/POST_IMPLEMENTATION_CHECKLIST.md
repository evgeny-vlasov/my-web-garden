# Psyling Email System - Post-Implementation Checklist

**Status:** Code implementation complete, awaiting Mailgun DNS setup
**Date:** 2026-02-04
**Completed by:** Claude Code

---

## What Was Done

✅ Flask-Mail already installed and configured
✅ Email templates enhanced for psychotherapy practice
✅ Added Reply-To functionality (Valery can click Reply to respond to clients)
✅ Added emergency contact resources in auto-reply emails
✅ Updated environment file template with psyling.com Mailgun config
✅ Created standalone SMTP test script
✅ Created comprehensive email system documentation
✅ Created DNS records reference guide

---

## What Eugene Needs to Do

Follow these steps **in order** to complete the email system deployment.

---

### Phase 1: Mailgun Domain Setup (15-30 minutes)

**Goal:** Add psyling.com domain to Mailgun and get DNS records

#### Step 1.1: Access Mailgun Account
```
[ ] Login to Mailgun: https://app.mailgun.com
[ ] Navigate to: Sending → Domains
[ ] Check if psyling.com domain already exists
```

**If domain exists:**
- Proceed to DNS Records tab
- Skip to Phase 2

**If domain does NOT exist:**
- Click "Add New Domain"
- Enter: psyling.com
- Select region: US (or appropriate region)
- Click "Add Domain"

#### Step 1.2: Get DNS Records
```
[ ] Click on psyling.com domain
[ ] Navigate to "DNS Records" tab
[ ] You will see records that need to be added:
    - SPF (TXT record for @)
    - DKIM (TXT record for smtp._domainkey)
    - Optionally: Tracking CNAME
    - Optionally: MX record (skip this for now)
[ ] Keep this tab open - you'll need these values for Cloudflare
```

---

### Phase 2: Cloudflare DNS Configuration (10-20 minutes)

**Goal:** Add required DNS records to Cloudflare

**Reference file:** `/var/www/webgarden/sites/psyling/MAILGUN_DNS_RECORDS.txt`

#### Step 2.1: Access Cloudflare
```
[ ] Login to Cloudflare: https://dash.cloudflare.com
[ ] Select domain: psyling.com
[ ] Navigate to: DNS → Records
[ ] Click "Add record"
```

#### Step 2.2: Add SPF Record
```
[ ] Type: TXT
[ ] Name: @ (or psyling.com)
[ ] Content: v=spf1 include:mailgun.org ~all
[ ] TTL: Auto
[ ] Proxy status: DNS only (grey cloud ☁️) - CRITICAL!
[ ] Click "Save"
```

#### Step 2.3: Add DKIM Record
```
[ ] Type: TXT
[ ] Name: smtp._domainkey
[ ] Content: <copy ENTIRE value from Mailgun dashboard>
    (starts with "k=rsa; p=..." - very long string)
[ ] TTL: Auto
[ ] Proxy status: DNS only (grey cloud ☁️) - CRITICAL!
[ ] Click "Save"
```

#### Step 2.4: Optional - Add Tracking CNAME (recommended to skip for privacy)
```
[ ] Type: CNAME
[ ] Name: email
[ ] Target: mailgun.org
[ ] TTL: Auto
[ ] Proxy status: DNS only (grey cloud ☁️)
[ ] Click "Save"
```

#### Step 2.5: Verify DNS Settings
```
[ ] All email DNS records show "DNS only" (grey cloud)
[ ] No email records are proxied (orange cloud)
[ ] Records match exactly what Mailgun dashboard shows
```

**CRITICAL:** Email records MUST be "DNS only" (grey cloud). Proxied records will break email authentication!

---

### Phase 3: Wait for DNS Propagation (10-60 minutes)

**Goal:** Allow DNS changes to propagate globally

```
[ ] Wait at least 10 minutes
[ ] Optional: Check propagation status
    dig TXT psyling.com +short | grep spf
    dig TXT smtp._domainkey.psyling.com +short
[ ] Continue to next phase after 10+ minutes
```

**Note:** DNS can take up to 24 hours to fully propagate, but 10-60 minutes is usually sufficient.

---

### Phase 4: Verify Domain in Mailgun (5 minutes)

**Goal:** Confirm Mailgun recognizes DNS records

```
[ ] Return to Mailgun dashboard
[ ] Go to: Domains → psyling.com → DNS Records tab
[ ] Click "Verify DNS Settings" button
[ ] Wait 30 seconds for verification
[ ] Check status of each record:
    ✓ Green checkmark = Verified (good!)
    ⚠️ Yellow warning = Not found yet (wait longer)
    ❌ Red X = Missing or incorrect (check Cloudflare)
[ ] Domain status should show "Active" (green indicator)
```

**If records not verified:**
- Wait another 10-20 minutes
- Click "Verify DNS Settings" again
- If still failing after 1 hour, check DNS records in Cloudflare match exactly

---

### Phase 5: Get SMTP Credentials (2 minutes)

**Goal:** Get SMTP password to configure Flask app

```
[ ] In Mailgun dashboard: Domains → psyling.com
[ ] Navigate to "SMTP Credentials" section (or tab)
[ ] Find username: Should be postmaster@psyling.com
[ ] Find password:
    - If shown, copy it
    - If not shown, click "Reset Password"
    - Copy the NEW password (you won't see it again!)
[ ] Save password temporarily in a secure note
```

**IMPORTANT:**
- This is the SMTP password (NOT the API key)
- You'll need this for the next step
- Store it securely - can't be viewed again (but can be reset)

---

### Phase 6: Update Server Configuration (5 minutes)

**Goal:** Update environment file with real SMTP password

#### Step 6.1: Install New Environment File
```bash
# Navigate to therapist directory
cd /var/www/webgarden/sites/psyling

# Backup current environment file
sudo cp /etc/webgarden/psyling.env /etc/webgarden/psyling.env.backup

# Copy new template
sudo cp psyling.env.NEW /etc/webgarden/psyling.env
```

#### Step 6.2: Update SMTP Password
```bash
# Edit environment file
sudo nano /etc/webgarden/psyling.env

# Find this line:
MAIL_PASSWORD=PLACEHOLDER_UPDATE_WITH_MAILGUN_SMTP_PASSWORD

# Replace PLACEHOLDER_UPDATE_WITH_MAILGUN_SMTP_PASSWORD with actual SMTP password from Mailgun

# Save file: Ctrl+O, Enter, Ctrl+X
```

#### Step 6.3: Set Proper Permissions
```bash
# Set ownership and permissions
sudo chown root:root /etc/webgarden/psyling.env
sudo chmod 600 /etc/webgarden/psyling.env

# Verify permissions
ls -la /etc/webgarden/psyling.env
# Should show: -rw------- 1 root root
```

#### Step 6.4: Checklist
```
[ ] Environment file updated with real SMTP password
[ ] File owned by root:root
[ ] File permissions set to 600
[ ] No placeholder text remaining in MAIL_PASSWORD
```

---

### Phase 7: Test SMTP Connection (5 minutes)

**Goal:** Verify email configuration works before going live

```bash
# Navigate to therapist directory
cd /var/www/webgarden/sites/psyling

# Activate virtual environment
source venv/bin/activate

# Run test script
python3 test_email_smtp.py
```

**Expected output:**
```
======================================================================
✅ SUCCESS: Test email sent successfully!
======================================================================

Check inbox: psyling@gmail.com
```

#### Step 7.1: Check Email Received
```
[ ] Check psyling@gmail.com inbox
[ ] Look for email with subject: "✅ Psyling Email System Test - SUCCESS"
[ ] Check inbox AND spam folder
[ ] Verify sender shows as: noreply@psyling.com
[ ] Email should arrive within 1-2 minutes
```

#### Step 7.2: If Test Fails
```
[ ] Review error message from test script
[ ] Common issues:
    - Wrong SMTP password → Reset in Mailgun, update env file
    - Domain not verified → Check Mailgun dashboard status
    - DNS not propagated → Wait longer (up to 24 hours)
    - Firewall blocking port 587 → Check server firewall settings
[ ] Check Mailgun logs: https://app.mailgun.com/logs
[ ] Re-run test after fixing issues
```

**Do NOT proceed to Phase 8 until test email succeeds!**

---

### Phase 8: Restart Production Service (2 minutes)

**Goal:** Load new configuration into production Flask app

```bash
# Restart psyling service
sudo systemctl restart psyling

# Check status
sudo systemctl status psyling

# Verify service is running
# Look for: "Active: active (running)"
```

#### Checklist
```
[ ] Service restarted successfully
[ ] Status shows "active (running)"
[ ] No errors in status output
```

---

### Phase 9: Test Production Contact Form (10 minutes)

**Goal:** Verify end-to-end email flow works in production

#### Step 9.1: Monitor Logs
```bash
# Open terminal window and run:
sudo journalctl -u psyling.service -f

# Leave this running to see real-time logs
```

#### Step 9.2: Submit Test Contact Form
```
[ ] Open browser: https://psyling.com/contact
[ ] Fill out contact form with:
    Name: Test User
    Email: <your_real_email_address>
    Phone: 555-1234
    Message: "This is a test submission to verify email system works correctly."
[ ] Submit form
[ ] Verify success message displayed
```

#### Step 9.3: Check Logs for Email Sends
In the log terminal, look for:
```
✅ Admin notification sent for submission from <your_email>
✅ Auto-reply confirmation sent to <your_email>
```

**If you see errors instead:**
- Copy the error message
- Check troubleshooting section in EMAIL_SETUP.md
- Check Mailgun logs: https://app.mailgun.com/logs

#### Step 9.4: Verify Emails Received
```
[ ] Check psyling@gmail.com inbox
[ ] Look for email: "New Contact Form Submission from Test User"
[ ] Verify email contains:
    - Client name, email, phone
    - Message content
    - Reply-To header (check email source)
[ ] Check YOUR email inbox (address you used in form)
[ ] Look for email: "Thank you for contacting Psyling"
[ ] Verify auto-reply contains:
    - Professional greeting
    - Emergency contact resources
    - Valery's contact information
```

#### Step 9.5: Test Reply Functionality
```
[ ] In psyling@gmail.com inbox, open admin notification email
[ ] Click "Reply" button
[ ] Verify To: field shows YOUR test email (not noreply@psyling.com)
[ ] This confirms Reply-To header is working correctly
[ ] Cancel or send test reply
```

---

### Phase 10: Production Validation (5 minutes)

**Goal:** Final checks before marking system as complete

#### Checklist
```
[ ] SMTP test script passes
[ ] Test contact form submission succeeded
[ ] Admin notification received at psyling@gmail.com
[ ] Auto-reply received at test email address
[ ] Reply-To functionality works (clicking Reply goes to visitor's email)
[ ] No errors in service logs
[ ] Mailgun dashboard shows delivered emails (check Logs section)
[ ] Both emails NOT in spam folder
```

---

## Troubleshooting Common Issues

### Issue: Test Script Shows "535 Authentication Failed"
**Cause:** Wrong SMTP password

**Fix:**
1. Go to Mailgun dashboard → Domains → psyling.com → SMTP Credentials
2. Click "Reset Password"
3. Copy new password
4. Update `/etc/webgarden/psyling.env`
5. Restart service: `sudo systemctl restart psyling`
6. Re-run test

---

### Issue: Domain Status Shows "Unverified" in Mailgun
**Cause:** DNS records not added or not propagated

**Fix:**
1. Check DNS records exist in Cloudflare
2. Verify records are "DNS only" (grey cloud)
3. Click "Verify DNS Settings" in Mailgun dashboard
4. Wait 30-60 minutes for DNS propagation
5. Try verification again

---

### Issue: Email Goes to Spam
**Cause:** DNS records not fully verified or domain reputation

**Fix:**
1. Verify SPF and DKIM records in Mailgun show green checkmarks
2. Add noreply@psyling.com to Gmail contacts
3. Mark test email as "Not Spam"
4. Check Mailgun logs for spam score
5. Wait 24-48 hours for domain reputation to improve

---

### Issue: Reply Button Goes to noreply@psyling.com Instead of Visitor
**Cause:** Reply-To header not working

**Fix:**
1. Check email source (Gmail: three dots → Show original)
2. Look for "Reply-To:" header with visitor's email
3. If missing, verify code in `/var/www/webgarden/webgarden/shared/email.py:52`
4. Should have: `reply_to=contact_submission.email` in Message constructor
5. Restart service after any code changes

---

### Issue: No Logs Showing Email Sends
**Cause:** Service not running or using old configuration

**Fix:**
```bash
# Check service status
sudo systemctl status psyling

# Restart service
sudo systemctl restart psyling

# Monitor logs
sudo journalctl -u psyling.service -f

# Submit test form again
```

---

## File Locations Reference

**Configuration:**
- Environment file: `/etc/webgarden/psyling.env`
- Environment template: `/var/www/webgarden/sites/psyling/psyling.env.NEW`
- Service config: `/etc/systemd/system/psyling.service`

**Application:**
- Main app: `/var/www/webgarden/sites/psyling/app.py`
- Email functions: `/var/www/webgarden/webgarden/shared/email.py`
- Base app: `/var/www/webgarden/webgarden/shared/base_app.py`

**Testing & Documentation:**
- Test script: `/var/www/webgarden/sites/psyling/test_email_smtp.py`
- Full documentation: `/var/www/webgarden/webgarden/docs/EMAIL_SETUP.md`
- DNS records guide: `/var/www/webgarden/sites/psyling/MAILGUN_DNS_RECORDS.txt`
- This checklist: `/var/www/webgarden/sites/psyling/POST_IMPLEMENTATION_CHECKLIST.md`

---

## Quick Command Reference

```bash
# Navigate to therapist directory
cd /var/www/webgarden/sites/psyling

# Activate virtual environment
source venv/bin/activate

# Run SMTP test
python3 test_email_smtp.py

# Restart service
sudo systemctl restart psyling

# Check service status
sudo systemctl status psyling

# Monitor logs (real-time)
sudo journalctl -u psyling.service -f

# View recent logs
sudo journalctl -u psyling.service -n 100

# Search for errors
sudo journalctl -u psyling.service | grep -i error

# Count email sends today
sudo journalctl -u psyling.service --since today | grep -c "notification sent"

# Check DNS propagation
dig TXT psyling.com +short
dig TXT smtp._domainkey.psyling.com +short

# Edit environment file
sudo nano /etc/webgarden/psyling.env
```

---

## Success Criteria

Email system is **COMPLETE** when:

- ✅ Mailgun domain shows "Active" status
- ✅ All DNS records verified (green checkmarks)
- ✅ SMTP test script passes
- ✅ Contact form sends admin notification to psyling@gmail.com
- ✅ Contact form sends auto-reply to visitor
- ✅ Reply-To header works (Valery can click Reply)
- ✅ Emails arrive in inbox (NOT spam)
- ✅ No errors in application logs
- ✅ Mailgun dashboard shows delivered emails

---

## Post-Deployment Monitoring

**Week 1:**
- Check logs daily for email errors
- Monitor Mailgun dashboard for bounces/failures
- Verify emails not going to spam

**Week 2-4:**
- Check logs weekly
- Review Mailgun usage stats
- Confirm no client complaints about not receiving responses

**Monthly:**
- Review Mailgun usage (should be well under 5,000 emails/month)
- Check for any bounced emails or complaints
- Update emergency resources if needed (in shared/email.py)

---

## Support Resources

**Mailgun:**
- Dashboard: https://app.mailgun.com
- Logs: https://app.mailgun.com/logs
- Documentation: https://documentation.mailgun.com

**Internal Documentation:**
- Full guide: `/var/www/webgarden/webgarden/docs/EMAIL_SETUP.md`
- DNS guide: `/var/www/webgarden/sites/psyling/MAILGUN_DNS_RECORDS.txt`

**Testing:**
- Test script: `/var/www/webgarden/sites/psyling/test_email_smtp.py`
- Contact form: https://psyling.com/contact

---

## Completion Sign-Off

When all phases are complete, document here:

```
Completed by: ___________________
Date: ___________________
Test email received: [ ] Yes [ ] No
Contact form tested: [ ] Yes [ ] No
Reply functionality verified: [ ] Yes [ ] No
Issues encountered: ___________________
```

---

**Questions?**

1. Check full documentation: `/var/www/webgarden/webgarden/docs/EMAIL_SETUP.md`
2. Run test script: `python3 test_email_smtp.py`
3. Check Mailgun logs: https://app.mailgun.com/logs
4. Check service logs: `sudo journalctl -u psyling.service -f`

---

**Good luck! 🚀**

The code implementation is complete. Just follow these steps to get the email system live!
