from kivy.event import EventDispatcher


class RaceEvents(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type("on_state_change")
        super().__init__(**kwargs)

    def on_state_change(self, old_state, new_state):
        pass
