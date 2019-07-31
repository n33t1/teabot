import os

from slackclient import SlackClient

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = SlackClient(SLACK_BOT_TOKEN)