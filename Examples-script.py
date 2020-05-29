# Example of use of Aircraft Opertaing Conditions class

# 1/ Import the required libraries
import pyEnvAC.operatingConditions as ACOp
import pyEnvAC.airProperties as airProp

# 2/ Create the operating conditions
'''
Based on the generic aircraft environmental envelope, define the operating conditions of your study:
Operating conditions = ACOp.operatingConditions(Name, Type of day, Altitude, Aircraft speed)
Name: name of the operating conditions (format: string)
Type of day: Extra-Hot, Hot, Normal, Cold, Extra-Cold (format: string)
Remark: Normal means ISA conditions
Altitude: altitude of the aircraft in feet (format: float)
Aircraft speed: speed in Mach (format: float)
'''
# Example 1: Aircraft on ground, ISA conditions, high altitude airport at 15000ft
Ground_1 = ACOp.operatingConditions('Ground_1', 'Normal', 15000., 0.)

# Example 2: Aircraft flying at Ma=0.7 and at 40000ft, Hot day condition (ISA+20)
Flight_1 = ACOp.operatingConditions('Flight_1', 'Hot', 40000., 0.7)

# 3/ Use of available methods in the class
# Ambient temperature for the considered operating conditions
Ambient_Temperature_F1 = Flight_1.Ttot()
Ambient_Temperature_FG = Ground_1.Ttot()