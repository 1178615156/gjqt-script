from pyhooked import Hook, KeyboardEvent
from functional import seq
hk = Hook()

def handle_events(args:KeyboardEvent):
    key = args.current_key
    print(key)
hk.handler = handle_events
hk.hook()