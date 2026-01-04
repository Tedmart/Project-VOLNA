import Reactor_Object
import Turbine_Object

class Unit:

    def __init__(self, reactor=Reactor_Object.Reactor(100), turbine=Turbine_Object.Turbine(), condenser=None, deaerator=None, electrical_pannel=None):
        # Partie réacteur et son alimentation
        self.reactor = reactor
        self.fwp_1 = pump()
        self.fwp_2 = pump()

        # Partie turbine
        self.turbine = turbine

        # Partie condensateur
        self.condenser = condenser

        # Partie désaérateur
        self.deaerator = deaerator

        # Panneau éléctrique
        self.electrical_pannel = electrical_pannel


        self.rods_speed = 0.025

    
    """Gestion globale"""

    def refresh(self):
        
        self.reactor.add_water(self.fwp_1, 100)
        self.reactor.add_water(self.fwp_2, 30)

        pressure = self.reactor.pressure

        steam_to_remove = self.turbine.refresh(pressure)

        self.reactor.remove_steam(steam_to_remove)

        self.reactor.refresh()


    def fast_refresh(self):
        self.fwp_1.refresh()
        self.fwp_2.refresh()


    """Gestion du réacteur"""
    def raise_rods(self, rods):
        value = self.rods_speed

        # Définition des tailles de groupes
        groups = [2, 4, 6, 6, 4, 2]

        # offset = position de départ de chaque groupe dans la liste plate
        offset = 0

        for g, group_size in enumerate(groups):
            for pos in range(group_size):
                flat_index = offset + pos

                if flat_index < len(rods) and rods[flat_index]:
                    try:
                        self.reactor.raise_rods(g, pos, value)
                    except IndexError:
                        print(f"position = {flat_index}, groupe = {g}, pos = {pos}, erreur = {IndexError}")

            offset += group_size

    def lower_rods(self, rods):
        value = -self.rods_speed

        # Définition des tailles de groupes
        groups = [2, 4, 6, 6, 4, 2]

        # offset = position de départ de chaque groupe dans la liste plate
        offset = 0

        for g, group_size in enumerate(groups):
            for pos in range(group_size):
                flat_index = offset + pos

                if flat_index < len(rods) and rods[flat_index]:
                    try:
                        self.reactor.raise_rods(g, pos, value)
                    except IndexError:
                        print(f"position = {flat_index}, groupe = {g}, pos = {pos}, erreur = {IndexError}")

            offset += group_size



    def thermal_power(self):
        return self.reactor.power()
    
    def period(self):
        return self.reactor.period(1)
    
    def temperature(self):
        return self.reactor.temperature()
    
    def __debug_raise__(self, amount=100):
        self.reactor.__debug_raise__(amount)

    def feed_pump1_set(self, value):
        self.fwp_1.set_point(value)

    def feed_pump2_set(self, value):
        self.fwp_2.set_point(value)

    # Gestion turbine
    def main_valve(self, open):
        if open:
            self.turbine.valve_open(self.reactor.pressure)
        else:
            self.turbine.valve_close()

    def set_valve(self, amount):
        self.turbine.valve_setpoint(amount)

    def bypass_valve(self, open):
        if open:
            self.turbine.bypass_open()
        else:
            self.turbine.bypass_close()

    def set_bypass(self, amount):
        self.turbine.bypass_setpoint(amount)
    

class pump:
    
    def __init__(self, coeff=1, lag=1):
        self.setpoint = 0
        self.rpm = 0
        self.flow = 0
        self.rpm_to_flow_coeff = coeff
        self.lag = lag

    def refresh(self):
        self.rpm = self.rpm + ( self.setpoint - self.rpm ) / self.lag
        self.flow = self.rpm * self.rpm_to_flow_coeff

    def set_point(self, value):
        self.setpoint = value
