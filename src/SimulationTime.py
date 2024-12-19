from datetime import timedelta
class SimulationTime:
    # Static global variables
    startTime = None
    currentTime = None
    endTime = None

    # INIT
    def __init__(self, initialTime, endTime):
        SimulationTime.startTime = initialTime
        SimulationTime.currentTime = initialTime
        SimulationTime.endTime = endTime

    # METHODS
    @staticmethod
    def printCurrentTime():
        print(f"{(SimulationTime.startTime + timedelta(minutes=SimulationTime.currentTime)).time().strftime('%H:%M')}")

    @staticmethod
    def printCurrentTimeAndMessage(message):
        print(f"{(SimulationTime.startTime + timedelta(minutes=SimulationTime.currentTime)).time().strftime('%H:%M')}: {message}")

    @staticmethod
    def forward(eventTime):
        SimulationTime.currentTime = eventTime

    @staticmethod
    def getHour():
        return SimulationTime.currentTime // 60 % 24
