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
        send_text_message(reply_token, "enter init")
##### routine
    def on_enter_state_routine(self, event):
        with open('./sessions/' + event.source.sender_id, 'w') as f:
            f.write('state_routine')
        print("enter state_routine")
        reply_token = event.source.sender_id
        send_text_message(reply_token, "enter routine")

        message = self.crawler.routine()
        send_text_message(reply_token, message)

        self.to_state_init(event)

    def on_exit_state_routine(self, event):
        print("Leaving state_routine")
##### query
    def on_enter_state_query(self, event):
        print("enter state_query")
        with open('./sessions/' + event.source.sender_id, 'w') as f:
            f.write('state_query')

        reply_token = event.source.sender_id
        send_text_message(reply_token, "enter query")

    def on_exit_state_query(self, event):
        print("Leaving state_query")

##### querying
    def on_enter_state_querying(self, event):
        print("enter state_querying")
        with open('./sessions/' + event.source.sender_id, 'w') as f:
            f.write('state_querying')

        reply_token = event.source.sender_id


        message = self.crawler.query(event.message.text)
        send_text_message(reply_token, message)

        self.compelete_query(event)

    def on_exit_state_querying(self, event):
        print("Leaving state_querying")

