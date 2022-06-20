from flask import Flask, request
import threading
import asyncio
from pyzeebe import ZeebeWorker, create_camunda_cloud_channel, create_insecure_channel


####################################################
#      SETUP TO USE C8 ZEEBE
####################################################
# Create channel to Zeebe
#channel = create_camunda_cloud_channel(
#    client_id="u_eR8WbpVLktYegPjKTy_LwrwtKycxQD",
#    client_secret="gTvDm-l92oXaTbdcS.6IeypQxDQ8~hKhaUVV0C4Rq4MaSfMj4huEMiipAFxwdA2M",
#    cluster_id="b6f56d09-397c-4d96-838a-96df7f1665e4",
#)

channel = create_insecure_channel(
    hostname='44.199.120.6',
    port=26500
)

# Create single threaded worker
worker = ZeebeWorker(channel)
webhook_id = "webhook_13be0034-09e6-4712-9601-8c77f79835e3"

def stopping_decorator(job):
    loop.stop()
    return job

worker.after(stopping_decorator)

@worker.task(task_type=f"{webhook_id}")
async def execute_webhook(url, method, webhook_uuid):
    # Now that Jira has returned the webhook_id, we just clear the task on Zeebe with return
    print('loop stopping')
    #loop.stop()
    return {}

async def my_coroutine():
    print("my co-routine")

loop = asyncio.get_event_loop()
try:
    #loop.run_until_complete(my_coroutine())
    loop.run_until_complete(worker.work())

finally:
    loop.close()


'''
class thread(threading.Thread):

    def __init__(self, webhook_id):
        threading.Thread.__init__(self)
        self.webhook_id = webhook_id

    def run(self):

        worker = ZeebeWorker(channel)

        @worker.task(task_type=f"{self.webhook_id}")
        async def execute_webhook(url, method, webhook_uuid):
            # Now that Jira has returned the webhook_id, we just clear the task on Zeebe with return
            return {}

        try:
            loop.run_until_complete(worker.work())
        except RuntimeError:
            pass

        # worker.stop()
        # del worker
        # close channel
        # delete channel
        # close loop?


####################################################
#   SETUP TO USE WEB SERVER TO RECEIVE WEBHOOK
####################################################
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Webhooks with Python'

@app.route('/CTL',methods=['POST'])
def recevieWebhook():
    """ Jira has return webhook_id for which a Zeebe task is waiting """

    webhook_id = request.form['webhook_id']
    thread1 = thread(webhook_id)
    results = thread1.start()
    return {"status":  "ok"}
'''


#if __name__ == '__main__':

    ####################################################
    #         Create thread for C8 job worker
    ####################################################


    #  Run the web server to accept webhooks
    # app.run(debug=True)