import matplotlib.pyplot as plt
import numpy as np

class Statistics:
    # Static global variables
    totalNumberOfBuses = 0
    busStopStatistics = None
    busStatistics = None
    language = "en"

    # INIT
    def __init__(self, totalNumberOfBuses, busStopStatistics, busStatistics, language):
        Statistics.totalNumberOfBuses = totalNumberOfBuses
        Statistics.busStopStatistics = Statistics.agregateBusStopStatistics(busStopStatistics)
        Statistics.busStatistics = Statistics.agregateBusStatistics(busStatistics)
        Statistics.language = language

    # METHODS
    @staticmethod
    def agregateBusStopStatistics(busStopStatistics):
        busStopStatisticsAgregated = BusStopStatistics("Agregated")
        for busStop in busStopStatistics:
            for hourValuePair in busStop.passengersArrivedPerHour:
                busStopStatisticsAgregated.updatePassengersArrivedPerHour(hourValuePair[1], hourValuePair[0])
            for hourValuePair in busStop.passengersDepartedPerHour:
                busStopStatisticsAgregated.updatePassengersDepartedPerHour(hourValuePair[1], hourValuePair[0])
            for hourValuePair in busStop.passengersWaitingForNextBusPerHour:
                busStopStatisticsAgregated.updatePassengersWaitingForNextBusPerHour(hourValuePair[1], hourValuePair[0])
            for hourValuePair in busStop.timeSpentWaitingPerHour:
                busStopStatisticsAgregated.updateTimeSpentWaitingPerHour(hourValuePair[1], hourValuePair[0])
            busStopStatisticsAgregated.updateTotalPassangersLeftUnboarded(busStop.totalPassangersLeftUnboarded)
        busStopStatisticsAgregated.agregateTotal()
        return busStopStatisticsAgregated

    @staticmethod
    def agregateBusStatistics(busStatistics):
        busStatisticsAgregated = BusStatistics("Agregated", 80)
        loadPerBusStop = {}
        for bus in busStatistics:
            for nameValuePair in bus.loadPerBusStop:
                if nameValuePair[0] not in loadPerBusStop:
                    loadPerBusStop[nameValuePair[0]] = []
                loadPerBusStop[nameValuePair[0]].append(nameValuePair[1])
            busStatisticsAgregated.updateTotalPassengersTransported(bus.totalPassengersTransported)
        
        for busStopName, loads in loadPerBusStop.items():
            averageLoad = sum(loads) / len(loads)
            busStatisticsAgregated.updateLoadPerBusStop(averageLoad, busStopName)
        
        busStatisticsAgregated.agregateTotal()
        return busStatisticsAgregated
    
    # CLEAR
    @staticmethod
    def clear():
        Statistics.totalNumberOfBuses = 0
        Statistics.busStopStatistics.clear()
        Statistics.busStatistics.clear()

    # SAVE GRAPHS
    @staticmethod
    def saveAllGraphs():
        Statistics.busStopStatistics.savePassengersArrivedPerHour("outputs/passengersArrivedPerHour.png")
        Statistics.busStopStatistics.savePassengersDepartedPerHour("outputs/passengersDepartedPerHour.png")
        Statistics.busStopStatistics.savePassengersWaitingForNextBusPerHour("outputs/passengersWaitingForNextBusPerHour.png")
        Statistics.busStopStatistics.saveTimeSpentWaitingPerHour("outputs/timeSpentWaitingPerHour.png")
        Statistics.busStatistics.saveLoadPerBusStop("outputs/loadPerBusStop.png")
        Statistics.busStatistics.saveLoadInPercentPerBusStop("outputs/loadInPercentPerBusStop.png")

    # STR
    @staticmethod
    def print():
        if (Statistics.language == "sk"):
            print( "================================================================\n" + \
                "Štatistiky\n" + \
                "================================================================\n" + \
                f"Celkový počet autobusov: {Statistics.totalNumberOfBuses}\n" + \
                f"Štatistiky zastávok:\n{Statistics.busStopStatistics}\n" + \
                f"Štatistiky autobusov:\n{Statistics.busStatistics}\n" + \
                "================================================================\n")
        else:
            print( "================================================================\n" + \
                "Statistics\n" + \
                "================================================================\n" + \
                f"Total number of buses: {Statistics.totalNumberOfBuses}\n" + \
                f"Bus stop statistics:\n{Statistics.busStopStatistics}\n" + \
                f"Bus statistics:\n{Statistics.busStatistics}\n" + \
                "================================================================\n")

    @staticmethod
    def keyValuePairArrayToString(keyValuePairArray):
        return "\n".join([f"{x[0]}: {x[1]}" for x in keyValuePairArray])

# ------------------------------ BUSSTOP ------------------------------
class BusStopStatistics:
    # INIT
    def __init__(self, name):
        self.name = name
        # total
        self.totalPassengersArrived = 0
        self.totalPassengersDeparted = 0
        self.totalPassengersWaitingForNextBus = 0
        self.totalTimeSpentWaiting = 0
        self.totalPassangersLeftUnboarded = 0
        # per hour
        self.passengersArrivedPerHour = []
        self.passengersDepartedPerHour = []
        self.passengersWaitingForNextBusPerHour = []
        self.timeSpentWaitingPerHour = []

    # PER HOUR
    def updatePassengersArrivedPerHour(self, passengersArrived, hour):
        for i in range(len(self.passengersArrivedPerHour)):
            if self.passengersArrivedPerHour[i][0] == hour:
                self.passengersArrivedPerHour[i] = (hour, self.passengersArrivedPerHour[i][1] + passengersArrived)
                return
        self.passengersArrivedPerHour.append((hour, passengersArrived))

    def updatePassengersDepartedPerHour(self, passengersDeparted, hour):
        for i in range(len(self.passengersDepartedPerHour)):
            if self.passengersDepartedPerHour[i][0] == hour:
                self.passengersDepartedPerHour[i] = (hour, self.passengersDepartedPerHour[i][1] + passengersDeparted)
                return
        self.passengersDepartedPerHour.append((hour, passengersDeparted))

    def updatePassengersWaitingForNextBusPerHour(self, passengersWaiting, hour):
        for i in range(len(self.passengersWaitingForNextBusPerHour)):
            if self.passengersWaitingForNextBusPerHour[i][0] == hour:
                self.passengersWaitingForNextBusPerHour[i] = (hour, self.passengersWaitingForNextBusPerHour[i][1] + passengersWaiting)
                return
        self.passengersWaitingForNextBusPerHour.append((hour, passengersWaiting))

    def updateTimeSpentWaitingPerHour(self, timeSpentWaiting, hour):
        for i in range(len(self.timeSpentWaitingPerHour)):
            if self.timeSpentWaitingPerHour[i][0] == hour:
                self.timeSpentWaitingPerHour[i] = (hour, self.timeSpentWaitingPerHour[i][1] + timeSpentWaiting)
                return
        self.timeSpentWaitingPerHour.append((hour, timeSpentWaiting))

    # TOTAL
    def agregateTotal(self):
        self.totalPassengersArrived = sum([x[1] for x in self.passengersArrivedPerHour])
        self.totalPassengersDeparted = sum([x[1] for x in self.passengersDepartedPerHour])
        self.totalPassengersWaitingForNextBus = sum([x[1] for x in self.passengersWaitingForNextBusPerHour])
        self.totalTimeSpentWaiting = sum([x[1] for x in self.timeSpentWaitingPerHour])
    
    def updateTotalPassangersLeftUnboarded(self, passengersLeftUnboarded):
        self.totalPassangersLeftUnboarded += passengersLeftUnboarded

    # CLEAR
    def clear(self):
        self.totalPassengersArrived = 0
        self.totalPassengersDeparted = 0
        self.totalPassengersWaitingForNextBus = 0
        self.totalTimeSpentWaiting = 0
        self.totalPassangersLeftUnboarded = 0
        self.passengersArrivedPerHour = []
        self.passengersDepartedPerHour = []
        self.passengersWaitingForNextBusPerHour = []
        self.timeSpentWaitingPerHour = []

    # SHOW GRAPHS
    def showPassengersArrivedPerHour(self):
        self.plotPassengersArrivedPerHour()
        plt.show()
    
    def showPassengersDepartedPerHour(self):
        self.plotPassengersDepartedPerHour()
        plt.show()
    
    def showPassengersWaitingForNextBusPerHour(self):
        self.plotPassengersWaitingForNextBusPerHour()
        plt.show()
    
    def showTimeSpentWaitingPerHour(self):
        self.plotTimeSpentWaitingPerHour()
        plt.show()
    
    # SAVE GRAPHS
    def savePassengersArrivedPerHour(self, filename):
        self.plotPassengersArrivedPerHour()
        plt.savefig(filename)
        plt.close()
    
    def savePassengersDepartedPerHour(self, filename):
        self.plotPassengersDepartedPerHour()
        plt.savefig(filename)
        plt.close()
    
    def savePassengersWaitingForNextBusPerHour(self, filename):
        self.plotPassengersWaitingForNextBusPerHour()
        plt.savefig(filename)
        plt.close()
    
    def saveTimeSpentWaitingPerHour(self, filename):
        self.plotTimeSpentWaitingPerHour()
        plt.savefig(filename)
        plt.close()

    # PLOT
    def plotPassengersArrivedPerHour(self):
        x = [x[0] for x in self.passengersArrivedPerHour]
        y = [x[1] for x in self.passengersArrivedPerHour]
        plt.bar(x, y)
        plt.xlabel('Hodina' if Statistics.language == "sk" else 'Hour')
        plt.ylabel('Cestujúci' if Statistics.language == "sk" else 'Passengers')
        plt.xlim(0, 24)
        plt.xticks(np.arange(0, 25, 1))
        if self.name != "Agregated":
            plt.title(f'Cestujúci prichádzajúci na {self.name}' if Statistics.language == "sk" else f'Passengers Arrived at {self.name}')
        else:
            plt.title('Cestujúci prichádzajúci na všetky zastávky' if Statistics.language == "sk" else 'Passengers Arrived at All Bus Stops')

    def plotPassengersDepartedPerHour(self):
        x = [x[0] for x in self.passengersDepartedPerHour]
        y = [x[1] for x in self.passengersDepartedPerHour]
        plt.bar(x, y)
        plt.xlabel('Hodina' if Statistics.language == "sk" else 'Hour')
        plt.ylabel('Cestujúci' if Statistics.language == "sk" else 'Passengers')
        plt.xlim(0, 24)
        plt.xticks(np.arange(0, 25, 1))
        if self.name != "Agregated":
            plt.title(f'Cestujúci odchádzajúci z {self.name}' if Statistics.language == "sk" else f'Passengers Departed at {self.name}')
        else:
            plt.title('Cestujúci odchádzajúci zo všetkých zastávok' if Statistics.language == "sk" else 'Passengers Departed at All Bus Stops')

    def plotPassengersWaitingForNextBusPerHour(self):
        x = [x[0] for x in self.passengersWaitingForNextBusPerHour]
        y = [x[1] for x in self.passengersWaitingForNextBusPerHour]
        plt.bar(x, y)
        plt.xlabel('Hodina' if Statistics.language == "sk" else 'Hour')
        plt.ylabel('Cestujúci' if Statistics.language == "sk" else 'Passengers')
        plt.xlim(0, 24)
        plt.xticks(np.arange(0, 25, 1))
        if self.name != "Agregated":
            plt.title(f'Cestujúci čakajúci na ďalší autobus na {self.name}' if Statistics.language == "sk" else f'Passengers Waiting for Next Bus at {self.name}')
        else:
            plt.title('Cestujúci čakajúci na ďalší autobus na všetkých zastávkach' if Statistics.language == "sk" else 'Passengers Waiting for Next Bus at All Bus Stops')

    def plotTimeSpentWaitingPerHour(self):
        x = [x[0] for x in self.timeSpentWaitingPerHour]
        y = [x[1] for x in self.timeSpentWaitingPerHour]
        plt.bar(x, y)
        plt.xlabel('Hodina' if Statistics.language == "sk" else 'Hour')
        plt.ylabel('Čas (minúty)' if Statistics.language == "sk" else 'Time (minutes)')
        plt.xlim(0, 24)
        plt.xticks(np.arange(0, 25, 1))
        if self.name != "Agregated":
            plt.title(f'Čas strávený čakaním cestujúcich na {self.name}' if Statistics.language == "sk" else f'Time Passengers Spent Waiting at {self.name}')
        else:
            plt.title('Čas strávený čakaním cestujúcich na všetkých zastávkach' if Statistics.language == "sk" else 'Time Passengers Spent Waiting at All Bus Stops')

    # STR
    def __str__(self):
        if (Statistics.language == "sk"):
            return "=============================================================\n" + \
                f"Zastávka: {self.name}\n" + \
                "=============================================================\n" + \
                f"Celkový počet prichádzajúcich cestujúcich: {self.totalPassengersArrived}\n" + \
                f"Celkový počet odchádzajúcich cestujúcich: {self.totalPassengersDeparted}\n" + \
                f"Celkový počet cestujúcich čakajúcich na ďalší autobus: {self.totalPassengersWaitingForNextBus}\n" + \
                f"Celkový čas strávený čakaním: {self.totalTimeSpentWaiting} minút\n" + \
                f"Celkový počet cestujúcich, ktorí ostali neobslúžení: {self.totalPassangersLeftUnboarded}\n" + \
                f"Prichádzajúci cestujúci za hodinu:\n{Statistics.keyValuePairArrayToString(self.passengersArrivedPerHour)}\n" + \
                f"Odchádzajúci cestujúci za hodinu:\n{Statistics.keyValuePairArrayToString(self.passengersDepartedPerHour)}\n" + \
                f"Cestujúci čakajúci na ďalší autobus za hodinu:\n{Statistics.keyValuePairArrayToString(self.passengersWaitingForNextBusPerHour)}\n" + \
                f"Čas strávený čakaním za hodinu (v minútach):\n{Statistics.keyValuePairArrayToString(self.timeSpentWaitingPerHour)}\n" + \
                "=============================================================\n"
        else:
            return "=============================================================\n" + \
                f"Bus Stop: {self.name}\n" + \
                "=============================================================\n" + \
                f"Total passengers arrived: {self.totalPassengersArrived}\n" + \
                f"Total passengers departed: {self.totalPassengersDeparted}\n" + \
                f"Total passengers waited for next bus: {self.totalPassengersWaitingForNextBus}\n" + \
                f"Total time spent waiting: {self.totalTimeSpentWaiting} minutes\n" + \
                f"Total passangers left unboarded: {self.totalPassangersLeftUnboarded}\n" + \
                f"Passengers arrived per hour:\n{Statistics.keyValuePairArrayToString(self.passengersArrivedPerHour)}\n" + \
                f"Passengers departed per hour:\n{Statistics.keyValuePairArrayToString(self.passengersDepartedPerHour)}\n" + \
                f"Passengers waiting for next bus per hour:\n{Statistics.keyValuePairArrayToString(self.passengersWaitingForNextBusPerHour)}\n" + \
                f"Time spent waiting per hour (in minutes):\n{Statistics.keyValuePairArrayToString(self.timeSpentWaitingPerHour)}\n" + \
                "=============================================================\n"
    
# -------------------------------- BUS --------------------------------
class BusStatistics:
    # INIT
    def __init__(self, busNumber, capacity):
        self.busNumber = busNumber
        self.capacity = capacity
        # total
        self.averageLoad = 0
        self.averageLoadInPercent = 0
        self.totalPassengersTransported = 0
        # per bus stop
        self.loadPerBusStop = []
        self.LoadInPercentPerBusStop = []
    
    # PER BUS STOP
    def updateLoadPerBusStop(self, load, busStopName):
        self.loadPerBusStop.append((busStopName, load))
        self.LoadInPercentPerBusStop.append((busStopName, load / self.capacity))

    # TOTAL
    def agregateTotal(self):
        self.averageLoad = sum([x[1] for x in self.loadPerBusStop]) / len(self.loadPerBusStop)
        self.averageLoadInPercent = sum([x[1] for x in self.LoadInPercentPerBusStop]) / len(self.LoadInPercentPerBusStop)
    
    def updateTotalPassengersTransported(self, passengersTransported):
        self.totalPassengersTransported += passengersTransported

    # CLEAR
    def clear(self):
        self.averageLoad = 0
        self.averageLoadInPercent = 0
        self.totalPassengersTransported = 0
        self.loadPerBusStop = []
        self.LoadInPercentPerBusStop = []

    # SHOW GRAPHS
    def showLoadPerBusStop(self):
        self.plotLoadPerBusStop()
        plt.show()
    
    def showLoadInPercentPerBusStop(self):
        self.plotLoadInPercentPerBusStop()
        plt.show()

    # SAVE GRAPHS
    def saveLoadPerBusStop(self, filename):
        self.plotLoadPerBusStop()
        plt.savefig(filename)
        plt.close()
    
    def saveLoadInPercentPerBusStop(self, filename):
        self.plotLoadInPercentPerBusStop()
        plt.savefig(filename)
        plt.close()

    # PLOT
    def plotLoadPerBusStop(self):
        x = np.arange(len(self.loadPerBusStop))
        y = [x[1] for x in self.loadPerBusStop][::-1]
        plt.figure(figsize=(15, 6))
        plt.barh(x, y)
        plt.yticks(x, [x[0] for x in self.loadPerBusStop][::-1])
        plt.axvline(self.averageLoad, color='r', linestyle='--', label=f'Priemerná naplnenosť: {self.averageLoad:.2f}' if Statistics.language == "sk" else f'Average Load: {self.averageLoad:.2f}')
        plt.xlabel('Naplnenosť' if Statistics.language == "sk" else 'Load')
        plt.ylabel('Autobusová zastávka' if Statistics.language == "sk" else 'Bus Stop')
        plt.xlim(0, self.capacity)
        plt.legend()
        if self.busNumber != "Agregated":
            plt.title(f'Naplnenosť autobusu #{self.busNumber} na zastávku' if Statistics.language == "sk" else f'Bus #{self.busNumber} Load per Bus Stop')
        else:
            plt.title(f'Priemerná naplnenosť autobusov na zastávku' if Statistics.language == "sk" else f'Average Bus Load per Bus Stop')

    def plotLoadInPercentPerBusStop(self):
        x = np.arange(len(self.LoadInPercentPerBusStop))
        y = [x[1] for x in self.LoadInPercentPerBusStop][::-1]
        plt.figure(figsize=(15, 6))
        plt.barh(x, y)
        plt.yticks(x, [x[0] for x in self.LoadInPercentPerBusStop][::-1])
        plt.axvline(self.averageLoadInPercent, color='r', linestyle='--', label=f'Priemerná naplnenosť: {round(self.averageLoadInPercent * 100)}%' if Statistics.language == "sk" else f'Average Load: {round(self.averageLoadInPercent * 100)}%')
        plt.xlabel('Naplnenosť' if Statistics.language == "sk" else 'Load')
        plt.ylabel('Autobusová zastávka' if Statistics.language == "sk" else 'Bus Stop')
        plt.xlim(0, 1)
        plt.xticks(np.linspace(0, 1, 11), [f'{int(x*100)}%' for x in np.linspace(0, 1, 11)])
        plt.legend()
        if self.busNumber != "Agregated":
            plt.title(f'Naplnenosť autobusu #{self.busNumber} v percentách na zastávku' if Statistics.language == "sk" else f'Bus #{self.busNumber} Load in Percent per Bus Stop')
        else:
            plt.title(f'Priemerná naplnenosť autobusov v percentách na zastávku' if Statistics.language == "sk" else f'Average Bus Load in Percent per Bus Stop')

    # STR
    def __str__(self):
        if (Statistics.language == "sk"):
            return "=============================================================\n" + \
               f"Autobus #{self.busNumber}\n" + \
               "=============================================================\n" + \
               f"Priemerná naplnenosť: {self.averageLoad}\n" + \
               f"Priemerná naplnenosť v percentách: {self.averageLoadInPercent}\n" + \
               f"Celkový počet prepravených cestujúcich: {self.totalPassengersTransported}\n" + \
               f"Naplnenosť na zastávku:\n{Statistics.keyValuePairArrayToString(self.loadPerBusStop)}\n" + \
               f"Naplnenosť v percentách na zastávku:\n{Statistics.keyValuePairArrayToString(self.LoadInPercentPerBusStop)}\n" + \
               "=============================================================\n"
        else:
            return "=============================================================\n" + \
               f"Bus #{self.busNumber}\n" + \
               "=============================================================\n" + \
               f"Average load: {self.averageLoad}\n" + \
               f"Average load in percent: {self.averageLoadInPercent}\n" + \
               f"Total passengers transported: {self.totalPassengersTransported}\n" + \
               f"Load per bus stop:\n{Statistics.keyValuePairArrayToString(self.loadPerBusStop)}\n" + \
               f"Load in percent per bus stop:\n{Statistics.keyValuePairArrayToString(self.LoadInPercentPerBusStop)}\n" + \
               "=============================================================\n"
