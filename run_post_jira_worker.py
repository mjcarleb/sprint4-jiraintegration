import asyncio
import uuid
import os

from pyzeebe import ZeebeWorker, create_insecure_channel
import requests

####################################################
#      SETUP TO USE C8 ZEEBE
####################################################
channel = create_insecure_channel(
    hostname='44.199.120.6',
    port=26500
)

# Create single threaded worker
worker = ZeebeWorker(channel)

####################################################
#          DEFINE WORKERS
####################################################
# Define work this client should do when trade_match_worker job exists in Zeebe
@worker.task(task_type="jira_interface")
async def execute_rest_call(method, url, project, issuetype, summary, assignee, webhook_response_url,
                            broken_trade):
    print(f"url = {url}")
    print(f"method = {method}")
    print(f"project = {project}")
    print(f"issuetype = {issuetype}")
    print(f"summary = {summary}")
    print(f"webhook_response_url {webhook_response_url}")
    print(f"assignee = {assignee}")
    print(f"broken trade = {broken_trade}")

    webhook_uuid = f"webhook_{uuid.uuid4()}"
    print(f"webhook_uuid = {webhook_uuid}")

    # include in the post the variables in form of following:
    #   - trade
    #   - webhook url (public flask url /CTL)
    username = os.getenv("JIRA_USERNAME")
    password = os.getenv("JIRA_PASSWORD")
    payload = {
        "fields": {"project":  {"key":  project},
                   "issuetype":  {"name":  issuetype},
                   "summary":  summary,
                   "assignee":  {"id":  assignee},
                   "description": {
                       "type": "doc",
                       "version":  1,
                       "content":  [
                           {"type":  "paragraph",
                            "content":  [
                                 {"text":  broken_trade,
                                  "type":  "text"
                                   }
                             ]}
                       ]
                   },
                   "customfield_10299":  webhook_response_url,
                   "customfield_10298":  webhook_uuid
                   }
    }
    if method == "post":
        r = requests.post(url=url, auth=(username, password), json=payload)
    else:
        breakpoint()

    status = r.status_code
    print(f"Jira response code = {status}")
    print()

    return {"webhook_uuid": f"{webhook_uuid}"}

# Main loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(worker.work())
finally:
    loop.stop()
    loop.close()