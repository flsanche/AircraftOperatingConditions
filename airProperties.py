# Air properties
# This object defines the classes and functions used to calculate the air properties
# The main assumptions are: ideal gas, pressure and temperature dependencies only considered

import math

class airProperties():
    '''
    # Calculation of the air properties for specific operating conditions
    operatingConditions: operating conditions of the aircraft
    ambTemperature: average ambient temperature of the environment under study (e.g. equipment bay,
    aircraf environment, etc.)
    '''
    # Sea level conditions
    pressureSL = 101325.
    densitySL = 1.225
    temperatureSL = 15.
    g = 9.80665
    gamma = 1.4
    R = 287.04

    def __init__(self,
                 Pamb: float,
                 ambTemperature: float,
                 *args,
                 **kwargs):

        self.Pamb = Pamb
        self.ambTemperature = ambTemperature

    def rho_air(self):
        # Air density in kg/m³
        return self.Pamb / (airProperties.R * self.ambTemperature)
    
    def k_air(self):
        # Thermal conductivity of air in W/m/K
        return 8.E-05 * self.ambTemperature + 0.0236

    def mu_air(self):
        # Dynamic viscosity of air in kg/m/s
        return 5.E-08 * self.ambTemperature + 2.E-05
    
    def beta_air(self):
        # Thermal expansion coefficient of air in 1/K
        # Ideal gas assumption
        return 1. / self.ambTemperature
    
    def Cp_air(self):
        # Heat capacity of air in J/kg/K
        return 1.E-05 * self.ambTemperature**3 - 0.0013 * self.ambTemperature**2 + 0.0422 * self.ambTemperature + 1006.4