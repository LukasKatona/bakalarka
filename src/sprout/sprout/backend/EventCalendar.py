"""
This file contains event calendar class and event class, both used in the simulation based on events.
"""

class Event:
    # INIT
    def __init__(self, time, action, actionArgument):
        self.id = None
        self.time = time
        self.action = action
        self.actionArgument = actionArgument

    # CALL
    def __call__(self):
        """
        Call the action associated with the event, with the action arguments.

        :raises TypeError: If the action is not callable.
        """
        if callable(self.action):
            self.action(self.actionArgument)
        else:
            raise TypeError(f"Action {self.action} is not callable")

     # STR
    def __str__(self):
        action_str = "Bus #" + str(self.action.__self__.busNumber) if hasattr(self.action, '__self__') and hasattr(self.action.__self__, 'busNumber') else self.action
        return f"{int(self.time/60)}:{int(self.time%60)} - {action_str} ({self.actionArgument})"
    
class EventCalendar:
    # INIT
    def __init__(self):
        self.events = []
        self.maxId = 0

    # METHODS
    def isEmpty(self) -> bool:
        """
        Check if the event calendar is empty.

        :return: True if the event calendar is empty, False otherwise.
        :rtype: bool
        """
        return len(self.events) == 0

    def addEvent(self, event: Event):
        """
        Add an event to the event calendar.

        :param event: The event to be added.
        :type event: Event
        """
        self.events.append(event)
        self.events.sort(key=lambda x: x.time)
        event.id = self.maxId
        self.maxId += 1

    def getNextEvent(self) -> Event | None:
        """
        Get the next event from the event calendar, then remove it from the calendar.

        :return: The next event in the calendar, or None if the calendar is empty.
        :rtype: Event | None
        """
        if len(self.events) > 0:
            event = self.events.pop(0)
            return event
        return None
    
    # STR
    def __str__(self):
        return "\n".join([str(event) for event in self.events])
