import asyncio
import uuid

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
async def execute_rest_call(method, url):

    webhook_uuid = f"webhook_{uuid.uuid4()}"
    print(f"url = {url} (will be Jira)")
    print(f"method = {method} (will be post with Jira)")
    print(f"webhook_uuid = {webhook_uuid}")
    print()


    # make post
    # use Jira username and secret
    # use Jira URL
    # include in the post the variables in form of following:
    #   - trade
    #   - assignee
    #   - webhook_uuid
    if method == "get":
        r = requests.get(url)
    else:
        breakpoint()

    status = r.status_code

    return {"webhook_uuid": f"{webhook_uuid}"}

# Main loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(worker.work())
finally:
    loop.stop()
    loop.close()