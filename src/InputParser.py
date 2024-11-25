from models import BusStop, TimeTable

def parseBusStopsFromFile(file):
    busStops = []

    for line in file:
        line = line.strip()
        if line.startswith("#") or line == "":
            continue

        (name, timeDeltaToArrive) = line.split(":")
        busStops.append(BusStop(name.strip(), int(timeDeltaToArrive.strip())))
        
    return busStops

def parseTimeTableFromFile(file):
    timeTable = TimeTable()

    for line in file:
        line = line.strip()
        if line.startswith("#") or line == "":
            continue

        (hour, minutes) = line.split(":")

        if minutes == "":
            continue

        minutes = minutes.split(",")
        minutesInt = []
        for minute in minutes:
            minutesInt.append(int(minute.strip()))
        
        timeTable.addRow(int(hour), minutesInt)
        
    return timeTable