import asyncio
import os
import json
import logging
import pyppeteer
from pyppeteer import launch

logger = logging.getLogger(__name__)

HOME = os.environ['HOME']

async def handle(event):
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
            await _process_pr_opened(org, org_id, repo, repo_id, pr, observation_link)
        elif action == 'closed':
            await _process_pr_closed(org, org_id, repo, repo_id, pr, observation_link)

    return None

async def _process_pr_opened(org, org_id, repo, repo_id, pr, html_link):
    _generate_pr_observation(org, org_id, repo, repo_id, pr, html_link, 'OPENED')

async def _process_pr_closed(org, org_id, repo, repo_id, pr, html_link):
    _generate_pr_observation(org, org_id, repo, repo_id, pr, html_link, 'CLOSED')

async def _generate_pr_observation(org, org_id, repo, repo_id, pr, html_link, pr_status):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(html_link)
    await page.screenshot({'path': f'{HOME}/observations/{org_id}-{org}_{repo_id}_{repo}_{pr}-{pr_status}.png', 'fullPage': 'true'})
    await browser.close()


# with open('/home/max/projects/mensch-gateway/ref_spec/github/pr_opened.json') as f:
#   content = json.load(f)
#   asyncio.get_event_loop().run_until_complete(handle(content))
