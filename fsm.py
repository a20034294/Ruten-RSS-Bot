from transitions.extensions import GraphMachine

from utils import send_text_message
from crawler import Crawler


class TocMachine(Crawler, GraphMachine):
    def __init__(self, crawler, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.crawler = crawler
##### init
    def on_enter_state_init(self, event):
        with open('./sessions/' + event.source.sender_id, 'w') as f:
            f.write('state_init')
        print("enter init")
        reply_token = event.source.sender_id
        send_text_message(reply_token, "init")
##### routine
    def on_enter_state_routine(self, event):
        with open('./sessions/' + event.source.sender_id, 'w') as f:
            f.write('state_routine')
        print("I'm entering state_routine")
        reply_token = event.source.sender_id
        send_text_message(reply_token, "routine")

        message = self.crawler.routine()
        send_text_message(reply_token, message)

        self.to_state_init(event)

    def on_exit_state_routine(self, event):
        print("Leaving state_routine")
##### query
    def on_enter_state_query(self, event):
        print("I'm entering state_query")
        with open('./sessions/' + event.source.sender_id, 'w') as f:
            f.write('state_query')

        reply_token = event.source.sender_id
        send_text_message(reply_token, "query")

        # message = self.crawler.query()
        # send_text_message(reply_token, message)

        # self.to_state_init(event)

    def on_exit_state_query(self, event):
        print("Leaving state_query")

