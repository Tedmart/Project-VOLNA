
import math
from statistics import mean



def Reactor_Fuel_Assembly(fuel):
    mask = [
        [0,0,1,1,0,0],
        [0,1,1,1,1,0],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [0,1,1,1,1,0],
        [0,0,1,1,0,0],
    ]
    matrice = [[Assembly(fuel) if mask[x][y]==1 else None for y in range(len(mask[x]))] for x in range(len(mask))]

    return matrice


class Reactor:
    """
        Permet de créer un objet réacteur.
        capable de gérer sa propre physique.
        capable de produire de la vapeur.
        possibilité d'y injecter de l'eau.
        possibilité d'y extraire de la vapeur ainsi que de la pression.
    """

    def __init__(self, fuel=100):
        # Gestion général du réacteur
        self.assembly = Reactor_Fuel_Assembly(fuel)
        self.previews_power = 0.0

        # Gestion de la température
        self.water_temperature = 30
        self.heat_per_power = 200
        self.energy_loss_coefficient = 0.03/100
        self.ambient_temperature = 30

        # Gestion de l'eau
        self.water_amount = 5000
        self.steam_amount = 0
        self.boiling_coefficient = 3
        self.condensation_coefficient = 3
        self.pressure = 0
        self.steam_pressure_coefficient = 0.5
        self.saturation_temperature = boiling_point(self.pressure)

        self.level_coefficient = 10

        self.water_density = 1000

    def refresh(self):
        # Actualise la physique du réacteur (toute les 1 secondes)
        self.previews_power = self.power()

        self.water_density = water_density(self.water_temperature)

        Propagation(self.assembly)

        for i in range(len(self.assembly)):
            for j in range(len(self.assembly[i])):
                if self.assembly[i][j] is None:
                    continue
                self.assembly[i][j].refresh(self.water_density)

        self.water_temperature += self.power() * self.heat_per_power

        self.water_temperature -= (
            (self.water_temperature - self.ambient_temperature)
            * self.energy_loss_coefficient
        )

        self.__weter_refresh__()
        
        return

    def power(self):
        # Permet de connaitre la puissance thermique du réacteur en pourcentage
        # calcul de la moyenne de la puissance de chaque assemblage
        temp = []
        for i in self.assembly:
            for j in i:
                if j is None:
                    continue
                temp.append(j.get_power())
        result = mean(temp)
        return result

    def period(self, time_step):
        # Permet de connaitre la période du réacteur
        # Calcul indépendant des assemblage 
        try:
            ReactorPeriod = 1 / math.log( self.power() / self.previews_power ) * (1 / time_step)
        except:
            return float("inf")
        if ReactorPeriod > 5000 or ReactorPeriod < -5000:
            return float("inf")
        return ReactorPeriod
    
    def raise_rods(self, x, y, value):
        # permet de controler les barres de contrôle de chaque assemblage
        self.assembly[x][y].raise_rods(value)

    def __debug_raise__(self, amount=100):
        # Permet de tester la physique du réacteur à pleine puissance
        # Permet de calibrer les coefficients
        for i in range(len(self.assembly)):
            for j in range(len(self.assembly[i])):
                if self.assembly[i][j] is None:
                    continue
                self.assembly[i][j].rods_pulled = amount

    def temperature(self):
        # Permet d'avoir la température de l'eau du réacteur
        return self.water_temperature
    
    def water_level(self):
        # Permet d'avoir le niveau d'eau dans le réacteur
        level = self.water_amount/self.water_density * self.level_coefficient
        return level
    
    def add_water(self, pump, feedwater_temperature):
        # Permet de simuler l'ajout d'eau dans le reacteur via les pompes d'alimentation
        MIXING_COEFF = 0.01
        self.water_temperature = (( self.water_temperature + pump.flow * feedwater_temperature * MIXING_COEFF ) / 
                                  ( 1 + pump.flow * MIXING_COEFF ))
        self.water_amount += int(pump.flow)

    def remove_steam(self, amount):
        self.steam_amount -= amount
    
    def __weter_refresh__(self):
        # Permet d'actualiser l'état et la physique de l'eau dans le réacteur
        # Auto géré par le refresh global
        if self.water_temperature > self.saturation_temperature:
            temperature_surplus = self.water_temperature - self.saturation_temperature
            amount_boiled = int(temperature_surplus * self.boiling_coefficient)

            self.water_temperature = self.saturation_temperature

            self.water_amount -= amount_boiled
            self.steam_amount += amount_boiled

            self.pressure = (self.steam_amount * 
                             self.steam_pressure_coefficient * 
                             ( self.water_temperature + 273 ) / 373)

            self.saturation_temperature = boiling_point(self.pressure)
        
        elif self.water_temperature < self.saturation_temperature:
            temperature_deficit = self.saturation_temperature - self.water_temperature
            amount_condensed = int(temperature_deficit * self.condensation_coefficient)

            amount_condensed = min(amount_condensed, self.steam_amount)

            self.steam_amount -= amount_condensed
            self.water_amount += amount_condensed

            self.pressure = (self.steam_amount * 
                            self.steam_pressure_coefficient * 
                            ( self.water_temperature + 273 ) / 373)

            self.saturation_temperature = boiling_point(self.pressure)



class Assembly():
    """
        Permet de créer un assemblage combustible nucléaire.
        Capable de gérer sa propre physique.
        Simule une activité neutronique avec des valeurs arbitraire ainsi que des facteurs
        réglé pour être le plus proche possible de la réalité.
        Capable de générer de la chaleur.
    """
    def __init__(self, fuel):
        # Gestion arbitraire des neutrons
        self.max_neutron = 100000000000
        self.number_of_neutrons = 1000
        self.idle_neutrons= 1000
        self.previews_neutrons = 1000

        # Gestion de la puissance/accelération du réacteur
        self.rods_pulled = 0
        self.some_factors = 1

        self.fuel = fuel

    def refresh(self, water_density):
        # Actualise la physique de l'assemblage combustible
        heat_coefficient =  1 - (0.3 * self.number_of_neutrons / self.max_neutron)

        self.some_factors = (2 * ( 0.2 + self.rods_pulled * 0.8 / 100 ) * 
                             (water_density / 1000) ** 0.1 * 
                             (self.fuel / 100) * 
                             heat_coefficient)
        self.previews_neutrons = self.number_of_neutrons
        self.number_of_neutrons = self.some_factors * (self.previews_neutrons + self.idle_neutrons)

        return


    def get_power(self):
        # Permet de connaitre la puissance thermique local de l'assemblage en pourcentage
        power = self.number_of_neutrons / self.max_neutron
        return power

    def get_period(self, TimeStep):
        # Permet de connaitre la période local de l'assemblage
        # Pas utilisé puisque c'est un réacteur 2 dimensions
        # M'a permis de tester le système d'assemblage (quand c'était encore un réacteur 1 dimension)
        try:
            reactor_period = 1 / math.log( self.number_of_neutrons / self.previews_neutrons ) * (1 / TimeStep)
        except:
            return float("inf")
        if reactor_period>10000:
            return float("inf")
        return reactor_period
    
    def raise_rods(self, value):
        #Permet de lever la barre de contrôle de l'assemblage
        if self.rods_pulled + value > 100:
            self.rods_pulled = 100.
            return
        if self.rods_pulled + value < 0:
            self.rods_pulled = 0.
            return
        self.rods_pulled += value

    def __debug_raise__(self):
        # Permet de tester la physique à pleine puissance (cela me permet de calibrer les différents coefficient
        # pour coller au mieux à la réalité)
        self.rods_pulled = 100

    



def Propagation(matrice:list[list[Assembly]]):
    #Permet de Gerer la propagation des neutrons entre les différents assemblages
    neutron_matrice = [[0 for void in range(len(matrice[i]))] for i in range(len(matrice))]

    direct_direction = ((0,1),(1,0),(0,-1),(-1,0))
    diagonal_direction = ((1,1),(1,-1),(-1,1),(-1,-1))

    for x in range(len(matrice)):
        for y in range(len(matrice[x])):

            if matrice[x][y] is None:
                continue

            neutrons = matrice[x][y].number_of_neutrons
            propagation = neutrons/2
            matrice[x][y].number_of_neutrons -= propagation

            direct_portion = propagation/6
            diagonal_portion = propagation/12

            neutrons_loss = 0

            for x1,y1 in direct_direction:
                if 0 <= x+x1 <= len(matrice)-1 and 0 <= y+y1 <= len(matrice[x+x1])-1 and matrice[x+x1][y+y1] is not None:
                    neutron_matrice[x+x1][y+y1] += direct_portion
                else:
                    neutrons_loss += direct_portion

            for x1,y1 in diagonal_direction:
                if 0 <= x+x1 <= len(matrice)-1 and 0 <= y+y1 <= len(matrice[x+x1])-1 and matrice[x+x1][y+y1] is not None:
                    neutron_matrice[x+x1][y+y1] += diagonal_portion
                else:
                    neutrons_loss += diagonal_portion


            matrice[x][y].number_of_neutrons += neutrons_loss*0.6
    
    for x in range(len(matrice)):
        for y in range(len(matrice[x])):
            if matrice[x][y] is None:
                continue
            matrice[x][y].number_of_neutrons += neutron_matrice[x][y]


def boiling_point(pressure):
    #Permet de calculer le point d'ébullition de l'eau à une préssion donnée en hPa
    pressure*=10000
    if pressure/10000000>20:
        pressure=20*10000000
    temperature =( 1.0002646407033929 * 10**2
        + 1.2485512687579338 * (10**( -5 )) * pressure
        - 6.0865396119409739 * (10**( -13 )) * pressure**2
        + 1.8961630152963698 * (10**( -20 )) * pressure**3
        - 3.4939669493500672 * (10**( -28 )) * pressure**4
        + 3.8256436415169860 * (10**( -36 )) * pressure**5
        - 2.4385640912095220 * (10**( -44 )) * pressure**6
        + 8.3341353038170792 * (10**( -53 )) * pressure**7
        - 1.1778965239174813 * (10**( -61 )) * pressure**8 )
    return temperature

def water_density(temperature):
    #Permet de calculer la densité de l'eau suivant une température donnée en Kelvin
    density = (-0.000004467711 * temperature**3
        -0.000560288485 * temperature**2
        -0.429148844451 * temperature
        +1010.035413387815)
    return density