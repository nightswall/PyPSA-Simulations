from core import Core
from datetime import timedelta, datetime as dt
from time import sleep
from libs.utils.data_functions import df_plotter
from libs.utils.adapter import BusAdapter

MODE = 1

if __name__ == '__main__':
     
    if MODE:
        core = Core('10', dt.now().timestamp(), resolution_by_seconds=1)
        i = 0
        while True:
            now = dt.strftime(dt.now()+timedelta(hours=i), '%Y-%m-%d %H:%M:%S')
            core.network.lpf(now)
            print( core.network.buses_t.p.loc[now])
            i+=1
            sleep(1)
            """
            maybe not datetime onlytime for 24h and reproduce again and again""" 
        """
        core = Core(seed, start_date=now(), interval_by_seconds=interval_by_seconds)
        """
        while True:
            pass
        """
        if end_of_list:
            core.change_weight
            core.renew_efficiency
            core.renew_voltage
        
        core.network.lpf(time_now)
            
        sleep(interval_by_seconds)
        """
    else:
        core = Core('10', dt.now().timestamp())

        core.network.lpf()

        import pandas as pd
        temp = {}
        voltage = {}
        current = {}
        index = core.network.buses_t.p.index.tolist()
        for bus in core.network.buses_t.p:
            current_bus = BusAdapter(core.network.buses_t.p[bus], core.bus_list[bus])
            temp[bus] = pd.Series(core.VE.calculate_temperature(current_bus), index=index)
            voltage[bus] = pd.Series(current_bus.v_set, index=index)
            current[bus] = pd.Series(core.VE.calculate_current(current_bus), index=index)

        core.network.buses_t['temp'] = pd.DataFrame(data=temp)
        core.network.buses_t['voltage'] = pd.DataFrame(data=voltage)
        core.network.buses_t['current'] = pd.DataFrame(data=current)

        df_plotter(core.network)