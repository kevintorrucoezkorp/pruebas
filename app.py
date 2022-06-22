
from asyncio import events
from datetime import datetime
from email import message
from chalice import Chalice
import boto3
from sqs.sqs_queues import SQSQueue
import json
from boto3.dynamodb.conditions import Key

def get_app_db():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('my-demo-table')
    return table

app = Chalice(app_name='pruebas')
@app.route('/book', methods=['POST'])
def add_book():
    data = app.current_request.json_body
    try:
        get_app_db().put_item(Item={
            'id': data['id'],
            "title": data['title'],
            "author": data['author']
        })
        return {'message': 'ok - CREATED', 'status': 201, "id": data['id'], "title": data['title'], "author": data['author']}
    except Exception as e:
        return {'message': str(e)}
@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/time')
def gettime():
    now= datetime.now()
    current_time= now.strftime("%D %H:%M:%S")
    return f"The Time is {current_time}"

@app.route('/echo', methods=['POST'])
def echoback():
    request=app.current_request
    message= request.json_body
    return message

@app.route('/sendsqs', methods=['POST'])
def echoback():
    q = SQSQueue(queueName='test_fifo.fifo')
    Message ={"name":"Prueba4"}
    MessageGroupId={"MessageGroupId":1000}
    response = q.send(Message=Message,MessageGroupId=MessageGroupId)
    

    return response
# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
