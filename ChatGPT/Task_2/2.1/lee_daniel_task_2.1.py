#refactoring code from repo_mining Daniel-Lee_CollectFiles.py (count files)
import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
PAGE_SIZE = 100  # Number of commits per page
def count_files(dictfiles, lsttokens, repo):
    ipage = 1  # URL page counter
    ct = 0  # Token counter

    try:
        while True:
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page={PAGE_SIZE}'
            json_commits, ct = github_auth(commits_url, lsttokens, ct)

            # Break out of the while loop if there are no more commits
            if not json_commits:
                break

            for commit in json_commits:
                sha = commit['sha']
                # Instead of a separate call, we can access files directly from the commit object
                if 'files' in commit:
                    for filenameObj in commit['files']:
                        filename = filenameObj['filename']
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)

            ipage += 1
    except requests.exceptions.RequestException as e:
        print(f"Error receiving data: {e}")
        exit(1)



repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

dictfiles = dict()
count_files(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
