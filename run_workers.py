import asyncio
from pyzeebe import ZeebeWorker, create_insecure_channel
import requests

response = requests.get('https://google.com/')
print(response)


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
@worker.task(task_type="rest_call")
async def execute_rest_call(method, url):

    print(f"method = {method}")
    print(f"url = {url}")

    if method == "get":
        r = requests.get(url)
    else:
        breakpoint()

    status = r.status_code
    return {"status": f"{status}"}

# Main loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(worker.work())
finally:
    loop.stop()
    loop.close()