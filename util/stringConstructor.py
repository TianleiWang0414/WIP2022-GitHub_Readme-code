"""
takes user/organization name and repo name and returns http url for the README file
"""


def buildREADMEpath(org: str, repo: str) -> str:
    read_url = 'https://raw.githubusercontent.com/'
    info = org + "/" + repo + "/"
    suffix = "master/README.md"
    return read_url + info + suffix


def buildREADMECommitPath(org: str, repo: str,sha:str) -> str:
    commit_url_markdown = 'https://api.github.com/repos/%s/%s/commits?sha=%s&path=README.md' % (org, repo,sha)
    return commit_url_markdown

def buildRepoStatusPath(org:str,repo:str)->str:
    return 'https://api.github.com/repos/%s/%s'% (org,repo)

#you would get the response header "link" -> rel=last -> page= ...
def buildContributorsPath(org:str,repo:str)->str:
    return 'https://api.github.com/repos/%s/%s/contributors?per_page=1' %(org,repo)
def buildWatches(org:str,repo:str)->str:
    return 'https://api.github.com/repos/%s/%s/subscribers?per_page=1' %(org, repo)
def buildPulllRequests(org:str,repo:str)->str:
    return "https://api.github.com/repos/%s/%s/pulls?per_page=1&state=all" %(org, repo)

def buildTopicSearch(topic:str)->str:

    return "https://api.github.com/search/repositories?q=topic:%s" %topic