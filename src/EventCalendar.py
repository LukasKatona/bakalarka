class EventCalendar:
    # INIT
    def __init__(self):
        self.events = []
        self.maxId = 0

    # METHODS
    def isEmpty(self):
        return len(self.events) == 0

    def addEvent(self, event):
        self.events.append(event)
        self.events.sort(key=lambda x: x.time)
        event.id = self.maxId
        self.maxId += 1

    def getNextEvent(self):
        if len(self.events) > 0:
            event = self.events.pop(0)
            return event
        return None
    
    # STR
    def __str__(self):
        return "\n".join([str(event) for event in self.events])
            
class Event:
    # INIT
    def __init__(self, time, action, actionArgument):
        self.id = None
        self.time = time
        self.action = action
        self.actionArgument = actionArgument

    # CALL
    def __call__(self):
        if callable(self.action):
            self.action(self.actionArgument)
        else:
            raise TypeError(f"Action {self.action} is not callable")

     # STR
    def __str__(self):
        action_str = "Bus #" + str(self.action.__self__.busNumber) if hasattr(self.action, '__self__') and hasattr(self.action.__self__, 'busNumber') else self.action
        return f"{int(self.time/60)}:{int(self.time%60)} - {action_str} ({self.actionArgument})"