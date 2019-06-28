from flask import Flask
from redis import Redis, RedisError
import os
import traceback
import socket
import slack_rpg_bot
from slack_rpg_bot.slackbot import main
import boto3

# Connect to Redis
# This needs to be made dynamic
redis = Redis(host="192.168.99.100", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)


def get_token(name):
    # This probably needs some IAM policy to get fully working but it's
    # better than other solutions
    ssm = boto3.client('ssm', region_name='us-east-1')
    param = ssm.get_parameter(Name=name, WithDecryption=True)
    return param['Parameter']['Value']


if __name__ == "__main__":
    try:
        args = {}
        args['slack_token'] = get_token('slack_token')
        args['kanka_token'] = get_token('kanka_token')
        # print(args)
        main(args)
        app.run(host='0.0.0.0', port=80)
    except Exception as e:
        print('Script Error:' + str(e))
        traceback.print_exc()
