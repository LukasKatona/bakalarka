from enum import Enum
from Time import forwardModelTime, printCurrentTimeAndMessage

# ------------------------------ BUSLINE ------------------------------
class BusLine:
    # INIT
    def __init__(self, number, bus_stops, travel_tiems_between_stops):
        self.number = number
        self.bus_stops = bus_stops
        self.travel_tiems_between_stops = travel_tiems_between_stops


# ------------------------------ BUSSTOP ------------------------------
class BusStop:
    # STATES
    class State(Enum):
        Idle = 1
        Bus_arrived = 2
        Boarding = 3

    # INPUT SIGNALS
    class InputSignals(Enum):
        Bus_arrived = 1
        Start_boarding = 2
        Finish_boarding = 3
    def trigger_input_signal(self, signal):
        if signal == BusStop.InputSignals.Bus_arrived:
            self.bus_arrived()
        elif signal == BusStop.InputSignals.Start_boarding:
            self.start_boarding()
        elif signal == BusStop.InputSignals.Finish_boarding:
            self.finish_boarding

    # OUTPUT SIGNALS
    def init_output_signals(self):
        pass
    def trigger_output_signal(self, signal):
        pass

    # INIT
    def __init__(self, name, passengers, boarding_time_per_passenger):
        self.name = name
        self.passengers = passengers
        self.boarding_time_per_passenger = boarding_time_per_passenger
        self.state = BusStop.State.Idle
        self.init_output_signals()

    # METHODS
    def time_to_board_passengers(self, passengers_boarding_at_once):
        return int(round((self.passengers * self.boarding_time_per_passenger) / passengers_boarding_at_once))
    
    def bus_arrived(self):
        self.state = BusStop.State.Bus_arrived
        printCurrentTimeAndMessage(f"At {self.name} there are {self.passengers} passengers waiting")

    def start_boarding(self):
        self.state = BusStop.State.Boarding
        
    def finish_boarding(self):
        self.state = BusStop.State.Idle
        self.passengers = 0
    

# -------------------------------- BUS --------------------------------
class Bus:
    # STATES
    class State(Enum):
        Starting = 1
        Traveling = 2
        Arrived = 3
        Boarding = 4
        Departed = 5
        Finished = 6

    # INPUT SIGNALS
    def trigger_input_signal(self, signal):
        pass

    # OUTPUT SIGNALS
    class OutputSignals(Enum):
        Arrival = 1
        Boarding = 2
        Departure = 3
    def init_output_signals(self):
        self.signals =  {
            Bus.OutputSignals.Arrival: [(self.current_bus_stop, BusStop.InputSignals.Bus_arrived)],
            Bus.OutputSignals.Boarding: [(self.current_bus_stop, BusStop.InputSignals.Start_boarding)],
            Bus.OutputSignals.Departure: [(self.current_bus_stop, BusStop.InputSignals.Finish_boarding)]
        }
    def trigger_output_signal(self, signal):
        for input_signal in self.signals[signal]:
            input_signal[0].trigger_input_signal(input_signal[1])

    # INIT
    def __init__(self, passangers_boarding_at_once, bus_line):
        self.passangers_boarding_at_once = passangers_boarding_at_once
        self.state = Bus.State.Starting
        self.bus_line = bus_line
        self.current_bus_stop = bus_line.bus_stops[0]
        self.init_output_signals()

    # METHODS
    def start(self):
        printCurrentTimeAndMessage(f"Bus {self.bus_line.number} has started its route at {self.current_bus_stop.name}")
        self.trigger_output_signal(Bus.OutputSignals.Arrival)
        self.state = Bus.State.Boarding 

    def travel_to_next_stop(self):
        if self.current_bus_stop == self.bus_line.bus_stops[-1]:
            printCurrentTimeAndMessage(f"Bus {self.bus_line.number} has finished its route")
            self.state = Bus.State.Finished
        else:
            current_stop_index = self.bus_line.bus_stops.index(self.current_bus_stop)
            travel_time = self.bus_line.travel_tiems_between_stops[current_stop_index]
            printCurrentTimeAndMessage(f"Bus {self.bus_line.number} is traveling to {self.bus_line.bus_stops[current_stop_index + 1].name} for {travel_time} minutes")
            forwardModelTime(travel_time)
            self.state = Bus.State.Arrived

    def arrive_at_stop(self):
        if self.state == Bus.State.Arrived:
            current_stop_index = self.bus_line.bus_stops.index(self.current_bus_stop)
            self.current_bus_stop = self.bus_line.bus_stops[current_stop_index + 1]
            printCurrentTimeAndMessage(f"Bus {self.bus_line.number} has arrived at {self.current_bus_stop.name}")
            self.trigger_output_signal(Bus.OutputSignals.Arrival)
            self.state = Bus.State.Boarding

    def board_passengers(self):
        if self.state == Bus.State.Boarding:
            self.trigger_output_signal(Bus.OutputSignals.Boarding)
            boarding_time = self.current_bus_stop.time_to_board_passengers(self.passangers_boarding_at_once)
            printCurrentTimeAndMessage(f"Bus {self.bus_line.number} is boarding passengers at {self.current_bus_stop.name} for {boarding_time} minutes")
            forwardModelTime(boarding_time)
            self.trigger_output_signal(Bus.OutputSignals.Departure)
            self.state = Bus.State.Departed

    def depart_stop(self):
        if self.state == Bus.State.Departed:
            printCurrentTimeAndMessage(f"Bus {self.bus_line.number} has departed {self.current_bus_stop.name}")
            self.state = Bus.State.Traveling