import pypsa
import pandas as pd
from utils import *
import logging
from random import randint
from functools import reduce

logging.basicConfig(level=logging.ERROR)

network = pypsa.Network()
network.set_snapshots(generate_timeseries())

network.add("Bus", "Bus 0", v_nom=380)
network.add("Generator", "Gen 0:0", bus="Bus 0", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)), p_max=1000, p_min=0, q_max=1000, q_min=-1000, ramp_limit_up=1000, ramp_limit_down=1000, voltage_set=1.0, voltage_angle_set=0.0, slack=True)
network.add("Generator", "Gen 1:0", bus="Bus 0", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)), ramp_limit_up=380)
network.add("Generator", "Gen 2:0", bus="Bus 0", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)), ramp_limit_up=380)
# network.add("Generator", "Gen 3:0", bus="Bus 0", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Generator", "Gen 4:0", bus="Bus 0", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Generator", "Gen 5:0", bus="Bus 0", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))

network.add("Line", "Line 0-1", bus0="Bus 0", bus1="Bus 1", length=150e3, p_nom=200e6, q_nom=100e6, r=0.2, x=0.4, b=0.01)

network.add("Bus", "Bus 1", v_nom=380)
network.add("StorageUnit", "Storage 0:1", bus="Bus 1",
            e_nom=50e6, p_nom=20e6, e_cyclic=True, max_hours=4,
            eta_charge=0.9, eta_discharge=0.9, standing_loss=0.0,
            min_e_stored=0.2, max_e_stored=0.8,
            cyclic_state_of_charge=True, initial_state_of_charge=0.5, efficiency=0.842, p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Load", "Load 0:1", bus="Bus 1", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))

network.add("Line", "Line 1-2", bus0="Bus 1", bus1="Bus 2", length=80e3, p_nom=300e6, q_nom=150e6, r=0.4, x=0.6, b=0.02)

network.add("Bus", "Bus 2", v_nom=380)
network.add("Load", "Load 0:2", bus="Bus 2", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))

network.add("Line", "Line 2-3", bus0="Bus 2", bus1="Bus 3", length=30e3, p_nom=400e6, q_nom=200e6, r=0.3, x=0.5, b=0.03)

network.add("Bus", "Bus 3", v_nom=600)
network.add("Load", "Load 0:3", bus="Bus 3", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
network.add("Generator", "Gen 0:3", bus="Bus 3", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
network.add("Generator", "Gen 1:3", bus="Bus 3", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))

network.add("Line", "Line 2-4", bus0="Bus 2", bus1="Bus 4", length=120e3, p_nom=400e6, q_nom=200e6, r=0.43, x=0.75, b=0.037)

network.add("Bus", "Bus 4", v_nom=380)

network.add("Line", "Line 4-5", bus0="Bus 4", bus1="Bus 5", length=30e3, p_nom=400e6, q_nom=200e6, r=0.3, x=0.5, b=0.03)

network.add("Bus", "Bus 5", v_nom=380)
network.add("Load", "Load 0:5", bus="Bus 5", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
network.add("Generator", "Gen 0:5", bus="Bus 5", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Store", "Storage 0:5", bus="Bus 5", p_nom=randint(50,250), max_hours=randint(4,16), p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Store", "Storage 1:5", bus="Bus 5", p_nom=randint(30,85), max_hours=randint(2,6), p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))

# network.add("Transformer", "Transformer 4-6", bus0="Bus 4", bus1="Bus 6", p_nom=600, s_nom=1000)

# network.add("Bus", "Bus 6", v_nom=380)
# network.add("Load", "Load 0:6", bus="Bus 6", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Load", "Load 1:6", bus="Bus 6", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))

# network.add("Line", "Line 6-7", bus0="Bus 6", bus1="Bus 7", x=0.01, r=0.001, g=0, b=0, s_nom=100, max_p=100, min_p=-100)

# network.add("Bus", "Bus 7", v_nom=380)
# network.add("Load", "Load 0:7", bus="Bus 7", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Load", "Load 1:7", bus="Bus 7", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))
# network.add("Load", "Load 2:7", bus="Bus 7", p_set=list_weighter(list_expander(random_list(), TIMESTAMP_PER_DAY)))

network.lpf()

temp = {}
voltage = {}
current = {}

for bus in network.buses_t.p:
    current_bus = network.buses_t.p[bus]
    current_efficiency = []
    current_voltage = []
    for _ in range(TIME_PERIOD_AS_DAY):
        current_efficiency+=list_expander(random_efficiency() , TIMESTAMP_PER_DAY)
        current_voltage+=list_expander(random_voltage_regulation(230, 5), TIMESTAMP_PER_DAY)

    temp[bus] = pd.Series([calculate_temperature(i, j, RESOLUTION_BY_SECONDS) for i,j in zip(current_bus, current_efficiency)], index=network.buses_t.p.index.tolist())
    voltage[bus] = pd.Series(current_voltage, index=network.buses_t.p.index.tolist())
    current[bus] = pd.Series([calculate_current(p, v, e) for p,v,e in zip(current_bus, current_voltage, current_efficiency)], index=network.buses_t.p.index.tolist())

network.buses_t['temp'] = pd.DataFrame(data=temp)
network.buses_t['voltage'] = pd.DataFrame(data=voltage)
network.buses_t['current'] = pd.DataFrame(data=current)

df_combine = df_combiner(network)
cvs_converter(df_combine)