"""
This file contains the Statistics class, which is used to gather information during simulation.

:author: Lukas Katona
"""

import matplotlib.pyplot as plt
import numpy as np

def averageStatistics(statsList: list['Statistics']) -> 'Statistics':
    """
    Calculate the average statistics from a list of statistics.

    :param statsList: List of statistics to be averaged.
    :type statsList: list[Statistics]
    :return: The average statistics.
    :rtype: Statistics
    """
    averageStat = Statistics()
    averageStat.language = statsList[0].language
    averageStat.totalNumberOfBuses = sum([x.totalNumberOfBuses for x in statsList]) / len(statsList)
    averageBusStopStat = BusStopStatistics("Agregated", statsList[0].language)
    averageBusStat = BusStatistics("Agregated", statsList[0].busStatistics.capacity, statsList[0].busStatistics.seats, statsList[0].language)

    for i in range(len(statsList[0].busStopStatistics.passengersArrivedPerHour)):
        averageBusStopStat.passengersArrivedPerHour.append((statsList[0].busStopStatistics.passengersArrivedPerHour[i][0], int(sum([x.busStopStatistics.passengersArrivedPerHour[i][1] for x in statsList]) / len(statsList))))
    for i in range(len(statsList[0].busStopStatistics.passengersDepartedPerHour)):
        averageBusStopStat.passengersDepartedPerHour.append((statsList[0].busStopStatistics.passengersDepartedPerHour[i][0], int(sum([x.busStopStatistics.passengersDepartedPerHour[i][1] for x in statsList]) / len(statsList))))
    for i in range(len(statsList[0].busStopStatistics.passengersLeftUnboardedPerHour)):
        averageBusStopStat.passengersLeftUnboardedPerHour.append((statsList[0].busStopStatistics.passengersLeftUnboardedPerHour[i][0], int(sum([x.busStopStatistics.passengersLeftUnboardedPerHour[i][1] for x in statsList]) / len(statsList))))
    for i in range(len(statsList[0].busStopStatistics.timeSpentWaitingPerHour)):
        averageBusStopStat.timeSpentWaitingPerHour.append((statsList[0].busStopStatistics.timeSpentWaitingPerHour[i][0], int(sum([x.busStopStatistics.timeSpentWaitingPerHour[i][1] for x in statsList]) / len(statsList))))
    averageBusStopStat.agregateTotal()
    averageBusStopStat.totalPassengersDeparted = averageBusStopStat.totalPassengersArrived - averageBusStopStat.totalPassengersLeftUnboarded
    averageStat.busStopStatistics = averageBusStopStat
    
    averageBusStat.totalPassengersTransported = averageBusStopStat.totalPassengersDeparted
    for i in range(len(statsList[0].busStatistics.loadPerBusStop)):
        averageBusStat.loadPerBusStop.append((statsList[0].busStatistics.loadPerBusStop[i][0], int(sum([x.busStatistics.loadPerBusStop[i][1] for x in statsList]) / len(statsList))))
    for i in range(len(statsList[0].busStatistics.loadInPercentPerBusStop)):
        averageBusStat.loadInPercentPerBusStop.append((statsList[0].busStatistics.loadInPercentPerBusStop[i][0], sum([x.busStatistics.loadInPercentPerBusStop[i][1] for x in statsList]) / len(statsList)))
    averageBusStat.agregateTotal()
    averageStat.busStatistics = averageBusStat
    
    averageStat.averagePassengerSatisfaction = sum([x.averagePassengerSatisfaction for x in statsList]) / len(statsList)
    
    return averageStat

def keyValuePairArrayToString(keyValuePairArray: list[tuple[str | int, int | float]]) -> str:
    """
    Convert a list of key-value pairs to a string.

    :param keyValuePairArray: List of key-value pairs to be converted to a string.
    :type keyValuePairArray: list[tuple[str | int, int | float]]
    :return: String representation of the key-value pairs.
    :rtype: str
    """
    return "\n".join([f"{x[0]}: {x[1]}" for x in keyValuePairArray])

class Statistics:
    # INIT
    def __init__(self, totalNumberOfBuses=0, busStopStatistics=None, busStatistics=None, language="en"):
        self.totalNumberOfBuses = totalNumberOfBuses
        self.language = language
        if busStopStatistics is None:
            busStopStatistics = []
        else:
            self.busStopStatistics = self.agregateBusStopStatistics(busStopStatistics)
        if busStatistics is None:
            busStatistics = []
            self.averagePassengerSatisfaction = 0
        else:
            self.busStatistics = self.agregateBusStatistics(busStatistics)
            self.averagePassengerSatisfaction = sum(self.busStatistics.passengerSatisfactions)/len(self.busStatistics.passengerSatisfactions)
        
    # METHODS
    def agregateBusStopStatistics(self, busStopStatistics: list['BusStopStatistics']) -> 'BusStopStatistics':
        """
        Agregate bus stop statistics from a list of bus stop statistics.

        :param busStopStatistics: List of bus stop statistics to be agregated.
        :type busStopStatistics: list[BusStopStatistics]
        :return: The agregated bus stop statistics.
        :rtype: BusStopStatistics
        """
        busStopStatisticsAgregated = BusStopStatistics("Agregated", self.language)
        for busStop in busStopStatistics:
            for hourValuePair in busStop.passengersArrivedPerHour:
                busStopStatisticsAgregated.updatePassengersArrivedPerHour(hourValuePair[1], hourValuePair[0])
            for hourValuePair in busStop.passengersDepartedPerHour:
                busStopStatisticsAgregated.updatePassengersDepartedPerHour(hourValuePair[1], hourValuePair[0])
            for hourValuePair in busStop.passengersLeftUnboardedPerHour:
                busStopStatisticsAgregated.updatePassengersLeftUnboardedPerHour(hourValuePair[1], hourValuePair[0])
            for hourValuePair in busStop.timeSpentWaitingPerHour:
                busStopStatisticsAgregated.updateTimeSpentWaitingPerHour(hourValuePair[1], hourValuePair[0])
        busStopStatisticsAgregated.agregateTotal()
        return busStopStatisticsAgregated

    def agregateBusStatistics(self, busStatistics: list['BusStatistics']) -> 'BusStatistics':
        """
        Agregate bus statistics from a list of bus statistics.

        :param busStatistics: List of bus statistics to be agregated.
        :type busStatistics: list[BusStatistics]
        :return: The agregated bus statistics.
        :rtype: BusStatistics
        """
        busStatisticsAgregated = BusStatistics("Agregated", busStatistics[0].capacity, busStatistics[0].seats, self.language)
        loadPerBusStop = {}
        for bus in busStatistics:
            for nameValuePair in bus.loadPerBusStop:
                if nameValuePair[0] not in loadPerBusStop:
                    loadPerBusStop[nameValuePair[0]] = []
                loadPerBusStop[nameValuePair[0]].append(nameValuePair[1])
            busStatisticsAgregated.updateTotalPassengersTransported(bus.totalPassengersTransported)
            busStatisticsAgregated.passengerSatisfactions += bus.passengerSatisfactions
        
        for busStopName, loads in loadPerBusStop.items():
            averageLoad = sum(loads) / len(loads)
            busStatisticsAgregated.updateLoadPerBusStop(averageLoad, busStopName)
        
        busStatisticsAgregated.agregateTotal()
        return busStatisticsAgregated
    
    # CLEAR
    def clear(self):
        """
        Clear the statistics.
        """
        self.totalNumberOfBuses = 0
        self.busStopStatistics.clear()
        self.busStatistics.clear()

    # STR
    def print(self):
        if (self.language == "sk"):
            print( "================================================================\n" + \
                "Štatistiky\n" + \
                "================================================================\n" + \
                f"Celkový počet autobusov: {self.totalNumberOfBuses}\n" + \
                f"Štatistiky zastávok:\n{self.busStopStatistics}\n" + \
                f"Štatistiky autobusov:\n{self.busStatistics}\n" + \
                "================================================================\n")
        else:
            print( "================================================================\n" + \
                "Statistics\n" + \
                "================================================================\n" + \
                f"Total number of buses: {self.totalNumberOfBuses}\n" + \
                f"Bus stop statistics:\n{self.busStopStatistics}\n" + \
                f"Bus statistics:\n{self.busStatistics}\n" + \
                "================================================================\n")

# ------------------------------ BUSSTOP ------------------------------
class BusStopStatistics:
    # INIT
    def __init__(self, name, language="en"):
        self.name = name
        self.language = language
        # total
        self.totalPassengersArrived = 0
        self.totalPassengersDeparted = 0
        self.totalPassengersLeftUnboarded = 0
        self.totalTimeSpentWaiting = 0
        # per hour
        self.passengersArrivedPerHour = []
        self.passengersDepartedPerHour = []
        self.passengersLeftUnboardedPerHour = []
        self.timeSpentWaitingPerHour = []

    # PER HOUR
    def updatePassengersArrivedPerHour(self, passengersArrived: int, hour: int):
        """
        Update the number of passengers arrived per hour.

        :param passengersArrived: The number of passengers arrived.
        :type passengersArrived: int
        :param hour: The hour of the day (0-23).
        :type hour: int
        """
        for i in range(len(self.passengersArrivedPerHour)):
            if self.passengersArrivedPerHour[i][0] == hour:
                self.passengersArrivedPerHour[i] = (hour, self.passengersArrivedPerHour[i][1] + passengersArrived)
                return
        self.passengersArrivedPerHour.append((hour, passengersArrived))

    def updatePassengersDepartedPerHour(self, passengersDeparted: int, hour: int):
        """
        Update the number of passengers departed per hour.

        :param passengersDeparted: The number of passengers departed.
        :type passengersDeparted: int
        :param hour: The hour of the day (0-23).
        :type hour: int
        """
        for i in range(len(self.passengersDepartedPerHour)):
            if self.passengersDepartedPerHour[i][0] == hour:
                self.passengersDepartedPerHour[i] = (hour, self.passengersDepartedPerHour[i][1] + passengersDeparted)
                return
        self.passengersDepartedPerHour.append((hour, passengersDeparted))

    def updatePassengersLeftUnboardedPerHour(self, passengersWaiting: int, hour: int):
        """
        Update the number of passengers left unboarded per hour.

        :param passengersWaiting: The number of passengers left unboarded.
        :type passengersWaiting: int
        :param hour: The hour of the day (0-23).
        :type hour: int
        """
        for i in range(len(self.passengersLeftUnboardedPerHour)):
            if self.passengersLeftUnboardedPerHour[i][0] == hour:
                self.passengersLeftUnboardedPerHour[i] = (hour, self.passengersLeftUnboardedPerHour[i][1] + passengersWaiting)
                return
        self.passengersLeftUnboardedPerHour.append((hour, passengersWaiting))

    def updateTimeSpentWaitingPerHour(self, timeSpentWaiting: int, hour: int):
        """
        Update the time spent waiting per hour.

        :param timeSpentWaiting: The time spent waiting (in minutes).
        :type timeSpentWaiting: int
        :param hour: The hour of the day (0-23).
        :type hour: int
        """
        for i in range(len(self.timeSpentWaitingPerHour)):
            if self.timeSpentWaitingPerHour[i][0] == hour:
                self.timeSpentWaitingPerHour[i] = (hour, self.timeSpentWaitingPerHour[i][1] + timeSpentWaiting)
                return
        self.timeSpentWaitingPerHour.append((hour, timeSpentWaiting))

    # TOTAL
    def agregateTotal(self):
        """
        Agregate the total statistics from the per hour statistics.
        """
        self.totalPassengersArrived = sum([x[1] for x in self.passengersArrivedPerHour])
        self.totalPassengersDeparted = sum([x[1] for x in self.passengersDepartedPerHour])
        self.totalPassengersLeftUnboarded = sum([x[1] for x in self.passengersLeftUnboardedPerHour])
        self.totalTimeSpentWaiting = sum([x[1] for x in self.timeSpentWaitingPerHour])

    # CLEAR
    def clear(self):
        """
        Clear the statistics.
        """
        self.totalPassengersArrived = 0
        self.totalPassengersDeparted = 0
        self.totalPassengersLeftUnboarded = 0
        self.totalTimeSpentWaiting = 0
        self.passengersArrivedPerHour = []
        self.passengersDepartedPerHour = []
        self.passengersLeftUnboardedPerHour = []
        self.timeSpentWaitingPerHour = []

    # STR
    def __str__(self):
        if (self.language == "sk"):
            return "=============================================================\n" + \
                f"Zastávka: {self.name}\n" + \
                "=============================================================\n" + \
                f"Celkový počet prichádzajúcich cestujúcich: {self.totalPassengersArrived}\n" + \
                f"Celkový počet odchádzajúcich cestujúcich: {self.totalPassengersDeparted}\n" + \
                f"Celkový čas strávený čakaním: {self.totalTimeSpentWaiting} minút\n" + \
                f"Celkový počet cestujúcich, ktorí ostali neobslúžení: {self.totalPassengersLeftUnboarded}\n" + \
                f"Prichádzajúci cestujúci za hodinu:\n{keyValuePairArrayToString(self.passengersArrivedPerHour)}\n" + \
                f"Odchádzajúci cestujúci za hodinu:\n{keyValuePairArrayToString(self.passengersDepartedPerHour)}\n" + \
                f"Cestujúci čakajúci na ďalší autobus za hodinu:\n{keyValuePairArrayToString(self.passengersLeftUnboardedPerHour)}\n" + \
                f"Čas strávený čakaním za hodinu (v minútach):\n{keyValuePairArrayToString(self.timeSpentWaitingPerHour)}\n" + \
                "=============================================================\n"
        else:
            return "=============================================================\n" + \
                f"Bus Stop: {self.name}\n" + \
                "=============================================================\n" + \
                f"Total passengers arrived: {self.totalPassengersArrived}\n" + \
                f"Total passengers departed: {self.totalPassengersDeparted}\n" + \
                f"Total time spent waiting: {self.totalTimeSpentWaiting} minutes\n" + \
                f"Total passengers left unboarded: {self.totalPassengersLeftUnboarded}\n" + \
                f"Passengers arrived per hour:\n{keyValuePairArrayToString(self.passengersArrivedPerHour)}\n" + \
                f"Passengers departed per hour:\n{keyValuePairArrayToString(self.passengersDepartedPerHour)}\n" + \
                f"Passengers waiting for next bus per hour:\n{keyValuePairArrayToString(self.passengersLeftUnboardedPerHour)}\n" + \
                f"Time spent waiting per hour (in minutes):\n{keyValuePairArrayToString(self.timeSpentWaitingPerHour)}\n" + \
                "=============================================================\n"
    
    
# -------------------------------- BUS --------------------------------
class BusStatistics:
    # INIT
    def __init__(self, busNumber, capacity, seats, language="en"):
        self.busNumber = busNumber
        self.capacity = capacity
        self.seats = seats
        self.language = language
        # total
        self.averageLoad = 0
        self.averageLoadInPercent = 0
        self.totalPassengersTransported = 0
        # per bus stop
        self.loadPerBusStop = []
        self.loadInPercentPerBusStop = []
        # passengers
        self.passengerSatisfactions = []
    
    # PER BUS STOP
    def updateLoadPerBusStop(self, load: int, busStopName: str):
        """
        Update the load per bus stop.

        :param load: The load of the bus at the bus stop.
        :type load: int
        :param busStopName: The name of the bus stop.
        :type busStopName: str
        """
        self.loadPerBusStop.append((busStopName, load))
        self.loadInPercentPerBusStop.append((busStopName, load / self.capacity))

    # PASSENGERS
    def updatePassengerSatisfactions(self, satisfaction: float):
        """
        Update the passenger satisfaction.

        :param satisfaction: The satisfaction of the passenger.
        :type satisfaction: float
        """
        self.passengerSatisfactions.append(satisfaction)

    # TOTAL
    def agregateTotal(self):
        """
        Agregate the total statistics from the per bus stop statistics.
        """
        self.averageLoad = sum([x[1] for x in self.loadPerBusStop]) / len(self.loadPerBusStop)
        self.averageLoadInPercent = self.averageLoad / self.capacity
    
    def updateTotalPassengersTransported(self, passengersTransported: int):
        """
        Update the total number of passengers transported.

        :param passengersTransported: The number of passengers transported.
        :type passengersTransported: int
        """
        self.totalPassengersTransported += passengersTransported

    # CLEAR
    def clear(self):
        """
        Clear the statistics.
        """
        self.averageLoad = 0
        self.averageLoadInPercent = 0
        self.totalPassengersTransported = 0
        self.loadPerBusStop = []
        self.loadInPercentPerBusStop = []

    # STR
    def __str__(self):
        if (self.language == "sk"):
            return "=============================================================\n" + \
               f"Autobus #{self.busNumber}\n" + \
               "=============================================================\n" + \
               f"Priemerná naplnenosť: {self.averageLoad}\n" + \
               f"Priemerná naplnenosť v percentách: {self.averageLoadInPercent}\n" + \
               f"Celkový počet prepravených cestujúcich: {self.totalPassengersTransported}\n" + \
               f"Naplnenosť na zastávku:\n{keyValuePairArrayToString(self.loadPerBusStop)}\n" + \
               f"Naplnenosť v percentách na zastávku:\n{keyValuePairArrayToString(self.loadInPercentPerBusStop)}\n" + \
               "=============================================================\n"
        else:
            return "=============================================================\n" + \
               f"Bus #{self.busNumber}\n" + \
               "=============================================================\n" + \
               f"Average load: {self.averageLoad}\n" + \
               f"Average load in percent: {self.averageLoadInPercent}\n" + \
               f"Total passengers transported: {self.totalPassengersTransported}\n" + \
               f"Load per bus stop:\n{keyValuePairArrayToString(self.loadPerBusStop)}\n" + \
               f"Load in percent per bus stop:\n{keyValuePairArrayToString(self.loadInPercentPerBusStop)}\n" + \
               "=============================================================\n"
