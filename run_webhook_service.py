from flask import Flask,request,json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Webhooks with Python'

@app.route('/CTL',methods=['POST'])
def ackUserForm():
    webhook_id = request.form['webhook_id']
    print(f"webhook_id =  {webhook_id}")
    return request.form

if __name__ == '__main__':
    app.run(debug=True)