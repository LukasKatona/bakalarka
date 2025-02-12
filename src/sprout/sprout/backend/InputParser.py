from .models import BusStop, TimeTable
from collections import namedtuple
import ast

class InputParser:
    @staticmethod
    def parseBusStopsFromFile(file) -> list[BusStop]:
        busStopsFile = open(file, "r")
        busStops = []

        for line in busStopsFile:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue

            (name, timeDeltaToArrive, passengerArrivalRatesPerHour, leavingPassengersRate) = line.split(":")
            HourRate = namedtuple('HourRate', ['hour', 'rate'])
            parsedHourRate = [HourRate(hour, rate) for hour, rate in ast.literal_eval(passengerArrivalRatesPerHour)]
            busStops.append(BusStop(name.strip(), int(timeDeltaToArrive.strip()), parsedHourRate, float(leavingPassengersRate.strip())))
            
        busStopsFile.close()
        return busStops
    
    @staticmethod
    def parseBusStopsFromString(string) -> list[BusStop]:
        busStops = []
        lines = string.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue

            (name, timeDeltaToArrive, passengerArrivalRatesPerHour, leavingPassengersRate) = line.split(":")
            HourRate = namedtuple('HourRate', ['hour', 'rate'])
            parsedHourRate = [HourRate(hour, rate) for hour, rate in ast.literal_eval(passengerArrivalRatesPerHour)]
            busStops.append(BusStop(name.strip(), int(timeDeltaToArrive.strip()), parsedHourRate, float(leavingPassengersRate.strip())))
            
        return busStops

    @staticmethod
    def parseTimeTableFromFile(file) -> TimeTable:
        timeTableFile = open(file, "r")
        timeTable = TimeTable()

        for line in timeTableFile:
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
            
        timeTableFile.close()
        return timeTable
    
    @staticmethod
    def parseTimeTableFromString(string) -> TimeTable:
        timeTable = TimeTable()

        lines = string.split("\n")
        for line in lines:
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