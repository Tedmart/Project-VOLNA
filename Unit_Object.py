import Reactor_Object

class Unit:

    def __init__(self, reactor=Reactor_Object.Reactor(100), turbine=None, condenser=None, deaerator=None):
        self.reactor = reactor
        self.fwp_1 = pump(1,1)
        self.fwp_2 = pump(1,1)

        self.turbine = turbine

        self.condenser = condenser

        self.deaerator = deaerator


        self.rods_speed = 0.025

    
    """Gestion blogale"""

    def refresh(self):
        #Refresh des système ensuite
        self.reactor.refresh()

    def fast_refresh(self):
        #Refresh des pompes en premier
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



    def thermal_power(self):
        return self.reactor.power()
    
    def period(self):
        return self.reactor.period()
    

class pump:
    
    def __init__(self, coeff, lag):
        self.setpoint = 0
        self.rpm = 0
        self.flow = 0
        self.rpm_to_flow_coeff = coeff
        self.lag = lag

    def refresh(self):
        self.rpm = self.rpm + ( self.setpoint - self.rpm ) / self.lag
        self.flow = self.rpm * self.rpm_to_flow_coeff

    def set_point_add(self, value):
        self.setpoint += value
