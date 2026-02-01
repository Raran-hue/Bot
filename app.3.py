import discord
from discord.ext import commands
import asyncio
import random
import json
from datetime import datetime
import aiohttp
import math

# ================= BOT SETUP =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= DATA =================
def load_json(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

scores = load_json("scores.json", {})
levels = load_json("levels.json", {})
teams = load_json("teams.json", {})


# ================= EVENTS =================
@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")
    await bot.change_presence(activity=discord.Game("!help"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    uid = str(message.author.id)
    data = levels.get(uid, {"xp": 0, "level": 1})

    gained = random.randint(5, 10)
    data["xp"] += gained

    needed = 50 + data["level"] * 25
    if data["xp"] >= needed:
        data["level"] += 1
        data["xp"] = 0
        await message.channel.send(f"🎉 {message.author.mention} وصل ليفل **{data['level']}**!")

    levels[uid] = data
    save_json("levels.json", levels)

    await bot.process_commands(message)

# ================= BASIC =================
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="whoisstrongest")
@commands.cooldown(1, 15, commands.BucketType.guild)
async def who_is_strongest(ctx):
    members = [m for m in ctx.guild.members if not m.bot]
    await ctx.send(f"💪 {random.choice(members).mention}")

@bot.command(name="8ball")
@commands.cooldown(1, 10, commands.BucketType.user)
async def eight_ball(ctx, *, question: str):
    answers = ["Yes", "No", "Maybe", "Definitely", "Ask later"]
    await ctx.send(f"🎱 {random.choice(answers)}")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def joke(ctx):
    jokes = [
        "Atoms make up everything.",
        "Skeletons don’t fight, no guts.",
        "PC went therapy, many bugs."
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def fact(ctx):
    facts = [
        "Honey never spoils.",
        "Octopus has 3 hearts.",
        "Bananas are berries."
    ]
    await ctx.send(random.choice(facts))

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rate(ctx, *, thing: str):
    await ctx.send(f"{thing}: {random.randint(1,10)}/10")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def today(ctx):
    await ctx.send(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def cat(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://api.thecatapi.com/v1/images/search") as r:
            data = await r.json()
            await ctx.send(data[0]["url"])

# ================= TEXT =================
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def reverse(ctx, *, text: str):
    await ctx.send(text[::-1])

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def mock(ctx, *, text: str):
    await ctx.send("".join(c.upper() if random.random()>0.5 else c.lower() for c in text))

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def say(ctx, *, text: str):
    if ctx.channel.permissions_for(ctx.guild.me).manage_messages:
        await ctx.message.delete()
    await ctx.send(text)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def clap(ctx, *, text: str):
    await ctx.send(" 👏 ".join(text.split()))

# ================= CHAOS =================
@bot.command()
@commands.cooldown(1, 20, commands.BucketType.guild)
async def chaos(ctx):
    msgs = ["🔥 CHAOS 🔥", "🌀 REALITY BREAKS", "💀 NO ESCAPE"]
    await ctx.send(random.choice(msgs))

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def spam(ctx, times: int = 5, *, text="CHAOS"):
    times = min(times, 10)
    for _ in range(times):
        await ctx.send(text)
        await asyncio.sleep(0.4)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def coinflip(ctx):
    await ctx.send(random.choice(["HEADS", "TAILS"]))

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def rng(ctx, a: int = 1, b: int = 100):
    await ctx.send(random.randint(a, b))

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def scream(ctx):
    await ctx.send("AAAAAAAAAAAA")

# ================= LEVEL =================
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = levels.get(str(member.id), {"level": 1, "xp": 0})
    await ctx.send(f"⭐ {member.name} | Level {data['level']} | XP {data['xp']}")

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.guild)
async def rank(ctx):
    sorted_lv = sorted(levels.items(), key=lambda x: x[1]["level"], reverse=True)
    text = ""
    for i, (uid, d) in enumerate(sorted_lv[:10], 1):
        user = await bot.fetch_user(int(uid))
        text += f"{i}. {user.name} — L{d['level']}\n"
    await ctx.send(embed=discord.Embed(title="🏆 RANKS", description=text))

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.guild)
async def zalgo(ctx, *, text: str):
    chaos = ["̸", "̷", "̴", "̶", "͜", "͝", "͞", "͟"]
    result = "".join(c + "".join(random.choice(chaos) for _ in range(2)) for c in text)
    await ctx.send(result)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def brainrot(ctx):
    await ctx.send(random.choice([
        "bro really said that 💀",
        "npc behavior detected",
        "ain't no way 😭",
        "chat is this real"
    ]))

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def owo(ctx, *, text: str = "hello"):
    text = text.replace("r", "w").replace("l", "w")
    await ctx.send(f"OwO 👉👈 {text}")

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def curse(ctx, member: discord.Member = None):
    target = member.mention if member else ctx.author.mention
    await ctx.send(f"🔮 {target} will step on a Lego today.")

# ================= ERRORS =================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ انتظر {round(error.retry_after,1)} ثانية")
    else:
        raise error



# ================= RUN =================
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("ERROR: DISCORD_TOKEN environment variable not set")
else:
    bot.run(token)
