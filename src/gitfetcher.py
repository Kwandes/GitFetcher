import os
from datetime import datetime
from slack import RTMClient

# region Event handling

@RTMClient.run_on(event="message")
def receiveEvent(**payload):
    data = payload['data']
    web_client = payload['web_client']
    if '@UTU20FNKX' in data['text']:
        respondMention(data, web_client)
    elif '!data' in data['text']:
        respondData(data, web_client)
    elif '!repeat' in data['text']:
        respondRepeat(data, web_client)


def respondData(data, web_client):
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    web_client.chat_postMessage(
        channel=channel_id,
        text="Here is the data you've requested"
    )
    print(str(datetime.now().time()) + "> Replied to <data>")


def respondMention(data, web_client):
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    web_client.chat_postMessage(
      channel=channel_id,
      text=f"Hey, thanks for mentioning me"
    )
    print(str(datetime.now().time()) + "> Replied to <Hello>")


def respondRepeat(data, web_client):
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    web_client.chat_postMessage(
      channel=channel_id,
      text=data['text'].replace("!repeat", '')
    )
    print(str(datetime.now().time()) + "> Replied to <repeat>")

# endregion

# Slack Connection

slack_token = os.environ["GITFETCHER_SLACK_BOT_TOKEN"]

rtm_client = RTMClient(
    token=slack_token,
    connect_method='rtm.start'
)

print("starting listening")
while True:
    try:
        print(str(datetime.now().time()) + "> Connection Started")
        rtm_client.start()
    except KeyError as e:
        print(str(datetime.now().time()) + "> Error: " + str(e))
