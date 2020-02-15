from datetime import datetime
import time
import github
import re
import traceback
import os

# region get Functions


def getRepoInfo(data):
    git = github.Github(os.environ["GITFETCHER_GITHUB_TOKEN"])

    repoAddress = data['text'].split(' ')[1]
    try:
        repo = git.get_repo(re.search("\.com\/(\S+)", repoAddress).group(1).replace('>', ''))
    except github.UnknownObjectException as e:
        print("Repository " + repoAddress + " not found")
        return "Repository not found"
    except AttributeError as e:
        print("Repository " + repoAddress + " regex failed")
        traceback.print_exc()
        return "Repository not found"

    # No checking for other errors, gitFetcher handles that

    repoName = "Name: " + repo.full_name
    repoDesc = "Description: " + repo.description
    repoLanguage = "Language: " + repo.language
    repoBranches = "Branches:\n"
    counter = 0
    for branch in repo.get_branches():
        if counter < 5:
            repoBranches += ">" + branch.name + '\n'
            counter += 1
        else:
            break
    return '\n'.join([repoName, repoDesc, repoLanguage, repoBranches])

# endregion
