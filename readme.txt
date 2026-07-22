# 🛡️ KRISHU X - ADMIN TOOLBOX BOT
================================================================
Complete Server Management & Moderation Bot
Made with ❤️ by Krishu X Cheats
Copyright © 2026 Krishu X Cheats. All Rights Reserved.
================================================================


📖 ABOUT THE BOT
================================================================

KRISHU X - Admin Toolbox is a professional Discord moderation bot 
that provides complete server management capabilities. It includes 
all essential moderation commands, warning system, channel management, 
purge/clear filters, giveaway system, poll system, announcement system, 
and server information tools.

This bot is designed to be the all-in-one solution for server 
administrators and moderators.


✨ KEY FEATURES
================================================================

✅ Timeout Members (1-1440 minutes)
✅ Ban Members (with message deletion)
✅ Kick Members
✅ Warn Members (with tracking system)
✅ View Warnings
✅ Clear Warnings
✅ Lock/Unlock Channels
✅ Slowmode Control (0-21600 seconds)
✅ Clear Messages (1-1000 messages)
✅ Purge with Filters (User, Contains, Bots, Images)
✅ Nuke Channel (Reset channel)
✅ Announce/Embed System
✅ Poll System (with reactions)
✅ Giveaway System (with auto-end & winner selection)
✅ Server Information
✅ User Information
✅ Role Information
✅ Audit Logging
✅ Slash & Prefix Commands
✅ Professional Embeds
✅ DM Warnings to Users
✅ Role-Based Permissions


📋 COMPLETE COMMANDS GUIDE
================================================================

MODERATION COMMANDS (Admin/Mod)
----------------------------------------------------------------

/timeout <member> <minutes> <reason>
-------------------------------------
Timeouts a member for specified duration.
- Minutes: 1 to 1440 (24 hours)
- Reason: Optional reason for timeout
Example: /timeout @user 10 Spamming in chat

/ban <member> <reason> <delete_days>
-------------------------------------
Bans a member from the server.
- Delete Days: 0 to 7 (messages to delete)
- Reason: Optional reason for ban
Example: /ban @user Breaking rules 1

/kick <member> <reason>
------------------------
Kicks a member from the server.
- Reason: Optional reason for kick
Example: /kick @user Inappropriate behavior

/warn <member> <reason>
------------------------
Gives a warning to a member.
- Tracks total warnings
- Sends DM to user
- Reason: Optional reason for warning
Example: /warn @user Warning for toxic behavior

/warns <member>
----------------
Shows all warnings of a member.
- Displays recent warnings (last 5)
- Shows total warning count
Example: /warns @user

/clearwarns <member>
---------------------
Clears all warnings of a member.
- Admin only command
Example: /clearwarns @user


🧹 CLEAR / PURGE COMMANDS (Admin/Mod)
----------------------------------------------------------------

/clear <amount> <channel>
--------------------------
Clears messages from a channel.
- Amount: 1 to 1000 messages
- If no channel specified, clears current channel
Example: /clear 50 #general

/purge <amount> <user> <contains> <bots> <images>
--------------------------------------------------
Purges messages with filters.
- amount: Number of messages to check
- user: Only delete from this user
- contains: Only delete messages with this text
- bots: Delete only bot messages
- images: Delete only messages with images
Example: /purge 100 user:@spammer contains:badword

!purgebots <amount>
--------------------
Deletes messages from bots.
- amount: Number of messages to check
Example: !purgebots 50

!purgeuser <user> <amount>
---------------------------
Deletes messages from a specific user.
Example: !purgeuser @spammer 100

!purgecontains <text> <amount>
-------------------------------
Deletes messages containing specific text.
Example: !purgecontains spam 50


🔧 CHANNEL MANAGEMENT (Admin/Mod)
----------------------------------------------------------------

/lock <channel> <reason>
-------------------------
Locks a channel so members can't send messages.
- If no channel specified, locks current channel
Example: /lock #general Channel maintenance

/unlock <channel> <reason>
---------------------------
Unlocks a previously locked channel.
- If no channel specified, unlocks current channel
Example: /unlock #general Back to normal

/slowmode <seconds> <channel>
------------------------------
Sets slowmode delay for a channel.
- Seconds: 0 to 21600 (6 hours)
- 0 = Disable slowmode
Example: /slowmode 5 #general

/nuke <channel> <reason>
-------------------------
Resets a channel (clones and deletes it).
- Preserves all settings (name, category, permissions)
Example: /nuke #general Channel reset


📢 UTILITY COMMANDS (Admin/Mod)
----------------------------------------------------------------

/announce <channel> <title> <description> <color> <footer> <thumbnail> <image>
--------------------------------------------------------------------------------
Sends an announcement with embed.
- channel: Where to send
- title: Announcement title
- description: Announcement description
- color: Color (red, green, blue, yellow, etc.)
- footer: Footer text (optional)
- thumbnail: Thumbnail URL (optional)
- image: Image URL (optional)
Example: /announce #announcements "Server Update" "New features added!" green

/poll <channel> <question> <options>
-------------------------------------
Creates a poll with reactions.
- options: Separated by | (e.g., Yes | No | Maybe)
- Max 10 options
Example: /poll #general "Best game?" "Free Fire | PUBG | COD"

/giveaway_start <channel> <prize> <duration> <winners> <requirement>
-----------------------------------------------------------------------
Starts a giveaway.
- channel: Where to host
- prize: Prize to give away
- duration: Duration in minutes (1-1440)
- winners: Number of winners (1-10)
- requirement: Role requirement (optional)
Example: /giveaway_start #giveaways "Free Fire Account" 60 2 @Member

/giveaway_end <message_id>
---------------------------
Ends a giveaway early.
- message_id: ID of the giveaway message
Example: /giveaway_end 123456789012345678


📊 INFO COMMANDS (Everyone)
----------------------------------------------------------------

/serverinfo
------------
Shows detailed server information.
- Owner, Created Date, Member Count
- Channel Count, Role Count, Boost Count
Example: /serverinfo

/userinfo <member>
-------------------
Shows detailed user information.
- ID, Nickname, Join Dates
- Top Role, Status, Bot Status
Example: /userinfo @user

/roleinfo <role>
-----------------
Shows detailed role information.
- ID, Color, Member Count
- Position, Mentionable, Hoist
Example: /roleinfo @Admin

/ping
------
Check bot latency.
Example: /ping

/helpadmin
-----------
Shows all available commands.
Example: /helpadmin


🔧 SETUP GUIDE
================================================================

STEP 1: Prerequisites
----------------------------------------------------------------

- Python 3.8 or higher
- Discord Bot Token
- Server with Administrator permissions

STEP 2: Download Files
----------------------------------------------------------------

Create a folder and save:
📁 AdminToolboxBot/
├── main.py              # Main bot file
├── .env                 # Configuration file
├── requirements.txt     # Dependencies
├── run.bat              # Windows startup script
├── README.txt           # This documentation
├── warn_data.json       # Warning data (Auto-created)
└── giveaway_data.json   # Giveaway data (Auto-created)

STEP 3: Install Dependencies
----------------------------------------------------------------

Open CMD in the folder and run:

pip install -r requirements.txt

STEP 4: Configure .env File
----------------------------------------------------------------

Create .env file with these settings:

# Discord Bot Token (Required)
TOKEN=your_bot_token_here

# Admin Role ID (Required - Full permissions)
ADMIN_ROLE_ID=your_admin_role_id_here

# Mod Role ID (Optional - Can use moderation commands)
MOD_ROLE_ID=your_mod_role_id_here

# Muted Role ID (Optional - Auto-created if 0)
MUTED_ROLE_ID=0

# Log Channel ID (Optional - For audit logs)
LOG_CHANNEL_ID=your_log_channel_id_here

# Flask Port (Optional)
PORT=10000

STEP 5: Get Your IDs
----------------------------------------------------------------

How to get Role ID:
1. Enable Developer Mode in Discord Settings
2. Go to Server Settings > Roles
3. Right-click on the role
4. Click "Copy ID"

How to get Channel ID:
1. Enable Developer Mode
2. Right-click on the channel
3. Click "Copy ID"

STEP 6: Run the Bot
----------------------------------------------------------------

Double-click RUN.bat OR run:

python main.py


🛡️ PERMISSIONS SYSTEM
================================================================

ADMIN ROLE
----------------------------------------------------------------
✅ Full access to all commands
✅ Can ban, kick, timeout
✅ Can lock/unlock/nuke channels
✅ Can clear warnings
✅ Can set slowmode
✅ Can clear/purge messages
✅ Can create announcements
✅ Can create polls
✅ Can start/end giveaways

MOD ROLE
----------------------------------------------------------------
✅ Can timeout members
✅ Can kick members
✅ Can warn members
✅ Can view warnings
✅ Can lock/unlock channels
✅ Can set slowmode
✅ Can clear/purge messages
✅ Can create announcements
✅ Can create polls
✅ Can start/end giveaways
❌ Cannot ban members
❌ Cannot clear warnings
❌ Cannot nuke channels

EVERYONE
----------------------------------------------------------------
✅ Can view server info
✅ Can view user info
✅ Can view role info
✅ Can check ping
✅ Can view help
❌ Cannot use moderation commands


⚙️ PERMISSIONS REQUIRED FOR BOT
================================================================

Permission                    | Purpose
------------------------------|------------------------------------
Send Messages                 | Send responses
Manage Messages               | Clear/Purge messages
Ban Members                   | Ban members
Kick Members                  | Kick members
Timeout Members               | Timeout members
Manage Channels               | Lock/Unlock/Nuke channels
Manage Roles                  | Create Muted role
View Channels                 | See channels
Read Message History          | Read messages
Embed Links                   | Send embeds
Use Slash Commands            | Slash commands
Add Reactions                 | Poll reactions

Recommended Permission Integer: 403008608


📁 FILE STRUCTURE
================================================================

AdminToolboxBot/
│
├── 📄 main.py              # Main bot file
├── 📄 .env                 # Configuration file
├── 📄 requirements.txt     # Python dependencies
├── 📄 run.bat              # Windows startup script
├── 📄 README.txt           # This documentation
├── 📄 warn_data.json       # Warning data (Auto-created)
└── 📄 giveaway_data.json   # Giveaway data (Auto-created)


🛠️ TROUBLESHOOTING
================================================================

PROBLEM: Bot not responding
SOLUTION:
- Check TOKEN in .env file
- Make sure token is valid
- Check internet connection

PROBLEM: Commands not working
SOLUTION:
- Check ADMIN_ROLE_ID and MOD_ROLE_ID in .env
- Make sure bot has required permissions
- Check if user has correct role

PROBLEM: Timeout not working
SOLUTION:
- Bot needs "Timeout Members" permission
- Check if user has higher role than target

PROBLEM: Lock/Unlock/Nuke not working
SOLUTION:
- Bot needs "Manage Channels" permission
- Check if channel exists

PROBLEM: Purge/Clear not working
SOLUTION:
- Bot needs "Manage Messages" permission
- Amount must be between 1-1000

PROBLEM: Giveaway not working
SOLUTION:
- Bot needs "Add Reactions" permission
- Bot needs "Send Messages" permission
- Check if duration is valid

PROBLEM: Logging not working
SOLUTION:
- Check LOG_CHANNEL_ID in .env
- Bot needs "Send Messages" permission in log channel
- Bot needs "Embed Links" permission


📊 LOGGING SYSTEM
================================================================

The bot logs all moderation actions to the specified log channel:

Logged Actions:
----------------------------------------------------------------
✅ Timeout - Member, Duration, Reason, Moderator
✅ Ban - Member, Reason, Moderator, Delete Days
✅ Kick - Member, Reason, Moderator
✅ Warn - Member, Reason, Moderator, Warning Number
✅ Lock - Channel, Reason, Moderator
✅ Unlock - Channel, Reason, Moderator
✅ Clear - Channel, Amount, Moderator
✅ Purge - Channel, Amount, Filters, Moderator
✅ Nuke - Channel, Reason, Moderator


🔐 SECURITY NOTES
================================================================

⚠️ IMPORTANT SECURITY GUIDELINES:

1. NEVER share your .env file or bot token
2. Keep ADMIN_ROLE_ID and MOD_ROLE_ID secure
3. Regularly check audit logs
4. Monitor warning system
5. Keep the bot updated


📞 SUPPORT & SOCIAL MEDIA
================================================================

Platform            | Link
--------------------|------------------------------------------------
Discord Server      | https://discord.com/invite/xmfKB7nJ8T
YouTube Channel     | https://www.youtube.com/@Krishu_X_Cheats
Instagram           | https://www.instagram.com/coder_krishu/

For support, join our Discord Server or DM on Instagram.


📄 LICENSE
================================================================

© 2026 Krishu X Cheats. All Rights Reserved.

This bot is proprietary software owned by Krishu X Cheats.
Unauthorized copying, distribution, or modification is prohibited.

For licensing inquiries, contact: support@krishuxcheats.com


🎉 CONCLUSION
================================================================

Thank you for using KRISHU X - Admin Toolbox Bot!

Features Summary:
- 🛡️ Complete Moderation System
- ⏰ Timeout, Ban, Kick, Warn
- 🔒 Lock/Unlock/Nuke Channels
- ⏱️ Slowmode Control
- 🧹 Clear/Purge with Filters
- 📢 Announce, Poll, Giveaway
- 📊 Server Information
- 📝 Audit Logging
- 🎭 Role-Based Permissions
- 💼 Professional Design

Made with ❤️ by Krishu X Cheats


================================================================
© 2026 Krishu X Cheats. All Rights Reserved.
Made with ❤️ by Krishu X Cheats
================================================================