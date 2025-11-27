class Turbine:
    def __init__(self):
        self.settings = 100
        self.steam_coeff = 1
        self.steam = 0
        self.mode = 0

    def refresh(self, pressure):
        self.steam = self.settings * self.steam_coeff * pressure
        return self.steam