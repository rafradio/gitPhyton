import re
import asyncio
import aiohttp
from urllib.parse import urlparse
import sys, os, shutil, time
import git,os
from git import Repo
from pathlib import Path

async def createRepo(repo_url, dirName):
    local_dir = dirName
    repo = Repo.clone_from(repo_url, local_dir)
    tree = repo.heads.master.commit.tree
    for entry in tree: 
        print(entry.hexsha)

def createTemplate(dirName, i):
    basename = str(os.path.basename(dirName)) + str(i)
    basename = os.path.join(os.getcwd(), basename)
    if os.path.exists(basename): return createTemplate(dirName, i+1)
    return basename

async def startAsync(urls):
    tasks = []
    for url in urls:
        pr = urlparse(url)
        dirName = os.path.join(os.getcwd(), pr.hostname)
        if os.path.exists(dirName):
            dirName = createTemplate(dirName, 1)
            # shutil.rmtree(dirName)
            os.mkdir(dirName)
        else:
            os.mkdir(dirName)
        task = asyncio.ensure_future(createRepo(url, dirName))
        tasks.append(task)
    await asyncio.gather(*tasks)
    
if __name__ == '__main__':
    initialData = sys.argv
    defaultData = ['https://gitea.radium.group/radium/project-configuration', 'https://gitea.radium.group/radium/project-configuration', 'https://gitea.radium.group/radium/project-configuration']
    urls = initialData[1:] if len(initialData) > 1 else defaultData
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startAsync(urls))