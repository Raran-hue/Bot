import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = 123456789012345678   # role to REMOVE
GUILD_ID = 123456789012345678
DURATION = timedelta(days=7)

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(ROLE_ID)
    if role:
        await member.add_roles(role)

@tasks.loop(hours=1)
async def role_cleanup():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return

    now = datetime.now(timezone.utc)
    role = guild.get_role(ROLE_ID)

    for member in guild.members:
        if role not in member.roles:
            continue
        if not member.joined_at:
            continue

        if now - member.joined_at >= DURATION:
            await member.remove_roles(role)

@bot.event
async def on_ready():
    role_cleanup.start()
    print("Bot ready")

# bot.run(os.getenv('DISCORD_TOKEN'))  # Use environment variable instead
bot.run("YOUR_BOT_TOKEN_HERE")
