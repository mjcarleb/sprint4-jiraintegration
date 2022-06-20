from flask import Flask, request
import asyncio
from pyzeebe import ZeebeWorker, create_insecure_channel


####################################################
#      SETUP TO USE ZEEBE
####################################################
channel = create_insecure_channel(
    hostname='44.199.120.6',
    port=26500
)

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
    print(f"webhook_id =  {webhook_id}")

    return {"status":  "ok"}

#############################################
# Create 1-time worker to clear Zeebe task waiting for Jira to return this webhook_id
webhook_id = "webhook_c194a702-8861-4bb7-a571-e49d022e973c"
worker = ZeebeWorker(channel)
@worker.task(task_type=f"{webhook_id}")
def execute_webhook(url, method, webhook_uuid):
    # Now that Jira has returned the webhook_id, we just clear the task on Zeebe with return
    return {}
#############################################


if __name__ == '__main__':

    #  Run the web server to accept webhooks
    #  app.run(debug=True)


    # Where does this loop run?
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
        loop.stop()
        loop.close()
    finally:
        loop.stop()
        loop.close()


