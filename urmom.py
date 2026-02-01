import os
import json
import asyncio
import random
import discord
from discord.ext import commands
from datetime import datetime
import aiohttp
import io

# ================= BOT SETUP =================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


# ================= UTIL =================
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

scores = load_json("scores.json")
levels = load_json("levels.json")
teams = load_json("teams.json")

# NOTE: `add_xp` implemented further below (more robust)

# ================= ON READY =================
@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")
    try:
        await bot.change_presence(activity=discord.Game("!list"))
    except Exception:
        pass

# ================= BASIC COMMANDS =================
@bot.command(name="whoisstrongest")
@commands.cooldown(1, 10, commands.BucketType.guild)
async def who_is_strongest(ctx):
    members = [m for m in ctx.guild.members if not m.bot]
    await ctx.send(f"💪 {random.choice(members).mention}")

@bot.command(name="8ball")
@commands.cooldown(1, 5, commands.BucketType.user)
async def eight_ball(ctx, *, question: str):
    responses = ["Yes!", "No!", "Maybe...", "Definitely!", "Ask again later.", "Absolutely!", "Impossible!"]
    await ctx.send(f"🎱 {random.choice(responses)}")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def joke(ctx):
    await ctx.send(random.choice([
        "Atoms make up everything.",
        "I would tell a joke about UDP, but you might not get it.",
        "Skeletons don’t fight. No guts."
    ]))

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def fact(ctx):
    await ctx.send(random.choice([
        "Honey never spoils.",
        "Octopus has 3 hearts.",
        "Bananas are berries.",
        "A group of Flamboy is flamboyance."
    ]))

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def roast(ctx, member: discord.Member):
    await ctx.send(f"{member.mention} {random.choice(['You tried.', 'Skill issue.', 'Evolution paused.'])}")

@bot.command()
async def today(ctx):
    await ctx.send(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as r:
            data = await r.json()
            await ctx.send(data[0]["url"])

# ================= TRIVIA =================
QUESTIONS = {
    "easy": [
        {"q": "What is 5 + 7?", "a": ["12"], "p": 1},
        {"q": "What color is a ripe banana?", "a": ["yellow"], "p": 1},
        {"q": "How many legs does a spider have?", "a": ["8"], "p": 1},
        {"q": "Which day comes after Monday?", "a": ["tuesday"], "p": 1},
        {"q": "What is the first letter of the alphabet?", "a": ["a"], "p": 1},
        {"q": "How many sides does a triangle have?", "a": ["3"], "p": 1},
        {"q": "What color is the sky on a clear day?", "a": ["blue"], "p": 1},
        {"q": "How many fingers do humans have on one hand?", "a": ["5"], "p": 1},
        {"q": "Which fruit is typically red?", "a": ["apple"], "p": 1},
        {"q": "What is 10 - 4?", "a": ["6"], "p": 1},
        {"q": "What do bees produce?", "a": ["honey"], "p": 1},
        {"q": "Which animal barks?", "a": ["dog"], "p": 1},
        {"q": "How many wheels does a bicycle have?", "a": ["2"], "p": 1},
        {"q": "What is the color of snow?", "a": ["white"], "p": 1},
        {"q": "How many months are in a year?", "a": ["12"], "p": 1},
        {"q": "What do cows produce?", "a": ["milk"], "p": 1},
        {"q": "Which animal says 'meow'?", "a": ["cat"], "p": 1},
        {"q": "What is 3 + 9?", "a": ["12"], "p": 1},
        {"q": "What color are carrots?", "a": ["orange"], "p": 1},
        {"q": "How many legs do humans have?", "a": ["2"], "p": 1},
        {"q": "Which fruit is yellow and sour?", "a": ["lemon"], "p": 1},
        {"q": "What is 7 + 5?", "a": ["12"], "p": 1},
        {"q": "Which animal lives in water and has fins?", "a": ["fish"], "p": 1},
        {"q": "How many letters are in the English alphabet?", "a": ["26"], "p": 1},
        {"q": "Which day comes before Wednesday?", "a": ["tuesday"], "p": 1},
        {"q": "What is the opposite of hot?", "a": ["cold"], "p": 1},
        {"q": "Which color comes from mixing red and white?", "a": ["pink"], "p": 1},
        {"q": "What do you call frozen water?", "a": ["ice"], "p": 1},
        {"q": "Which fruit is green on the outside and red inside?", "a": ["watermelon"], "p": 1},
        {"q": "How many days are in a week?", "a": ["7"], "p": 1},
        {"q": "What do you breathe in?", "a": ["air"], "p": 1},
        {"q": "Which animal says 'oink'?", "a": ["pig"], "p": 1},
        {"q": "What is 6 + 6?", "a": ["12"], "p": 1},
        {"q": "Which color is associated with stop signs?", "a": ["red"], "p": 1},
        {"q": "What shape has four equal sides?", "a": ["square"], "p": 1},
        {"q": "Which fruit is orange and round?", "a": ["orange"], "p": 1},
        {"q": "How many eyes do humans have?", "a": ["2"], "p": 1},
        {"q": "What is 9 - 3?", "a": ["6"], "p": 1},
        {"q": "Which animal hops and carries its baby in a pouch?", "a": ["kangaroo"], "p": 1},
        {"q": "What do you wear on your feet?", "a": ["shoes"], "p": 1},
        {"q": "Which color do you get by mixing blue and yellow?", "a": ["green"], "p": 1},
        {"q": "What is 8 + 4?", "a": ["12"], "p": 1},
        {"q": "Which animal is known as man's best friend?", "a": ["dog"], "p": 1},
        {"q": "What do you write with?", "a": ["pen", "pencil"], "p": 1},
        {"q": "How many legs does a cat have?", "a": ["4"], "p": 1},
        {"q": "Which fruit is small, red, and grows in clusters?", "a": ["cherry"], "p": 1},
        {"q": "What is 1 + 11?", "a": ["12"], "p": 1},
        {"q": "Which animal has a long trunk?", "a": ["elephant"], "p": 1},
        {"q": "What color are clouds on a sunny day?", "a": ["white"], "p": 1},
        {"q": "What do you drink to stay hydrated?", "a": ["water"], "p": 1},
        {"q": "Which animal is black and white and eats bamboo?", "a": ["panda"], "p": 1},
        {"q": "What is 0 + 12?", "a": ["12"], "p": 1},
        {"q": "Which fruit is red and often used in pies?", "a": ["apple"], "p": 1},
        {"q": "How many letters are in 'hello'?", "a": ["5"], "p": 1}
    ],

    "medium": [
        {"q": "Capital of Germany?", "a": ["berlin"], "p": 2},
        {"q": "Largest planet in our solar system?", "a": ["jupiter"], "p": 2},
        {"q": "Which ocean is the largest?", "a": ["pacific"], "p": 2},
        {"q": "Who wrote 'Romeo and Juliet'?", "a": ["shakespeare"], "p": 2},
        {"q": "H2O is the chemical formula for what?", "a": ["water"], "p": 2},
        {"q": "Which country is famous for the Eiffel Tower?", "a": ["france"], "p": 2},
        {"q": "What gas do plants produce?", "a": ["oxygen"], "p": 2},
        {"q": "Which planet is known as the Red Planet?", "a": ["mars"], "p": 2},
        {"q": "Who painted the Mona Lisa?", "a": ["da vinci", "leonardo da vinci"], "p": 2},
        {"q": "What is the freezing point of water in Celsius?", "a": ["0"], "p": 2},
        {"q": "What is the largest mammal?", "a": ["blue whale"], "p": 2},
        {"q": "Which continent is Egypt in?", "a": ["africa"], "p": 2},
        {"q": "What language do they speak in Brazil?", "a": ["portuguese"], "p": 2},
        {"q": "Which element has the symbol 'O'?", "a": ["oxygen"], "p": 2},
        {"q": "Who discovered gravity?", "a": ["newton", "isaac newton"], "p": 2},
        {"q": "Which planet has rings?", "a": ["saturn"], "p": 2},
        {"q": "Which country is known for sushi?", "a": ["japan"], "p": 2},
        {"q": "What is the square root of 64?", "a": ["8"], "p": 2},
        {"q": "Which ocean is on the west coast of the USA?", "a": ["pacific"], "p": 2},
        {"q": "Who wrote '1984'?", "a": ["george orwell"], "p": 2},
        {"q": "What is the largest desert in the world?", "a": ["sahara"], "p": 2},
        {"q": "Which city is known as the Big Apple?", "a": ["new york"], "p": 2},
        {"q": "What is the capital of Italy?", "a": ["rome"], "p": 2},
        {"q": "Which metal is liquid at room temperature?", "a": ["mercury"], "p": 2},
        {"q": "Who is known as the father of computers?", "a": ["charles babbage"], "p": 2},
        {"q": "Which is the fastest land animal?", "a": ["cheetah"], "p": 2},
        {"q": "Which country is famous for its pyramids?", "a": ["egypt"], "p": 2},
        {"q": "Which organ pumps blood?", "a": ["heart"], "p": 2},
        {"q": "What is the chemical symbol for iron?", "a": ["fe"], "p": 2},
        {"q": "Which planet is closest to the sun?", "a": ["mercury"], "p": 2},
        {"q": "Who wrote 'Hamlet'?", "a": ["shakespeare"], "p": 2},
        {"q": "Which gas is essential for humans to breathe?", "a": ["oxygen"], "p": 2},
        {"q": "What is the largest organ in the human body?", "a": ["skin"], "p": 2},
        {"q": "Which continent is Australia in?", "a": ["australia"], "p": 2},
        {"q": "Which ocean touches the east coast of Africa?", "a": ["indian"], "p": 2},
        {"q": "Who invented the telephone?", "a": ["alexander graham bell"], "p": 2},
        {"q": "Which country has the maple leaf on its flag?", "a": ["canada"], "p": 2},
        {"q": "What is the largest planet in the solar system?", "a": ["jupiter"], "p": 2},
        {"q": "Which planet is called the morning star?", "a": ["venus"], "p": 2},
        {"q": "Who painted the Starry Night?", "a": ["van gogh", "vincent van gogh"], "p": 2},
        {"q": "What is the capital of Spain?", "a": ["madrid"], "p": 2},
        {"q": "Which is the smallest continent?", "a": ["australia"], "p": 2},
        {"q": "Which animal is known as the king of the jungle?", "a": ["lion"], "p": 2},
        {"q": "What is the boiling point of water in Celsius?", "a": ["100"], "p": 2},
        {"q": "Which country is known for its tulips?", "a": ["netherlands"], "p": 2},
        {"q": "Which organ removes waste from the blood?", "a": ["kidney"], "p": 2}
    ], 
        "hard": [
        {"q": "What is the derivative of x^2?", "a": ["2x"], "p": 3},
        {"q": "Who developed the theory of relativity?", "a": ["einstein", "albert einstein"], "p": 3},
        {"q": "What is the capital of Iceland?", "a": ["reykjavik"], "p": 3},
        {"q": "Which element has atomic number 79?", "a": ["gold"], "p": 3},
        {"q": "Who wrote 'The Divine Comedy'?", "a": ["dante alighieri", "dante"], "p": 3},
        {"q": "What is the square root of 256?", "a": ["16"], "p": 3},
        {"q": "Which planet has the most moons?", "a": ["saturn"], "p": 3},
        {"q": "What is the chemical formula for table salt?", "a": ["nacl"], "p": 3},
        {"q": "Who painted the ceiling of the Sistine Chapel?", "a": ["michelangelo"], "p": 3},
        {"q": "What is the largest internal organ in the human body?", "a": ["liver"], "p": 3},
        {"q": "What is the speed of light in m/s?", "a": ["299792458", "299,792,458"], "p": 3},
        {"q": "Which mathematician is known for the Last Theorem?", "a": ["fermat", "pierre de fermat"], "p": 3},
        {"q": "Which gas has the chemical symbol 'Ne'?", "a": ["neon"], "p": 3},
        {"q": "Who is known as the father of modern physics?", "a": ["galileo", "galileo galilei"], "p": 3},
        {"q": "Which country hosted the 2016 Summer Olympics?", "a": ["brazil"], "p": 3},
        {"q": "What is the powerhouse of the cell?", "a": ["mitochondria"], "p": 3},
        {"q": "What is 15 * 12?", "a": ["180"], "p": 3},
        {"q": "Which scientist proposed the three laws of motion?", "a": ["newton", "isaac newton"], "p": 3},
        {"q": "What is the heaviest naturally occurring element?", "a": ["uranium"], "p": 3},
        {"q": "What is the capital of Mongolia?", "a": ["ulaanbaatar"], "p": 3},
        {"q": "Which disease is caused by Mycobacterium tuberculosis?", "a": ["tuberculosis", "tb"], "p": 3},
        {"q": "Who wrote 'Pride and Prejudice'?", "a": ["jane austen"], "p": 3},
        {"q": "Which planet is known for its Great Red Spot?", "a": ["jupiter"], "p": 3},
        {"q": "Which blood type is the universal donor?", "a": ["o-", "o negative", "onegative"], "p": 3},
        {"q": "What is the hardest natural substance on Earth?", "a": ["diamond"], "p": 3},
        {"q": "Which is the smallest prime number?", "a": ["2"], "p": 3},
        {"q": "Which is the heaviest organ in the human body?", "a": ["liver"], "p": 3},
        {"q": "Who is the author of 'The Iliad'?", "a": ["homer"], "p": 3},
        {"q": "What is the 10th Fibonacci number?", "a": ["55"], "p": 3},
        {"q": "What is the most abundant gas in Earth's atmosphere?", "a": ["nitrogen"], "p": 3},
        {"q": "Which planet is furthest from the sun?", "a": ["neptune"], "p": 3},
        {"q": "What is the atomic number of carbon?", "a": ["6"], "p": 3},
        {"q": "Which metal has the highest electrical conductivity?", "a": ["silver"], "p": 3},
        {"q": "Who developed the polio vaccine?", "a": ["jonas salk"], "p": 3},
        {"q": "What is the chemical symbol for potassium?", "a": ["k"], "p": 3},
        {"q": "Which is the smallest country in the world?", "a": ["vatican city"], "p": 3},
        {"q": "Who painted 'Guernica'?", "a": ["picasso", "pablo picasso"], "p": 3},
        {"q": "Which planet spins on its side?", "a": ["uranus"], "p": 3},
        {"q": "What is 2^8?", "a": ["256"], "p": 3},
        {"q": "Which organ regulates hormones?", "a": ["endocrine system", "glands"], "p": 3},
        {"q": "Who is the author of 'War and Peace'?", "a": ["leo tolstoy"], "p": 3},
        {"q": "Which gas is used in balloons to make them float?", "a": ["helium"], "p": 3},
        {"q": "What is the largest bone in the human body?", "a": ["femur"], "p": 3},
        {"q": "Who was the first person in space?", "a": ["yuri gagarin"], "p": 3},
        {"q": "What is 13 squared?", "a": ["169"], "p": 3},
        {"q": "Which country is the origin of chess?", "a": ["india"], "p": 3}
    ],

    "gd": [
        {"q": "Geometry Dash: How many stars to unlock 'Back on Track'?", "a": ["0"], "p": 1},
        {"q": "Geometry Dash: What is the name of the cube's default character?", "a": ["cube"], "p": 1},
        {"q": "Geometry Dash: Who created the game?", "a": ["robert topala", "topala"], "p": 2},
        {"q": "Geometry Dash: How many demons are in the main game?", "a": ["21"], "p": 2},
        {"q": "Geometry Dash: What is the fastest speed in practice mode?", "a": ["3x", "3"], "p": 2},
        {"q": "Geometry Dash: Name the song used in level 'Electroman Adventures'", "a": ["electroman adventures"], "p": 2},
        {"q": "Geometry Dash: How many coins per main level?", "a": ["3"], "p": 2},
        {"q": "Geometry Dash: Which level introduced the wave form?", "a": ["polargeist"], "p": 2},
        {"q": "Geometry Dash: What year was the game released?", "a": ["2013"], "p": 2},
        {"q": "Geometry Dash: Name the level with the song 'Clubstep'", "a": ["clubstep"], "p": 3},
        {"q": "Geometry Dash: How many attempts does practice mode allow?", "a": ["unlimited"], "p": 1},
        {"q": "Geometry Dash: What icon shape is unlocked after 10 stars?", "a": ["ship"], "p": 1}
    ],

    "minecraft": [
        {"q": "What do you use to mine stone?", "a": ["pickaxe"], "p": 1},
        {"q": "What material do you need to make a torch?", "a": ["coal", "stick"], "p": 1},
        {"q": "Which mob explodes?", "a": ["creeper"], "p": 1},
        {"q": "What do pigs drop when killed?", "a": ["porkchop"], "p": 1},
        {"q": "Which block can you use to make portals?", "a": ["obsidian"], "p": 1},
        {"q": "What do cows drop?", "a": ["beef", "milk"], "p": 1},
        {"q": "Which dimension has the Ender Dragon?", "a": ["end"], "p": 2},
        {"q": "What is the rarest ore in vanilla Minecraft?", "a": ["emerald"], "p": 2},
        {"q": "Which mob drops string?", "a": ["spider"], "p": 1},
        {"q": "What do you need to tame a wolf?", "a": ["bone"], "p": 1}
    ],

    "silent": [
        {"q": "Type the secret word: 'echo'", "a": ["echo"], "p": 1},
        {"q": "Type the hidden phrase: 'whisper'", "a": ["whisper"], "p": 1},
        {"q": "What is the silent key? 'quiet'", "a": ["quiet"], "p": 1},
        {"q": "Enter the password: 'mute'", "a": ["mute"], "p": 1},
        {"q": "Type the word that is invisible: 'ghost'", "a": ["ghost"], "p": 1}
    ]
}

@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
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
        msg_content = msg.content.lower().replace(" ", "")

        if any(a.lower().replace(" ", "") == msg_content for a in q["a"]):
            leveled = add_xp(msg.author.id, q["p"])

            save("scores.json", scores)
            save("levels.json", levels)

            await ctx.send(f"✅ {msg.author.mention} +{q['p']} XP")

            if leveled:
                await send_level_up(ctx, msg.author)

        else:
            await ctx.send("❌ Wrong.")

    except asyncio.TimeoutError:
        await ctx.send("⏱️ Time up.")

# ================= LEADERBOARDS =================
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def leaderboard(ctx):
    data = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    text = ""
    for i, (uid, pts) in enumerate(data, 1):
        user = await bot.fetch_user(int(uid))
        lvl = levels.get(uid, {}).get("level", 1)
        text += f"{i}. {user.name} — {pts} pts (Lv {lvl})\n"
    await ctx.send(embed=discord.Embed(title="🏆 Leaderboard", description=text, color=0x00ff00))

# ================= TEAMS =================
@bot.command()
async def team(ctx, color):
    color = color.lower()
    if color not in ["red", "blue"]:
        await ctx.send("You need to choose only red or blue 😎")
        return
    teams[str(ctx.author.id)] = color
    save("teams.json", teams)
    await ctx.send(f"{ctx.author.mention} Joined {color.upper()} 🔥")

@bot.command(name="team_leaderboard")
@commands.cooldown(1, 30, commands.BucketType.guild)
async def team_leaderboard(ctx):
    totals = {"red": 0, "blue": 0}
    for uid, t in teams.items():
        if t in totals:
            totals[t] += scores.get(uid, 0)
    await ctx.send(f"🔴 Red: {totals['red']}\n🔵 Blue: {totals['blue']}")

# ================= LIST =================

# ================= HELP COMMAND WITH PAGINATION =================
HELP_PAGES = [
    {
        "title": "🧰 Basic Commands - Page 1/10",
        "commands": [
            ("whoisstrongest", "Pick the strongest member randomly"),
            ("8ball <question>", "Ask the magic 8ball a question"),
            ("joke", "Get a random joke"),
            ("fact", "Get a random fact"),
            ("rate <thing>", "Rate something 1-10"),
            ("today", "Get current date and time"),
            ("cat", "Get a random cat image"),
            ("chaos", "Embrace the chaos!"),
        ]
    },
    {
        "title": "🧠 Trivia & Leveling - Page 2/10",
        "commands": [
            ("trivia [category]", "Play trivia! Categories: easy, medium, hard, gd, minecraft, silent"),
            ("leaderboard", "View top 10 players"),
            ("level", "Check your level and XP"),
            ("rank", "See the global ranking"),
            ("team red/blue", "Join a team"),
            ("team_leaderboard", "View team scores"),
        ]
    },
    {
        "title": "🎲 Chaos & Fun - Page 3/10",
        "commands": [
            ("coinflip", "Flip a coin"),
            ("rng <min> <max>", "Generate random number"),
            ("reverse <text>", "Reverse text"),
            ("scream", "SCREAM!!!"),
            ("uwu <text>", "Convert text to uwu speak"),
            ("dice [NdM]", "Roll dice (e.g., 2d6)"),
            ("choose <opt1>, <opt2>...", "Choose from options"),
            ("spam <times> <text>", "Spam a message (max 10)"),
        ]
    },
    {
        "title": "😄 Social Interactions - Page 4/10",
        "commands": [
            ("hug <member>", "Give someone a hug"),
            ("slap <member>", "Slap someone playfully"),
            ("kiss <member>", "Kiss someone"),
            ("pet <member>", "Pet someone"),
            ("bite <member>", "Bite someone"),
            ("scratch <member>", "Scratch someone"),
            ("yeet <member>", "YEET someone"),
            ("bonk <member>", "Bonk to horny jail"),
        ]
    },
    {
        "title": "🎭 Expressions & Emotes - Page 5/10",
        "commands": [
            ("hello [member]", "Say hello"),
            ("wave", "Wave at everyone"),
            ("cry", "Cry emoji"),
            ("happy", "Be happy"),
            ("angry", "Be angry"),
            ("sad", "Be sad"),
            ("confused", "Show confusion"),
            ("dance", "Dance with the bot"),
        ]
    },
    {
        "title": "🔥 Actions & Magic - Page 6/10",
        "commands": [
            ("love <member>", "Love someone"),
            ("hate <member>", "Dislike someone (jk)"),
            ("attack <member>", "Attack someone"),
            ("protect <member>", "Protect someone"),
            ("heal <member>", "Heal someone"),
            ("boost <member>", "Boost someone's stats"),
            ("curse <member>", "Curse someone"),
            ("bless <member>", "Bless someone"),
        ]
    },
    {
        "title": "✨ Text Manipulation - Page 7/10",
        "commands": [
            ("mock <text>", "Mock text (aLtErNaTiNg CaSe)"),
            ("clap <text>", "Add clap emojis between words"),
            ("emojify <text>", "Convert text to emoji"),
            ("ascii <text>", "Show ASCII values"),
            ("calc <expression>", "Calculate math expression"),
            ("hex <text>", "Convert to hex"),
            ("base64 <text>", "Encode to base64"),
            ("riddle", "Get a riddle"),
        ]
    },
    {
        "title": "⚔️ Games & Gambling - Page 8/10",
        "commands": [
            ("play quizbattle", "Quiz battle game"),
            ("play rapidfire", "Rapid fire yes/no questions"),
            ("play riddlehunt", "Solve a riddle"),
            ("play memorygrid", "Memory sequence game"),
            ("play wordlink", "Word linking game"),
            ("roulette", "Russian roulette (safe)"),
            ("gacha", "Gacha roll"),
            ("ship <user1> <user2>", "Ship two users"),
        ]
    },
    {
        "title": "🛡️ Moderation - Page 9/10",
        "commands": [
            ("warn <member> [reason]", "Warn a user"),
            ("mute <member> [minutes]", "Mute a user"),
            ("unmute <member>", "Unmute a user"),
            ("kick <member> [reason]", "Kick a user"),
            ("ban <member> [reason]", "Ban a user"),
            ("unban <user>", "Unban a user"),
            ("purge [count]", "Delete messages (max 100)"),
            ("slowmode [seconds]", "Set channel slowmode"),
        ]
    },
    {
        "title": "👑 Admin & Info - Page 10/10",
        "commands": [
            ("userinfo [member]", "Get user information"),
            ("serverinfo", "Get server information"),
            ("avatar [member]", "Show user avatar"),
            ("banner [member]", "Show user banner"),
            ("announce <message>", "Make announcement (owner)"),
            ("setprefix <prefix>", "Change bot prefix (owner)"),
            ("eval <code>", "Eval Python (owner)"),
            ("load <extension>", "Load a cog (owner)"),
        ]
    },
]

@bot.command(name="h")
@commands.cooldown(1, 5, commands.BucketType.user)
async def help_cmd(ctx):
    """Show paginated help with all commands."""
    current_page = 0
    
    def create_embed(page_num):
        page = HELP_PAGES[page_num]
        embed = discord.Embed(
            title=page["title"],
            color=0x5865F2,
            description="Use buttons below to navigate!"
        )
        
        for cmd, desc in page["commands"]:
            embed.add_field(name=f"❯ `!{cmd}`", value=desc, inline=False)
        
        embed.set_footer(text=f"Page {page_num + 1}/{len(HELP_PAGES)}")
        return embed
    
    # Create buttons
    from discord.ui import View, Button
    
    class HelpView(View):
        def __init__(self, ctx_user, initial_page):
            super().__init__(timeout=60)
            self.ctx_user = ctx_user
            self.current_page = initial_page
            self.message = None
        
        @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.blurple)
        async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.ctx_user:
                await interaction.response.defer()
                return
            
            self.current_page = (self.current_page - 1) % len(HELP_PAGES)
            await interaction.response.edit_message(embed=create_embed(self.current_page))
        
        @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.blurple)
        async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.ctx_user:
                await interaction.response.defer()
                return
            
            self.current_page = (self.current_page + 1) % len(HELP_PAGES)
            await interaction.response.edit_message(embed=create_embed(self.current_page))
        
        @discord.ui.button(label="🏠 Home", style=discord.ButtonStyle.success)
        async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.ctx_user:
                await interaction.response.defer()
                return
            
            self.current_page = 0
            await interaction.response.edit_message(embed=create_embed(self.current_page))
        
        @discord.ui.button(label="❌ Close", style=discord.ButtonStyle.danger)
        async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != self.ctx_user:
                await interaction.response.defer()
                return
            
            await interaction.response.defer()
            await self.message.delete()
            self.stop()
    
    view = HelpView(ctx.author, current_page)
    msg = await ctx.send(embed=create_embed(current_page), view=view)
    view.message = msg

# ================= CHAOS / FUN =================
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def chaos(ctx):
    await ctx.send(random.choice(["🔥 CHAOS 🔥", "💥 PANIC 💥", "😈 DOOM 😈"]))

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def coinflip(ctx):
    await ctx.send(random.choice(["🪙 Heads", "🪙 Tails"]))

@bot.command()
async def rng(ctx, min: int, max: int):
    if min > max:
        min, max = max, min
    await ctx.send(f"🎲 {random.randint(min, max)}")

@bot.command()
async def reverse(ctx, *, text):
    await ctx.send(text[::-1])

@bot.command()
async def scream(ctx):
    await ctx.send("AAAAAAAAAAHHHHHHHHHH 😱")

@bot.command()
async def uwu(ctx, *, text):
    text = text.replace("r", "w").replace("l", "w")
    await ctx.send(text + " uwu")


@bot.command()
async def dice(ctx, dice: str = "1d6"):
    """Roll dice in NdM format, e.g. 2d6 or d20"""
    try:
        if 'd' not in dice:
            raise ValueError
        parts = dice.lower().split('d')
        n = int(parts[0]) if parts[0] else 1
        sides = int(parts[1])
        if n < 1 or sides < 1 or n > 100:
            await ctx.send("❌ Invalid dice. Use something like `2d6` (max 100 dice).")
            return
        rolls = [random.randint(1, sides) for _ in range(n)]
        await ctx.send(f"🎲 Rolled {dice}: {rolls} -> **{sum(rolls)}**")
    except Exception:
        await ctx.send("❌ Usage: `!dice 2d6` or `!dice d20`")


@bot.command()
async def choose(ctx, *, choices: str):
    """Choose between comma-separated options."""
    opts = [c.strip() for c in choices.split(',') if c.strip()]
    if not opts:
        await ctx.send("❌ Provide choices separated by commas.")
        return
    await ctx.send(f"🎯 I choose: {random.choice(opts)}")


@bot.command()
async def meme(ctx):
    """Fetch a random meme from meme-api."""
    url = "https://meme-api.com/gimme"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as r:
                data = await r.json()
                title = data.get('title')
                post = data.get('postLink')
                img = data.get('url')
                if img:
                    await ctx.send(f"{title} - {post}", file=None)
                    await ctx.send(img)
                else:
                    await ctx.send("Couldn't fetch a meme right now.")
        except Exception:
            await ctx.send("Failed to fetch meme.")


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    """Show a user's avatar and send it as a downloadable file."""
    member = member or ctx.author
    avatar_url = member.display_avatar.url

    embed = discord.Embed(title=f"{member.display_name}'s Avatar")
    embed.set_image(url=avatar_url)
    embed.set_footer(text="Click image to open/download")
    await ctx.send(embed=embed)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar_url)) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    buf = io.BytesIO(data)
                    buf.seek(0)
                    filename = f"avatar_{member.id}.png"
                    await ctx.send(file=discord.File(buf, filename=filename))
    except Exception:
        pass


@bot.command()
async def banner(ctx, member: discord.Member = None):
    """Show a user's banner (if any) and send it as a downloadable file."""
    member = member or ctx.author
    try:
        user = await bot.fetch_user(member.id)
    except Exception:
        await ctx.send("❌ Could not fetch user data.")
        return

    banner = getattr(user, "banner", None)
    if not banner:
        await ctx.send("❌ This user has no banner.")
        return

    banner_url = banner.url
    embed = discord.Embed(title=f"{member.display_name}'s Banner")
    embed.set_image(url=banner_url)
    embed.set_footer(text="Click image to open/download")
    await ctx.send(embed=embed)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(str(banner_url)) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    buf = io.BytesIO(data)
                    buf.seek(0)
                    filename = f"banner_{member.id}.png"
                    await ctx.send(file=discord.File(buf, filename=filename))
    except Exception:
        pass


# ================= UTILITY COMMANDS =================
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info: {member.display_name}")
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Status", value=member.status)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server: {guild.name}")
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)



@bot.command()
async def time(ctx):
    now = datetime.now().strftime("%H:%M:%S")
    await ctx.send(f"🕐 Current Time: {now}")

@bot.command()
async def ascii(ctx, *, text: str):
    """Convert text to ASCII art (simple)."""
    lines = []
    for char in text[:10]:
        lines.append(f"`{char}` → `{ord(char)}`")
    await ctx.send("\n".join(lines))

@bot.command()
async def calc(ctx, *, expr: str):
    """Simple calculator."""
    try:
        result = eval(expr)
        await ctx.send(f"🧮 {expr} = **{result}**")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:100]}")

@bot.command()
async def hex(ctx, *, text: str):
    """Convert text to hex."""
    hex_str = text.encode().hex()
    await ctx.send(f"🔤 {text} → `{hex_str}`")

@bot.command()
async def base64(ctx, *, text: str):
    """Encode text to base64."""
    import base64
    encoded = base64.b64encode(text.encode()).decode()
    await ctx.send(f"📝 {text} → `{encoded}`")


# ================= FUN COMMANDS =================
@bot.command()
async def compliment(ctx, member: discord.Member = None):
    member = member or ctx.author
    compliments = [
        f"You're awesome, {member.mention}! 🌟",
        f"{member.mention}, you light up the room! 💫",
        f"{member.mention}, you're incredibly kind! 💖",
        f"Your energy is contagious, {member.mention}! ⚡",
        f"{member.mention}, you deserve good things! 🎁"
    ]
    await ctx.send(random.choice(compliments))

@bot.command()
async def pickup(ctx):
    """Send a pickup line."""
    lines = [
        "Do you believe in love at first sight, or should I walk by again?",
        "Are you a magician? Because whenever I look at you, everyone else disappears.",
        "Do you have a map? Because I just got lost in your eyes.",
        "Are you French? Because Eiffel for you.",
        "If you were a vegetable, you'd be a cute-cumber!"
    ]
    await ctx.send(f"💘 {random.choice(lines)}")

@bot.command()
async def dadjoke(ctx):
    """Tell a dad joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the claustrophobic astronaut? He just needed a little space.",
        "I'm reading a book on the history of glue – can't put it down!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a fake noodle? An impasta!"
    ]
    await ctx.send(f"😄 {random.choice(jokes)}")

@bot.command()
async def quote(ctx):
    """Send an inspiring quote."""
    quotes = [
        '"The only way to do great work is to love what you do." - Steve Jobs',
        '"Innovation distinguishes between a leader and a follower." - Steve Jobs',
        '"Life is what happens when you\'re busy making other plans." - John Lennon',
        '"The future belongs to those who believe in the beauty of their dreams." - Eleanor Roosevelt',
        '"It is during our darkest moments that we must focus to see the light." - Aristotle'
    ]
    await ctx.send(f"💭 {random.choice(quotes)}")

@bot.command()
async def pun(ctx):
    """Tell a pun."""
    puns = [
        "I'd tell you a chemistry joke, but I know I wouldn't get a reaction.",
        "Time flies like an arrow. Fruit flies like a banana.",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing.",
        "Parallel lines have so much in common. It's a shame they'll never meet."
    ]
    await ctx.send(f"🎭 {random.choice(puns)}")

@bot.command()
async def riddle(ctx):
    """Send a riddle."""
    riddles_list = [
        {"q": "I speak without a mouth and hear without ears. What am I?", "a": "echo"},
        {"q": "What has keys but can't open locks?", "a": "piano"},
        {"q": "What has hands but cannot clap?", "a": "clock"}
    ]
    r = random.choice(riddles_list)
    await ctx.send(f"🧩 Riddle: {r['q']}")

@bot.command()
async def fortune(ctx):
    """Get a fortune."""
    fortunes = [
        "A pleasant surprise is waiting for you.",
        "You will have good luck and abundant happiness.",
        "Adventure awaits you at the corner.",
        "Your talents will be recognized.",
        "A new perspective will bring you success."
    ]
    await ctx.send(f"🔮 {random.choice(fortunes)}")

@bot.command()
async def insultme(ctx):
    """Insult yourself (safely)."""
    insults = [
        f"{ctx.author.mention}, you're so lazy you need instructions to sleep!",
        f"{ctx.author.mention}, you're not stupid; you just have bad luck thinking!",
        f"If {ctx.author.mention} were a spice, you'd be cumin!",
        f"{ctx.author.mention}, you're proof that evolution can go backwards!"
    ]
    await ctx.send(random.choice(insults))

@bot.command()
async def flip(ctx):
    """Flip a coin with style."""
    result = random.choice(["🪙 Heads", "🪙 Tails"])
    await ctx.send(result)

@bot.command()
async def ship(ctx, user1: discord.Member, user2: discord.Member):
    """Ship two users."""
    percent = random.randint(1, 100)
    ship_name = user1.display_name[:len(user1.display_name)//2] + user2.display_name[len(user2.display_name)//2:]
    bar = "█" * (percent // 10) + "░" * (10 - percent // 10)
    await ctx.send(f"💕 {user1.mention} + {user2.mention}\nShip name: **{ship_name}**\nCompatibility: `{bar}` {percent}%")

@bot.command()
async def hug(ctx, member: discord.Member):
    """Hug someone."""
    await ctx.send(f"🤗 {ctx.author.mention} gives {member.mention} a warm hug!")

@bot.command()
async def slap(ctx, member: discord.Member):
    """Slap someone (playfully)."""
    await ctx.send(f"👋 {ctx.author.mention} slaps {member.mention}!")

@bot.command()
async def kiss(ctx, member: discord.Member):
    """Kiss someone (playfully)."""
    await ctx.send(f"💋 {ctx.author.mention} kisses {member.mention}!")

@bot.command()
async def dance(ctx):
    """Dance with the bot."""
    dances = ["💃", "🕺", "🪘", "🎵"]
    await ctx.send(f"{ctx.author.mention} {random.choice(dances)} Let's dance!")


# ================= CHAOS COMMANDS =================
@bot.command()
async def shrug(ctx):
    """Shrug."""
    await ctx.send("¯\\_(ツ)_/¯")

@bot.command()
async def tableflip(ctx):
    """Flip a table."""
    await ctx.send("(╯°□°)╯︵ ┻━┻")

@bot.command()
async def unflip(ctx):
    """Unflip a table."""
    await ctx.send("┬─┬ノ( º _ ºノ)")

@bot.command()
async def disapprove(ctx):
    """Show disapproval."""
    await ctx.send("ಠ_ಠ")

@bot.command()
async def mock(ctx, *, text: str):
    """Mock a text (alternating case)."""
    result = "".join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text)])
    await ctx.send(f"🤡 {result}")

@bot.command()
async def clap(ctx, *, text: str):
    """Add clap emojis between words."""
    result = " 👏 ".join(text.split())
    await ctx.send(f"👏 {result} 👏")

@bot.command()
async def emojify(ctx, *, text: str):
    """Convert text to emoji."""
    emoji_map = {'a': '🅰️', 'e': '🅴', 'i': 'ℹ️', 'o': '⭕', 'u': '🅤'}
    result = "".join([emoji_map.get(c.lower(), c) for c in text])
    await ctx.send(result)

@bot.command()
async def vibecheck(ctx, member: discord.Member = None):
    """Check someone's vibe."""
    member = member or ctx.author
    vibes = ["✨ Amazing vibes!", "😊 Good vibes!", "🤔 Neutral vibes...", "😤 Bad vibes...", "💀 Chaotic vibes!"]
    await ctx.send(f"{member.mention} {random.choice(vibes)}")

@bot.command()
async def spam(ctx, times: int = 1, *, text: str = "📢"):
    """Spam a message (max 10 times)."""
    if times > 10:
        times = 10
    for _ in range(times):
        await ctx.send(text)

@bot.command()
async def lmao(ctx):
    """Laugh."""
    laughs = ["LMAOOO 😂", "HAHAHAHA", "😆😆😆", "bro i'm dying 💀"]
    await ctx.send(random.choice(laughs))

@bot.command()
async def yeet(ctx, member: discord.Member = None):
    """YEET someone."""
    member = member or ctx.author
    await ctx.send(f"🚀 YEEEET {member.mention} 🚀")

@bot.command()
async def bonk(ctx, member: discord.Member = None):
    """Bonk someone."""
    member = member or ctx.author
    await ctx.send(f"🔨 BONK {member.mention} to horny jail!")

@bot.command()
async def simp(ctx, member: discord.Member = None):
    """Simp for someone."""
    member = member or ctx.author
    await ctx.send(f"🛎️ {ctx.author.mention} is simp-ing for {member.mention}!")

@bot.command()
async def roulette(ctx):
    """Russian roulette (always safe)."""
    if random.random() < 0.5:
        await ctx.send(f"🔫 *click* ... {ctx.author.mention} survives!")
    else:
        await ctx.send(f"💥 {ctx.author.mention} didn't make it...")

@bot.command()
async def gacha(ctx):
    """Gacha roll."""
    rarities = ["🌟 Common", "💙 Rare", "💜 Epic", "⭐ Legendary", "🌈 Mythic"]
    await ctx.send(f"🎲 You pulled: {random.choice(rarities)}!")

@bot.command()
async def highfive(ctx, member: discord.Member = None):
    """High five."""
    member = member or ctx.author
    await ctx.send(f"✋ {ctx.author.mention} high-fives {member.mention}!")

@bot.command()
async def pet(ctx, member: discord.Member = None):
    """Pet someone."""
    member = member or ctx.author
    await ctx.send(f"🐶 *pets {member.mention}*")

@bot.command()
async def bite(ctx, member: discord.Member = None):
    """Bite someone."""
    member = member or ctx.author
    await ctx.send(f"🧛 {ctx.author.mention} bites {member.mention}!")

@bot.command()
async def scratch(ctx, member: discord.Member = None):
    """Scratch someone."""
    member = member or ctx.author
    await ctx.send(f"🐱 {ctx.author.mention} scratches {member.mention}!")

@bot.command()
async def kill(ctx, member: discord.Member = None):
    """Playfully 'kill' someone."""
    member = member or ctx.author
    methods = ["with a fish", "with sarcasm", "with a stare", "with kindness"]
    await ctx.send(f"☠️ {ctx.author.mention} kills {member.mention} {random.choice(methods)}!")

@bot.command()
async def bye(ctx):
    """Say goodbye."""
    await ctx.send(f"👋 {ctx.author.mention} says goodbye!")

@bot.command()
async def hello(ctx, member: discord.Member = None):
    """Say hello."""
    member = member or ctx.author
    await ctx.send(f"👋 Hello {member.mention}!")

@bot.command()
async def wave(ctx):
    """Wave at everyone."""
    await ctx.send(f"👋 {ctx.author.mention} waves at everyone!")

@bot.command()
async def cry(ctx):
    """Cry."""
    await ctx.send(f"😭 {ctx.author.mention} is crying...")

@bot.command()
async def happy(ctx):
    """Be happy."""
    await ctx.send(f"😄 {ctx.author.mention} is happy!")

@bot.command()
async def angry(ctx):
    """Be angry."""
    await ctx.send(f"😠 {ctx.author.mention} is angry!")

@bot.command()
async def sad(ctx):
    """Be sad."""
    await ctx.send(f"😢 {ctx.author.mention} is sad...")

@bot.command()
async def confused(ctx):
    """Be confused."""
    await ctx.send(f"🤔 {ctx.author.mention} is confused!")

@bot.command()
async def love(ctx, member: discord.Member):
    """Love someone."""
    await ctx.send(f"❤️ {ctx.author.mention} loves {member.mention}!")

@bot.command()
async def hate(ctx, member: discord.Member):
    """Hate someone (playfully)."""
    await ctx.send(f"😠 {ctx.author.mention} hates {member.mention}! (jk)")

@bot.command()
async def bully(ctx, member: discord.Member):
    """Bully someone (playfully)."""
    await ctx.send(f"😤 {ctx.author.mention} bullies {member.mention}! (it's just jokes)")

@bot.command()
async def protect(ctx, member: discord.Member):
    """Protect someone."""
    await ctx.send(f"🛡️ {ctx.author.mention} protects {member.mention}!")

@bot.command()
async def attack(ctx, member: discord.Member):
    """Attack someone (playfully)."""
    await ctx.send(f"⚔️ {ctx.author.mention} attacks {member.mention}!")

@bot.command()
async def heal(ctx, member: discord.Member = None):
    """Heal someone."""
    member = member or ctx.author
    await ctx.send(f"💚 {ctx.author.mention} heals {member.mention}!")

@bot.command()
async def boost(ctx, member: discord.Member = None):
    """Boost someone's stats (roleplay)."""
    member = member or ctx.author
    stats = ["speed", "strength", "intelligence", "luck"]
    await ctx.send(f"⚡ {ctx.author.mention} boosts {member.mention}'s {random.choice(stats)}!")

@bot.command()
async def curse(ctx, member: discord.Member):
    """Curse someone (playfully)."""
    await ctx.send(f"🧙 {ctx.author.mention} curses {member.mention}!")

@bot.command()
async def bless(ctx, member: discord.Member):
    """Bless someone."""
    await ctx.send(f"😇 {ctx.author.mention} blesses {member.mention}!")

@bot.command()
async def slime(ctx, member: discord.Member):
    """Slime someone."""
    await ctx.send(f"💚 {ctx.author.mention} slimes {member.mention}!")

@bot.command()
async def fireblast(ctx, member: discord.Member):
    """Fire blast."""
    await ctx.send(f"🔥 {ctx.author.mention} shoots a fire blast at {member.mention}!")

@bot.command()
async def freeze(ctx, member: discord.Member):
    """Freeze someone."""
    await ctx.send(f"❄️ {ctx.author.mention} freezes {member.mention}!")

@bot.command()
async def shock(ctx, member: discord.Member):
    """Shock someone."""
    await ctx.send(f"⚡ {ctx.author.mention} shocks {member.mention}!")


# ================= MODERATION COMMANDS =================
@bot.command()
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason: str = "No reason"):
    """Warn a user."""
    await ctx.send(f"⚠️ {member.mention} has been warned. Reason: {reason}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: int = 5, *, reason: str = "No reason"):
    """Mute a user (in minutes)."""
    try:
        await member.timeout(discord.utils.utcnow() + asyncio.sleep(duration * 60), reason=reason)
        await ctx.send(f"🔇 {member.mention} has been muted for {duration} minutes. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:100]}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    """Unmute a user."""
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} has been unmuted.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:100]}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, count: int = 10):
    """Delete messages (max 100)."""
    if count > 100:
        count = 100
    deleted = await ctx.channel.purge(limit=count)
    await ctx.send(f"🗑️ Deleted {len(deleted)} messages.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    """Lock the channel."""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel locked!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    """Unlock the channel."""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel unlocked!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, seconds: int = 0):
    """Set slowmode."""
    await ctx.channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await ctx.send("⚡ Slowmode disabled.")
    else:
        await ctx.send(f"⏱️ Slowmode set to {seconds} seconds.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "No reason"):
    """Ban a user."""
    try:
        await member.ban(reason=reason)
        await ctx.send(f"❌ {member.mention} has been banned. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:100]}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "No reason"):
    """Kick a user."""
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} has been kicked. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:100]}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
    """Unban a user."""
    try:
        await ctx.guild.unban(user)
        await ctx.send(f"✅ {user.mention} has been unbanned.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:100]}")


# ================= ADMIN COMMANDS =================
@bot.command()
@commands.is_owner()
async def announce(ctx, *, message: str):
    """Make an announcement (owner only)."""
    embed = discord.Embed(title="📢 Announcement", description=message, color=0xff9900)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def setprefix(ctx, prefix: str):
    """Change bot prefix (owner only)."""
    bot.command_prefix = prefix
    await ctx.send(f"✅ Prefix changed to: `{prefix}`")

@bot.command()
@commands.is_owner()
async def eval(ctx, *, code: str):
    """Evaluate Python code (owner only) - USE WITH CAUTION."""
    try:
        result = eval(code)
        await ctx.send(f"```\n{result}\n```")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:200]}")

@bot.command()
@commands.is_owner()
async def load(ctx, extension: str):
    """Load a cog (owner only)."""
    try:
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"✅ Loaded {extension}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)[:100]}")


# ================= GAMES =================
# --------- All Games ---------
play_commands = [
    # Knowledge / Logic
    "quizbattle", "rapidfire", "riddlehunt", "memorygrid", "wordlink",
    "factstorm", "logicduel", "codebreak",

    # Competitive
    "capturecore", "laststand", "arena", "tagrun", "dodgeball",
    "snipershot", "timeduel",

    # Co-op / Unity
    "buildrush", "puzzlelock", "bridgecraft", "relayquest", "syncmove",
    "rescueops", "supplychain",

    # Creative
    "drawguess", "storychain", "emoteplay", "buildstatue", "skincontest",
    "musicmatch",

    # Skill / Speed
    "parkourrace", "mazerun", "aimtrial", "reflex", "obstacleloop",
    "timelock",

    # Strategy
    "territory", "resourcewar", "towerdef", "chesslite", "cardclash",
    "roleplayops",

    # Social / Party
    "votemystery", "truthortrap", "guesswho", "liarscore", "speedvote",

    # Events / Exploration
    "scavenger", "worldevent", "bossraid", "timedexpedition", "checkpoint",

    # Quick / Extra Fun
    "coinrush", "reactionchain", "colorclaim", "patternmatch", "shadowtag",
    "flagshift", "numbergrid", "echoquiz", "survivalscore", "challengewheel"
]

# ----------------- Sample Data -----------------
trivia_questions = [
    {"question": "Capital of France?", "answer": "paris"},
    {"question": "2 + 2 * 2 = ?", "answer": "6"},
    {"question": "Closest planet to Sun?", "answer": "mercury"}
]

yesno_questions = [
    {"question": "Is sky blue?", "answer": "yes"},
    {"question": "Is 5 a prime number?", "answer": "yes"},
    {"question": "Is water dry?", "answer": "no"}
]

riddles = [
    {"question": "I speak without a mouth and hear without ears. What am I?", "answer": "echo"},
    {"question": "What has keys but can't open locks?", "answer": "piano"},
    {"question": "What has hands but cannot clap?", "answer": "clock"}
]

memory_sequences = ["123", "5482", "76931", "246813"]
wordlink_words = ["apple", "elephant", "tiger", "rabbit", "tree", "ear", "rose"]

# ----------------- PLAY COMMAND -----------------
@bot.command(name="play")
async def play(ctx, game: str):
    game = game.lower()

    if game not in play_commands:
        await ctx.send(f"❌ Unknown game `{game}`. Available: {', '.join(play_commands)}")
        return

    # ----------------- Knowledge / Logic -----------------
    if game in ["quizbattle", "factstorm", "logicduel", "codebreak"]:
        q = random.choice(trivia_questions)
        await ctx.send(f"🎮 **{game.title()}**: {q['question']}")
        try:
            msg = await bot.wait_for("message", timeout=20.0,
                                     check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            if msg.content.lower() == q["answer"]:
                await ctx.send("✅ Correct!")
            else:
                await ctx.send(f"❌ Wrong! Answer: `{q['answer']}`")
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Time's up! Answer: `{q['answer']}`")

    elif game == "rapidfire":
        score = 0
        await ctx.send(f"🎮 **Rapid Fire**: 3 yes/no questions!")
        for i in range(3):
            q = random.choice(yesno_questions)
            await ctx.send(f"Q{i+1}: {q['question']}")
            try:
                msg = await bot.wait_for("message", timeout=5.0,
                                         check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                if msg.content.lower() == q["answer"]:
                    score += 1
                    await ctx.send("✅ Correct!")
                else:
                    await ctx.send(f"❌ Wrong! Answer: `{q['answer']}`")
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Time's up! Answer: `{q['answer']}`")
        await ctx.send(f"🏆 Score: {score}/3")

    elif game == "riddlehunt":
        q = random.choice(riddles)
        await ctx.send(f"🎮 **Riddle Hunt**: {q['question']}")
        try:
            msg = await bot.wait_for("message", timeout=20.0,
                                     check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            if msg.content.lower() == q["answer"]:
                await ctx.send("✅ Correct!")
            else:
                await ctx.send(f"❌ Wrong! Answer: `{q['answer']}`")
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Time's up! Answer: `{q['answer']}`")

    elif game == "memorygrid":
        seq = random.choice(memory_sequences)
        await ctx.send(f"🎮 **Memory Grid**: Remember `{seq}` (10s)")
        await asyncio.sleep(10)
        await ctx.send("Now type the sequence!")
        try:
            msg = await bot.wait_for("message", timeout=15.0,
                                     check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            if msg.content == seq:
                await ctx.send("✅ Correct!")
            else:
                await ctx.send(f"❌ Wrong! It was `{seq}`")
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Time's up! It was `{seq}`")

    elif game == "wordlink":
        word = random.choice(wordlink_words)
        await ctx.send(f"🎮 **Word Link**: Start with `{word}` (next word must start with `{word[-1]}`)")
        try:
            msg = await bot.wait_for("message", timeout=15.0,
                                     check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            if msg.content.lower().startswith(word[-1]):
                await ctx.send("✅ Good link!")
            else:
                await ctx.send(f"❌ Wrong. Must start with `{word[-1]}`")
        except asyncio.TimeoutError:
            await ctx.send("⏰ Time's up!")

    # ----------------- Competitive / Co-op / Creative / Skill / Strategy / Social / Events / Fun -----------------
    else:
        # Generate a simple random outcome for the remaining 60+ games
        result = random.choice([
            "🎉 You won!", "💥 You lost!", "🤝 Success!", "❌ Failed!", "🏆 Victory!", "😢 Defeat!",
            "✨ Great job!", "⚡ Try again!"
        ])
        await ctx.send(f"🎮 **{game.title()}**: {result}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"⏳ Slow down! Try again in **{error.retry_after:.1f}** seconds."
        )
    else:
        raise error

@bot.command()
async def gen(ctx, service: str):
    service = service.lower()

    fake_services = [
        "mcfa", "vvs", "crunchyroll",
        "netflix", "spotify", "nitro",
        "roblox", "minecraft", "GD", "OnlyFans", "Twitch", "Fortnite",
    ]

    if service not in fake_services:
        await ctx.send("❌ Unknown generator.")
        return

    embed = discord.Embed(
        title=f"🎁 {service.upper()} Generator",
        description="**Heres your free reward: Ummm. The bot did not responded.**",
        color=0xff0000
    )
    embed.set_footer(text="Nice try.")

    try:
        await ctx.author.send(embed=embed)
        await ctx.send("📬 Check your DMs.")
    except discord.Forbidden:
        await ctx.send("❌ I can’t DM you. Enable DMs first.")

# ================= COLOR ROLES =================
# Format: (emoji, label, role_id)
COLOR_ROLES = [
    ("🔵", "Blue", 1460979432637337787),
    ("🔴", "Red", 1460978993045045365),
    ("🟢", "Green", 1460979598236844137),
    ("🟡", "Yellow", 1460979681648971808),
    ("🟣", "Purple", 1460979512111009943),
    ("🟠", "Orange", 1460046616550576198),
    ("🟤", "Brown", 1460047171591344188),
    ("⚫", "Black", 1460249184916475965),
    ("⚪", "White", 1460249043895844987),
    ("💙", "Light Blue", 1460248804157816957),
    ("💛", "Light Yellow", 1460246776203317289),
    ("💜", "Light Purple", 1460246873892847821)
]

# ================= SEND WELCOME EMBED ==================
@bot.command()
async def welcome(ctx):
    embed = discord.Embed(
        title="🔷 Welcome 🔷",
        description="🌌 **Welcome, User!**\n\n🎨 Choose a Role/Color and make this place yours.\n⚡ Clean • 🌊 Cool • 🧊 Blue vibes only.",
        color=0x3498db  # CHANGE EMBED COLOR HERE
    )
    embed.set_footer(text="Pick wisely 🔵")

    # CREATE BUTTONS
    from discord.ui import ActionRow, Button

    rows = []
    row = ActionRow()
    for i, (emoji, label, role_id) in enumerate(COLOR_ROLES):
        button = Button(style=discord.ButtonStyle.primary, label=label, emoji=emoji, custom_id=f"role_{role_id}")
        row.add_item(button)
        # Discord allows max 5 buttons per row
        if (i+1) % 5 == 0:
            rows.append(row)
            row = ActionRow()
    if len(row.children) > 0:
        rows.append(row)

# ================= BUTTON HANDLER ==================
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data.get("custom_id")
    if not custom_id or not custom_id.startswith("role_"):
        return

    new_role_id = int(custom_id.replace("role_", ""))
    member = interaction.user
    guild = interaction.guild
    if not guild:
        return

    role_to_add = guild.get_role(new_role_id)
    if not role_to_add:
        await interaction.response.send_message("❌ Role not found.", ephemeral=True)
        return

    # REMOVE ALL OTHER COLOR ROLES
    roles_to_remove = [guild.get_role(rid) for (_, _, rid) in COLOR_ROLES if rid != new_role_id and guild.get_role(rid) in member.roles]
    if roles_to_remove:
        await member.remove_roles(*roles_to_remove)

    # TOGGLE THE SELECTED ROLE
    if role_to_add in member.roles:
        await member.remove_roles(role_to_add)
        await interaction.response.send_message(f"❌ Removed **{role_to_add.name}**", ephemeral=True)
    else:
        await member.add_roles(role_to_add)
        await interaction.response.send_message(f"✅ Assigned **{role_to_add.name}**", ephemeral=True)
 
 # ================= LEVEL SYSTEM =================

def xp_needed(level: int) -> int:
    return 10 * (level ** 2) + 10


def add_xp(uid: int, amount: int):
    uid = str(uid)
    levels.setdefault(uid, {"level": 1, "xp": 0})

    levels[uid]["xp"] += amount
    leveled_up = False

    while levels[uid]["xp"] >= xp_needed(levels[uid]["level"]):
        levels[uid]["xp"] -= xp_needed(levels[uid]["level"])
        levels[uid]["level"] += 1
        leveled_up = True

    save("levels.json", levels)
    return leveled_up

async def send_level_up(ctx, member):
    data = levels[str(member.id)]

    embed = discord.Embed(
        title="🎉 LEVEL UP!",
        description=(
            f"🔥 **{member.display_name}** reached a new level!\n\n"
            f"🏆 **Level:** `{data['level']}`\n"
            f"⚡ XP to next: `{xp_needed(data['level']) - data['xp']}`"
        ),
        color=discord.Color.gold()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="XP System • Progress Saved")

    await ctx.send(embed=embed)

@bot.command()
async def level(ctx):
    uid = str(ctx.author.id)
    levels.setdefault(uid, {"level": 1, "xp": 0})

    data = levels[uid]
    needed = xp_needed(data["level"])

    embed = discord.Embed(
        title="📊 Your Level",
        description=(
            f"👤 **User:** {ctx.author.mention}\n"
            f"🏆 **Level:** `{data['level']}`\n"
            f"⚡ **XP:** `{data['xp']} / {needed}`"
        ),
        color=0x5865F2
    )

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def rank(ctx):
    uid = str(ctx.author.id)
    levels.setdefault(uid, {"level": 1, "xp": 0})

    # Sort users by level then XP
    sorted_users = sorted(
        levels.items(),
        key=lambda x: (x[1]["level"], x[1]["xp"]),
        reverse=True
    )

    rank_pos = next(i for i, (u, _) in enumerate(sorted_users, 1) if u == uid)

    top10 = sorted_users[:10]
    leaderboard = ""

    for i, (u, data) in enumerate(top10, 1):
        user = await bot.fetch_user(int(u))
        leaderboard += f"**#{i}** {user.name} — Lv `{data['level']}` ({data['xp']} XP)\n"

    me = levels[uid]

    embed = discord.Embed(
        title="🏆 XP Leaderboard",
        description=leaderboard,
        color=discord.Color.green()
    )

    embed.add_field(
        name="📌 Your Rank",
        value=(
            f"👤 {ctx.author.mention}\n"
            f"🏅 **Rank:** `#{rank_pos}`\n"
            f"🏆 **Level:** `{me['level']}`\n"
            f"⚡ **XP:** `{me['xp']} / {xp_needed(me['level'])}`"
        ),
        inline=False
    )

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text="Top 10 Global Ranking")

    await ctx.send(embed=embed)

# ================= RUN BOT =================
cfg = load_json("config.json")
token = os.environ.get("DISCORD_TOKEN") or cfg.get("token")
if not token:
    print("ERROR: No Discord token found. Set DISCORD_TOKEN environment variable or add token to config.json")
else:
    bot.run(token)