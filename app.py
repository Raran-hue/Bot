import json
import asyncio
import discord
import random
from discord.ext import commands
from datetime import datetime
import aiohttp

# ----------------- BOT SETUP -----------------
# intents = discord.Intents.default()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------- ON READY -----------------
# @bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("!help")
    )

# ----------------- BASIC COMMANDS -----------------
# @bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="whoisstrongest")
async def who_is_strongest(ctx):
    members = [m for m in ctx.guild.members if not m.bot]
    if not members:
        await ctx.send("Nobody to choose from! 😢")
        return
    chosen = random.choice(members)
    await ctx.send(f"💪 Today, {chosen.mention} is the strongest!")

@bot.command(name="8ball")
async def eight_ball(ctx, *, question: str = None):
    if not question:
        await ctx.send("❓ You need to ask a question. Example: !8ball Will I be rich?")
        return
    responses = [
        "Yes!", "No!", "Maybe...", "Definitely!",
        "I don't think so.", "Ask again later.",
        "Absolutely!", "Nah.", "For sure.", "Impossible!"
    ]
    await ctx.send(f"🎱 Question: {question}\nAnswer: {random.choice(responses)}")

@bot.command(name="joke")
async def joke(ctx):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 😂",
        "Why did the computer go to therapy? Too many bugs. 🐛",
        "I told my dog to play dead... now he won't move. 😅",
        "Why don’t skeletons fight each other? They don’t have the guts. 💀",
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾"
    ]
    await ctx.send(f"😂 {random.choice(jokes)}")

@bot.command(name="fact")
async def fact(ctx):
    facts = [
        "Honey never spoils.",
        "Bananas are berries, but strawberries aren't.",
        "A group of flamingos is called a 'flamboyance'.",
        "Octopuses have 3 hearts.",
        "Cats can’t taste sweetness."
    ]
    await ctx.send(f"🧠 Random Fact: {random.choice(facts)}")

@bot.command(name="roast")
async def roast(ctx, member: discord.Member):
    roasts = [
        "You're as useful as a screen door on a submarine.",
        "You're not stupid; you just have bad luck thinking.",
        "If I had a dollar for every smart thing you said, I’d be broke.",
        "You're proof that even evolution takes a break sometimes."
    ]
    await ctx.send(f"{member.mention}, {random.choice(roasts)} 💀")

@bot.command(name="rate")
async def rate(ctx, *, thing: str = None):
    if not thing:
        await ctx.send("🔢 You need to tell me what to rate! Example: !rate your idea")
        return
    score = random.randint(1, 10)
    await ctx.send(f"📊 I'd rate **{thing}** a **{score}/10**")

@bot.command(name="today")
async def today(ctx):
    now = datetime.now()
    await ctx.send(f"📅 Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command(name="cat")
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
            if resp.status != 200:
                await ctx.send("😿 Couldn't fetch a cat right now.")
                return
            data = await resp.json()
            await ctx.send(f"🐱 Here's a cat for you:\n{data[0]['url']}")

# ================= DATA =================
def load(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

scores = load("scores.json")
levels = load("levels.json")
teams = load("teams.json")

# ================= QUESTIONS =================
QUESTIONS = {
    "easy": [
        {"q": "2 + 2?", "a": ["4"], "p": 1},
        {"q": "Sky color?", "a": ["blue"], "p": 1}
    ],
    "medium": [
        {"q": "Capital of France?", "a": ["paris"], "p": 2},
        {"q": "Red Planet?", "a": ["mars"], "p": 2}
    ],
    "hard": [
        {"q": "Chemical symbol for Gold?", "a": ["au"], "p": 3},
        {"q": "Square root of 144?", "a": ["12"], "p": 3}
    ],
    "gd": [
        {"q": "Who created Geometry Dash?", "a": ["robtop"], "p": 3}
    ],
    "minecraft": [
        {"q": "End boss?", "a": ["ender dragon", "enderdragon"], "p": 3}
    ],
    "silent": [
        {"q": "What exists before existence?", "a": ["nothing", "void"], "p": 6}
    ]
}

# ================= LEVELING =================
def add_xp(user_id, points):
    uid = str(user_id)
    scores[uid] = scores.get(uid, 0) + points
    levels.setdefault(uid, {"level": 1, "xp": 0})

    levels[uid]["xp"] += points
    needed = levels[uid]["level"] * 10

    if levels[uid]["xp"] >= needed:
        levels[uid]["xp"] = 0
        levels[uid]["level"] += 1
        return True
    return False

# ================= TRIVIA =================
@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def trivia(ctx, category="easy"):
    category = category.lower()
    if category not in QUESTIONS:
        await ctx.send("Invalid category.")
        return

    q = random.choice(QUESTIONS[category])
    await ctx.send(f"🧠 **{category.upper()}**\n{q['q']}")

    def check(m):
        return m.channel == ctx.channel and not m.author.bot

    try:
        msg = await bot.wait_for("message", timeout=15, check=check)
        msg_content = msg.content.lower().strip()
        if msg_content in [a.lower().strip() for a in q["a"]]:
            leveled = add_xp(msg.author.id, q["p"])
            save("scores.json", scores)
            save("levels.json", levels)

            text = f"✅ {msg.author.mention} +{q['p']} points"
            if leveled:
                text += " 🎉 LEVEL UP!"
            await ctx.send(text)
        else:
            await ctx.send("❌ Wrong answer.")
    except asyncio.TimeoutError:
        await ctx.send("⏱️ Time's up!")

# ================= LEADERBOARD =================
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def leaderboard(ctx):
    if not scores:
        await ctx.send("No data.")
        return

    sorted_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    text = ""
    for i, (uid, score) in enumerate(sorted_users, 1):
        user = await bot.fetch_user(int(uid))
        lvl = levels.get(uid, {}).get("level", 1)
        text += f"**{i}. {user.name}** — {score} pts (Lv {lvl})\n"

    await ctx.send(embed=discord.Embed(
        title="🏆 Trivia Leaderboard",
        description=text
    ))

# ================= TEAMS =================
@bot.command()
async def team(ctx, color):
    color = color.lower()
    if color not in ["red", "blue"]:
        await ctx.send("Choose red or blue.")
        return

    teams[str(ctx.author.id)] = color
    save("teams.json", teams)
    await ctx.send(f"Joined **{color.upper()}** team.")

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def team_leaderboard(ctx):
    totals = {"red": 0, "blue": 0}
    for if team in totals:
            uid, team in teams.items():
        totals[team] += scores.get(uid, 0)

    await ctx.send(
        f"🔴 Red: {totals['red']} pts\n"
        f"🔵 Blue: {totals['blue']} pts"
    )

# ================= LIST =================
@bot.command(name="list")
@commands.cooldown(1, 10, commands.BucketType.user)
async def list_cmd(ctx):
    await ctx.send(embed=discord.Embed(
        title="📜 Trivia Commands",
        description=(
            "**Commands**\n"
            "`!trivia <category>`\n"
            "`!leaderboard`\n"
            "`!team red / blue`\n"
            "`!team_leaderboard`\n\n"
            "**Categories**\n"
            "easy, medium, hard, gd, minecraft, silent"
        ),
        color=0x00ffff
    ))

# ================= SETUP =================
def setup(bot):
    bot.add_command(trivia)
    bot.add_command(leaderboard)
    bot.add_command(team)
    bot.add_command(team_leaderboard)
    bot.add_command(list_cmd)
    # ----------------- CHAOS COMMANDS -----------------

@bot.command(name="chaos")
async def chaos(ctx):
    messages = [
        "🔥 CHAOS MODE ACTIVATED 🔥",
        "💥 EVERYTHING IS FINE (IT IS NOT) 💥",
        "🌀 REALITY IS COLLAPSING 🌀",
        "😈 CHAOS CHAOS CHAOS 😈",
        "🚨 TOO LATE TO ESCAPE 🚨"
    ]
    await ctx.send(random.choice(messages))

@bot.command(name="spam")
async def spam(ctx, times: int = 5, *, text: str = "CHAOS"):
    times = min(times, 10)
    for _ in range(times):
        await ctx.send(text)
        await asyncio.sleep(0.5)

@bot.command(name="coinflip")
async def coinflip(ctx):
    await ctx.send(f"🪙 {random.choice(['HEADS', 'TAILS'])}")

@bot.command(name="rng")
async def rng(ctx, min_num: int = 1, max_num: int = 100):
    await ctx.send(f"🎲 {random.randint(min_num, max_num)}")

@bot.command(name="explode")
async def explode(ctx, member: discord.Member = None):
    target = member.mention if member else ctx.author.mention
    await ctx.send(f"💣 {target} has exploded into 1,000,000 pieces.")

@bot.command(name="reverse")
async def reverse(ctx, *, text: str):
    await ctx.send(text[::-1])

@bot.command(name="scream")
async def scream(ctx):
    await ctx.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

@bot.command(name="insultme")
async def insultme(ctx):
    insults = [
        "You have the intelligence of a burnt toaster.",
        "I've seen smarter rocks.",
        "Even Google can't find your brain.",
        "You're not dumb, just… extremely unlucky thinking."
    ]
    await ctx.send(random.choice(insults))

@bot.command(name="randomping")
async def randomping(ctx):
    members = [m for m in ctx.guild.members if not m.bot]
    await ctx.send(random.choice(members).mention)

@bot.command(name="chaosfact")
async def chaosfact(ctx):
    facts = [
        "This command exists for no reason.",
        "Chaos is a feature, not a bug.",
        "Someone typed !chaos and regretted it.",
        "This bot is slowly losing its sanity."
    ]
    await ctx.send(random.choice(facts))
    # ----------------- EXTRA CHAOS / FUN COMMANDS -----------------

@bot.command(name="uwu")
async def uwu(ctx, *, text: str = None):
    if not text:
        text = "hello"
    uwu_map = {
        "r": "w", "l": "w",
        "R": "W", "L": "W",
        "no": "nu", "has": "haz",
        "you": "uu", "the": "da"
    }
    for k, v in uwu_map.items():
        text = text.replace(k, v)
    await ctx.send(f"UwU 👉👈 {text}")
@bot.command(name="dadjoke")
async def dadjoke(ctx):
    jokes = [
        "I'm afraid for the calendar. Its days are numbered.",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "I only know 25 letters of the alphabet. I don't know y.",
        "What do you call fake spaghetti? An impasta."
    ]
    await ctx.send(random.choice(jokes))

@bot.command(name="emojify")
async def emojify(ctx, *, text: str):
    result = ""
    for c in text.lower():
        if c.isalpha():
            result += f":regional_indicator_{c}: "
        elif c.isdigit():
            nums = {
                "0": ":zero:", "1": ":one:", "2": ":two:", "3": ":three:",
                "4": ":four:", "5": ":five:", "6": ":six:", "7": ":seven:",
                "8": ":eight:", "9": ":nine:"
            }
            result += nums[c] + " "
        else:
            result += c + " "
    await ctx.send(result)

@bot.command(name="clap")
async def clap(ctx, *, text: str):
    await ctx.send(" 👏 ".join(text.split()))

@bot.command(name="mock")
async def mock(ctx, *, text: str):
    mocked = "".join(
        c.upper() if random.random() > 0.5 else c.lower()
        for c in text
    )
    await ctx.send(mocked)

@bot.command(name="say")
async def say(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(text)

@bot.command(name="vibecheck")
async def vibecheck(ctx, member: discord.Member = None):
    target = member.mention if member else ctx.author.mention
    vibes = [
        "IMMACULATE VIBES ✨",
        "CHAOTIC ENERGY 😈",
        "SUSPICIOUSLY CALM 😐",
        "NO VIBES DETECTED 💀",
        "ELITE VIBES 🔥"
    ]
    await ctx.send(f"{target}: {random.choice(vibes)}")

@bot.command(name="shrug")
async def shrug(ctx):
    await ctx.send("¯\\_(ツ)_/¯")

@bot.command(name="tableflip")
async def tableflip(ctx):
    await ctx.send("(╯°□°）╯︵ ┻━┻")

@bot.command(name="unflip")
async def unflip(ctx):
    await ctx.send("┬─┬ ノ( ゜-゜ノ)")

@bot.command(name="fortune")
async def fortune(ctx):
    fortunes = [
        "You will forget why you opened Discord.",
        "Great chaos is coming. Probably.",
        "Today is a good day to type !chaos.",
        "You will win trivia. Maybe."
    ]
    await ctx.send(random.choice(fortunes))
  ================= RUN BOT =================
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("ERROR: DISCORD_TOKEN environment variable not set")
else:
    bot.run(token
# bot.run("TM4MzIwNDYwODI0NzA3MDgxMA.GF09cR.8X6wQF9rZQvIrUI-x1IhFFm3ATig56lg6_sUAw")