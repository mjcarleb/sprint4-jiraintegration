from flask import Flask,request,json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Webhooks with Python'

@app.route('/CTL',methods=['POST'])
def ackUserForm():
    external_user_task_ack_id = request.form['external_user_task_ack_id']
    print(f"external_user_task_ack_id =  {external_user_task_ack_id}")
    return request.form

if __name__ == '__main__':
    app.run(debug=True)