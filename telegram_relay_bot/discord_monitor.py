import discord, json, re, os, logging, pyperclip


logging.basicConfig(
    filename="discordmonitor.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


intents = discord.Intents.all()
client = discord.Client(intents=intents)


def get_code(message):
    pattern = r"\b[c|C]ode\s*:\s*(\w+)\b"
    code = re.findall(pattern, message)
    if code:
        return code[0]
    else:
        return None


def get_message(message):
    pattern = r"\*\*.*\*\*\s*:\s*(.*)"
    code = re.findall(pattern, message)
    logger.info(f"CODE for message: {message} : {code}")
    if code:
        if len(code) != 1:
            logger.error("Something unexpected matched the regex!")
        return code[0]
    else:
        return None


@client.event
async def on_ready():
    logger.info("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    logger.info(f"Message {message.content}!")
    if message.author == client.user:
        return
    if str(message.channel.id) != "1026664696448819230":
        return

    code = get_message(message.content)
    if code is None:
        return
    else:
        # launch a new process to run the code
        await message.channel.send("Message extracted: {}".format(code))
        pyperclip.copy(code)
        os.system("start C:\\Users\\Administrator\\Desktop\\Discord.ed.mcr")


with open("config.json", "r") as f:
    config = json.load(f)

client.run(config["discord_bot_token"])
