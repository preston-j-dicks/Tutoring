# MEE6 + Carl-bot Setup — FissionLab Discord

## 1. Add MEE6

Go to **mee6.xyz** → Add to Discord → select **FissionLab** server.

---

## 2. Leveling Plugin (XP + Rank Roles)

Dashboard → **Leveling** → Enable

**Role rewards** — set these exact level thresholds:

| Level | Role to assign |
|-------|----------------|
| 0     | @Recruit        |
| 5     | @Private        |
| 10    | @Corporal       |
| 20    | @Sergeant       |
| 35    | @Lieutenant     |
| 50    | @Captain        |
| 75    | @Colonel        |
| 100   | @General        |

Settings to configure:
- **XP rate**: Normal
- **XP per message**: 15–25 (randomized)
- **No XP channels**: #leaderboard, #daily-question (bot channel)
- **Level-up message**: Enable, set channel to `#wins-and-milestones`
- **Level-up message text**:
  ```
  Congratulations {mention}! You reached Level {level} and earned the rank of **{role}**. Keep studying — General awaits. 🎯
  ```

---

## 3. Welcome Plugin

Dashboard → **Welcome** → Enable

**DM new members**:
```
Welcome to FissionLab — the AFOQT Study Community!

You've joined a free server built for Air Force officer candidates.

FIRST STEPS:
1. Go to #choose-your-roles and pick your subject focus
2. Introduce yourself in #introductions (test date + weak subtest)
3. Check #daily-question for today's practice question

Free resources: fissionlab.net/community/
Book a session with Dr. Preston: https://calendly.com/preston-j-dicks/introductory-meeting

Good luck — we're rooting for you.
```

**Welcome channel**: #introductions
**Welcome channel message**:
```
Welcome {mention} to FissionLab! Start in #welcome for the server guide. Drop your test date in #test-dates. 🎯
```

---

## 4. Auto Moderator

Dashboard → **Auto Moderator** → Enable

Rules to set:
- **Spam protection**: Enabled (5+ identical messages)
- **Link filter**: Block links in all channels EXCEPT: #pinned-resources, #book-recommendations, #youtube-videos, #websites-and-apps, #full-practice-tests, #share-your-notes
- **Caps filter**: Warn if >70% caps in a message
- **Bad words**: Add any relevant filter list

---

## 5. Scheduled Posts (Daily Question)

Dashboard → **Scheduled Posts** → Enable

**Post**: Daily at 08:00 ET in `#daily-question`

Template to rotate:
```
DAILY QUESTION — {date}

[Paste today's question here]

A) ...
B) ...
C) ...
D) ...

React with your answer! Answer revealed tomorrow.
More practice: fissionlab.net/community/practice/
```

---

## 6. Commands (!rank, !leaderboard)

These work automatically once Leveling is enabled:
- `!rank` or `/rank` — shows member's XP + level
- `!leaderboard` or `/leaderboard` — server rankings
- `!level` — same as rank

---

## 7. Carl-bot Reaction Roles (more reliable than MEE6 for this)

Go to **carl.gg** → Add to Discord → select FissionLab.

In `#choose-your-roles`, post this message manually (or have Carl-bot post it via Dashboard → ReactionRoles → Message):

```
React to get your subject focus role:

🔢 = @Math Focus
📖 = @Verbal Focus
✈️ = @Aviation Focus
🔬 = @Physical Science Focus
🎯 = @All Subtests

React to 🔔 for daily question notifications
React to 📅 for office hours reminders
```

Then in Carl-bot Dashboard → **Reaction Roles** → pick that message → add each emoji → role mapping.

Set mode: **Single** for subject roles (can only pick one), **Normal** for notification roles.

---

## 8. Achievement Roles (Manual)

These are awarded by Preston manually:

| Role | When to award |
|------|---------------|
| @Test Passed | Member posts they passed the AFOQT in #wins-and-milestones |
| @Study Streak 7 | 7 consecutive days of activity (MEE6 can track, award manually) |
| @Study Streak 30 | 30 consecutive days |
| @100 Questions | Member completes 100+ practice questions (self-report + honor system) |
| @Helper | Regularly answers questions in subtest channels |
| @OG Member | Award to the first 50 members |

To award: right-click member → Roles → add role.

---

## 9. Summary Checklist

- [ ] MEE6 added to server
- [ ] Leveling plugin enabled with 8 rank roles configured
- [ ] Level-up messages going to #wins-and-milestones
- [ ] Welcome DM enabled with server guide
- [ ] Auto moderator link filter configured
- [ ] Scheduled posts set for 08:00 ET daily in #daily-question
- [ ] Carl-bot added to server
- [ ] Reaction roles wired in #choose-your-roles (all 7 emoji)
- [ ] @Dr. Preston role assigned to Preston manually
- [ ] @OG Member assigned to first 50 members
