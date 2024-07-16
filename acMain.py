import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Input variables
temperature = ctrl.Antecedent(np.arange(0, 111, 1), 'temperature')
cloud = ctrl.Antecedent(np.arange(0, 101, 1), 'cloud')

# Output variable
cooling_temp = ctrl.Consequent(np.arange(16, 31, 1), 'cooling_temp')

# temp func
temperature['freezing'] = fuzz.trapmf(temperature.universe, [0, 0, 30, 50])
temperature['cool'] = fuzz.trimf(temperature.universe, [30, 50, 70])
temperature['warm'] = fuzz.trimf(temperature.universe, [50, 70, 90])
temperature['hot'] = fuzz.trapmf(temperature.universe, [70, 90, 110, 110])

#  cloud func
cloud['sunny'] = fuzz.trapmf(cloud.universe, [0, 0, 20, 40])
cloud['cloudy'] = fuzz.trimf(cloud.universe, [20, 50, 80])
cloud['overcast'] = fuzz.trapmf(cloud.universe, [60, 80, 100, 100])

# Fungsi cooling temperature
cooling_temp['very_cold'] = fuzz.trapmf(cooling_temp.universe, [16, 16, 18, 20])
cooling_temp['cold'] = fuzz.trimf(cooling_temp.universe, [18, 20, 22])
cooling_temp['normal'] = fuzz.trimf(cooling_temp.universe, [20, 24, 28])
cooling_temp['warm'] = fuzz.trapmf(cooling_temp.universe, [26, 28, 30, 30])

# Rules
rule1 = ctrl.Rule(cloud['sunny'] & temperature['warm'], cooling_temp['cold'])
rule2 = ctrl.Rule(cloud['cloudy'] & temperature['cool'], cooling_temp['normal'])
rule3 = ctrl.Rule(cloud['sunny'] | temperature['hot'], cooling_temp['very_cold'])
rule4 = ctrl.Rule(cloud['overcast'] | temperature['freezing'], cooling_temp['warm'])

# Control system
cooling_temp_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
cooling_temp_simulation = ctrl.ControlSystemSimulation(cooling_temp_ctrl)

# Menghitung temperature cooling berdasarkan input
def compute_cooling_temp(temp, cloud_coverage):
    cooling_temp_simulation.input['temperature'] = temp
    cooling_temp_simulation.input['cloud'] = cloud_coverage
    cooling_temp_simulation.compute()
    return cooling_temp_simulation.output['cooling_temp']

# Inputs
temperature_value = 70
cloud_value = 80

cooling_temp_value = compute_cooling_temp(temperature_value, cloud_value)
print(f'Atur suhu AC anda menjadi: {round(cooling_temp_value)}°C')
