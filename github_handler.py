import asyncio
import json
import logging
import pyppeteer
from pyppeteer import launch
from multiprocessing import Process

logger = logging.getLogger(__name__)

def handle(event):
    if 'action' in event and 'pull_request' in event:
        action = event['action']
        org = event['pull_request']['base']['repo']['owner']['login']
        org_id = event['pull_request']['base']['repo']['owner']['id']
        repo = event['pull_request']['base']['repo']["name"]
        repo_id = event['pull_request']['base']['repo']["id"]
        pr = event['number']
        observation_link = event['pull_request']["_links"]["html"]["href"]

        logger.info(f"Processing event {action=} {org=} {org_id=} {repo=} {repo_id=} {pr=}")

        if action == 'opened':
            process_pr_opened(org, org_id, repo, repo_id, pr, observation_link)
        elif action == 'closed':
            process_pr_closed(org, org_id, repo, repo_id, pr, observation_link)

    return ''

def process_pr_opened(org, org_id, repo, repo_id, pr, html_link):
    generate_pr_observation(org, org_id, repo, repo_id, pr, html_link, 'OPENED')

def process_pr_closed(org, org_id, repo, repo_id, pr, html_link):
    generate_pr_observation(org, org_id, repo, repo_id, pr, html_link, 'CLOSED')

def generate_pr_observation(org, org_id, repo, repo_id, pr, html_link, pr_status):    
    path = f'/opt/observations/org={org_id}-{org}_repo={repo_id}_{repo}_pr={pr}-status={pr_status}.png'

    # Work around 3.8 regression https://bugs.python.org/issue38904 occuring on pyppeter signal to chrome.
    p = Process(target=takescreenshot, args=(html_link, path))
    p.start()
    p.join()    

def takescreenshot(html_link, path):
    async def page_to_png(url, image):
        browser = await launch(options={'args': ['--no-sandbox']})
        page = await browser.newPage()
        await page.goto(url)
        await page.screenshot({'path': image, 'fullPage': 'true'})
        await browser.close()

    asyncio.run(page_to_png(html_link, path))
    


# with open('/home/max/projects/mensch-gateway/ref_spec/github/pr_closed.json') as f:
#   content = json.load(f)
#   handle(content)
