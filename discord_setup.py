#!/usr/bin/env python3
"""
FissionLab Discord Server Setup
Configures the FissionLab server: categories, channels, roles, permissions, pinned messages.

Usage:
    pip install discord.py python-dotenv
    Add DISCORD_BOT_TOKEN=your_token to .env
    Add DISCORD_GUILD_ID=your_server_id to .env (optional — auto-detects if bot is in one server)
    python discord_setup.py
"""

import asyncio
import os
import sys
from pathlib import Path

import discord
from discord import PermissionOverwrite
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
CALENDLY = "https://calendly.com/preston-j-dicks/introductory-meeting"
SITE = "https://fissionlab.net"
DISCORD_INVITE = "https://discord.gg/rkzrxET7"

CATEGORIES = [
    {
        "name": "📋 INFORMATION",
        "channels": ["welcome", "announcements", "resources", "ask-dr-preston"],
        "dr_only_send": ["announcements"],
        "readonly": ["announcements"],
    },
    {
        "name": "📚 AFOQT STUDY ROOMS",
        "channels": [
            "general-afoqt", "math-knowledge", "verbal",
            "aviation-instruments", "physical-science",
            "reading-comp", "study-schedules",
        ],
    },
    {
        "name": "📝 PRACTICE & SCORES",
        "channels": ["daily-question", "score-reports", "study-partners", "test-dates"],
    },
    {
        "name": "🎓 DR. PRESTON",
        "channels": ["office-hours", "book-a-session", "success-stories"],
        "readonly": ["office-hours", "book-a-session"],
    },
    {
        "name": "🔧 COMMUNITY",
        "channels": ["introductions", "off-topic"],
    },
]

ROLES_CONFIG = [
    {"name": "Dr. Preston",       "color": 0xC9A84C, "admin": True,  "hoist": True},
    {"name": "Tutor",             "color": 0x3498DB, "admin": False, "hoist": True},
    {"name": "Study Group Leader","color": 0x9B59B6, "admin": False, "hoist": False},
    {"name": "Test Passed ✓",     "color": 0x2ECC71, "admin": False, "hoist": False},
    {"name": "AFOQT Student",     "color": 0x95A5A6, "admin": False, "hoist": False},
]

PINNED_MESSAGES = {
    "welcome": f"""\
Welcome to FissionLab — the AFOQT Study Community run by Dr. Preston, \
PhD Nuclear Engineering and USAF Captain.

This server is completely free. Here's how to get started:

1. Introduce yourself in #introductions
2. Tell us your target test date in #study-schedules
3. Explore the study channels for your weak subtests
4. Check #daily-question every day for practice
5. Book a 1:1 tutoring session: {CALENDLY}

Free resources at {SITE}/community/

📋 RULES
• Be respectful — everyone here is working toward the same goal
• Keep questions in the right channel (math in #math-knowledge, etc.)
• No spam, no unsolicited DMs
• Share your scores and schedules — accountability is the point
• Do not post actual AFOQT questions from a test you took""",

    "resources": f"""\
Free AFOQT resources from Dr. Preston:

📚 Full subtest breakdown: {SITE}/community/resources/
✏️ 60 free practice questions: {SITE}/community/practice/
📖 Book recommendations: {SITE}/community/resources/
📧 Weekly newsletter: https://www.beehiiv.com/?via=preston-dicks
📅 Book a session: {CALENDLY}""",

    "book-a-session": f"""\
Ready to work with Dr. Preston 1:1?

🎓 PhD Nuclear Engineering · USAF Captain · Expert AFOQT tutor

Book your session: {CALENDLY}

Packages available at {SITE}:
• Single session $70/hr
• 5-session pack (save $25)
• 10-session pack (save $100)""",
}


class SetupBot(discord.Client):
    def __init__(self, guild_id):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self.target_guild_id = guild_id

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        guild = self._find_guild()
        if guild is None:
            print("ERROR: Could not find target guild. Make sure the bot is invited to the server.")
            await self.close()
            return
        try:
            await self._setup_guild(guild)
        except Exception as e:
            print(f"ERROR during setup: {e}")
            raise
        finally:
            await self.close()

    def _find_guild(self):
        if self.target_guild_id:
            return discord.utils.get(self.guilds, id=self.target_guild_id)
        if len(self.guilds) == 1:
            return self.guilds[0]
        if len(self.guilds) == 0:
            return None
        print(f"Bot is in {len(self.guilds)} servers. Set DISCORD_GUILD_ID in .env.")
        for g in self.guilds:
            print(f"  {g.id}: {g.name}")
        return None

    async def _setup_guild(self, guild):
        print(f"\nConfiguring: {guild.name} ({guild.id})")

        # --- Roles (create bottom-to-top so hoisting works correctly) ---
        print("\n[1/4] Creating roles...")
        role_map = {r.name: r for r in guild.roles}
        dr_role = None
        student_role = None

        for cfg in reversed(ROLES_CONFIG):
            existing = role_map.get(cfg["name"])
            if existing:
                print(f"  role exists: {cfg['name']}")
                role = existing
            else:
                perms = discord.Permissions.all() if cfg.get("admin") else discord.Permissions.none()
                role = await guild.create_role(
                    name=cfg["name"],
                    color=discord.Color(cfg["color"]),
                    permissions=perms,
                    hoist=cfg["hoist"],
                    reason="FissionLab setup",
                )
                print(f"  created role: {cfg['name']}")
            if cfg["name"] == "Dr. Preston":
                dr_role = role
            if cfg["name"] == "AFOQT Student":
                student_role = role

        # --- Categories & Channels ---
        print("\n[2/4] Creating categories and channels...")
        everyone = guild.default_role
        channel_map = {c.name: c for c in guild.channels}
        cat_map = {c.name: c for c in guild.categories}

        for cat_cfg in CATEGORIES:
            cat_name = cat_cfg["name"]
            readonly_names = set(cat_cfg.get("readonly", []))
            dr_only_names = set(cat_cfg.get("dr_only_send", []))

            cat = cat_map.get(cat_name)
            if cat is None:
                cat = await guild.create_category(cat_name, reason="FissionLab setup")
                print(f"  category: {cat_name}")
            else:
                print(f"  category exists: {cat_name}")

            for ch_name in cat_cfg["channels"]:
                if ch_name in channel_map:
                    print(f"    channel exists: #{ch_name}")
                    continue

                overwrites = {}
                if ch_name in readonly_names:
                    overwrites[everyone] = PermissionOverwrite(send_messages=False, read_messages=True)
                    if dr_role:
                        overwrites[dr_role] = PermissionOverwrite(send_messages=True, read_messages=True)
                elif ch_name in dr_only_names:
                    overwrites[everyone] = PermissionOverwrite(send_messages=False, read_messages=True)
                    if dr_role:
                        overwrites[dr_role] = PermissionOverwrite(send_messages=True, read_messages=True)

                ch = await guild.create_text_channel(
                    ch_name,
                    category=cat,
                    overwrites=overwrites,
                    reason="FissionLab setup",
                )
                print(f"    created: #{ch_name}")
                channel_map[ch_name] = ch

        # --- Pinned Messages ---
        print("\n[3/4] Posting and pinning messages...")
        for ch_name, msg_text in PINNED_MESSAGES.items():
            ch = channel_map.get(ch_name)
            if ch is None:
                print(f"  WARNING: #{ch_name} not found, skipping pin")
                continue
            # Check if already pinned (avoid duplicates on re-runs)
            pins = await ch.pins()
            already_pinned = any(p.author == self.user for p in pins)
            if already_pinned:
                print(f"  already pinned in #{ch_name}")
                continue
            msg = await ch.send(msg_text)
            await msg.pin()
            print(f"  pinned in #{ch_name}")

        # --- Summary ---
        print("\n[4/4] Setup complete.")
        print(f"\n  Guild:   {guild.name}")
        print(f"  Invite:  {DISCORD_INVITE}")
        print(f"  Calendly: {CALENDLY}")
        if student_role:
            print(f"\n  NOTE: Configure MEE6 (mee6.xyz) to auto-assign @{student_role.name} on join.")
        print("\nRUN COMPLETE")
        print(f"Live site: {SITE}/community/")


def main():
    if not TOKEN:
        print("No DISCORD_BOT_TOKEN found in .env")
        print("See DISCORD_SETUP_INSTRUCTIONS.md for setup steps.")
        sys.exit(1)

    guild_id = int(GUILD_ID) if GUILD_ID else None
    client = SetupBot(guild_id)

    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        print("ERROR: Invalid bot token. Check DISCORD_BOT_TOKEN in .env")
        sys.exit(1)


if __name__ == "__main__":
    main()
