import pypsa
import logging
from libs.network.custom_components import *
from libs.utils.engines import *

logging.basicConfig(level=logging.ERROR)

class Core:
    def __init__(self, seed=''):
        self.VE = ValueEngine(RandomEngine(seed), TimestampEngine())
        self.network = pypsa.Network()
        self.network.set_snapshots(self.VE.TE.generate_timeseries())

        self.bus_list = {
            "bus_A" : CustomBus("A", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "bus_B" : CustomBus("B", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "bus_C" : CustomBus("C", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "bus_D" : CustomBus("D", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "bus_E" : CustomBus("E", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "bus_F" : CustomBus("F", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5))
        }

        for _, v in self.bus_list.items():
            network_dict = v.network_syntax()
            self.network.add(**network_dict['Bus'])
            for gen in network_dict['Generators']: self.network.add(**gen)
            for load in network_dict['Loads']: self.network.add(**load)

        self.network.add("Line", "Line A-B", bus0=self.bus_list["bus_A"].name, bus1=self.bus_list["bus_B"].name)
        self.network.add("Line", "Line A-C", bus0=self.bus_list["bus_A"].name, bus1=self.bus_list["bus_C"].name)
        self.network.add("Line", "Line B-D", bus0=self.bus_list["bus_B"].name, bus1=self.bus_list["bus_D"].name)
        self.network.add("Line", "Line B-E", bus0=self.bus_list["bus_B"].name, bus1=self.bus_list["bus_E"].name)
        self.network.add("Line", "Line E-F", bus0=self.bus_list["bus_E"].name, bus1=self.bus_list["bus_F"].name)
        self.network.add("Line", "Line F-C", bus0=self.bus_list["bus_F"].name, bus1=self.bus_list["bus_C"].name)