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


def getContributors(data):

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

    repoName = "Name: " + repo.full_name
    repoContributors = "Contributors:\n"
    counter = 0
    for contributor in repo.get_contributors():
        if counter < 5:
            repoContributors += "> Name: " + str(contributor.name) + "\n| Contributions: " + str(contributor.contributions) + "\n"
            counter += 1
        else:
            break
    return '\n'.join([repoName, repoContributors])


def getContributor(data):

    git = github.Github(os.environ["GITFETCHER_GITHUB_TOKEN"])

    repoAddress = data['text'].split(' ')[1]
    contributorName = ""
    try:
        contributorName = data['text'].split(' ')[2]
        contributorName += " " + data['text'].split(' ')[3]
        print("Contributor name: " + contributorName)
    except:
        contributorName = ""

    try:
        repo = git.get_repo(re.search("\.com\/(\S+)", repoAddress).group(1).replace('>', ''))
    except github.UnknownObjectException as e:
        print("Repository " + repoAddress + " not found")
        return "Repository not found"
    except AttributeError as e:
        print("Repository " + repoAddress + " regex failed")
        traceback.print_exc()
        return "Repository not found"

    repoName = "Name: " + repo.full_name
    repoContributor = "Top commits contributor:\n"

    # if no contributor was chosen, pick top commits one
    if not contributorName:
        for contributor in repo.get_contributors():
            repoContributor += "> Name: " + str(contributor.name) + \
                               "\n| Bio: " + contributor.bio + \
                               "\n| Contributions: " + str(contributor.contributions) + \
                               "\n| Email: " + str(contributor.email)
            break
        return '\n'.join([repoName, repoContributor])
    # otherwise seaech through the list until you find one
    else:
        for contributor in repo.get_contributors():
            if contributor.name == contributorName:
                repoContributor += "> Name: " + str(contributor.name) + \
                               "\n| Bio: " + str(contributor.bio) + \
                               "\n| Contributions: " + str(contributor.contributions) + \
                               "\n| Email: " + str(contributor.email)
                return '\n'.join([repoName, repoContributor])
    # In case none is found
    return "Contributor not found"

# endregion
