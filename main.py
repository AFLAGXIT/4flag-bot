import os
import sys
import json
import random
import asyncio
import threading
import traceback
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands, tasks
from flask import Flask

# =========================================================
# CONFIGURATION & CONSTANTS
# =========================================================

TOKEN = os.getenv("DISCORD_TOKEN")

ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID", "1569705058151440414"))
MOD_ROLE_ID = int(os.getenv("MOD_ROLE_ID", "1569705058151440414"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "1569705952419127426"))
DATA_FILE = "warns.json"

# =========================================================
# FLASK WEB SERVER (For 24/7 Hosting)
# =========================================================

app = Flask(__name__)

@app.route("/")
def home():
    return "4FLAG SECURITY is running online 24/7!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump({"users": {}}, f)
        return {"users": {}}
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception:
        return {"users": {}}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# =========================================================
# BOT SETUP & INTENTS
# =========================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

bot_name = "4FLAG SECURITY"

# =========================================================
# ADMIN TOOLBOX COG
# =========================================================

class AdminToolbox(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.warn_data = load_json(DATA_FILE)

    def is_admin(self, member: discord.Member) -> bool:
        if member.guild_permissions.administrator:
            return True
        return any(role.id == ADMIN_ROLE_ID for role in member.roles)

    def is_mod(self, member: discord.Member) -> bool:
        if self.is_admin(member) or member.guild_permissions.manage_messages:
            return True
        return any(role.id == MOD_ROLE_ID for role in member.roles)

    async def log_action(self, guild: discord.Guild, action: str, moderator: discord.Member, target=None, reason: str = "No reason provided", extra: str = None):
        if not LOG_CHANNEL_ID:
            return
        channel = guild.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title=f"🛡️ Action Logged: {action}",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👮 Moderator", value=moderator.mention, inline=True)
        if target:
            embed.add_field(name="🎯 Target", value=target.mention if isinstance(target, discord.Member) else str(target), inline=True)
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        if extra:
            embed.add_field(name="ℹ️ Details", value=extra, inline=False)
        embed.set_footer(text="4FLAG SECURITY - Logging System")

        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"⚠️ Failed to send log: {e}")

    # ---------------------------------------------------------
    # WARN COMMANDS
    # ---------------------------------------------------------

    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.describe(member="The member to warn", reason="Reason for warning")
    async def warn_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await self._handle_warn(interaction, member, reason, is_slash=True)

    @commands.command(name="warn")
    @commands.has_permissions(administrator=True)
    async def warn_prefix(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        await self._handle_warn(ctx, member, reason, is_slash=False)

    async def _handle_warn(self, ctx_or_interaction, member: discord.Member, reason: str, is_slash: bool):
        author = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
        guild = ctx_or_interaction.guild
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        if not self.is_mod(author):
            await send_response("❌ You don't have permission to use this command!", ephemeral=True)
            return

        user_id = str(member.id)
        if user_id not in self.warn_data["users"]:
            self.warn_data["users"][user_id] = {"warns": [], "total": 0}

        warn_id = len(self.warn_data["users"][user_id]["warns"]) + 1
        self.warn_data["users"][user_id]["warns"].append({
            "id": warn_id,
            "reason": reason,
            "moderator": str(author),
            "date": datetime.now().isoformat()
        })
        self.warn_data["users"][user_id]["total"] = len(self.warn_data["users"][user_id]["warns"])
        save_json(DATA_FILE, self.warn_data)

        embed = discord.Embed(
            title="⚠️ Member Warned",
            color=discord.Color.yellow(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Member", value=member.mention, inline=True)
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        embed.add_field(name="👮 Moderator", value=author.mention, inline=True)
        embed.add_field(name="📊 Total Warnings", value=str(self.warn_data["users"][user_id]["total"]), inline=True)
        embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")

        await send_response(embed=embed)
        await self.log_action(guild, "Warn", author, member, reason, f"Warning #{warn_id}")

        try:
            dm_embed = discord.Embed(
                title="⚠️ You Have Been Warned",
                description=f"You have been warned in **{guild.name}**",
                color=discord.Color.yellow(),
                timestamp=datetime.now()
            )
            dm_embed.add_field(name="📝 Reason", value=reason, inline=False)
            dm_embed.add_field(name="👮 Moderator", value=author.name, inline=True)
            dm_embed.add_field(name="📊 Total Warnings", value=str(self.warn_data["users"][user_id]["total"]), inline=True)
            dm_embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")
            await member.send(embed=dm_embed)
        except Exception:
            pass

    @app_commands.command(name="warns", description="View warnings of a member")
    @app_commands.describe(member="The member to view warnings for")
    async def warns_slash(self, interaction: discord.Interaction, member: discord.Member):
        await self._handle_warns(interaction, member, is_slash=True)

    @commands.command(name="warns")
    async def warns_prefix(self, ctx: commands.Context, member: discord.Member):
        await self._handle_warns(ctx, member, is_slash=False)

    async def _handle_warns(self, ctx_or_interaction, member: discord.Member, is_slash: bool):
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send
        user_id = str(member.id)
        user_data = self.warn_data["users"].get(user_id, {"warns": [], "total": 0})

        embed = discord.Embed(
            title=f"📋 Warnings for {member.name}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(name="📊 Total Warnings", value=str(user_data["total"]), inline=True)

        if user_data["warns"]:
            warns_text = ""
            for warn in user_data["warns"][-5:]:
                date = datetime.fromisoformat(warn["date"]).strftime("%d-%m-%Y %H:%M")
                warns_text += f"**#{warn['id']}** - {warn['reason']}\n👮 {warn['moderator']} | 📅 {date}\n\n"
            embed.add_field(name="📝 Recent Warnings (Last 5)", value=warns_text[:1000] or "None", inline=False)
        else:
            embed.add_field(name="📝 Warnings", value="No warnings for this user.", inline=False)

        embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")
        await send_response(embed=embed)

    @app_commands.command(name="clearwarns", description="Clear all warnings of a member")
    @app_commands.describe(member="The member to clear warnings for")
    async def clearwarns_slash(self, interaction: discord.Interaction, member: discord.Member):
        await self._handle_clearwarns(interaction, member, is_slash=True)

    @commands.command(name="clearwarns")
    @commands.has_permissions(administrator=True)
    async def clearwarns_prefix(self, ctx: commands.Context, member: discord.Member):
        await self._handle_clearwarns(ctx, member, is_slash=False)

    async def _handle_clearwarns(self, ctx_or_interaction, member: discord.Member, is_slash: bool):
        author = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        if not self.is_admin(author):
            await send_response("❌ You don't have permission to use this command!", ephemeral=True)
            return

        user_id = str(member.id)
        if user_id in self.warn_data["users"]:
            self.warn_data["users"][user_id] = {"warns": [], "total": 0}
            save_json(DATA_FILE, self.warn_data)

            embed = discord.Embed(
                title="✅ Warnings Cleared",
                description=f"All warnings for {member.mention} have been cleared.",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name="👮 Moderator", value=author.mention, inline=True)
            embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")

            await send_response(embed=embed)
        else:
            await send_response(f"❌ {member.name} has no warnings!")

    # ---------------------------------------------------------
    # CHANNEL MANAGEMENT COMMANDS
    # ---------------------------------------------------------

    @app_commands.command(name="lock", description="Lock a channel")
    @app_commands.describe(channel="The channel to lock", reason="Reason for locking")
    async def lock_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None, reason: str = "No reason provided"):
        await self._handle_lock(interaction, channel, reason, is_slash=True)

    @commands.command(name="lock")
    @commands.has_permissions(administrator=True)
    async def lock_prefix(self, ctx: commands.Context, channel: discord.TextChannel = None, *, reason: str = "No reason provided"):
        await self._handle_lock(ctx, channel, reason, is_slash=False)

    async def _handle_lock(self, ctx_or_interaction, channel: discord.TextChannel, reason: str, is_slash: bool):
        author = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
        guild = ctx_or_interaction.guild
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        if not self.is_mod(author):
            await send_response("❌ You don't have permission to use this command!", ephemeral=True)
            return

        if channel is None:
            channel = ctx_or_interaction.channel

        try:
            overwrite = channel.overwrites_for(guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔒 Channel Locked",
                description=f"{channel.mention} has been locked.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.add_field(name="📝 Reason", value=reason, inline=False)
            embed.add_field(name="👮 Moderator", value=author.mention, inline=True)
            embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")

            await send_response(embed=embed)
            await self.log_action(guild, "Lock", author, reason=reason, extra=f"Channel: {channel.mention}")
        except Exception as e:
            await send_response(f"❌ Failed to lock channel: {e}", ephemeral=True)

    @app_commands.command(name="unlock", description="Unlock a channel")
    @app_commands.describe(channel="The channel to unlock", reason="Reason for unlocking")
    async def unlock_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None, reason: str = "No reason provided"):
        await self._handle_unlock(interaction, channel, reason, is_slash=True)

    @commands.command(name="unlock")
    @commands.has_permissions(administrator=True)
    async def unlock_prefix(self, ctx: commands.Context, channel: discord.TextChannel = None, *, reason: str = "No reason provided"):
        await self._handle_unlock(ctx, channel, reason, is_slash=False)

    async def _handle_unlock(self, ctx_or_interaction, channel: discord.TextChannel, reason: str, is_slash: bool):
        author = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
        guild = ctx_or_interaction.guild
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        if not self.is_mod(author):
            await send_response("❌ You don't have permission to use this command!", ephemeral=True)
            return

        if channel is None:
            channel = ctx_or_interaction.channel

        try:
            overwrite = channel.overwrites_for(guild.default_role)
            overwrite.send_messages = None
            await channel.set_permissions(guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{channel.mention} has been unlocked.",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name="📝 Reason", value=reason, inline=False)
            embed.add_field(name="👮 Moderator", value=author.mention, inline=True)
            embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")

            await send_response(embed=embed)
            await self.log_action(guild, "Unlock", author, reason=reason, extra=f"Channel: {channel.mention}")
        except Exception as e:
            await send_response(f"❌ Failed to unlock channel: {e}", ephemeral=True)

    @app_commands.command(name="slowmode", description="Set slowmode for a channel")
    @app_commands.describe(seconds="Slowmode delay in seconds (0-21600)", channel="The channel to set slowmode for")
    async def slowmode_slash(self, interaction: discord.Interaction, seconds: int, channel: discord.TextChannel = None):
        await self._handle_slowmode(interaction, seconds, channel, is_slash=True)

    @commands.command(name="slowmode")
    @commands.has_permissions(administrator=True)
    async def slowmode_prefix(self, ctx: commands.Context, seconds: int, channel: discord.TextChannel = None):
        await self._handle_slowmode(ctx, seconds, channel, is_slash=False)

    async def _handle_slowmode(self, ctx_or_interaction, seconds: int, channel: discord.TextChannel, is_slash: bool):
        author = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        if not self.is_mod(author):
            await send_response("❌ You don't have permission to use this command!", ephemeral=True)
            return

        if channel is None:
            channel = ctx_or_interaction.channel

        if seconds < 0 or seconds > 21600:
            await send_response("❌ Slowmode must be between 0 and 21600 seconds!", ephemeral=True)
            return

        try:
            await channel.edit(slowmode_delay=seconds)
            status = "disabled" if seconds == 0 else f"set to {seconds} seconds"

            embed = discord.Embed(
                title="⏱️ Slowmode Updated",
                description=f"Slowmode for {channel.mention} has been {status}.",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.add_field(name="👮 Moderator", value=author.mention, inline=True)
            embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")

            await send_response(embed=embed)
        except Exception as e:
            await send_response(f"❌ Failed to set slowmode: {e}", ephemeral=True)

    # ---------------------------------------------------------
    # INFO COMMANDS
    # ---------------------------------------------------------

    @app_commands.command(name="serverinfo", description="Get server information")
    async def serverinfo_slash(self, interaction: discord.Interaction):
        await self._handle_serverinfo(interaction, is_slash=True)

    @commands.command(name="serverinfo")
    async def serverinfo_prefix(self, ctx: commands.Context):
        await self._handle_serverinfo(ctx, is_slash=False)

    async def _handle_serverinfo(self, ctx_or_interaction, is_slash: bool):
        guild = ctx_or_interaction.guild
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="👑 Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%d-%m-%Y %H:%M"), inline=True)
        embed.add_field(name="👥 Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="💬 Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="🎭 Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="📊 Boosts", value=str(guild.premium_subscription_count or 0), inline=True)
        embed.set_footer(text=f"ID: {guild.id}")

        await send_response(embed=embed)

    @app_commands.command(name="userinfo", description="Get user information")
    @app_commands.describe(member="The member to get information about")
    async def userinfo_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        await self._handle_userinfo(interaction, member, is_slash=True)

    @commands.command(name="userinfo")
    async def userinfo_prefix(self, ctx: commands.Context, member: discord.Member = None):
        await self._handle_userinfo(ctx, member, is_slash=False)

    async def _handle_userinfo(self, ctx_or_interaction, member: discord.Member, is_slash: bool):
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send
        if member is None:
            member = ctx_or_interaction.user if is_slash else ctx_or_interaction.author

        embed = discord.Embed(
            title=f"👤 {member.name}",
            color=member.color,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="🆔 ID", value=str(member.id), inline=True)
        embed.add_field(name="📛 Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="📅 Joined Discord", value=member.created_at.strftime("%d-%m-%Y %H:%M"), inline=True)
        embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%d-%m-%Y %H:%M") if member.joined_at else "Unknown", inline=True)
        embed.add_field(name="🎭 Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name="🟢 Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="👑 Bot", value="✅ Yes" if member.bot else "❌ No", inline=True)
        embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")

        await send_response(embed=embed)

    @app_commands.command(name="roleinfo", description="Get role information")
    @app_commands.describe(role="The role to get information about")
    async def roleinfo_slash(self, interaction: discord.Interaction, role: discord.Role):
        await self._handle_roleinfo(interaction, role, is_slash=True)

    @commands.command(name="roleinfo")
    async def roleinfo_prefix(self, ctx: commands.Context, role: discord.Role):
        await self._handle_roleinfo(ctx, role, is_slash=False)

    async def _handle_roleinfo(self, ctx_or_interaction, role: discord.Role, is_slash: bool):
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        embed = discord.Embed(
            title=f"🎭 {role.name}",
            color=role.color,
            timestamp=datetime.now()
        )
        embed.add_field(name="🆔 ID", value=str(role.id), inline=True)
        embed.add_field(name="🎨 Color", value=str(role.color).upper(), inline=True)
        embed.add_field(name="👥 Members", value=str(len(role.members)), inline=True)
        embed.add_field(name="📊 Position", value=str(role.position), inline=True)
        embed.add_field(name="🔗 Mentionable", value="✅ Yes" if role.mentionable else "❌ No", inline=True)
        embed.add_field(name="🔒 Hoist", value="✅ Yes" if role.hoist else "❌ No", inline=True)
        embed.add_field(name="📅 Created", value=role.created_at.strftime("%d-%m-%Y %H:%M"), inline=True)
        embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")

        await send_response(embed=embed)

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping_slash(self, interaction: discord.Interaction):
        await self._handle_ping(interaction, is_slash=True)

    @commands.command(name="ping")
    async def ping_prefix(self, ctx: commands.Context):
        await self._handle_ping(ctx, is_slash=False)

    async def _handle_ping(self, ctx_or_interaction, is_slash: bool):
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: `{latency}ms`",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="4FLAG SECURITY - Admin Toolbox")
        await send_response(embed=embed)

    @app_commands.command(name="helpadmin", description="Show admin commands help")
    async def helpadmin_slash(self, interaction: discord.Interaction):
        await self._handle_helpadmin(interaction, is_slash=True)

    @commands.command(name="helpadmin")
    async def helpadmin_prefix(self, ctx: commands.Context):
        await self._handle_helpadmin(ctx, is_slash=False)

    async def _handle_helpadmin(self, ctx_or_interaction, is_slash: bool):
        send_response = ctx_or_interaction.response.send_message if is_slash else ctx_or_interaction.send

        embed = discord.Embed(
            title="🛡️ 4FLAG SECURITY",
            description="Complete server management bot",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )

        embed.add_field(
            name="🛠️ Moderation Commands",
            value=(
                "`/timeout <member> <minutes> <reason>` - Timeout a member\n"
                "`/ban <member> <reason> <delete_days>` - Ban a member\n"
                "`/kick <member> <reason>` - Kick a member\n"
                "`/warn <member> <reason>` - Warn a member\n"
                "`/warns <member>` - View warnings\n"
                "`/clearwarns <member>` - Clear warnings"
            ),
            inline=False
        )

        embed.add_field(
            name="🧹 Clear/Purge Commands",
            value=(
                "`/clear <amount> <channel>` - Clear messages\n"
                "`/purge <amount> <filters>` - Purge with filters\n"
                "`!purgebots <amount>` - Delete bot messages\n"
                "`!purgeuser <user> <amount>` - Delete user messages\n"
                "`!purgecontains <text> <amount>` - Delete messages with text"
            ),
            inline=False
        )

        embed.add_field(
            name="🔧 Channel Commands",
            value=(
                "`/lock <channel> <reason>` - Lock a channel\n"
                "`/unlock <channel> <reason>` - Unlock a channel\n"
                "`/slowmode <seconds> <channel>` - Set slowmode\n"
                "`/nuke <channel> <reason>` - Reset a channel"
            ),
            inline=False
        )

        embed.add_field(
            name="📢 Utility Commands",
            value=(
                "`/announce <channel> <title> <description>` - Send announcement\n"
                "`/poll <channel> <question> <options>` - Create a poll\n"
                "`/giveaway_start <channel> <prize> <duration>` - Start giveaway\n"
                "`/giveaway_end <message_id>` - End giveaway"
            ),
            inline=False
        )

        embed.add_field(
            name="📊 Info Commands",
            value=(
                "`/serverinfo` - Server information\n"
                "`/userinfo <member>` - User information\n"
                "`/roleinfo <role>` - Role information\n"
                "`/ping` - Bot latency"
            ),
            inline=False
        )

        embed.add_field(
            name="🛡️ Permissions",
            value=(
                f"• **Admin Role ID:** `{ADMIN_ROLE_ID}`\n"
                f"• **Mod Role ID:** `{MOD_ROLE_ID}`\n"
                f"• **Log Channel ID:** `{LOG_CHANNEL_ID}`"
            ),
            inline=False
        )

        embed.set_footer(text="Made with ❤️ by 4FLAG SECURITY")
        await send_response(embed=embed)

# =========================================================
# MAIN BOT CLASS
# =========================================================

class KrishuXBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=["!", "krishu "], intents=intents, help_command=None)
        self.initialized = False

    async def setup_hook(self):
        print("🔄 Setting up bot...")

        try:
            await self.add_cog(AdminToolbox(self))
            print("✅ AdminToolbox cog loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load cog: {e}")
            traceback.print_exc()

        try:
            # =====================================================
            # ⚠️ HNA 7ET L'ID DYAL SERVER DYALEK (4FLAG CHEATS) ⚠️
            # =====================================================
            YOUR_GUILD_ID = 1422055422864396389  # <-- ID dyal l'server dyalek
            
            guild = discord.Object(id=YOUR_GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"✅ Synced {len(synced)} slash commands to your server")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")

        self.initialized = True
        self.update_activity_task.start()
        print("✅ Bot setup complete!")

    async def on_ready(self):
        global bot_name
        if not self.initialized:
            return

        server_count = len(self.guilds)
        bot_name = f"{self.user.name}"

        print("\n" + "=" * 60)
        print("🛡️ 4FLAG SECURITY - ADMIN TOOLBOX")
        print("=" * 60)
        print(f"✅ Bot: {bot_name}")
        print(f"📊 Servers: {server_count}")
        print(f"📝 Commands: {len(self.tree.get_commands())}")
        print("=" * 60)

        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="𝟒𝐅𝐋𝐀𝐆 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝟐𝟒/𝟕"
        )
        await self.change_presence(activity=activity)

    @tasks.loop(minutes=5)
    async def update_activity_task(self):
        try:
            if self.initialized:
                server_count = len(self.guilds)
                activity = discord.Activity(
                    type=discord.ActivityType.watching,
                    name="𝟒𝐅𝐋𝐀𝐆 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝟐𝟒/𝟕"
                )
                await self.change_presence(activity=activity)
        except Exception as e:
            print(f"⚠️ Activity update error: {e}")

    @update_activity_task.before_loop
    async def before_update_activity_task(self):
        await self.wait_until_ready()

# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":
    try:
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        print("🚀 Flask server started on port 10000")

        bot = KrishuXBot()
        bot.run(TOKEN)

    except discord.errors.LoginFailure:
        print("❌ Invalid Discord token")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)