import json
import requests
import re
from io import BytesIO

# Used to call Python 2.7 from 3.6
import subprocess

from aiohttp import web
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext)
from botbuilder.schema import (Activity, ActivityTypes)


# Settings
BOT_APP_ID = ''
BOT_APP_PASSWORD = ''
SETTINGS = BotFrameworkAdapterSettings(BOT_APP_ID, BOT_APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

LUIS_APP_ID = '<your luis application id>'
LUIS_SUBSCRIPTION_KEY = '<your luis subscription key>'

COMPUTER_VISION_ANALYZE_URL = "https://westus.api.cognitive.microsoft.com/vision/v2.0/analyze"
COMPUTER_VISION_SUBSCRIPTION_KEY = "<your computer vision subscription key>"


class ComputerVisionApiService:
    @staticmethod
    def analyze_image(image_url):
        # Request headers and parameters
        

        # Get image bytes content
        
        
        try:
            return None # Replace with implementation
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


class LuisApiService:
    @staticmethod
    def post_utterance(message):
        # Request headers and parameters


        try:
            return None # Replace with implementation
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


class BotRequestHandler:
    async def create_reply_activity(request_activity, text) -> Activity:
        return Activity(
            type=ActivityTypes.message,
            channel_id=request_activity.channel_id,
            conversation=request_activity.conversation,
            recipient=request_activity.from_property,
            from_property=request_activity.recipient,
            text=text,
            service_url=request_activity.service_url)
    
    async def handle_message(context: TurnContext) -> web.Response:
        activity = context.activity
        if activity.text:
            intent = None

            response = await BotRequestHandler.create_reply_activity(activity, f'Top Intent: {intent}.')
            await context.send_activity(response)

            if intent == 'MoveArm':
                BotCommandHandler.move_arm()
            else:
                response = await BotRequestHandler.create_reply_activity(activity, 'Please provide a valid instruction')
                await context.send_activity(response)
        else:
            process_image(activity, context)
        
        return web.Response(status=202)
    
    async def handle_conversation_update(context: TurnContext) -> web.Response:
        if context.activity.members_added[0].id != context.activity.recipient.id:
            response = await BotRequestHandler.create_reply_activity(context.activity, 'Welcome to Sawyer Robot!')
            await context.send_activity(response)
        return web.Response(status=200)
    
    async def unhandled_activity() -> web.Response:
        return web.Response(status=404)
    
    def process_image(activity: Activity, context: TurnContext):
        print("Process image") # Replace with implementation
    
    def get_image_url(attachments):
        p = re.compile('^image/(jpg|jpeg|png|gif)$')
        for attachment in attachments:
            rs = p.match(attachment.content_type)
            if rs:
                return attachment.content_url
        return None
        
    
    @staticmethod
    async def request_handler(context: TurnContext) -> web.Response:
        if context.activity.type == 'message':
            return await BotRequestHandler.handle_message(context)
        elif context.activity.type == 'conversationUpdate':
            return await BotRequestHandler.handle_conversation_update(context)
        else:
            return await BotRequestHandler.unhandled_activity()
    
    async def messages(req: web.web_request) -> web.Response:
        body = await req.json()
        activity = Activity().deserialize(body)
        auth_header = req.headers['Authorization'] if 'Authorization' in req.headers else ''
        try:
            return await ADAPTER.process_activity(activity, auth_header, BotRequestHandler.request_handler)
        except Exception as e:
            raise e

class BotCommandHandler:
    def move_arm():
        print('Moving arm... do something cool')
        # launch your python2 script using bash
        python2_command = "python2.7 bot-wave-arm-node.py"  

        process = subprocess.Popen(python2_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()  # receive output from the python2 script
      
        print('done moving arm . . .')
        print('returncode: '  + str(process.returncode))
        print('output: ' + output.decode("utf-8"))

    def show_stats():
        # Replace with your code
    
    def move_cube(color):
        # Replace with your code
    
    def blink_light():
        # Replace with your code
    


app = web.Application()
app.router.add_post('/api/messages', BotRequestHandler.messages)

try:
    web.run_app(app, host='localhost', port=9000)
    print('Started http server on localhost:9000')
except Exception as e:
    raise e