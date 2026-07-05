# Contact Submissions Access Guide

## Summary

✅ **Good News!** All 113 contact form submissions are safely stored in the database and **fully accessible** through your admin panel.

The admin contact management system is already implemented and working. You just need to know where to navigate!

---

## Quick Access Steps

### 1. Login to Admin Panel
- Go to: **https://psyling.com/admin/login**
- Use your admin credentials (username and password)

### 2. Navigate to Contacts
Once logged in, you have **three ways** to access contact submissions:

#### Option A: Click "Contacts" in Navigation Bar
- Look at the top navigation bar
- Click on **"Contacts"** (has an envelope icon 📧)
- You'll see a red badge showing the number of unread messages (currently 113)

#### Option B: From Dashboard
- After login, you'll be on the Dashboard
- In the stats cards at the top, click **"View All"** under "Total Contacts"
- Or click **"All Contacts"** in the Quick Actions section
- Or scroll down to see "Recent Contacts" and click **"View All Contacts"**

#### Option C: Direct URL
- Go directly to: **https://psyling.com/admin/contacts**

---

## What You'll See

### Main Contacts Page (`/admin/contacts`)

The contacts list page shows all 113 submissions with:

**Filter Tabs at Top:**
- **All (113)** - Shows all contact submissions
- **New (113)** - Unread messages (all current messages are "new")
- **Read (0)** - Messages you've opened
- **Responded (0)** - Messages you've marked as responded

**Table Columns:**
- Name (with "New" badge for unread)
- Contact Info (email and phone)
- Message preview (truncated)
- Date & time submitted
- Status badge
- Actions (View button)

**Pagination:**
- Shows 20 messages per page
- Use navigation at bottom to view pages 2-6

---

## Viewing Individual Messages

### To View a Message:
1. Click the blue **"View"** button next to any contact
2. A modal popup will open showing:
   - Full name, email, phone
   - Complete message text
   - Submission date and time
   - Status dropdown (New/Read/Responded)
   - Internal notes field

### When You View a Message:
- Status automatically changes from "New" to "Read"
- The badge count updates
- Message is highlighted differently in the list

---

## Managing Contacts

### Update Status
In the message detail modal:
- Use the **Status** dropdown to change:
  - **New** - Unread message
  - **Read** - You've seen it but haven't replied
  - **Responded** - You've replied to this person

### Add Internal Notes
- In the message detail modal, scroll down to **"Internal Notes"**
- Type your notes (e.g., "Called back on 2026-03-01", "Scheduled for Tuesday")
- Click **"Save Notes"** button
- Notes are private and only visible to admins

### Reply to Contact
- Click the email link to open your email client
- Or use the phone number link to call directly

---

## Current Contact Stats

```
Total Submissions: 113
New (Unread):      113
Read:              0
Responded:         0
```

All 113 messages are currently marked as "new" because they haven't been opened yet.

---

## Features Available

✅ View all contact submissions (paginated)
✅ Filter by status (New/Read/Responded)
✅ View full message details in modal popup
✅ Auto-mark as "read" when viewing
✅ Update status manually
✅ Add internal notes to each submission
✅ Click email to reply directly
✅ Click phone to call directly
✅ See submission date/time
✅ Badge notification for unread count

---

## Common Questions

### Q: Why can't I see my contact submissions?
**A:** You need to be logged into the admin panel. Go to `/admin/login` first.

### Q: Are all 113 messages really there?
**A:** Yes! Confirmed in database. Run this to verify anytime:
```bash
cd /var/www/webgarden/sites/psyling
venv/bin/python check_contacts.py
```

### Q: How do I filter for only new messages?
**A:** Click the **"New"** tab at the top of the contacts list (shows badge with 113).

### Q: Can I delete spam messages?
**A:** The delete functionality is not currently implemented in the UI, but we can add it if needed. For now, you can mark spam as "Read" and add a note "SPAM" to filter them mentally.

### Q: How do I know if I have new messages?
**A:** The navigation bar shows a red badge on "Contacts" with the count of unread messages.

---

## Screenshots Guide

### Navigation:
```
[Dashboard] [Blog Posts] [Contacts (113)] [Edit Pages] [username ▼]
                            ↑
                    Click here to see all contacts
```

### Dashboard Stats:
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Total Posts     │  │ Total Contacts  │  │ Unread Contacts │
│      5          │  │     113         │  │     113         │
│ [View All →]    │  │ [View All →]    │  │ [View Unread →] │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Contacts List:
```
[All (113)] [New (113)] [Read (0)] [Responded (0)]
                ↑
        Click tabs to filter

┌─────────────────────────────────────────────────────────────┐
│ Name          │ Contact         │ Message      │ Date │ ... │
├─────────────────────────────────────────────────────────────┤
│ Clark B. (New)│ seoclark2024@...│ I can help...│ 2/28 │[View]│
│ RobertHap (New)│ zekisuquc419@..│ Hello...     │ 2/28 │[View]│
└─────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### "I'm logged in but don't see the Contacts link"
- Refresh the page
- Clear your browser cache
- Make sure you're logged in as an admin user

### "The page loads but shows 'No contact submissions'"
- Check which filter tab is active (try clicking "All")
- The service might need restart:
  ```bash
  sudo systemctl restart psyling
  ```

### "I get an error when clicking View"
- Check browser console for errors (F12)
- The admin contact view route might have an issue
- Try refreshing and clicking again

---

## Technical Details

**Routes:**
- `/admin/contacts` - List all contacts with filters
- `/admin/contacts/<id>` - View individual contact (JSON API)
- `/admin/contacts/<id>/status` - Update status (POST)
- `/admin/contacts/<id>/notes` - Update notes (POST)

**Templates:**
- `templates/admin/contacts_list.html` - Main contacts page
- Modal popup for viewing individual messages

**Database:**
- All 113 submissions stored in `contact_submissions` table
- Fields: id, name, email, phone, message, submitted_at, status, notes

**Service Status:**
```bash
sudo systemctl status psyling
```
Currently: ✅ Active (running)

---

## Next Steps

1. **Login** to https://psyling.com/admin/login
2. **Click "Contacts"** in the navigation bar
3. **View the 113 messages** waiting for you!
4. **Update statuses** as you respond to people
5. **Add notes** to track your conversations

---

## Need Help?

If you encounter any issues accessing the contacts:

1. Verify service is running: `sudo systemctl status psyling`
2. Check database: `venv/bin/python check_contacts.py`
3. Review logs: `sudo journalctl -u psyling -n 50`

All the functionality is working and ready to use! 🎉

---

**Last Verified:** 2026-03-01
**Contact Count:** 113 submissions
**Service Status:** ✅ Running
**Admin Panel URL:** https://psyling.com/admin
