import pandas as pd
import dask.dataframe as dd
import asyncio
from pyzeebe import ZeebeClient, create_camunda_cloud_channel, create_insecure_channel


async def deploy_run_web_call(bpmn_process_id):
    """ TBD """

    await client.deploy_process("process_models/call-website.bpmn")
    results = await client.run_process_with_result(bpmn_process_id=bpmn_process_id, timeout=10000)
    a=3

channel = create_insecure_channel(
    hostname='44.199.120.6',
    port=26500
)

# Create single threaded worker
client = ZeebeClient(channel)

bpmn_process_id = "Process_088975fa-2f84-4796-b13f-104af6cb4fd1"

loop = asyncio.get_event_loop()
try:
    results = loop.run_until_complete(deploy_run_web_call(bpmn_process_id))
finally:
    loop.stop()
    loop.close()