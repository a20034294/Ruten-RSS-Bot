from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def on_enter_user(self, event):
        print("enter user")
        reply_token = event.source.sender_id
        send_text_message(reply_token, "Trigger user")

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.source.sender_id
        print(reply_token)
        send_text_message(reply_token, "Trigger state1")
        self.go_back(event)

    def on_exit_state1(self, event):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.source.sender_id
        send_text_message(reply_token, "Trigger state2")
        self.go_back(event)

    def on_exit_state2(self, event):
        print("Leaving state2")
