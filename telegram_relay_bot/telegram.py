import json, sys, logging, re, os, pyperclip


from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
from discord import Webhook, RequestsWebhookAdapter


logging.basicConfig(
    filename="telegramrelayer.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("telethon").setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)


def get_code(message):
    pattern = r"\b[c|C]ode\s*:\s*(\w+)\b"
    code = re.findall(pattern, message)
    if code:
        return code[0]
    else:
        return None


def start(config):
    webhookUrl = config["discord_channel_webhook"]
    webhook = Webhook.from_url(webhookUrl, adapter=RequestsWebhookAdapter())

    client = TelegramClient(
        config["session_name"], config["api_id"], config["api_hash"]
    )
    client.start()

    print(config)
    valid_input_channel_ids = []

    all_dialogs = client.iter_dialogs()
    dialog_ids = [d.entity.id for d in all_dialogs]
    dialog_names = [d.name for d in all_dialogs]
    print(list(zip(dialog_ids, dialog_names)))
    for input_channel in config["input_channel_ids"]:
        if input_channel not in dialog_ids:
            logger.error(f"Channel {input_channel} not found in your dialogs")
            continue
        valid_input_channel_ids.append(input_channel)

    for input_channel_names in config["input_channel_names"]:
        if input_channel_names not in dialog_names:
            logger.error(f"Channel {input_channel_names} not found in your dialogs")
            continue
        valid_input_channel_ids.append(
            dialog_ids[dialog_names.index(input_channel_names)]
        )

    if not valid_input_channel_ids:
        logger.error(f"Could not find any input channels in the user's dialogs")
        sys.exit(1)

    logging.info(f"Listening on {len(valid_input_channel_ids)} channels.")

    # @client.on(events.NewMessage(chats=input_channels_entities))
    @client.on(events.NewMessage(chats=valid_input_channel_ids))
    async def handler(event):
        logging.info(f"Message Was: {event.message}")
        try:
            parsed_response = (
                event.message.message + "\n" + event.message.entities[0].url
            )
            parsed_response = "".join(parsed_response)
        except:
            parsed_response = event.message.message
        print(parsed_response, "Parsed Response")
        # Send Message to Discord
        webhook.send(parsed_response)
        code = get_code(parsed_response)
        if code is None:
            return
        else:
            pyperclip.copy(code)
            os.system("start C:\\Users\\Administrator\\Desktop\\Telegram.ed.mcr")

    # start the event loop
    client.run_until_disconnected()


if __name__ == "__main__":
    with open("./config.json", "r") as f:
        config = json.load(f)
    start(config)
