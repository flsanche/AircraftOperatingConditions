# Operating Conditions
# This object defines the classes and functions used to define the oprating conditions

import math
import numpy as np

class operatingConditions():
    '''
    # Definition of the operating conditions
    name: name of the operating conditions
    dayType: type of the day
    altitude: altitude of the aircraft in ft
    speed: aircraft speed in Ma
    '''
    # Sea level conditions
    pressureSL = 101325.
    densitySL = 1.225
    temperatureSL = 15.
    g = 9.80665
    gamma = 1.4
    R = 287.04

    def __init__(self,
                 name: str,
                 dayType: str,
                 altitude: float,
                 speed: float,
                 time: str,
                 *args,
                 **kwargs):

        self.name = name
        self.dayType = dayType
        self.altitude = altitude
        self.speed = speed
        self.time = time

    def pressure(self):
        # Ambient pressure in Pa
        altitudeMeter = self.altitude / 3.28084
        T_ISA_K = operatingConditions.T_ISA(self) + 273.15
        return operatingConditions.pressureSL * (1.-(0.0065*altitudeMeter/T_ISA_K))**5.255

    def T_ISA(self):
        # International Standard Atmosphere Temperature
        if self.altitude<=36000.:
            return operatingConditions.temperatureSL - 1.98 * self.altitude / 1000.
        else:
            return -56.5
    
    def Tstat(self):
        # Ambient Static Temperature based on a temperature envelope
        # Flight conditions
        if self.speed != 0.:
            if self.dayType == 'Extra-Hot':
                if self.altitude <= 15000.:
                    return operatingConditions.T_ISA(self) + 40.
                else:
                    if self.altitude <=35000.:
                        return operatingConditions.T_ISA(self) + 35.
                    else:
                        return operatingConditions.T_ISA(self) + 30.
            else:
                if self.dayType == 'Hot':
                    if self.altitude <= 15000.:
                        return operatingConditions.T_ISA(self) + 20.
                    else:
                        if self.altitude <=35000.:
                            return operatingConditions.T_ISA(self) + 15.
                        else:
                            return operatingConditions.T_ISA(self) + 10.
                else:
                    if self.dayType == 'Normal':
                        return operatingConditions.T_ISA(self)
                    else:
                        if self.dayType == 'Cold':
                            if self.altitude <= 15000.:
                                return operatingConditions.T_ISA(self) - 30.
                            else:
                                if self.altitude <=35000.:
                                    return operatingConditions.T_ISA(self) - 10.
                                else:
                                    return operatingConditions.T_ISA(self) - 15.
                        else:
                            if self.dayType == 'Extra-Cold':
                                if self.altitude <= 15000.:
                                    return -55.
                                else:
                                    if self.altitude <= 30000.:
                                        return operatingConditions.T_ISA(self) - 30.
                                    else:
                                        return operatingConditions.T_ISA(self) - 20.
        # Ground conditions
        else:
            if self.dayType == 'Extra-Hot':
                if self.altitude < 15000.:
                    return operatingConditions.T_ISA(self) + 40.
                else:
                    return operatingConditions.T_ISA(self) + 45.
            else:
                if self.dayType == 'Hot':
                    if self.altitude < 15000.:
                        return operatingConditions.T_ISA(self) + 30.
                    else:
                        return operatingConditions.T_ISA(self) + 25.
                else:
                    if self.dayType == 'Normal':
                        return operatingConditions.T_ISA(self)
                    else:
                        if self.dayType == 'Cold':
                            if self.altitude < 15000.:
                                return operatingConditions.T_ISA(self) - 30.
                            else:
                                return operatingConditions.T_ISA(self) - 5.

                        else:
                            if self.dayType == 'Extra-Cold':
                                if self.altitude <= 10000.:
                                    return -55.
                                else:
                                    return self.altitude * 0.005 - 105

    def Ttot(self):
        # Total air temperature
        return (1+((operatingConditions.gamma-1)/2) * self.speed**2) * (operatingConditions.Tstat(self)+273.15) - 273.15

    def solarLoad(self):
        # Solar heat flux outside the atmosphere
        Q_sun = 1367.

        if self.altitude == 0.:
            # Percentages of solar heat flux that reaches the earth surface
            # Direct to Earth = 0.7
            # Scattered to Earth = 0.07
            return 0.77 * Q_sun
        else:
            if self.altitude <= 10000.:
            # Percentages of solar heat flux that is available at 10000 feet
            # Direct to Earth = 0.7
            # Scattered to Earth = 0.07
            # Absorbed by the layers below 10000. = 0.07
                return 0.84 * Q_sun
            else:
            # Percentages of solar heat flux that is available at 10000 feet
            # Direct to Earth = 0.7
            # Scattered to Earth = 0.07
            # Absorbed by the layers below 30000. = 0.15
                return 0.92 * Q_sun

    def radSky(self):
        # Relative Humidity
        RH = 50.
        # Dew point Temperature
        dewTemp = -34.56 + 0.446 * RH + 0.873 * operatingConditions.Ttot(self)
        # Sky emissivity
        skyEmissivity = 0.741 + 0.0062 * dewTemp
        # Stefan-Boltzmann Constant
        sigmaB = 5.67E-8

        return skyEmissivity * sigmaB * operatingConditions.Ttot(self)**4

    def Tground(self):
        # The models are based on Khan et al. 2019 "Determining asphalt surface temperature using weather parameters"
        # Wind speed on ground (assumed)
        wind = 5.
        # Solar load
        Q_sun = operatingConditions.solarLoad(self)
        # Relative Humidity (assumed)
        RH = 50.
        # Temperature of the environment
        Tenv = operatingConditions.Ttot(self)

        if self.time == 'day':
            return 41.51 + 0.102 * wind + 1.71 * Tenv + 0.032 * RH - 0.029 * Q_sun + 0.002 * Tenv * RH + 5.7E-4 * wind * Q_sun + 0.0014 * Q_sun + 4.09E10-5 * Q_sun**2 - 1.15E-6 * Tenv * Q_sun**2
        else:
            return 18.471 + 0.507 * Tenv - 0.00345 * RH - 0.649 * wind + 0.00941 * Tenv**2 + 4.8946E-5 * Tenv**3