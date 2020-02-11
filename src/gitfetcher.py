import os
from slack import RTMClient


@RTMClient.run_on(event="message")
def receiveEvent(**payload):
    data = payload['data']
    web_client = payload['web_client']
    if '!Hello' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
          channel=channel_id,
          text=f"Hi <@{user}>!"
        )
        print("Replied to <Hello>")
    elif '!data' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
          channel=channel_id,
          text=f"Here is the data you've requested"
        )
        print("Replied to <data>")


slack_token = os.environ["GITFETCHER_SLACK_BOT_TOKEN"]

rtm_client = RTMClient(
    token=slack_token,
    connect_method='rtm.start'
)

print ("starting listening")
while(True):
    try:
        rtm_client.start()
    except KeyError as e:
        print("Error: " + str(e))