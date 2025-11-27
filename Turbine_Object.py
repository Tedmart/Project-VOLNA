
# URSS's Grid Frequency = 50Hz
# Turbine rmp goal for 50Hz = 1500

class Turbine:
    def __init__(self):
        self.settings = 100
        self.steam_coeff = 1
        self.steam = 0
        self.mode = 0

        self.vale_on = False
        self.bypass_on = False

        self.valve = 0
        self.bypass = 0

        self.relief = False

    def refresh(self, pressure):
        self.steam = self.settings * self.steam_coeff * pressure
        return self.steam
    
    def valve_off(self):
        self.valve_on = False
        self.valve = 0
    
    def valve_open(self):
        self.valve_on = True

    def valve_setpoint(self, value):
        if self.vale_on:
            self.valve += value
    
    def bypass_off(self):
        self.bypass_on = False
        self.bypass = 0
    
    def bypass_open(self):
        self.bypass_on = True
    
    def bypass_setpoint(self, value):
        if self.bypass_on:
            self.bypass += value