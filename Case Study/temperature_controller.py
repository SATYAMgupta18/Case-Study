import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define input and output variables
temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
error = ctrl.Antecedent(np.arange(-10, 11, 1), 'error')
output = ctrl.Consequent(np.arange(-10, 11, 1), 'output')

# Define membership functions
temperature['low'] = fuzz.trimf(temperature.universe, [0, 0, 50])
temperature['medium'] = fuzz.trimf(temperature.universe, [20, 50, 80])
temperature['high'] = fuzz.trimf(temperature.universe, [50, 100, 100])

error['negative'] = fuzz.trimf(error.universe, [-10, -10, 0])
error['zero'] = fuzz.trimf(error.universe, [-5, 0, 5])
error['positive'] = fuzz.trimf(error.universe, [0, 10, 10])

output['low'] = fuzz.trimf(output.universe, [-10, -10, 0])
output['medium'] = fuzz.trimf(output.universe, [-5, 0, 5])
output['high'] = fuzz.trimf(output.universe, [0, 10, 10])

# Define fuzzy rules for Controller 1
rule1_ctrl1 = ctrl.Rule(temperature['low'] & error['negative'], output['high'])
rule2_ctrl1 = ctrl.Rule(temperature['medium'] & error['zero'], output['medium'])
rule3_ctrl1 = ctrl.Rule(temperature['high'] & error['positive'], output['low'])

# Define fuzzy rules for Controller 2 (backup controller)
rule1_ctrl2 = ctrl.Rule(temperature['low'] | error['negative'], output['high'])
rule2_ctrl2 = ctrl.Rule(temperature['medium'] | error['zero'], output['medium'])
rule3_ctrl2 = ctrl.Rule(temperature['high'] | error['positive'], output['low'])

# Create fuzzy control systems for both controllers
control_system_ctrl1 = ctrl.ControlSystem([rule1_ctrl1, rule2_ctrl1, rule3_ctrl1])
control_system_ctrl2 = ctrl.ControlSystem([rule1_ctrl2, rule2_ctrl2, rule3_ctrl2])

controller1 = ctrl.ControlSystemSimulation(control_system_ctrl1)
controller2 = ctrl.ControlSystemSimulation(control_system_ctrl2)

# Simulate temperature control with potential faults
faulty_sensor = False  # Simulate faulty sensor
desired_temperature = 70

for t in range(100):
    # Simulate temperature measurement (with or without fault)
    if not faulty_sensor:
        measured_temperature = np.random.normal(desired_temperature, 2)  # Normal temperature measurement
    else:
        measured_temperature = np.random.normal(desired_temperature, 5)  # Faulty temperature measurement

    # Compute control action using Controller 1
    controller1.input['temperature'] = measured_temperature
    controller1.input['error'] = desired_temperature - measured_temperature
    controller1.compute()
    control_action = controller1.output['output']

    # If Controller 1 output is unreliable (e.g., due to fault), switch to Controller 2
    if np.isnan(control_action):
        controller2.input['temperature'] = measured_temperature
        controller2.input['error'] = desired_temperature - measured_temperature
        controller2.compute()
        control_action = controller2.output['output']

    print(f"Time: {t}, Measured Temperature: {measured_temperature}, Control Action: {control_action}")
