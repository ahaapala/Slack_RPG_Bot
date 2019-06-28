# Slack_RPG_Bot
Slack bot that uses the ttrpg core code and provides a possible interface to use it to help run games

Status:
* Can connect to slack channels
* Recognizes commands
* Can invoke ttrpg library code

TODO:
* Plan out and implement bot interface 
* Adapt interface to library invocations
* Can probably improve on how to map bot command syntax

Notes:
* Had to fix for https://github.com/slackapi/python-slackclient/issues/57
* This helps running sudo and python in a virtualenv
```
$ sudo -E `which python` ./app.py
```
