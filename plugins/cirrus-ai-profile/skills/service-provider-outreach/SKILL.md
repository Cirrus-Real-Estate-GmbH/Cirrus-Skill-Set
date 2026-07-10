---
name: service-provider-outreach
description: Research verified local, regional, or international service providers and manage personalized multi-employee outreach through Google Drive, Google Sheets, Gmail, Google Calendar, Google Contacts, Chrome, Google Maps, Kleinanzeigen, Yellow Pages-style directories, MyHammer, Blauarbeit, and relevant web sources. Use when Codex should ask which employee is using the skill, load or create employee-specific sender profiles, ask whether skill changes apply globally or only to one employee, create a dedicated campaign chat/thread, create a dedicated MSP campaign folder, create a Google Sheets tracker, run a guided campaign setup wizard with button-style choices, score lead quality, check duplicates and suppression lists, classify replies, create Gmail reply drafts, manage approval modes, A/B-test subjects and bodies, update KPI dashboards, send daily tracking summaries, and produce campaign closure reports.
---

# Service Provider Outreach

## Overview

Use this skill to run a complete, evidence-first provider acquisition workflow: clarify the research target, gather verified provider data, create a Google Drive project with a Google Sheets tracker, draft individualized outreach emails, send only after approval, and maintain follow-up and reply tracking.

Always keep factual accuracy, consent, and traceability ahead of speed. Do not invent contact details, specialties, team size, service areas, references, or personalizations.

## Multi-User Handling

This skill may be used by several employees at the same time. At the start of every workflow, ask who is currently using the skill unless the active user is already unambiguous from the request or thread context.

Store and load employee-specific data only from `references/people/<employee-slug>.md`. These profile files hold sender identity, email address, company role, signature, booking links, individual attachment paths, tone preferences, campaign-specific defaults, and other personal outreach details. Do not keep person-specific details in this global `SKILL.md`.

If the named employee already has a profile, read that profile before asking for sender identity or drafting outreach. If no profile exists for the named employee, ask for the missing profile data and create `references/people/<employee-slug>.md` before drafting or sending:

- Full name and preferred visible sender name.
- Company, role, email address, phone number, and signature.
- Booking or calendar links.
- Personal tone preferences and default language.
- Reusable company links, attachment paths, disclaimers, and campaign defaults.
- Preferred salutation, close, personal intro, no-go phrases, industry focus, default summary email address, and default approval mode.

When a user asks to change this skill or any reusable skill behavior, first ask whether the change should apply to all employees or only to the current employee. Apply all-employee changes in this `SKILL.md` or shared reference files. Apply employee-only changes in that employee's profile file. If the scope is unclear, do not modify shared instructions until the user chooses the scope.

Use per-project Google Drive folders, trackers, dashboards, labels, and automation prompts so simultaneous users do not overwrite one another's outreach state. Include the active employee name in internal notes, dashboards, summaries, and automation prompts whenever it helps prevent ambiguity.

## Start Workflow

Begin every new campaign with a guided setup wizard. Ask concise questions in German unless the user chooses another language. Prefer button-style choices whenever the UI supports buttons, and store the answers in the `Campaign Settings` tracker tab:

- Active employee using the skill, then load or create the corresponding profile in `references/people/`.
- Campaign workspace: for each new campaign, create or route work into its own dedicated campaign chat/thread and its own dedicated MSP campaign folder before storing research results or Google Sheets.
- Research segment: trade, service, industry, provider type, or niche.
- Region: city, radius, state, country, or named market.
- Target quantity and quality bar: number of providers, must-have criteria, exclusions.
- Outreach goal: what the user wants from the provider.
- Sender identity: only ask for fields missing from the active employee profile.
- Attachment: ask whether a PDF should be sent, and where it is stored in Drive/local disk or whether the user wants to upload it in the chat.
- Schedule and automation settings: ask with button-style choices whenever the UI supports buttons. Capture monitoring frequency, whether automations should be created, first follow-up timing in business days, whether Gmail reply drafts should be created automatically, and whether the active employee should receive a daily email summary.
- Approval mode, duplicate policy, A/B-test mode, and whether a campaign closure report should be created at the end.

Use these default button-style choices for campaign settings, adapting labels only when the user already gave a clear preference:

- Monitoring frequency: `3x daily (recommended)`, `Daily`, `Weekdays only`, `Custom`.
- First follow-up timing: `3 business days (recommended)`, `5 business days`, `7 business days`, `Custom`.
- Create automations: `Yes, create automations (recommended)`, `No, manual only`.
- Gmail reply drafts: `Yes, draft replies automatically (recommended)`, `No, only report replies`.
- Daily email summary: `Yes, email daily summary (recommended)`, `No summary email`, `Custom summary time`.
- Approval mode: `Draft only (recommended)`, `Approve each email`, `Approve batch after sample`, `Follow-ups draft automatically`.
- A/B testing: `No A/B test`, `Subject A/B test`, `Subject + body A/B test`.
- Duplicate handling: `Block duplicates (recommended)`, `Warn only`, `Allow with approval`.
- Closure report: `Create report at campaign end (recommended)`, `No closure report`.

If the user gives enough detail in the first request, proceed without re-asking answered questions.

## Tool Routing

Use the available connected tools in this order:

- Use Chrome or the in-app browser for web research that depends on visible search results, Google Maps, directory pages, marketplaces, or websites.
- Use the Kleinanzeigen connector when searching German classified listings.
- Use Google Drive to create the project folder and manage attachments or source files.
- Use Google Sheets through Google Drive to create and update the tracking table.
- When new provider data is found, always create a Google Sheets tracker if one does not already exist for the workflow, then transfer the new data into it before finishing the turn. If a tracker already exists, update that tracker instead of leaving the new data only in chat, CSV, notes, or a local file.
- Use Google Contacts to check whether providers already exist as contacts and to enrich only with factual saved data.
- Use Gmail to create drafts, send approved emails, label campaign mail, search replies, and snooze threads.
- Use Google Calendar for scheduled review blocks or reminders when useful.
- Use the Codex automation tool `automation_update`, if available, to create daily reply checks and summary runs after user approval. If automation tools are not available, create explicit calendar reminders and record the limitation in the tracker.

When using connector skills, read and follow their SKILL.md instructions first.

## Campaign Chat, MSP Folder, And Tracker

For every new campaign, create a separate Codex chat/thread and a separate Google Drive MSP campaign folder before substantive research, sheet creation, dashboards, Gmail drafts, or automations. Do not run multiple unrelated campaigns in the same chat or folder.

Name the dedicated campaign chat/thread with this pattern:

`MSP - YYYY-MM-DD - <segment> - <region> - <employee>`

When a thread creation tool is available and the user is starting a new campaign, create the thread explicitly and keep its link or thread id in the campaign tracker, dashboard, and daily summaries. If a thread creation tool is not available, tell the user to open a new chat for the campaign and record the limitation in the tracker once it exists.

Create a new Google Drive folder named with this pattern:

`MSP - YYYY-MM-DD Outreach - <segment> - <region> - <employee>`

Inside it, create a Google Sheets tracker named:

`Tracking - <segment> - <region>`

Use `references/tracking-schema.md` for the sheet tabs and columns. Include source URLs and verification status for each factual field.

Store all campaign artifacts inside the dedicated MSP folder: research notes, source exports, temporary local-to-Drive uploads, Google Sheets trackers, dashboards, approved attachments, sent-mail logs, and daily summaries. Do this as soon as any new provider records have been collected. The tracker is the source of truth for researched providers, so every newly found provider must be written to the Google Sheet in the MSP folder with its source URLs, verification status, and missing fields noted. Local CSV or spreadsheet files may be used as temporary build artifacts, but they are not a substitute for the Google Sheets tracker in the MSP folder.

Before creating drafts or sending any campaign mail, check the tracker, Gmail label, existing Gmail threads, and `Suppression List` tab for duplicate companies, duplicate domains, previous outreach, bounces, opt-outs, negative replies, and do-not-contact entries. Block duplicates by default unless the user approved another duplicate policy in campaign settings.

Always apply colored status coding in Google Sheets trackers. At minimum, format the `status` column with conditional colors:

- `new`: light gray
- `researched` or `verified`: light blue
- `drafted`: light yellow
- `sent`: light green
- `reply_received`: medium green
- `follow_up_due`: orange
- `not_interested`, `do_not_contact`, or `bounced`: light red

When updating statuses later, preserve or repair this conditional formatting so the tracker remains scannable.

For each active workflow in the project, also create an HTML dashboard in the project folder. Read `references/dashboard.md` and start from `assets/dashboard-template.html`. Name dashboards with this pattern:

`Dashboard - <workflow-name>.html`

The dashboard must be an operational status surface, not a marketing page. It should summarize live progress, bottlenecks, data quality, outreach activity, replies, due follow-ups, source coverage, and next actions.

## Research Rules

Read `references/research-and-verification.md` before collecting provider data.

Research broadly, then verify narrowly. Useful sources include Google Maps, provider websites, legal imprint pages, trade directories, Gelbe Seiten-style directories, MyHammer, Blauarbeit, Kleinanzeigen, chamber or association directories, review platforms, and local business listings. Add other relevant sources when they materially improve coverage or verification.

Only record facts that are directly visible in a source or confirmed by two consistent sources. For email addresses, phone numbers, postal addresses, websites, named contacts, service areas, and specialties, record the source URL and the date checked. Mark uncertain fields as blank or `needs verification`; never guess.

Score every researched provider before drafting. Use `references/research-and-verification.md` for lead scoring, source quality, and disqualification rules. Do not draft first-contact emails for providers marked duplicate, suppressed, do-not-contact, bounced, source quality blocked, or below the campaign's minimum score unless the user explicitly approves an exception.

## Email Drafting And Sending

Read `references/email-and-followup.md` before drafting or sending.

Ask the user what the email should say before drafting the first contact. Convert the user's intent into a short, natural, individual message for each recipient. Use provider-specific facts from verified sources, such as a service focus, project type, geography, family business note, reference project, certification, or stated availability.

Write outreach emails in a particularly warm, sympathetic, and personal tone. The message should feel like a thoughtful individual note from the sender, not a generic campaign.

For every outreach email subject line, include `Suche` and include the recipient company name in parentheses at the end of the subject. Example: `Suche Apartmenthaus-Projekt an der Nordsee (Muster Immobilien GmbH)`.

Respect the campaign approval mode from `Campaign Settings`. Default to draft-only. For batch sending, show the campaign label, counts, attachment names, duplicate/suppression results, A/B variants, and representative examples before asking for explicit approval.

If A/B testing is enabled, create the approved subject or body variants, assign each eligible provider a stable `variant_id`, track the variant in `Outreach Log`, and compare reply rates only after enough messages were actually sent. Do not change mid-campaign variants without recording the change in `Experiments`.

Apply active employee profile instructions from `references/people/<employee-slug>.md`, including sender introduction, signature, booking links, attachment rules, company framing, and campaign-specific tone rules. If the profile conflicts with the user's current request, ask whether to update the employee profile or use a one-time exception for this workflow.

Use formatting in the email body when creating Gmail drafts:

- clear paragraphs
- bold for the core search line or the concrete question
- bullet points for search criteria; do not write acquisition criteria or other enumerations as a run-on sentence in body text
- optional blue emphasis for one short heading or core phrase when using HTML drafts
- enough spacing and formatting so the email is easy to scan on mobile and desktop
- optionally one or two fitting emojis in the body when it makes the note warmer, but never more than 2 emojis per email and never in the signature

Every first-contact email must ask the concrete question: `Können Sie mir hier konkret weiterhelfen?`

Use the active employee profile for fallback acquisition profile links, visible sender name, and signature handling.

Avoid generic LLM phrasing, mass-tender language, exaggerated praise, and unsupported claims. Proofread every draft for spelling, typos, grammar, and tone.

Before sending, present a compact review sample and get explicit user approval for the campaign or batch. Do not send Gmail messages without explicit approval. If an attachment is requested, verify the exact PDF file and include it only after approval.

For providers in other countries, write the email in the local language and include an English version below it unless the user requests a different approach.

## Gmail Labels, Snoozes, And Follow-ups

Create or reuse a Gmail label that identifies the action:

`Outreach/<YYYY-MM-DD> <segment> <region>`

Apply the label to all campaign emails and replies. After sending, snooze each sent thread until the user-approved first follow-up date. Treat business days as Monday-Friday and skip weekends.

Default follow-up cadence:

- First contact: day 0.
- Follow-up 1: after the user-approved number of business days without reply; ask for this with button-style choices before the campaign starts.
- Follow-up 2: 7 days after follow-up 1 without reply.
- Follow-up 3: 7 days after follow-up 2 without reply.

Each follow-up must be brief, friendly, and individually grounded in the original context. Stop follow-ups immediately when a contact replies, opts out, declines, or is marked `do not contact`.

## Automation And Daily Summary

When the project starts, ask with button-style choices whether recurring automations should be created in the user's timezone. Do not assume automation is allowed without user confirmation.

- Dashboard and reply monitoring frequency: use the user-approved frequency, defaulting to 3 times per day only when selected.
- Daily summary: send once per day at the user-approved time when the user selected daily email summaries.

For every active outreach campaign, set up ongoing Gmail monitoring only when the user approves monitoring automations. The monitoring workflow must:

  - Search the campaign Gmail label and the inbox for matching reply subjects and sender addresses.
- Treat auto-replies, delivery confirmations, internal reactions, and unrelated inbox messages separately from real provider replies.
- Read each relevant thread before drafting any response.
- Classify each reply before changing status: `positive`, `question`, `neutral`, `not_interested`, `do_not_contact`, `bounce`, `auto_reply`, `internal`, or `unrelated`.
- Update the Google Sheets tracker with reply status, reply date, reply summary, and next action.
- When the user approved Gmail reply draft automation, draft suitable Gmail replies in the original thread for questions, positive leads, objections, declines, and requests for a call. Keep them as Gmail drafts unless the user gives explicit send approval.
- For requests to schedule a call or meeting, include the active employee's stored booking link from `references/people/<employee-slug>.md` when one exists and ask the recipient to choose a suitable appointment there directly.
- Never send replies or follow-ups without explicit user approval.
  - Stop follow-ups for contacts that replied, declined, opted out, bounced, or are marked `do_not_contact`.
- Preserve or repair colored status coding in the tracker after status updates.
  - Include complete tracking counts in the tracker and daily summary: total outbound emails sent, first contacts sent, follow-ups sent, replies received, positive replies, negative replies, Gmail reply drafts created, draft replies sent after approval, user-sent/manual replies, due follow-ups, stopped follow-ups, and items needing user action.

If Codex or the user's computer was not live at the scheduled check time, run the missed mailbox check at the next available live session and treat it as due work, not as skipped work.

The dashboard refresh automation should:

- Read the Google Sheets tracker.
- Search Gmail for labeled campaign threads and replies.
- Update tracker statuses when new replies or due follow-ups are found.
- Regenerate each workflow dashboard HTML file from current tracker data.
- Keep links to the Google Sheet, project folder, campaign label, and active Codex/GPT project/thread when available.
- Recalculate complete campaign tracking counts and write them to the tracker before refreshing the dashboard.
- Recalculate conversion funnel and A/B-test performance by source, region, lead score band, and variant when the data exists.

The daily summary automation should:

- Search Gmail for labeled campaign threads and replies.
- Update the tracker status, latest reply date, and next action.
- Identify due follow-ups and draft or send them according to the user's approved mode.
- If the user selected daily email summaries, send the active employee a daily summary email with the complete tracking readout and links to the Google Drive MSP folder, Google Sheet, dashboard, Gmail label, and campaign chat/thread.

Daily summary content:

- Active employee and campaign name.
- Link to the Google Drive MSP folder.
- Link to the Google Sheet.
- Link or clear reference to the active Codex/GPT project/thread when available.
- Number of total outbound emails sent.
- Number of first-contact emails sent.
- Number of follow-ups sent.
- Number of replies received.
- Number of positive replies, negative replies, and neutral/question replies.
- Number of Gmail reply drafts created automatically.
- Number of draft replies sent after approval.
- Number of replies sent manually/by the active employee.
- Number of due follow-ups, stopped follow-ups, and contacts needing user action.
- Reply quality/status and short notes on important replies.
- Responsible next steps.
- Statement of which AI system prepared or sent the summary.

## Campaign Closure Report

When the user ends a campaign or the campaign reaches its planned volume, offer to create a closure report in the MSP folder as a Google Doc or PDF. Include:

- Campaign goal, employee, date range, segment, region, and links to the MSP folder, tracker, dashboard, Gmail label, and campaign chat/thread.
- Funnel: researched, verified, eligible, drafted, approved, sent, replied, positive, meeting/call interest, declined, bounced, do-not-contact.
- Response rates by source, region, lead score band, and A/B variant when available.
- Best-performing subject/body variants and examples of strong personalization angles.
- Data quality findings, source reliability, duplicate/suppression issues, and blocked records.
- Lessons learned and concrete recommendation for the next campaign.

If an automation cannot be created with the available tools, create a Calendar reminder and document the fallback in the tracker.

Do not write raw automation schedules by hand for the user. Use the available automation tool schema and include the workspace/project folder, a clear daily schedule, and a self-contained prompt that tells the automation to use the campaign label and tracker links.
