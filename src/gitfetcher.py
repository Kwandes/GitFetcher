import traceback
from datetime import datetime
from slack import RTMClient

import sys, os
sys.path.append('/path/to/gitAPI')     # apparently it updates the path variable, allowing import of local scripts
import gitAPI as api


def stripCommand(data, command):
    data['text'] = data['text'].replace(command, '', 1)

# region Event handling


@RTMClient.run_on(event="message")
def receiveEvent(**payload):
    data = payload['data']
    web_client = payload['web_client']

    # check payload for command keywords
    if data['text'].startswith('@UTU20FNKX'):
        print(str(datetime.now().time()) + "> Received command <mention>")
        # remove the command call from the message
        stripCommand(data, '@UTU20FNKX')
        channel_id = data['channel']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hey, thanks for mentioning me"
        )
        print(str(datetime.now().time()) + "> Replied to <Mention>")

    elif data['text'].startswith('!help'):
        print(str(datetime.now().time()) + "> Received command <help>")
        stripCommand(data, '!info')
        channel_id = data['channel']

        response = """Commands:
> help
list of commands
> info <repo>
shows basic repository info
> contributors <repo>
shows a list of contributors and their commit numbers, sorted from most to least
> contributor <repo> <contributorName>
shows info on a specific contributor in a given repo
> branches <repo>
shows top 5 active branches, sorted by commits
> branch <repo>
shows basic info about a branch
> commits <repo> optional<branch>
shows last 5 commits on chosen branch, defaults to master
> commit <repo> optional<sha>
shows details about a commit, defaults to the newest one
> readme <repo>
shows a readme"""

        web_client.chat_postMessage(
            channel=channel_id,
            text=response
        )
        print(str(datetime.now().time()) + "> Replied to <help>")

    elif data['text'].startswith('!info'):
        print(str(datetime.now().time()) + "> Received command <info>")
        stripCommand(data, '!info')
        channel_id = data['channel']
        response = ""

        try:
            # get Repository info
            response = str(api.getRepoInfo(data))
            # If there is an issue, response might be empty
            if not response:
                raise Exception
        except:
            traceback.print_exc()
            response = "invalid parameters"

        web_client.chat_postMessage(
            channel=channel_id,
            text=response
        )
        print(str(datetime.now().time()) + "> Replied to <info>")

    elif data['text'].startswith('!contributors'):
        print(str(datetime.now().time()) + "> Received command <contributors>")
        stripCommand(data, '!contributors')
        channel_id = data['channel']
        response = ""

        try:
            # get Repository info
            response = str(api.getContributors(data))
            # If there is an issue, response might be empty
            if not response:
                raise Exception
        except:
            traceback.print_exc()
            response = "invalid parameters"

        web_client.chat_postMessage(
            channel=channel_id,
            text=response
        )
        print(str(datetime.now().time()) + "> Replied to <Contributors>")

    elif data['text'].startswith('!contributor'):
        print(str(datetime.now().time()) + "> Received command <contributor>")
        stripCommand(data, '!contributors')
        channel_id = data['channel']
        response = ""

        try:
            # get Repository info
            response = str(api.getContributor(data))
            # If there is an issue, response might be empty
            if not response:
                raise Exception
        except:
            traceback.print_exc()
            response = "invalid parameters"

        web_client.chat_postMessage(
            channel=channel_id,
            text=response
        )
        print(str(datetime.now().time()) + "> Replied to <Contributor>")

# endregion

# region Slack Connection


slack_token = os.environ["GITFETCHER_SLACK_BOT_TOKEN"]

rtm_client = RTMClient(
    token=slack_token,
    connect_method='rtm.start'
)

print(str(datetime.now().time()) + ">starting listening")
while True:
    try:
        print(str(datetime.now().time()) + "> Connection Started")
        rtm_client.start()
    except KeyError as e:
        print(str(datetime.now().time()) + "> Error: " + str(e))
        traceback.print_exc()

# endregion
