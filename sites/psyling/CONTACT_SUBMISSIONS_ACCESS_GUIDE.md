# Psyling contact inbox guide

> Contact inquiries are private client data. Use the authenticated Psyling
> admin interface and do not copy inquiry content into logs, tickets, or chat.
> Operational work must follow the current [Psyling README](README.md) and
> [Webgarden operations guide](../../docs/operations.md).

## Open the inbox

1. Sign in at `https://psyling.com/admin/login`.
2. Choose **Contacts** in the navigation bar, or open
   `https://psyling.com/admin/contacts`.
3. Use the inbox views:
   - **Active** contains non-spam inquiries that have not been archived.
   - **Unread** is the subset of Active that has not been opened. Its count is
     based only on the `is_read` flag.
   - **Spam** contains active spam-classified inquiries.
   - **Archived** contains safely stored inquiries removed from the active list.

The navigation badge and dashboard **Unread inquiries** card use the same
`is_read`-based count. They do not infer unread state from reply status.

## Read state and reply status

Opening an inquiry automatically clears its **Unread** marker. This does not
mean the client has received a reply.

The separate reply/workflow labels are:

- **Needs reply**: stored as the compatible `new` status; the inquiry has not
  yet been recorded as contacted.
- **Contacted**: a successful reply was sent from Psyling, or an administrator
  recorded contact made outside Psyling.
- **Booked**: the inquiry progressed to a booking.
- **Closed**: no further active reply workflow is expected.
- **Spam**: the inquiry is classified as spam.

Use **Mark unread** on the detail page when an opened inquiry needs to return to
the Unread view. That action returns to the Unread list so the detail page does
not immediately mark it read again.

## Reply and record contact

The detail page can send an email to the address stored on the inquiry. A reply
is shown as sent and the inquiry becomes **Contacted** only after SMTP accepts
the message. Failed attempts remain in the history and do not falsely mark the
inquiry contacted.

If contact happened by telephone, a separate mail application, or another
channel, use **Mark as contacted (without email)**. Replies written outside
Psyling are not imported automatically.

## Remove an inquiry from the active list safely

Use **Archive from active list** on the inquiry detail page. Archiving:

- removes the inquiry from Active, Unread, and the dashboard's recent active
  inquiries;
- keeps the original message, notes, activities, and email history stored; and
- makes the inquiry available in **Archived**, where **Restore to active list**
  returns it to Active.

Archive is the safe inbox-removal action. Permanent deletion is not the normal
contact-inbox workflow.

## Technical route summary

- `GET /admin/contacts` — active/unread/spam/archive lists and search
- `GET /admin/contacts/<id>/view` — HTML detail page; marks the inquiry read
- `POST /admin/contacts/<id>/toggle-read` — manual read/unread control
- `POST /admin/contacts/<id>/crm` — workflow, notes, and follow-up changes
- `POST /admin/contacts/<id>/reply` — send and record a reply
- `POST /admin/contacts/<id>/mark-contacted` — record contact without email
- `POST /admin/contacts/<id>/archive` — archive or restore without deletion
- `POST /admin/contacts/<id>/toggle-spam` — spam classification

All detail and mutation routes require administrator authentication; POST
actions are CSRF-protected and remain functional without JavaScript.
