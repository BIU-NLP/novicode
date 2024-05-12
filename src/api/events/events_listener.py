class EventListener(list):
    def add_event_listener(self, event_type, callback, **kwarg):
        self.event_type = event_type
        self.callback = callback

    def __call__(self, *args, **kwargs):
        for event_listener in self:
            if event_listener.event_type == self.event_type:
                event_listener.callback(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)
