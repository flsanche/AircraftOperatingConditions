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
                 *args,
                 **kwargs):

        self.name = name
        self.dayType = dayType
        self.altitude = altitude
        self.speed = speed

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