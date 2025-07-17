from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_TOKEN, SLACK_CHANNEL
client = WebClient(token=SLACK_TOKEN)

def send_slack_alert(message):
    try:
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
    except SlackApiError as e:
        print("Slack alert failed:", e)
