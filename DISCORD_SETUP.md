# AFOQT Study Community — Discord Setup Guide
**Estimated time: 20 minutes**

---

## Step 1: Create the Server (2 min)

1. Open Discord → click the **+** button in the left sidebar
2. Select **"Create My Own"** → **"For a club or community"**
3. Name the server: `AFOQT Study Community`
4. Upload a server icon (optional — use the FissionLab atom logo or leave blank for now)
5. Click **Create**

---

## Step 2: Create Categories and Channels (8 min)

Delete the default channels first (`#general`, `#general-1`).

Then create the following structure **in order**:

### 📋 INFORMATION (Category)
Right-click the server name → **Create Category** → name it `📋 INFORMATION`

Under this category, create text channels:
- `welcome`
- `announcements`
- `resources`

### 📚 STUDY ROOMS (Category)
Create category: `📚 STUDY ROOMS`

Channels:
- `general-afoqt`
- `math-knowledge`
- `verbal`
- `aviation-instruments`
- `physical-science`
- `reading-comprehension`
- `study-schedules`

### 📝 PRACTICE (Category)
Create category: `📝 PRACTICE`

Channels:
- `daily-question`
- `score-reports`
- `study-partners`

### 🎓 DR. PRESTON (Category)
Create category: `🎓 DR. PRESTON`

Channels:
- `office-hours`
- `book-a-session`

---

## Step 3: Configure #announcements (1 min)

1. Click the ⚙️ settings icon next to `#announcements`
2. Go to **Permissions** → **@everyone**
3. Toggle **Send Messages** to ❌ (OFF)
4. This makes it so only you (Preston) can post announcements

---

## Step 4: Pin Content in #welcome (3 min)

Post this message in `#welcome`, then right-click → **Pin Message**:

```
👋 Welcome to the AFOQT Study Community — free prep, led by Dr. Preston (PhD Nuclear Engineering, USAF Captain).

📋 RULES
1. Be respectful — everyone here is working toward the same goal
2. Keep questions in the relevant channel (math in #math-knowledge, etc.)
3. No spam, no self-promotion without asking first
4. Share your study schedules and scores — accountability is the point

🚀 GETTING STARTED
→ Introduce yourself in #general-afoqt (name, test date, target score)
→ Check #resources for the full study guide at fissionlab.net/community/
→ Post your first practice score in #score-reports

📅 OFFICE HOURS
Dr. Preston hosts live Q&A every week. Check #office-hours for the schedule.

📞 1:1 TUTORING
Book a personal session: https://calendly.com/preston-j-dicks/introductory-meeting
```

---

## Step 5: Pin Calendly in #book-a-session (1 min)

Post in `#book-a-session`:
```
📅 Book a 1:1 tutoring session with Dr. Preston:
https://calendly.com/preston-j-dicks/introductory-meeting

Free introductory call available. Sessions are personalized to your weak areas and target score.
```
Pin the message.

---

## Step 6: Pin Resource Links in #resources (1 min)

Post in `#resources`:
```
📚 Free AFOQT resources at fissionlab.net:

🔗 Full resource library (all 12 subtests): https://fissionlab.net/community/resources/
✏️ 60 free practice questions: https://fissionlab.net/community/practice/
📋 Community landing page: https://fissionlab.net/community/
```
Pin the message.

---

## Step 7: Set Up MEE6 Bot (Free Tier) (3 min)

1. Go to **mee6.xyz** → click **Add to Discord** → select your server
2. In the MEE6 dashboard, go to **Welcome**:
   - Enable the Welcome plugin
   - Set welcome channel: `#general-afoqt`
   - Set welcome message:
     ```
     Welcome {user} to the AFOQT Study Community! 👋
     You've just joined a free community built for Air Force officer candidates.
     → Start in #welcome for the rules
     → Post your test date in #general-afoqt
     → Check fissionlab.net/community/ for all resources
     Good luck — we're rooting for you. 🎯
     ```
3. Go to **Roles** in MEE6:
   - Create a role called `AFOQT Student` in Discord Server Settings → Roles first
   - In MEE6 Roles, set auto-assign on join: `AFOQT Student`

### Optional: Daily Question Automation
- In MEE6, go to **Commands** → enable a scheduled post to `#daily-question`
- Or post manually — either works fine while the community is small

---

## Step 8: Create a Permanent Invite Link (1 min)

1. Click the server name at the top → **Invite People**
2. Click **Edit invite link** (or the settings icon)
3. Set **Expire after** → **Never**
4. Set **Max uses** → **No limit**
5. Click **Generate a New Link**
6. Copy the link (format: `discord.gg/XXXXXXX`)

**Save this link** — you'll need it for the next step.

---

## Step 9: Add the Invite Link to fissionlab.net (2 min)

Once you have your permanent invite link, open a terminal and run:

```
claude "Replace all instances of [DISCORD_INVITE_LINK] in the community pages with https://discord.gg/YOURLINK"
```

Or manually find/replace `[DISCORD_INVITE_LINK]` in these files:
- `community/index.html`
- `community/resources/index.html`
- `community/forum/index.html`
- `community/practice/index.html`
- `community/about/index.html`

Then push to GitHub:
```
git add community/
git commit -m "Add Discord invite link to all community pages"
git push
```

---

## Moderation Rules Template (copy-paste ready)

```
📋 SERVER RULES — AFOQT Study Community

1. RESPECT — Treat everyone the way you'd want to be treated as a fellow officer candidate. No harassment, no belittling, no politics.

2. STAY ON TOPIC — Use the correct channel. Aviation questions in #aviation-instruments, math in #math-knowledge. Keeps things searchable for everyone.

3. NO SPAM — Don't flood channels. Don't DM members unsolicited.

4. NO SOLICITATION — Don't advertise tutoring services, courses, or products without explicit permission from Dr. Preston.

5. SHARE OPENLY — Post your scores, your study schedules, your questions. The value of this community comes from everyone contributing.

6. HONEST EFFORT — Don't share actual AFOQT questions from a test you took. It's against regulations and could get you disqualified.

Violations: first offense = warning, second = mute, third = ban. Dr. Preston has final say.
```

---

## Summary Checklist

- [ ] Server created: "AFOQT Study Community"
- [ ] All 4 categories created
- [ ] All 13 channels created
- [ ] #announcements locked to members (only Preston can post)
- [ ] #welcome message pinned with rules
- [ ] #book-a-session Calendly link pinned
- [ ] #resources links pinned
- [ ] MEE6 welcome message configured
- [ ] MEE6 auto-role "AFOQT Student" on join
- [ ] Permanent invite link generated
- [ ] Invite link inserted into fissionlab.net community pages
- [ ] Pages pushed to GitHub
