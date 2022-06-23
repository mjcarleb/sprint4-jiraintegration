import asyncio
import uuid
import json

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
async def execute_rest_call(method, url, project, issuetype, summary, assignee):
    print(f"url = {url}")
    print(f"method = {method}")
    print(f"project = {project}")
    print(f"issuetype = {issuetype}")
    print(f"summary = {summary}")
    print(f"assignee = {assignee}")

    webhook_uuid = f"webhook_{uuid.uuid4()}"
    print(f"webhook_uuid = {webhook_uuid}")

    # include in the post the variables in form of following:
    #   - trade
    #   - webhook url (public flask url /CTL)
    username = "mcarlebach@ctepl.com"  # Jira
    password = "KNIubBqwWYTWbD7bmYVBDE66"  # Jir
    payload = {
        "fields": {"project":  {"key":  project},
                   "issuetype":  {"name":  issuetype},
                   "summary":  summary,
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