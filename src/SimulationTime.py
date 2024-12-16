import time
from datetime import datetime, timedelta

class SimulationTime:
    # INIT
    def __init__(self, initialTime, endTime):
        self.startTime = initialTime
        self.currentTime = initialTime
        self.endTime = endTime

    # METHODS
    def printCurrentTime(self):
        print(f"{(self.startTime + timedelta(minutes=self.currentTime)).time().strftime('%H:%M')}")

    def printCurrentTimeAndMessage(self, message):
        print(f"{(self.startTime + timedelta(minutes=self.currentTime)).time().strftime('%H:%M')}: {message}")

    def forward(self, eventTime):
        self.currentTime = eventTime