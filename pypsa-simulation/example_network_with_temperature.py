import pypsa
import pandas as pd
from utils import *
import logging

logging.basicConfig(level=logging.ERROR)

network = pypsa.Network()
network.set_snapshots(generate_timeseries())
n_buses = 3

for i in range(n_buses):
    network.add("Bus", "My bus {}".format(i), v_nom=20.0)

for i in range(n_buses):
    network.add(
        "Line",
        "My line {}".format(i),
        bus0="My bus {}".format(i),
        bus1="My bus {}".format((i + 1) % n_buses),
        x=0.1,
        r=0.01,
    )
    
network.add("Generator", "Solar", bus="My bus 0", p_set=list_weighter(list_expander([110,205,270,80], TIMESTAMP_PER_DAY)), control="PQ")
network.add("Generator", "Wind", bus="My bus 2", p_set=list_weighter(list_expander([10,50,20,30], TIMESTAMP_PER_DAY)), efficiency=0.106)

network.add("Load", "My load", bus="My bus 1", p_set=100)
network.add("Load", "My load 2", bus="My bus 0", p_set=list_weighter(list_expander([70,20,70,90,120], TIMESTAMP_PER_DAY)))

network.loads.q_set = 100.0

network.lpf()

# for index in network.buses_t.p.index:
#     for bus in network.buses_t.p:
#         network.buses_t.p


temp = {}
for bus in network.buses_t.p:
    temp[bus] = pd.Series([calculate_temperature(i, 1, 3600) for i in network.buses_t.p[bus]], index=network.buses_t.p.index.tolist())

df = pd.DataFrame(data=temp, columns=network.buses_t.p.columns)
network.buses_t['temp'] = df
from matplotlib import pyplot as plt
network.buses_t.p.plot()
network.buses_t.temp.plot()
plt.show()

# for k, df in df_cluster.groupby(label_fields):
#     df.plot(x=time_series_field, y=actual_data_field)
#     plt.xticks(rotation=90)
#     plt.legend([' '.join(k)])
#     plt.savefig(''.join(k)+'.png', dpi=600, format='png', bbox_inches='tight')