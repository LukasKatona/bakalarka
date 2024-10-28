import time
from datetime import datetime, timedelta

simulationStartedAt = datetime.now()
modelTimeInMinutes = 0
timeSpeedScale = 0

def printCurrentTime():
    print(f"{(simulationStartedAt + timedelta(minutes=modelTimeInMinutes)).time().strftime('%H:%M')}")

def printCurrentTimeAndMessage(message):
    print(f"{(simulationStartedAt + timedelta(minutes=modelTimeInMinutes)).time().strftime('%H:%M')}: {message}")

def forwardModelTime(timeToAdvance):
    global modelTimeInMinutes
    modelTimeInMinutes += timeToAdvance

    # sleep for the time to advance
    if (timeSpeedScale == 0):
        return
    timeToAdvance *= 60
    timeToAdvance /= timeSpeedScale
    time.sleep(timeToAdvance)