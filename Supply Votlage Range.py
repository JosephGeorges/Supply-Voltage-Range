'''
This Python script automates the supply voltage range test required for DV-testing according to the regulations of CS.00054.

Supply Voltage Range: Apply 9V-16V, 0.5V increments  to the DUT 
Requirement: DUT specified functions must operate as intended at each voltage.

Program: Automates R&S HMC8041 Power Supply, Keithley  DMM6500 Multi-meter

Python 3.7.7
PyVISA 1.10.1
'''
import pyvisa
import pandas as pd
import numpy as np
import time

#Variables: Delay time between increments, two lists to display voltage and currenting readings
delay = 10 
volt_list = []
current_list = []

#Configure Devices through IP Address
rm = pyvisa.ResourceManager()
HMC = rm.open_resource('TCPIP0::172.21.120.111::inst0::INSTR')
DMM = rm.open_resource('TCPIP0::172.21.120.129::inst0::INSTR')

#Identify Devices
print(HMC.query("*IDN?"))
print(DMM.query("*IDN?"))

#Reset Devices to Default
HMC.write('*RST')
DMM.write("*RST")

#Configure DMM Multimeter to measure current up to 3A
DMM.write(":SENS:FUNC 'CURRENT:DC'") 
DMM.write(":SENS:CURRENT:RANG 3") 

#Begin Test by Setting PSU Voltage to 9V
HMC.write("SOURce:VOLTage:LEVel:IMMediate:AMPLitude 9V")
HMC.write("OUTPUT ON")

#Enter loop for test cycle
time.sleep(delay)
for voltage in np.arange(9.5,16.5,0.5):
    HMC.write("SOURce:VOLTage:LEVel:IMMediate:AMPLitude {}V".format(voltage))
    volt_meas = HMC.query("MEASure:SCALar:VOLTage:DC?")
    volt_list.append(volt_meas)
    current_meas = DMM.query(":READ?")
    current_list.append(current_meas)
    time.sleep(delay) #change delay to whatever needed

#Final measurements
volt_meas = HMC.query("MEASure:SCALar:VOLTage:DC?")
volt_list.append(volt_meas)

current_meas = DMM.query(":READ?")
current_list.append(current_meas)

print("Voltage measurements: \n")
print(volt_list)
print("\n")
print("Current measurements: \n")
print(current_list)

#Writing data to excel
filepath = 'Supply Voltage Range.xlsx'
df = pd.DataFrame({'Voltage': volt_list, 'Current': current_list})
df.to_excel(filepath, index = False)






