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

        for i in range(len(rods)):
            if rods[i]:
                if i<2:
                    self.reactor.raise_rods(i, 0, value)
                elif i<6:
                    self.reactor.raise_rods(i-2, 1, value)
                elif i<12:
                    self.reactor.raise_rods(i-6, 2, value)
                elif i<18:
                    self.reactor.raise_rods(i-12, 3, value)
                elif i<22:
                    self.reactor.raise_rods(i-18, 4, value)
                else:
                    self.reactor.raise_rods(i-22, 5, value)
                
                print(i)


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
