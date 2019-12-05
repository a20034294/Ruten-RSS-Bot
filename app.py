import os
import sys
import time

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from selenium import webdriver

from fsm import TocMachine
from utils import send_text_message
from crawler import Crawler

load_dotenv()

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

os.system('pkill -9 chrome')
os.system('rm ./sessions/*')
driver_opt = webdriver.ChromeOptions()
driver_opt.add_argument('--headless')
driver_opt.add_argument('--disable_gpu')
driver_opt.add_argument('--no-sandbox')
driver_opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36')
prefs = {
    'profile.managed_default_content_settings.images': 2,
}
driver_opt.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome('./chromedriver', chrome_options=driver_opt)

crawler = Crawler(driver)


app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
machine = {}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        if not event.source.sender_id in machine.keys():
            print('create machine')

            if not os.path.isfile('./sessions/' + event.source.sender_id):
                with open('./sessions/' + event.source.sender_id, 'w') as f:
                    f.write('state_init')

            with open('./sessions/' + event.source.sender_id, 'r') as f:
                state = f.readline()

            new_machine = TocMachine(crawler,
                states=["state_init", "state_query", "state_routine", "state_querying"],
                transitions=[
                    {
                        "trigger": "to_state_init",
                        "source": ["state_query", "state_routine"],
                        "dest": "state_init"
                    },
                    {
                        "trigger": "to_state_query",
                        "source": "state_init",
                        "dest": "state_query"
                    },
                    {
                        "trigger": "to_state_routine",
                        "source": "state_init",
                        "dest": "state_routine"
                    },
                    {
                        "trigger": "one_query",
                        "source": "state_query",
                        "dest": "state_querying"
                    },
                    {
                        "trigger": "compelete_query",
                        "source": "state_querying",
                        "dest": "state_query"
                    },
                ],
                initial=state,
                auto_transitions=False,
                show_conditions=True,
            )
            new_machine.get_graph().draw("fsm.png", prog="dot", format="png")
            machine[event.source.sender_id] = new_machine

        state = machine[event.source.sender_id].state
        print(machine[event.source.sender_id].state)
        print(f"\nFSM STATE: {machine[event.source.sender_id].state}")
        print(f"REQUEST BODY: \n{body}")
        response = False
        if state == 'state_query':
            if event.message.text == 'exit':
                response = machine[event.source.sender_id].to_state_init(event)
            else:
                send_text_message(event.source.sender_id, 'crawlering please wait')
                response = machine[event.source.sender_id].one_query(event)
        elif state == 'state_querying':
            send_text_message(event.source.sender_id, 'crawlering please wait')
        elif event.message.text == 'routine':
            response = machine[event.source.sender_id].to_state_routine(event)
        elif event.message.text == 'query':
            response = machine[event.source.sender_id].to_state_query(event)
        else:
            send_text_message(event.source.sender_id, "command not found")


    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    #machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)

driver.quit()
