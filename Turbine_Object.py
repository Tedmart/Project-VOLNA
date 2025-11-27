
# URSS's Grid Frequency = 50Hz
# Turbine rpm goal for 50Hz = 1500


class Turbine:
    """
        Permet de créer une turbine
        capable de gérer sa propre physique
        capable de modifier ses valve (bypass/contournement et valve principal)
        possède deux mode, mode libre (0) et mode synchronisé (1)
    """
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
    
    def valve_close(self):
        self.valve_on = False
        self.valve = 0
    
    def valve_open(self):
        self.valve_on = True

    def valve_setpoint(self, value):
        if self.vale_on:
            self.valve += value
    
    def bypass_close(self):
        self.bypass_on = False
        self.bypass = 0
    
    def bypass_open(self):
        self.bypass_on = True
    
    def bypass_setpoint(self, value):
        if self.bypass_on:
            self.bypass += value


