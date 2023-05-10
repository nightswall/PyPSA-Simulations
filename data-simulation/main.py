from core import Core
from libs.utils.data_functions import df_plotter

MODE = 0

if __name__ == '__main__':
    core = Core('10') 
    if MODE:
        pass
    else:
        core.network.lpf()
        df_plotter(core.network)