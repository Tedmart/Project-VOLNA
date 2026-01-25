
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

        # Rotation libre (False) ou Rotation synchronisée (True)
        self.mode = False

        self.phase = 0

        # Etat de l'activation de la valve principal et de la valve de contournement
        self.valve_on = False
        self.bypass_on = False

        # Position de la valve principal et de la valve de contournement
        self.valve = 0
        self.bypass = 0

        # Coefficient d'ouverture -- à ajuster
        self.turbine_coeff = 0.4
        self.bypass_coeff = 0.1

        # Valve d'urgence pour drainer la pression de la vapeur
        self.relief = False
        self.relief_coeff = 1.5

    def refresh(self, pressure):
        phase_coeff = 1
        #self.phase = self.phase + phase_coeff * (self.rpm - 1500, 1500)

        # Conversion % vers fraction
        valve_frac = self.valve / 100
        bypass_frac = self.bypass / 100

        # Calcul vapeur
        turbine_steam = valve_frac  * self.turbine_coeff * pressure
        bypass_steam  = bypass_frac * self.bypass_coeff * pressure

        total_out = int(turbine_steam + bypass_steam)
        print(total_out)

        if self.mode:
            rpm_goal = turbine_steam * pressure * self.RPM_COEFF
            self.rpm = self.rpm + (rpm_goal - self.rpm)/self.LAG

        else:
            self.rpm = 1500


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

    # Disjoncteur principal
    def breaker(self):
        if not self.mode and not self.check_condition():
            return
        else:
            self.mode = not self.mode
        
    def check_condition(self):
        return True

    # Turbine en elle-même
    def get_rpm(self):
        return self.rpm



turbine = Turbine()
turbine.bypass_open()
turbine.bypass_setpoint(100)

turbine.refresh(7100)