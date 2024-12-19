from models import BusStop, TimeTable
from collections import namedtuple
import ast

def parseBusStopsFromFile(file):
    busStops = []

    for line in file:
        line = line.strip()
        if line.startswith("#") or line == "":
            continue

        (name, timeDeltaToArrive, passengerArrivalRatesPerHour, leavingPassengersRate) = line.split(":")
        HourRate = namedtuple('HourRate', ['hour', 'rate'])
        parsedHourRate = [HourRate(hour, rate) for hour, rate in ast.literal_eval(passengerArrivalRatesPerHour)]
        busStops.append(BusStop(name.strip(), int(timeDeltaToArrive.strip()), parsedHourRate, float(leavingPassengersRate.strip())))
        
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