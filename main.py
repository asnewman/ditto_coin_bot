import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import re
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

app = App()
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Set up the bot command: /send_coin
@app.command("/send_coin")
def handle_send_coin(ack, respond, command):
    # Acknowledge command request
    ack()

    pattern = r"@(\w+) (\d+) (.+)"  # Updated pattern to include reason
    match = re.search(pattern, command['text'])

    if not match:
        respond("Please use the format: /send_coin @user [amount] [reason]")
        print("Failed " + command['text'])
        return

    user_id, amount, reason = match.groups()  # Updated to include reason
    amount = int(amount)

    if amount < 1 or amount > 10:
        respond("Invalid amount. You can only send 1 to 10 Ditto coins.")
        return

    sender = command['user_id']
    message = f"🪙 <@{sender}> sent {amount} Ditto coins to <@{user_id}> for \"{reason}\"! 🪙"  # Updated message to include reason

    try:
        response = client.chat_postMessage(
            channel=command['channel_id'],
            text=message
        )
    except SlackApiError as e:
        print(f"Error posting message: {e}")

if __name__ == "__main__":
    # Load the Slack app token and bot token from the .env file
    SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

