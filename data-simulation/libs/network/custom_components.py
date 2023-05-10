class CustomBus:
    typename = 'Bus'
    def __init__(self, name, valueEngine, num_of_gen=1, num_of_load=1, init_temp=25, heat_cap=500):
        self.name = name
        self.initial_temperature = init_temp
        self.heat_capacity = heat_cap
        self.average_voltage = None # need random voltage
        self.generator_list = [CustomGenerator(f"{i} - {self.typename}:{self.name}", valueEngine) for i in range(num_of_gen)]
        self.load_list = [CustomLoad(f"{i} - {self.typename}:{self.name}", valueEngine) for i in range(num_of_load)]

    def network_syntax(self):
        return {
            'Bus': {'class_name': self.typename, 
                    'name': self.name},
            'Generators': [
                dict(gen.network_syntax(), **{'bus': self.name}) for gen in self.generator_list
            ],
            'Loads': [
                dict(load.network_syntax(), **{'bus': self.name}) for load in self.load_list
            ]
        }


class CustomComponent:
    typename = None
    def __init__(self, name, valueEngine):
        self.VE = valueEngine
        self.name = name
        self.mass = None
        self.power_list = self.VE.list_expander(self.VE.random_power_list())

    def network_syntax(self):
        return {
            'class_name': self.typename, 
            'name': self.name,
            'p_set': self.power_list
        }
    
    def renew_power_list(self):
        self.power_list = self.VE.list_expander(self.VE.random_power_list())

class CustomLoad(CustomComponent):
    typename = 'Load'
    def __init__(self, name, valueEngine):
        super().__init__(f"{self.typename}:{name}", valueEngine)

class CustomGenerator(CustomComponent):
    typename = 'Generator'
    def __init__(self, name, valueEngine):
        super().__init__(f"{self.typename}:{name}", valueEngine)
        self.efficiency = self.VE.list_expander(self.VE.random_efficiency_list())

    def renew_efficiency_list(self):
        self.efficiency = self.VE.list_expander(self.VE.random_efficiency_list())