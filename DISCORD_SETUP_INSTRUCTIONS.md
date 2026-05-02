# FissionLab Bot Setup — Step-by-Step

Run `discord_setup.py` once to auto-configure the FissionLab Discord server.

---

## 1. Create the Bot

1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it `FissionLab Bot` → Create
3. Go to the **Bot** tab → click **Add Bot** → confirm
4. Under **Token**, click **Reset Token** → copy and save it (shown once)
5. Enable these Privileged Gateway Intents:
   - **Server Members Intent** ✓
   - **Message Content Intent** ✓
   - **Presence Intent** ✓

---

## 2. Generate the Invite URL

Still on the Bot page, go to **OAuth2 → URL Generator**:

**Scopes:** `bot`

**Bot Permissions:**
- Manage Channels
- Manage Roles
- Send Messages
- Embed Links
- Read Message History
- Add Reactions
- Mention Everyone
- Pin Messages

Copy the generated URL and open it in your browser → select **FissionLab** server → Authorize.

---

## 3. Get Your Server ID

In Discord, go to **User Settings → Advanced → enable Developer Mode**.

Right-click the **FissionLab** server icon → **Copy Server ID**.

---

## 4. Create .env

In `C:\Users\prest\projects\Tutoring\`, create a file named `.env`:

```
DISCORD_BOT_TOKEN=your_token_here
DISCORD_GUILD_ID=your_server_id_here
```

The `.gitignore` already excludes `.env` files.

---

## 5. Install Dependencies and Run

```bash
pip install discord.py python-dotenv
python discord_setup.py
```

The script will:
- Create all categories and channels (skips any that already exist)
- Create all 5 roles with correct colors and permissions
- Lock #announcements, #office-hours, #book-a-session to read-only (Dr. Preston can post)
- Post and pin welcome/resources/booking messages

Re-running is safe — it skips anything that already exists.

---

## 6. Finish in Discord

After the script runs:

1. **MEE6 auto-role** — go to mee6.xyz → your server → Roles → set auto-assign `@AFOQT Student` on join
2. **Assign yourself `@Dr. Preston`** in Server Settings → Members
3. **Verify #announcements** is locked (only you can post)
