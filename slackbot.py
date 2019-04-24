import os
import time
import re
import traceback
import slack_pybot
from slack_pybot.data import Event, Command
from redis import StrictRedis
from die import dice_pool
from kanka_wrapper import kanka_wrapper


class RpgBot(slack_pybot.PyBot):

    def roll_command(self,command):
        my_dice = dice_pool(self.d_note,name='Rolling test')
        my_dice.roll()
        self.postMessage('rpg',my_dice.get_results(),None)

    def roll_conditional(self,event):
        self.d_note = ""
        words = event.text.split(' ')
        express = re.compile('\d+d\d+')
        for i in words:
            if express.match(i):
                self.d_note = i
                return True

        return False

    def sys_command(self):
        # Check the instance variables to create a table-top
        self.system
        self.postMessage('rpg',output,None)
        

    def sys_conditional(self, event):
        """
            Parse for rpg system option
            - Parse for system
            - Parse for roll type
            - Bail if something goes wrong
            Notes:
        """
        words = event.text.split()
        express = re.compile('(DnD5th)')

        if express.match(words[2]):
            self.system = DnD5th()
            if words[3]:
                self.roll_type = words[3]
                return True
        return False

    def kanka_command(self,command):
        """
           Need a reliable way to pass a campaign name to the wrapper 
        """
        try:
            kanka = kanka_wrapper(self.KANKA_TOKEN,command.args[1])
            # Need to parse the rest of the args to determine what method to use...
        except Exception as e:
            self.postMessage('rpg kanka Error',str(e),None)
        
        self.postMessage('rpg kanka',output,None)

    def kanka_conditional(self):

        if self.KANKA_TOKEN:
            return True

        if 'KANKA_TOKEN' in os.environ:
            self.KANKA_TOKEN = os.environ['KANKA_TOKEN']
            return True

        return False

    def _messageEventToCommand(self, event: Event):
        for trigger in self._triggers.keys():
            if event['text'].startswith(trigger):
                args = event['text'][len(trigger):].strip().split()
                return Command(
                    trigger,
                    args,
                    Event(
                        event.get('type'),
                        event.get('subtype'),
                        event.get('channel'),
                        event.get('user'),
                        event.get('text'),
                        event.get('ts'),
                        event.get('thread_ts')
                    ),
                    self._getCachedUser(event.get('user'))   # Had to alter this line to fix it from breaking
                )

        return None        

def main(args):
    if 'SLACK_TOKEN' in os.environ:
        SLACK_TOKEN = os.environ['SLACK_TOKEN']

    if 'KANKA_TOKEN' in os.environ:
        KANKA_TOKEN = os.environ['KANKA_TOKEN']

    db = StrictRedis(host='localhost', port=6379, db=0)
    bot = slack_pybot.Bot(name='TestRPGApp',icon_emoji=':)')
    pb = RpgBot(SLACK_TOKEN,bot,db)
    #response = pb.postMessage('rpg', 'Test.  I am a Bot','')
    pb.register('rpg_bot roll', pb.roll_command, pb.roll_conditional)
    pb.register('rpg_bot rpg', pb.sys_command, pb.sys_conditional)
    pb.register('rpg_bot kanka', pb.kanka_command, pb.kanka_conditional)
    pb.listen()
    while True:
        response = ''
        response = pb.tm_read()
        print(response)
        time.sleep(0.5) 
    return 0 

if __name__ == "__main__":
    try:
        #args = parse_args()
        args = ""
        main(args)
    except Exception as e:
        print('Script Error:'+str(e))
        traceback.print_exc()
