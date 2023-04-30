from random import uniform, random, randint
from datetime import datetime as dt
import math
from functools import reduce

START_DAY = "2023-01-01 00:00:00"
TIME_PERIOD_AS_DAY = 1
RESOLUTION_BY_SECONDS = 60
TIMESTAMP_PER_DAY = int(24*3600/RESOLUTION_BY_SECONDS)


def generate_timeseries():
    timeseries = []
    start_ts = int(dt.strptime(START_DAY, '%Y-%m-%d %H:%M:%S').timestamp())
    for gen_ts in range(start_ts, start_ts+TIME_PERIOD_AS_DAY*24*3600, RESOLUTION_BY_SECONDS):
        datetime = dt.fromtimestamp(gen_ts)
        timeseries.append(str(datetime))

    return timeseries

def list_expander(_list: list, new_len: int):
    old_len = len(_list)
    assert new_len > old_len
    tmp, result = _list, []
    tmp.extend([tmp[0]])

    for i in range(old_len):
        result.extend(
            [round(tmp[i]+j*(tmp[i+1]-tmp[i])/new_len, 3)
                for j in range(new_len)
            ]
        )

    return [result[i] for i in range(0, len(result), old_len)]

def list_weighter(_list: list):
    tmp = []
    sin_mult = 0.8
    for _ in range(TIME_PERIOD_AS_DAY):
        tmp.extend(
            map(lambda x: x*round(uniform(3, 7),3), _list)
        )
        # tmp.extend(
        #     map(lambda x: x*(1-sin_mult+sin_mult*math.sin(random()*math.pi)), _list)
        # )
        # tmp.extend(
        #     map(lambda x: x, _list)
        # )
    return tmp

def calculate_temperature(p_set, efficiency, time_diff):
    # Specific heat capacity of the generator material (J/kg K)
    C_p = 500
    # Density of the generator material (kg/m^3)
    density = round(uniform(800, 1200),3)
    # Volume of the generator (m^3)
    volume = round(uniform(0.5, 3.5),3)
    # Mass of the generator (kg)
    mass = density * volume
    # Total energy produced by the generator (J)
    energy = p_set * efficiency * time_diff
    # Temperature rise of the generator (K)
    delta_T = energy / (mass * C_p)
    # Final temperature of the generator (K)
    temperature = delta_T*(1+random()) + 25

    return temperature

def calculate_current(power, voltage, efficiency):
    effective_power = power*efficiency
    current = round(effective_power/voltage, 3)
    return current

def random_list():
    return [randint(randint(30,70), randint(135,300)) for _ in range(randint(7,17))]

def random_efficiency():
    return [randint(45,78)*0.01 for _ in range(randint(3,7))]

def random_voltage_regulation(main_voltage, regulation_range):
    return [uniform(main_voltage+regulation_range,main_voltage-regulation_range) for _ in range(randint(4,8))]

def df_combiner(network):
    import pandas as pd
    network.buses_t.temp.index.name='snapshot'
    network.buses_t.voltage.index.name='snapshot'
    network.buses_t.current.index.name='snapshot'

    df_power = network.buses_t.p.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Power")
    df_temp = network.buses_t.temp.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Temperature")
    df_voltage = network.buses_t.voltage.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Voltage")
    df_current = network.buses_t.current.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Current")

    df_combined = reduce(lambda  left,right: pd.merge(left,right,on=["snapshot", "Bus"],
                                            how='inner'), [df_power, df_temp, df_voltage, df_current])

    df_combined.columns = ["DateTime", "Bus", "Power", "Temperature", "Voltage", "Current"]
    df_combined = df_combined.set_index("DateTime")
    df_combined = df_combined.sort_index()
    return df_combined

def cvs_converter(df, path='output.csv'):
    df.to_csv(path)  

def df_plotter(network):
    from matplotlib import pyplot as plt
    network.buses_t.p.plot()
    network.buses_t.temp.plot()
    network.buses_t.voltage.plot()
    network.buses_t.current.plot()
    plt.show()