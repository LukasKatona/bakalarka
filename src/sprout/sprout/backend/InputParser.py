"""
This file contains InputParser class with static methods for parsing the input.

:author: Lukas Katona
"""

from .models import BusStop, TimeTable
from collections import namedtuple
import ast

HourRate = namedtuple('HourRate', ['hour', 'rate'])

class InputParser:    
    @staticmethod
    def parseBusStopsFromFile(file) -> list[BusStop]:
        """
        Parse the bus stops from a file.

        :param file: The file containing the bus stops.
        :type file: FileDescriptorOrPath
        :return: A list of bus stops.
        :rtype: list[BusStop]
        """
        with open(file, "r") as f:
            return InputParser._parseBusStopsFromLines(f)

    @staticmethod
    def parseBusStopsFromString(string: str) -> list[BusStop]:
        """
        Parse the bus stops from a string.

        :param string: The string containing the bus stops.
        :type string: str
        :return: A list of bus stops.
        :rtype: list[BusStop]
        """
        lines = string.split("\n")
        return InputParser._parseBusStopsFromLines(lines)

    @staticmethod
    def _parseBusStopsFromLines(lines) -> list[BusStop]:
        """
        Parse the bus stops from a list of lines.
        The line should contain the bus stops in the following format:
        name:timeDeltaToArrive:passengerArrivalRatesPerHour:leavingPassengersRate
        Example:
        Arbesova:3:[(5, 60), (6, 90), (7, 90), (8, 70), (9, 60), (10, 60), (11, 60), (12, 60), (13, 60), (14, 60), (15, 90), (16, 90), (17, 90), (18, 60), (19, 60), (20, 50), (21, 40), (22, 30)]:0.1

        :param lines: The list of lines containing the bus stops.
        :type lines: list[str] | TextIOWrapper[_WrappedBuffer]
        :return: A list of bus stops.
        :rtype: list[BusStop]
        """
        busStops = []

        for line in lines:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue

            name, timeDeltaToArrive, passengerArrivalRatesPerHour, leavingPassengersRate = line.split(":")
            parsedHourRate = [HourRate(hour, rate) for hour, rate in ast.literal_eval(passengerArrivalRatesPerHour)]
            busStops.append(
                BusStop(
                    name.strip(),
                    int(timeDeltaToArrive.strip()),
                    parsedHourRate,
                    float(leavingPassengersRate.strip())
                )
            )

        return busStops
    
    @staticmethod
    def parseTimeTableFromFile(file) -> TimeTable:
        """
        Parse the time table from a file.

        :param file: The file containing the time table.
        :type file: FileDescriptorOrPath
        :return: The time table.
        :rtype: TimeTable
        """
        with open(file, "r") as f:
            return InputParser._parseTimeTableFromLines(f)

    @staticmethod
    def parseTimeTableFromString(string: str) -> TimeTable:
        """
        Parse the time table from a string.

        :param string: The string containing the time table.
        :type string: str
        :return: The time table.
        :rtype: TimeTable
        """
        lines = string.split("\n")
        return InputParser._parseTimeTableFromLines(lines)

    @staticmethod
    def _parseTimeTableFromLines(lines) -> TimeTable:
        """
        Parse the time table from a list of lines.

        :param lines: The list of lines containing the time table.
        :type lines: list[str] | TextIOWrapper[_WrappedBuffer]
        :return: The time table.
        :rtype: TimeTable
        """
        timeTable = TimeTable()

        for line in lines:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue

            hour, minutes = line.split(":")

            if minutes == "":
                continue

            minutesInt = [int(minute.strip()) for minute in minutes.split(",")]
            timeTable.addRow(int(hour), minutesInt)

        return timeTable