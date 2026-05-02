#!/usr/bin/env python3
"""
FissionLab Discord Server Setup — Upgraded
Builds the full study-server structure: roles, categories, text + voice channels, pinned messages.

Usage:
    pip install discord.py python-dotenv
    Set DISCORD_BOT_TOKEN and DISCORD_GUILD_ID in .env
    python discord_setup.py
"""

import asyncio
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

import discord
from discord import PermissionOverwrite
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
CALENDLY = "https://calendly.com/preston-j-dicks/introductory-meeting"
SITE = "https://fissionlab.net"
DISCORD_INVITE = "https://discord.gg/rkzrxET7"

# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------

STAFF_ROLES = [
    {"name": "Dr. Preston", "color": 0xC9A84C, "admin": True,  "hoist": True},
    {"name": "Moderator",   "color": 0x6BA3D6, "admin": False, "hoist": True},
    {"name": "Tutor",       "color": 0x4CA878, "admin": False, "hoist": True},
]

TIER_ROLES = [
    {"name": "General",    "color": 0xE74C3C, "hoist": True},
    {"name": "Colonel",    "color": 0xE67E22, "hoist": True},
    {"name": "Captain",    "color": 0xC9A84C, "hoist": True},
    {"name": "Lieutenant", "color": 0x9B59B6, "hoist": True},
    {"name": "Sergeant",   "color": 0x6BA3D6, "hoist": True},
    {"name": "Corporal",   "color": 0x4CA878, "hoist": True},
    {"name": "Private",    "color": 0xFFFFFF, "hoist": False},
    {"name": "Recruit",    "color": 0x95A5A6, "hoist": False},
]

ACHIEVEMENT_ROLES = [
    {"name": "Test Passed",      "color": 0xF1C40F},
    {"name": "Study Streak 30",  "color": 0xE67E22},
    {"name": "Study Streak 7",   "color": 0x2ECC71},
    {"name": "100 Questions",    "color": 0x3498DB},
    {"name": "Helper",           "color": 0x9B59B6},
    {"name": "OG Member",        "color": 0xC9A84C},
]

SUBJECT_ROLES = [
    {"name": "All Subtests",       "color": 0xC9A84C},
    {"name": "Physical Science Focus", "color": 0xE67E22},
    {"name": "Aviation Focus",     "color": 0x87CEEB},
    {"name": "Verbal Focus",       "color": 0xFF69B4},
    {"name": "Math Focus",         "color": 0xF1C40F},
]

ALL_ROLES = STAFF_ROLES + TIER_ROLES + ACHIEVEMENT_ROLES + SUBJECT_ROLES

# ---------------------------------------------------------------------------
# Channel structure
# ---------------------------------------------------------------------------

CATEGORIES = [
    {
        "name": "🚀 START HERE",
        "text": ["welcome", "announcements", "changelog", "choose-your-roles"],
        "dr_only_send": ["announcements", "changelog"],
        "readonly": ["announcements", "changelog"],
    },
    {
        "name": "🎯 ONBOARDING",
        "text": ["introductions", "test-dates", "goals", "study-plans"],
    },
    {
        "name": "📚 AFOQT SUBTESTS",
        "text": [
            "math-knowledge", "verbal", "reading-comp", "physical-science",
            "aviation-info", "instrument-comp", "block-counting", "situational-judgment",
        ],
    },
    {
        "name": "📝 PRACTICE",
        "text": [
            "daily-question", "practice-problems", "score-reports",
            "answer-explanations", "full-practice-tests",
        ],
    },
    {
        "name": "📖 RESOURCES",
        "text": [
            "pinned-resources", "book-recommendations", "youtube-videos",
            "study-techniques", "websites-and-apps", "share-your-notes",
        ],
        "dr_only_send": ["pinned-resources"],
        "readonly": ["pinned-resources"],
    },
    {
        "name": "⏱️ STUDY ROOMS",
        "voice": [
            "📚 Study Room 1",
            "📚 Study Room 2",
            "🔇 Silent Study",
            "⏱️ Pomodoro Room",
            "🎯 Test Prep Sprint",
            "🎙️ Office Hours",
        ],
    },
    {
        "name": "🏆 COMMUNITY",
        "text": [
            "leaderboard", "wins-and-milestones", "accountability",
            "study-buddy-finder", "motivation",
        ],
    },
    {
        "name": "💬 GENERAL",
        "text": ["general-chat", "memes-and-humor", "off-topic"],
    },
    {
        "name": "🎓 DR. PRESTON",
        "text": [
            "ask-dr-preston", "office-hours-info", "book-a-session",
            "student-success", "tutoring-resources",
        ],
        "dr_only_send": ["office-hours-info", "book-a-session"],
        "readonly": ["office-hours-info", "book-a-session", "tutoring-resources"],
    },
]

# ---------------------------------------------------------------------------
# Pinned messages
# ---------------------------------------------------------------------------

PINNED_MESSAGES = {
    "welcome": f"""\
Welcome to FissionLab — the AFOQT Study Community
Run by Dr. Preston | PhD Nuclear Engineering | USAF Captain

NEW HERE? Do these 5 things:
1. Read the rules (pinned below)
2. Go to #choose-your-roles and pick your focus subjects
3. Introduce yourself in #introductions (test date + weak subtest)
4. Pin your test date in #test-dates
5. Jump into today's question in #daily-question

HOW TO RANK UP:
Chat, help others, and show up daily — MEE6 tracks your XP automatically.
Recruit → Private → Corporal → Sergeant → Lieutenant → Captain → Colonel → General

RULES:
1. Be respectful — everyone here is working toward the same goal
2. Keep questions in the right channel (math in #math-knowledge, etc.)
3. No spam, no unsolicited DMs, no self-promotion without permission
4. Share your scores and schedules — accountability is the point
5. Do not post actual AFOQT questions from a test you took

FREE RESOURCES: {SITE}/community/
BOOK A SESSION: {SITE} (Calendly)
DISCORD: {DISCORD_INVITE}""",

    "choose-your-roles": f"""\
React to get your subject focus role:

🔢 = Math Focus
📖 = Verbal Focus
✈️ = Aviation Focus
🔬 = Physical Science Focus
🎯 = All Subtests

React to 🔔 for daily question notifications
React to 📅 for office hours reminders

(Use Carl-bot reaction roles — instructions in #changelog)""",

    "pinned-resources": f"""\
FREE AFOQT RESOURCES FROM DR. PRESTON

Full subtest breakdown + study tips:
{SITE}/community/resources/

60 free practice questions:
{SITE}/community/practice/

Recommended books (Amazon affiliate):
{SITE}/community/resources/#books

Book a 1:1 session with Dr. Preston:
{CALENDLY}

Weekly newsletter + study tips:
https://www.beehiiv.com/?via=preston-dicks

Best YouTube AFOQT resources:
- Search: "AFOQT [subtest name] tips" on YouTube
- Pilot's Path channel (aviation + instruments)
- Military Flight Aptitude Test prep playlists""",

    "book-a-session": f"""\
Work 1:1 with Dr. Preston

PhD Nuclear Engineering · USAF Captain · 6+ years active duty
Commissioned at 19 · Trained by the best military educators

PACKAGES:
Single session — $70/hr
5-session pack — save $25
10-session pack — save $100

BOOK NOW: {CALENDLY}

Results from 1:1 students in #student-success""",

    "daily-question": """\
DAILY QUESTION — Day 1

MATH KNOWLEDGE
If 3x + 7 = 22, what is the value of 2x?

A) 5
B) 10
C) 15
D) 20

React with your answer: A / B / C / D

Answer revealed tomorrow. More practice in #practice-problems.""",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _p(msg):
    """Print with flush, stripping non-ASCII for Windows terminal safety."""
    safe = msg.encode('ascii', errors='replace').decode('ascii')
    print(safe, flush=True)


# ---------------------------------------------------------------------------
# Bot
# ---------------------------------------------------------------------------

class SetupBot(discord.Client):
    def __init__(self, guild_id):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self.target_guild_id = guild_id

    async def on_ready(self):
        _p(f"Logged in as {self.user}")
        guild = self._find_guild()
        if guild is None:
            _p("ERROR: Could not find target guild. Bot must be in the server.")
            await self.close()
            return
        try:
            await self._setup(guild)
        except Exception as e:
            _p(f"ERROR during setup: {e}")
            raise
        finally:
            await self.close()

    def _find_guild(self):
        if self.target_guild_id:
            return discord.utils.get(self.guilds, id=self.target_guild_id)
        if len(self.guilds) == 1:
            return self.guilds[0]
        _p(f"Bot is in {len(self.guilds)} servers. Set DISCORD_GUILD_ID in .env.")
        for g in self.guilds:
            _p(f"  {g.id}: {g.name}")
        return None

    async def _setup(self, guild):
        _p(f"\nConfiguring: {guild.name} ({guild.id})")

        dr_role = await self._create_roles(guild)
        await self._create_channels(guild, dr_role)
        await self._post_pinned(guild)

        _p("\n[4/4] Done.")
        _p(f"  Guild:    {guild.name}")
        _p(f"  Invite:   {DISCORD_INVITE}")
        _p(f"  Calendly: {CALENDLY}")
        _p("\nNEXT STEPS:")
        _p("  1. Configure MEE6 XP level roles — see MEE6_SETUP.md")
        _p("  2. Configure Carl-bot reaction roles in #choose-your-roles — see MEE6_SETUP.md")
        _p("  3. Assign yourself @Dr. Preston in Server Settings -> Members")
        _p("\nRUN COMPLETE")
        _p(f"Live site: {SITE}/community/")

    async def _create_roles(self, guild):
        _p("\n[1/4] Creating roles...")
        existing = {r.name: r for r in guild.roles}
        dr_role = None

        for cfg in reversed(ALL_ROLES):
            name = cfg["name"]
            if name in existing:
                _p(f"  exists: {name}")
                if name == "Dr. Preston":
                    dr_role = existing[name]
                continue

            role = await guild.create_role(
                name=name,
                color=discord.Color(cfg["color"]),
                hoist=cfg.get("hoist", False),
                reason="FissionLab setup",
            )
            _p(f"  created: {name}")
            if name == "Dr. Preston":
                dr_role = role

        return dr_role

    async def _create_channels(self, guild, dr_role):
        _p("\n[2/4] Creating categories and channels...")
        everyone = guild.default_role
        existing_text = {c.name: c for c in guild.text_channels}
        existing_voice = {c.name: c for c in guild.voice_channels}
        existing_cats = {c.name: c for c in guild.categories}

        for cat_cfg in CATEGORIES:
            cat_name = cat_cfg["name"]
            readonly = set(cat_cfg.get("readonly", []))
            dr_only = set(cat_cfg.get("dr_only_send", []))

            cat = existing_cats.get(cat_name)
            if cat is None:
                cat = await guild.create_category(cat_name, reason="FissionLab setup")
                _p(f"  category: {cat_name}")
            else:
                _p(f"  category exists: {cat_name}")

            for ch_name in cat_cfg.get("text", []):
                if ch_name in existing_text:
                    _p(f"    text exists: #{ch_name}")
                    continue
                ow = {}
                if ch_name in readonly or ch_name in dr_only:
                    ow[everyone] = PermissionOverwrite(send_messages=False, read_messages=True)
                    if dr_role:
                        ow[dr_role] = PermissionOverwrite(send_messages=True, read_messages=True)
                ch = await guild.create_text_channel(ch_name, category=cat, overwrites=ow, reason="FissionLab setup")
                existing_text[ch_name] = ch
                _p(f"    created text: #{ch_name}")

            for vc_name in cat_cfg.get("voice", []):
                if vc_name in existing_voice:
                    _p(f"    voice exists: {vc_name}")
                    continue
                await guild.create_voice_channel(vc_name, category=cat, reason="FissionLab setup")
                existing_voice[vc_name] = True
                _p(f"    created voice: {vc_name}")

    async def _post_pinned(self, guild):
        _p("\n[3/4] Posting pinned messages...")
        ch_map = {c.name: c for c in guild.text_channels}
        needs_manual_pin = []

        for ch_name, msg_text in PINNED_MESSAGES.items():
            ch = ch_map.get(ch_name)
            if ch is None:
                _p(f"  WARNING: #{ch_name} not found, skipping")
                continue
            already = False
            async for pin in ch.pins():
                if pin.author == self.user:
                    already = True
                    break
            if already:
                _p(f"  already posted: #{ch_name}")
                continue
            try:
                msg = await ch.send(msg_text)
            except discord.Forbidden:
                needs_manual_pin.append(ch_name)
                _p(f"  SKIPPED (no send permission): #{ch_name} — post manually")
                continue
            try:
                await msg.pin()
                _p(f"  posted + pinned: #{ch_name}")
            except discord.Forbidden:
                needs_manual_pin.append(ch_name)
                _p(f"  posted (pin manually): #{ch_name}")

        if needs_manual_pin:
            _p("\n  ACTION NEEDED: Bot lacks Manage Messages — pin these manually:")
            for ch_name in needs_manual_pin:
                _p(f"    #{ch_name}")


def main():
    if not TOKEN:
        _p("No DISCORD_BOT_TOKEN found in .env")
        _p("See DISCORD_SETUP_INSTRUCTIONS.md for setup steps.")
        sys.exit(1)

    guild_id = int(GUILD_ID) if GUILD_ID else None
    client = SetupBot(guild_id)

    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        _p("ERROR: Invalid bot token. Check DISCORD_BOT_TOKEN in .env")
        sys.exit(1)


if __name__ == "__main__":
    main()
