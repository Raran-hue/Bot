import json
import asyncio
import os
import discord
import random
from discord.ext import commands
from datetime import datetime
import aiohttp

# ================= BOT SETUP =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ================= UTIL =================
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

# ================= ON READY =================
@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")
    await bot.change_presence(activity=discord.Game("!list"))

# ================= BASIC COMMANDS =================
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="whoisstrongest")
@commands.cooldown(1, 10, commands.BucketType.guild)
async def who_is_strongest(ctx):
    members = [m for m in ctx.guild.members if not m.bot]
    await ctx.send(f"💪 {random.choice(members).mention}")

@bot.command(name="8ball")
@commands.cooldown(1, 5, commands.BucketType.user)
async def eight_ball(ctx, *, question: str):
    responses = [
        "Yes!", "No!", "Maybe...", "Definitely!",
        "Ask again later.", "Absolutely!", "Impossible!"
    ]
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
        "Bananas are berries."
    ]))

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def roast(ctx, member: discord.Member):
    await ctx.send(f"{member.mention} {random.choice(['You tried.', 'Skill issue.', 'Evolution paused.'])}")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def rate(ctx, *, thing: str):
    await ctx.send(f"{thing}: {random.randint(1,10)}/10")

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
    {"q": "What is 15 + 27?", "a": ["42"], "p": 2},
    {"q": "Which country has the largest population?", "a": ["china"], "p": 2},
    {"q": "Which instrument has black and white keys?", "a": ["piano"], "p": 2},
    {"q": "What is the smallest prime number?", "a": ["2"], "p": 2},
    {"q": "Which language has the most native speakers?", "a": ["mandarin", "chinese"], "p": 2},
    {"q": "Who discovered gravity?", "a": ["newton", "isaac newton"], "p": 2},
    {"q": "Which organ pumps blood?", "a": ["heart"], "p": 2},
    {"q": "What is 12 × 8?", "a": ["96"], "p": 2},
    {"q": "Which continent is Egypt in?", "a": ["africa"], "p": 2},
    {"q": "Which metal is liquid at room temperature?", "a": ["mercury"], "p": 2},
    {"q": "What is 50 ÷ 5?", "a": ["10"], "p": 2},
    {"q": "Who was the first man on the moon?", "a": ["neil armstrong"], "p": 2},
    {"q": "Which planet is closest to the Sun?", "a": ["mercury"], "p": 2},
    {"q": "What is the chemical symbol for Iron?", "a": ["fe"], "p": 2},
    {"q": "Which continent is Australia?", "a": ["australia"], "p": 2},
    {"q": "Who wrote '1984'?", "a": ["george orwell"], "p": 2},
    {"q": "Which country is known for maple syrup?", "a": ["canada"], "p": 2},
    {"q": "Which gas do humans breathe in?", "a": ["oxygen"], "p": 2},
    {"q": "How many bones are in the adult human body?", "a": ["206"], "p": 2},
    {"q": "What is 7 × 9?", "a": ["63"], "p": 2},
    {"q": "Which country is famous for sushi?", "a": ["japan"], "p": 2},
    {"q": "Which ocean is on the west coast of the USA?", "a": ["pacific"], "p": 2},
    {"q": "What is the largest mammal?", "a": ["blue whale"], "p": 2},
    {"q": "What is the square root of 144?", "a": ["12"], "p": 2},
    {"q": "Who painted the Starry Night?", "a": ["van gogh", "vincent van gogh"], "p": 2},
    {"q": "What is the largest desert in the world?", "a": ["sahara"], "p": 2},
    {"q": "Which animal is known as the king of the jungle?", "a": ["lion"], "p": 2},
    {"q": "What is 100 ÷ 4?", "a": ["25"], "p": 2},
    {"q": "Which planet has rings?", "a": ["saturn"], "p": 2},
    {"q": "What is 9 × 9?", "a": ["81"], "p": 2},
    {"q": "Which fruit is tropical and spiky?", "a": ["pineapple"], "p": 2},
    {"q": "Which continent has the most countries?", "a": ["africa"], "p": 2},
    {"q": "Who is known as the Father of Computers?", "a": ["charles babbage"], "p": 2},
    {"q": "Which animal lays eggs?", "a": ["chicken"], "p": 2},
    {"q": "What is the main gas in the air we breathe?", "a": ["nitrogen"], "p": 2},
    {"q": "What is 36 ÷ 6?", "a": ["6"], "p": 2},
    {"q": "Which organ is responsible for filtering blood?", "a": ["kidney"], "p": 2},
    {"q": "Which planet is known as the Earth’s twin?", "a": ["venus"], "p": 2},
    {"q": "Who wrote 'Harry Potter'?", "a": ["j.k. rowling", "jk rowling"], "p": 2},
    {"q": "Which animal is the largest land animal?", "a": ["elephant"], "p": 2}
],
    "hard": [
    {"q": "Chemical symbol for Gold?", "a": ["au"], "p": 3},
    {"q": "Square root of 144?", "a": ["12"], "p": 3},
    {"q": "What is 25 x 4?", "a": ["100"], "p": 3},
    {"q": "What is 81 ÷ 9?", "a": ["9"], "p": 3},
    {"q": "What is the capital of Japan?", "a": ["tokyo"], "p": 3},
    {"q": "Which element has the symbol 'Na'?", "a": ["sodium"], "p": 3},
    {"q": "How many bones are in the human body?", "a": ["206"], "p": 3},
    {"q": "What is the boiling point of water in Celsius?", "a": ["100"], "p": 3},
    {"q": "Which planet is known as the Morning Star?", "a": ["venus"], "p": 3},
    {"q": "What is 15 squared?", "a": ["225"], "p": 3},
    {"q": "Who developed the theory of relativity?", "a": ["einstein", "albert einstein"], "p": 3},
    {"q": "What is the chemical formula for table salt?", "a": ["nacl"], "p": 3},
    {"q": "Which country is known as the Land of the Rising Sun?", "a": ["japan"], "p": 3},
    {"q": "Who wrote '1984'?", "a": ["george orwell"], "p": 3},
    {"q": "What is 9 cubed?", "a": ["729"], "p": 3},
    {"q": "What is the largest internal organ in the human body?", "a": ["liver"], "p": 3},
    {"q": "Which planet has the shortest day?", "a": ["jupiter"], "p": 3},
    {"q": "Who painted 'Starry Night'?", "a": ["van gogh", "vincent van gogh"], "p": 3},
    {"q": "What is the hardest natural substance?", "a": ["diamond"], "p": 3},
    {"q": "What is the currency of the UK?", "a": ["pound"], "p": 3},
    {"q": "Which ocean is Bermuda located in?", "a": ["atlantic"], "p": 3},
    {"q": "What is 7 factorial (7!)?", "a": ["5040"], "p": 3},
    {"q": "What is the capital of Canada?", "a": ["ottawa"], "p": 3},
    {"q": "Which metal is liquid at room temperature?", "a": ["mercury"], "p": 3},
    {"q": "Which scientist discovered penicillin?", "a": ["alexander fleming"], "p": 3},
    {"q": "Which country has the most pyramids?", "a": ["sudan"], "p": 3},
    {"q": "Who is known as the father of computers?", "a": ["charles babbage"], "p": 3},
    {"q": "Which gas is most abundant in Earth's atmosphere?", "a": ["nitrogen"], "p": 3},
    {"q": "Which planet is called the Blue Planet?", "a": ["earth"], "p": 3},
    {"q": "What is 0 factorial (0!)?", "a": ["1"], "p": 3},
    {"q": "Which blood type is universal donor?", "a": ["o negative", "o-"], "p": 3},
    {"q": "Who painted the Sistine Chapel ceiling?", "a": ["michelangelo"], "p": 3},
    {"q": "Which country has the longest coastline?", "a": ["canada"], "p": 3},
    {"q": "What is the smallest prime number?", "a": ["2"], "p": 3},
    {"q": "Which chemical element has atomic number 1?", "a": ["hydrogen"], "p": 3},
    {"q": "Which planet is the hottest in the solar system?", "a": ["venus"], "p": 3},
    {"q": "What is the distance light travels in one year called?", "a": ["light year", "lightyear"], "p": 3},
    {"q": "What is the speed of sound in air (approx m/s)?", "a": ["343"], "p": 3},
    {"q": "Which country invented paper?", "a": ["china"], "p": 3},
    {"q": "Which organ filters blood in the human body?", "a": ["kidney"], "p": 3},
    {"q": "Which planet has the most moons?", "a": ["saturn"], "p": 3},
    {"q": "What is the cube root of 125?", "a": ["5"], "p": 3},
    {"q": "Who formulated the laws of motion?", "a": ["newton", "isaac newton"], "p": 3},
    {"q": "Which vitamin is produced when skin is exposed to sunlight?", "a": ["vitamin d"], "p": 3},
    {"q": "Which element is used in pencils?", "a": ["carbon", "graphite"], "p": 3},
    {"q": "Which gas do humans exhale?", "a": ["carbon dioxide", "co2"], "p": 3},
    {"q": "Which continent has the least population?", "a": ["antarctica"], "p": 3},
    {"q": "Which number is the smallest two-digit prime?", "a": ["11"], "p": 3},
    {"q": "What is the largest planet in our solar system?", "a": ["jupiter"], "p": 3},
    {"q": "Which planet is known as Earth's twin?", "a": ["venus"], "p": 3},
    {"q": "Which metal is used for wires due to conductivity?", "a": ["copper"], "p": 3}
],
    "gd": [
    {"q": "Who created Geometry Dash?", "a": ["robtop"], "p": 3},
    {"q": "Hardest official GD level?", "a": ["deadlocked"], "p": 3},
    {"q": "Whats the first demon in gd (official)?", "a": ["clubstep"], "p": 3},
    {"q": "What is the default character in GD?", "a": ["cube"], "p": 3},
    {"q": "Which GD level is known as the hardest Demon?", "a": ["ts2", "thinking space 2", "thinking space ii"], "p": 3},
    {"q": "Which GD update added the spider?", "a": ["2.1"], "p": 3},
    {"q": "What is the in-game currency in GD?", "a": ["orbs", "orb"], "p": 3},
    {"q": "Whats the first level that featured breakable blocks?", "a": ["electroman", "electroman adventures", "clubstep"], "p": 3},
    {"q": "What does UFO Gamemode do?", "a": ["Flies", "Fly"], "p": 3},
    {"q": "Which is the first level to introduce orbs?", "a": ["polargeist"], "p": 3},
    {"q": "Which GD update added orbs?", "a": ["1.0"], "p": 3},
    {"q": "Which level is a daily challenge in GD?", "a": ["daily level", "daily"], "p": 3},
    {"q": "Who is the creator of Clubstep?", "a": ["robtop"], "p": 3},
    {"q": "Which GD object allows gravity flipping?", "a": ["portal"], "p": 3},
    {"q": "Which level is known for speed changes?", "a": ["electrodynamix"], "p": 3},
    {"q": "Whats the first two gamemodes in gd?", "a": ["cube and ship", "cube & ship", "cube, ship"], "p": 3},
    {"q": "Do you respect Andromedas exposing? (if you dont know, he came back to gd legit years ago)", "a": ["Yes", "no"], "p": 3},
    {"q": "Which update added the wave gamemode?", "a": ["1.9"], "p": 3},
    {"q": "Which level uses the mini-cube mechanic?", "a": ["clutterfunk"], "p": 3},
    {"q": "Which GD level has multiple Blindjumps?", "a": ["time machine"], "p": 3},
    {"q": "What level introduced ufo gamemode?", "a": ["Theory of everything", "TOE"], "p": 3},
    {"q": "Which GD update added spider?", "a": ["2.1"], "p": 3},
    {"q": "Note most famous riots works.", "a": ["bloodbath", "quantum processing"], "p": 3},
    {"q": "Which GD feature allows double jumps?", "a": ["Orbs"], "p": 3},
    {"q": "Which level has extreme gravity flips?", "a": ["deadlocked"], "p": 3},
    {"q": "Whats the first gd level?", "a": ["stereo madness"], "p": 3},
    {"q": "What level do you find in vault of secrets?", "a": ["the challenge"], "p": 3},
    {"q": "ORBIT JUMPSCARE!!!", "a": ["AAH", "AAAH", "AAAAH", "AAAAAH", "Wtf is orbit?"], "p": 3},
    {"q": "Which level is the easiest Demon?", "a": ["the nightmare"], "p": 3},
    {"q": "Which level uses dual portals?", "a": ["hexagon force"], "p": 3},
    {"q": "Which level is famous for memory challenge?", "a": ["LIMBO"], "p": 3},
    {"q": "Did zonk fluked orbit from 43 or 34?", "a": ["43"], "p": 3},
    {"q": "When did triggers were added?", "a": ["2.0"], "p": 3},
    {"q": "Which level is the most downloaded?", "a": ["Outerspace"], "p": 3},
    {"q": "Which level has first UFO?", "a": ["theory of everything", "toe"], "p": 3},
    {"q": "Which level features mini cube?", "a": ["clutterfunk"], "p": 3},
    {"q": "Which GD feature flips gravity?", "a": ["portal"], "p": 3}
],
    "minecraft": [
    {"q": "End boss?", "a": ["ender dragon", "enderdragon"], "p": 3},
    {"q": "Strongest block?", "a": ["bedrock"], "p": 3},
    {"q": "Crafting table uses how many wood planks?", "a": ["4"], "p": 3},
    {"q": "How do you tame a wolf?", "a": ["bone"], "p": 3},
    {"q": "What is the Nether portal made of?", "a": ["obsidian"], "p": 3},
    {"q": "Which mob explodes?", "a": ["creeper"], "p": 3},
    {"q": "Which ore gives diamonds?", "a": ["diamond ore"], "p": 3},
    {"q": "What animal drops leather?", "a": ["cow"], "p": 3},
    {"q": "How do you breed cows?", "a": ["wheat"], "p": 3},
    {"q": "Which mob shoots fireballs?", "a": ["blaze"], "p": 3},
    {"q": "What do you need to make TNT?", "a": ["gunpowder", "sand"], "p": 3},
    {"q": "How many blocks high is a full Nether fortress?", "a": ["6"], "p": 3},
    {"q": "Which mob drops ender pearls?", "a": ["enderman"], "p": 3},
    {"q": "What item lights a Nether portal?", "a": ["flint and steel"], "p": 3},
    {"q": "Which biome is covered in ice?", "a": ["ice plains", "snowy tundra"], "p": 3},
    {"q": "Which potion gives underwater breathing?", "a": ["water breathing"], "p": 3},
    {"q": "Which mob gives gunpowder?", "a": ["creeper", "ghast"], "p": 3},
    {"q": "Which mob explodes with a fuse?", "a": ["creeper"], "p": 3},
    {"q": "Which item is used to feed horses?", "a": ["sugar", "apple", "wheat"], "p": 3},
    {"q": "How do you cure zombie villagers?", "a": ["potion of weakness", "golden apple"], "p": 3},
    {"q": "Which tool breaks stone the fastest?", "a": ["pickaxe"], "p": 3},
    {"q": "Which mob drops feathers?", "a": ["chicken"], "p": 3},
    {"q": "Which block is transparent?", "a": ["glass"], "p": 3},
    {"q": "Which item can smelt ores?", "a": ["furnace"], "p": 3},
    {"q": "Which mob explodes into many tiny pieces?", "a": ["silverfish"], "p": 3},
    {"q": "Which mob drops string?", "a": ["spider"], "p": 3},
    {"q": "Which biome has giant mushrooms?", "a": ["mushroom island"], "p": 3},
    {"q": "Which ore is purple?", "a": ["amethyst"], "p": 3},
    {"q": "Which mob is neutral until provoked?", "a": ["piglin"], "p": 3},
    {"q": "Which block lets you float upwards with soul sand?", "a": ["soul sand"], "p": 3},
    {"q": "Which mob drops blaze rods?", "a": ["blaze"], "p": 3},
    {"q": "Which mob drops rotten flesh?", "a": ["zombie"], "p": 3},
    {"q": "Which potion gives invisibility?", "a": ["invisibility"], "p": 3},
    {"q": "Which mob can teleport?", "a": ["enderman"], "p": 3},
    {"q": "Which block prevents Enderman from picking it up?", "a": ["pumpkin"], "p": 3},
    {"q": "Which biome has large cacti?", "a": ["desert"], "p": 3},
    {"q": "Which food restores the most hunger?", "a": ["steak", "porkchop"], "p": 3},
    {"q": "Which mob drops gunpowder and can fly?", "a": ["ghast"], "p": 3},
    {"q": "Which block is indestructible in survival?", "a": ["bedrock"], "p": 3},
    {"q": "Which item is used to cure a zombie villager?", "a": ["golden apple"], "p": 3},
    {"q": "Which item is needed to make a map?", "a": ["compass"], "p": 3},
    {"q": "Which mob drops experience when killed?", "a": ["all mobs"], "p": 3},
    {"q": "Which mob spawns in dark caves and drops bones?", "a": ["skeleton"], "p": 3},
    {"q": "Which block allows redstone circuits?", "a": ["redstone dust"], "p": 3},
    {"q": "Which mob can be tamed with bones?", "a": ["wolf"], "p": 3},
    {"q": "Which mob explodes underwater in Bedrock?", "a": ["creeper"], "p": 3},
    {"q": "Which mob shoots arrows?", "a": ["skeleton"], "p": 3},
    {"q": "Which biome is covered in sand?", "a": ["desert"], "p": 3},
    {"q": "Which mob turns hostile when struck by lightning?", "a": ["villager -> witch"], "p": 3},
    {"q": "Which block is used to make potions?", "a": ["brewing stand"], "p": 3},
    {"q": "Which mob is passive and drops milk?", "a": ["cow"], "p": 3}
],
    "silent": [
    {"q": "What exists before existence?", "a": ["nothing", "void"], "p": 6},
    {"q": "What is the answer when no question exists?", "a": ["nothing", "silence"], "p": 6},
    {"q": "What number comes after infinity?", "a": ["none", "nothing"], "p": 6},
    {"q": "Can a thought exist without a thinker?", "a": ["yes", "no"], "p": 6},
    {"q": "What is heavier: a kilogram of air or a kilogram of stone?", "a": ["they are equal", "equal"], "p": 6},
    {"q": "If time stops, what moves?", "a": ["nothing", "time"], "p": 6},
    {"q": "What is the sound of one hand clapping?", "a": ["silence"], "p": 6},
    {"q": "Can you touch darkness?", "a": ["no"], "p": 6},
    {"q": "Which came first: thought or language?", "a": ["thought"], "p": 6},
    {"q": "What is beyond the universe?", "a": ["nothing", "void"], "p": 6},
    {"q": "If a tree falls in a forest with no one around, does it make a sound?", "a": ["no"], "p": 6},
    {"q": "Can zero be divided?", "a": ["no"], "p": 6},
    {"q": "What is the color of the void?", "a": ["black", "nothing"], "p": 6},
    {"q": "If everything is possible, what is impossible?", "a": ["nothing"], "p": 6},
    {"q": "Can infinity be measured?", "a": ["no"], "p": 6},
    {"q": "What is the weight of nothing?", "a": ["0", "nothing"], "p": 6},
    {"q": "What is inside a black hole?", "a": ["singularity", "nothing"], "p": 6},
    {"q": "Does the future exist?", "a": ["no"], "p": 6},
    {"q": "Can a circle have a corner?", "a": ["no"], "p": 6},
    {"q": "If a question has no answer, what is it?", "a": ["nothing"], "p": 6},
    {"q": "Can you touch a thought?", "a": ["no"], "p": 6},
    {"q": "Is darkness a substance?", "a": ["no"], "p": 6},
    {"q": "What is the end of infinity?", "a": ["none"], "p": 6},
    {"q": "Can something come from nothing?", "a": ["no"], "p": 6},
    {"q": "What is the beginning of everything?", "a": ["nothing"], "p": 6},
    {"q": "Can a circle be squared?", "a": ["no"], "p": 6},
    {"q": "If a shadow falls in a void, does it exist?", "a": ["no"], "p": 6},
    {"q": "Can emptiness be filled?", "a": ["no"], "p": 6},
    {"q": "What is beyond death?", "a": ["nothing"], "p": 6},
    {"q": "Can light exist without darkness?", "a": ["no"], "p": 6},
    {"q": "Is the universe infinite?", "a": ["yes"], "p": 6},
    {"q": "Can you divide by zero?", "a": ["no"], "p": 6},
    {"q": "What is the meaning of meaningless?", "a": ["nothing"], "p": 6},
    {"q": "Does time have a shape?", "a": ["no"], "p": 6},
    {"q": "What is the color of absolute nothing?", "a": ["black", "nothing"], "p": 6},
    {"q": "If everything is temporary, what is permanent?", "a": ["nothing"], "p": 6},
    {"q": "Can you measure emptiness?", "a": ["no"], "p": 6},
    {"q": "What is the sound of silence?", "a": ["silence"], "p": 6},
    {"q": "Can infinity have limits?", "a": ["no"], "p": 6},
    {"q": "Does nothing weigh anything?", "a": ["no"], "p": 6},
    {"q": "What exists without a mind to perceive?", "a": ["nothing"], "p": 6},
    {"q": "Can a shadow exist without light?", "a": ["no"], "p": 6},
    {"q": "Is the void full of something?", "a": ["no"], "p": 6},
    {"q": "What is beyond understanding?", "a": ["nothing"], "p": 6},
    {"q": "Can chaos exist without order?", "a": ["yes"], "p": 6},
    {"q": "What is inside a cube of nothing?", "a": ["nothing"], "p": 6},
    {"q": "Can a point have length?", "a": ["no"], "p": 6},
    {"q": "What is before the beginning?", "a": ["nothing"], "p": 6},
    {"q": "Is infinity bigger than everything?", "a": ["yes"], "p": 6},
    {"q": "Can a void be empty?", "a": ["yes"], "p": 6},
    {"q": "What is deeper than the deepest ocean?", "a": ["nothing"], "p": 6},
    {"q": "Can you reach the end of space?", "a": ["no"], "p": 6},
    {"q": "What exists in absolute stillness?", "a": ["nothing"], "p": 6}
]
}

def add_xp(uid, points):
    uid = str(uid)
    scores[uid] = scores.get(uid, 0) + points
    levels.setdefault(uid, {"level": 1, "xp": 0})
    levels[uid]["xp"] += points
    need = levels[uid]["level"] * 10
    if levels[uid]["xp"] >= need:
        levels[uid]["xp"] = 0
        levels[uid]["level"] += 1
        return True
    return False

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
        if msg.content.lower().strip() in [a.lower().strip() for a in q["a"]]:
            lvl = add_xp(msg.author.id, q["p"])
            save("scores.json", scores)
            save("levels.json", levels)
            await ctx.send(f"✅ {msg.author.mention} +{q['p']} pts" + (" 🎉 LEVEL UP!" if lvl else ""))
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
    await ctx.send(embed=discord.Embed(title="🏆 Leaderboard", description=text))

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
@bot.command(name="list")
@commands.cooldown(1, 10, commands.BucketType.user)
async def list_cmd(ctx):
    await ctx.send(embed=discord.Embed(
        title="📜 Bot Commands",
        description=(
            "**🧰 Basic Commands**\n"
            "`!ping`, `!whoisstrongest`, `!8ball <question>`, `!joke`, `!fact`, `!rate <thing>`, `!today`, `!cat`\n\n"
            
            "**🧠 Trivia / Leveling**\n"
            "`!trivia <category>`, `!leaderboard`, `!team red/blue`, `!team_leaderboard`\n"
            "**Categories:** easy, medium, hard, gd, minecraft, silent\n\n"
            
            "**🎲 Chaos / Fun Commands**\n"
            "`!chaos`, `!spam <times> <text>`, `!coinflip`, `!rng <min> <max>`, `!reverse <text>`, `!scream`,\n"
            "`!uwu <text>`, `!dadjoke`, `!shrug`, `!tableflip`, `!unflip`, `!fortune`\n\n"
            
            "**🎨 Text / Emoji Commands**\n"
            "`!clap <text>`, `!mock <text>`, `!say <text>`, `!emojify <text>`, `!vibecheck [member]`, `!insultme`\n\n"
            
            "**🔥 Teams / Games**\n"
            "`!team red/blue`, `!team_leaderboard`\n\n"
            
            "**🎮 Knowledge / Logic**\n"
            "`!play quizbattle`, `!play rapidfire`, `!play riddlehunt`, `!play memorygrid`, `!play wordlink`, `!play factstorm`, `!play logicduel`, `!play codebreak`\n\n"
            
            "**⚔️ Competitive**\n"
            "`!play capturecore`, `!play laststand`, `!play arena`, `!play tagrun`, `!play dodgeball`, `!play snipershot`, `!play timeduel`\n\n"
            
            "**🤝 Co-op / Unity**\n"
            "`!play buildrush`, `!play puzzlelock`, `!play bridgecraft`, `!play relayquest`, `!play syncmove`, `!play rescueops`, `!play supplychain`\n\n"
            
            "**🎨 Creative**\n"
            "`!play drawguess`, `!play storychain`, `!play emoteplay`, `!play buildstatue`, `!play skincontest`, `!play musicmatch`\n\n"
            
            "**🏃 Skill / Speed**\n"
            "`!play parkourrace`, `!play mazerun`, `!play aimtrial`, `!play reflex`, `!play obstacleloop`, `!play timelock`\n\n"
            
            "**🎯 Strategy**\n"
            "`!play territory`, `!play resourcewar`, `!play towerdef`, `!play chesslite`, `!play cardclash`, `!play roleplayops`\n\n"
            
            "**🧩 Social / Party**\n"
            "`!play votemystery`, `!play truthortrap`, `!play guesswho`, `!play liarscore`, `!play speedvote`\n\n"
            
            "**🌍 Events / Exploration**\n"
            "`!play scavenger`, `!play worldevent`, `!play bossraid`, `!play timedexpedition`, `!play checkpoint`\n\n"
            
            "**⚡ Quick / Extra Fun**\n"
            "`!play coinrush`, `!play reactionchain`, `!play colorclaim`, `!play patternmatch`, `!play shadowtag`, `!play flagshift`, `!play numbergrid`, `!play echoquiz`, `!play survivalscore`, `!play challengewheel`"
        ),
        color=0x00ffff
    ))

# ================= CHAOS / FUN =================
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def chaos(ctx):
    await ctx.send(random.choice([
        "🔥 CHAOS 🔥", "💥 PANIC 💥", "😈 DOOM 😈"
    ]))

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def spam(ctx, times: int = 5, *, text="CHAOS"):
    for _ in range(min(times, 5)):
        await ctx.send(text)
        await asyncio.sleep(0.5)

@bot.command()
async def coinflip(ctx):
    await ctx.send(random.choice(["HEADS", "TAILS"]))

@bot.command()
async def rng(ctx, a: int = 1, b: int = 100):
    await ctx.send(random.randint(a, b))

@bot.command()
async def reverse(ctx, *, text: str):
    await ctx.send(text[::-1])

@bot.command()
async def scream(ctx):
    await ctx.send("AAAAAAAAAAAA")

@bot.command()
async def uwu(ctx, *, text="hello"):
    await ctx.send("UwU " + text.replace("r", "w").replace("l", "w"))

@bot.command()
async def dadjoke(ctx):
    await ctx.send(random.choice([
        "Calendar scared. Days numbered.",
        "Egg joke? Crack.",
        "Fake spaghetti = impasta."
    ]))

@bot.command()
async def shrug(ctx):
    await ctx.send("¯\\_(ツ)_/¯")

@bot.command()
async def tableflip(ctx):
    await ctx.send("(╯°□°）╯︵ ┻━┻")

@bot.command()
async def unflip(ctx):
    await ctx.send("┬─┬ ノ( ゜-゜ノ)")

# ================= ERROR HANDLER =================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Wait {error.retry_after:.1f}s")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing argument.")
@bot.command(name="level")
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    uid = str(member.id)
    lvl_data = levels.get(uid, {"level": 1, "xp": 0})
    await ctx.send(f"🎖️ {member.name} — Level {lvl_data['level']} | XP: {lvl_data['xp']}")

@bot.command(name="rank")
@commands.cooldown(1, 30, commands.BucketType.guild)
async def rank(ctx):
    if not levels:
        await ctx.send("No leveling data yet.")
        return

    sorted_levels = sorted(levels.items(), key=lambda x: x[1]["level"], reverse=True)[:10]
    text = ""
    for i, (uid, data) in enumerate(sorted_levels, 1):
        user = await bot.fetch_user(int(uid))
        text += f"**{i}. {user.name}** — Level {data['level']} | XP: {data['xp']}\n"

    await ctx.send(embed=discord.Embed(
        title="🏆 Leveling Leaderboard",
        description=text,
        color=0x00ff00
    ))
    # ================= TEXT / EMOJI =================
@bot.command()
async def clap(ctx, *, text: str):
    await ctx.send("👏 " + " 👏 ".join(text.split()))

@bot.command()
async def mock(ctx, *, text: str):
    await ctx.send("".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text)))

@bot.command()
async def say(ctx, *, text: str):
    await ctx.send(text)

@bot.command()
async def emojify(ctx, *, text: str):
    await ctx.send(" ".join(f":regional_indicator_{c.lower()}:" if c.isalpha() else c for c in text))

@bot.command()
async def vibecheck(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"{member.mention} has passed the vibe check! ✅" if random.randint(0,1) else f"{member.mention} failed the vibe check! ❌")

@bot.command()
async def insultme(ctx):
    insults = [
        "You're as sharp as a marble.",
        "You have something on your chin… no, the third one down.",
        "You bring everyone so much joy… when you leave the room."
    ]
    await ctx.send(random.choice(insults))

# ================= FORTUNE =================
@bot.command()
async def fortune(ctx):
    fortunes = [
        "You will have a pleasant surprise.",
        "A thrilling time is in your near future.",
        "Do not forget to smile today.",
        "Challenges are ahead, but you can overcome them."
    ]
    await ctx.send(f"🔮 {random.choice(fortunes)}")
import discord
from discord.ext import commands
import random
from collections import defaultdict
from enum import Enum

# ======================
# BOT SETUP
# ======================

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ======================
# RANK SYSTEM
# ======================

players = defaultdict(lambda: {"rank": 1, "xp": 0})

def get_rank(user):
    return players[user]["rank"]

def add_xp(user, xp):
    players[user]["xp"] += xp
    players[user]["rank"] = 1 + players[user]["xp"] // 500

# ======================
# GAMES
# ======================

class Mode(Enum):
    SOLO = "solo"
    TEAM = "team"

GAMES = {
    "quizbattle","rapidfire","riddlehunt","memorygrid","wordlink",
    "factstorm","logicduel","codebreak","capturecore","laststand",
    "arena","tagrun","dodgeball","snipershot","timeduel",
    "buildrush","puzzlelock","bridgecraft","relayquest","syncmove",
    "rescueops","supplychain","drawguess","storychain","emoteplay",
    "buildstatue","skincontest","musicmatch","parkourrace","mazerun",
    "aimtrial","reflex","obstacleloop","timelock","territory",
    "resourcewar","towerdef","chesslite","cardclash","roleplayops",
    "votemystery","truthortrap","guesswho","liarscore","speedvote",
    "scavenger","worldevent","bossraid","timedexpedition","checkpoint",
    "coinrush","reactionchain","colorclaim","patternmatch","shadowtag",
    "flagshift","numbergrid","echoquiz","survivalscore","challengewheel"
}

# ======================
# GAME ENGINE
# ======================

def play_game(game, users, mode):
    scores = {}
    for u in users:
        scores[u] = random.randint(10, 100) + get_rank(u) * 10

    if mode == Mode.SOLO:
        winner = max(scores, key=scores.get)
        add_xp(winner, 50)
        return [winner]

    for u in users:
        add_xp(u, 65)  # team bonus
    return users

# ======================
# COMMAND
# ======================

@bot.command()
async def play(ctx, game: str, *members: discord.Member):
    game = game.lower()
    if game not in GAMES:
        await ctx.send("Invalid game.")
        return

    if not members:
        users = [ctx.author.name]
        winners = play_game(game, users, Mode.SOLO)
    else:
        users = [m.name for m in members]
        winners = play_game(game, users, Mode.TEAM)

    msg = f"🎮 **{game}**\n🏆 Winners: {', '.join(winners)}\n"
    for u in winners:
        msg += f"{u} → Rank {get_rank(u)} | XP {players[u]['xp']}\n"

    await ctx.send(msg)

# ================= RUN =================
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("ERROR: DISCORD_TOKEN environment variable not set")
else:
    bot.run(token)