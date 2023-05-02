import pypsa
import pandas as pd
from utils import *
import logging

logging.basicConfig(level=logging.ERROR)

network = pypsa.Network()
network.set_snapshots(generate_timeseries())
# n_buses = 3

# for i in range(n_buses):
#     network.add("Bus", "My bus {}".format(i), v_nom=20.0)

# for i in range(n_buses):
#     network.add(
#         "Line",
#         "My line {}".format(i),
#         bus0="My bus {}".format(i),
#         bus1="My bus {}".format((i + 1) % n_buses),
#         x=0.1,
#         r=0.01,
#     )
    
# network.add("Generator", "Solar", bus="My bus 0", p_set=list_weighter(list_expander([110,205,270,80], TIMESTAMP_PER_DAY)), control="PQ")
# network.add("Generator", "Wind", bus="My bus 2", p_set=list_weighter(list_expander([10,50,20,30], TIMESTAMP_PER_DAY)))

# network.add("Load", "My load", bus="My bus 1", p_set=100)
# network.add("Load", "My load 2", bus="My bus 0", p_set=list_weighter(list_expander([70,20,70,90,120], TIMESTAMP_PER_DAY)))

network.add("Bus", "Bus: Load & Generator 1", v_nom=220)
network.add("Generator", "Generator 1", bus="Bus: Load & Generator 1", p_set=list_weighter(list_expander([70,20,70,90,120], TIMESTAMP_PER_DAY)), efficiency=0.89, ramp_limit_up=380)
network.add("Load", "Load 1", bus="Bus: Load & Generator 1", p_set=list_weighter(list_expander([10,50,20,30], TIMESTAMP_PER_DAY)))

network.add("Line", "Line 1", bus0="Bus: Load & Generator 1", bus1="Bus: Load & Generator 2", x=0.1, r=0.01)

network.add("Bus", "Bus: Load & Generator 2", v_nom=220)
network.add("Generator", "Generator 2", bus="Bus: Load & Generator 2", p_set=list_weighter(list_expander([60,30,90,50], TIMESTAMP_PER_DAY)), efficiency=0.71, ramp_limit_up=380)
network.add("Load", "Load 2", bus="Bus: Load & Generator 2", p_set=list_weighter(list_expander([100,20,35,25], TIMESTAMP_PER_DAY)))

# network.add("Line", "Line 2", bus0="Bus: Load & Generator 2", bus1="Bus: Loads & Transformer", x=4.5, r=0.32)

network.add("Bus", "Bus: Loads & Transformer", v_nom=380)
network.add("Transformer", "Transformer 1", bus0="Bus: Load & Generator 2", bus1="Bus: Loads & Transformer", x=10.7, r=2.8)
network.add("Load", "Load 3", bus="Bus: Loads & Transformer", p_set=list_weighter(list_expander([5, 20, 7, 13, 6, 8, 19], TIMESTAMP_PER_DAY)))
network.add("Load", "Load 4", bus="Bus: Loads & Transformer", p_set=list_weighter(list_expander([3, 7, 12, 5], TIMESTAMP_PER_DAY)))



network.loads.q_set = 0.0

network.lpf()

from matplotlib import pyplot as plt
network.buses_t.p.plot()
plt.show()

# for k, df in df_cluster.groupby(label_fields):
#     df.plot(x=time_series_field, y=actual_data_field)
#     plt.xticks(rotation=90)
#     plt.legend([' '.join(k)])
#     plt.savefig(''.join(k)+'.png', dpi=600, format='png', bbox_inches='tight')