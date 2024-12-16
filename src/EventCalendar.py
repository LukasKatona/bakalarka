class EventCalendar:
    def __init__(self):
        self.events = []
        self.maxId = 0

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
    
    def __str__(self):
        return "\n".join([str(event) for event in self.events])
            
class Event:
    def __init__(self, time, action, actionArgument):
        self.id = None
        self.time = time
        self.action = action
        self.actionArgument = actionArgument

    def __str__(self):
        return f"{int(self.time/60)}:{int(self.time%60)} - {self.action}"

    def __call__(self):
        if callable(self.action):
            self.action(self.actionArgument)
        else:
            print(self.action)