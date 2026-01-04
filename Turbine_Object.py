
# URSS's Grid Frequency = 50Hz
# Turbine rpm goal for 50Hz = 1500 rpm


class Turbine:
    """
        Permet de créer une turbine
        capable de gérer sa propre physique
        capable de modifier ses valve (bypass/contournement et valve principal)
        possède deux mode, mode libre (0) et mode synchronisé (1)
    """
    def __init__(self):

        self.rpm = 0
        self.RPM_COEFF = 0.05
        self.LAG = 10

        # Rotation libre (0) ou Rotation synchronisée (1)
        self.mode = 0

        # Etat de l'activation de la valve principal et de la valve de contournement
        self.valve_on = False
        self.bypass_on = False

        # Position de la valve principal et de la valve de contournement
        self.valve = 0
        self.bypass = 0

        # Coefficient d'ouverture -- à ajuster
        self.turbine_coeff = 1.0
        self.bypass_coeff = 0.1

        # Valve d'urgence pour drainer la pression de la vapeur
        self.relief = False
        self.relief_coeff = 1.5

    def refresh(self, pressure):
        # Conversion % vers fraction
        valve_frac = self.valve / 100
        bypass_frac = self.bypass / 100

        # Calcul vapeur
        turbine_steam = valve_frac  * self.turbine_coeff * pressure
        bypass_steam  = bypass_frac * self.bypass_coeff * pressure

        total_out = int(turbine_steam + bypass_steam)
        print(total_out)

        rpm_goal = turbine_steam * pressure * self.RPM_COEFF
        self.rpm = self.rpm + (rpm_goal - self.rpm)/self.LAG

        return total_out
    
    # Valve principale
    def valve_close(self):
        self.valve_on = False
        self.valve = 0
    
    def valve_open(self, pressure):
        if pressure < 4000:
            return
        self.valve_on = True

    def valve_setpoint(self, value):
        if self.valve_on:
            self.valve = value
    
    # Valve de contournement
    def bypass_close(self):
        self.bypass_on = False
        self.bypass = 0
    
    def bypass_open(self):
        self.bypass_on = True
    
    def bypass_setpoint(self, value):
        if self.bypass_on:
            self.bypass = value

    # Turbine en elle-même
    def get_rpm(self):
        return self.rpm



turbine = Turbine()
turbine.bypass_open()
turbine.bypass_setpoint(100)

turbine.refresh(7100)