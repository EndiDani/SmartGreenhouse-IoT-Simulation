from factories.sensor_factory   import sensor_factory
from factories.actuator_factory import actuator_factory
from zones.zone                 import Zone 
from sensors                    import thermometer_sensor, airquality_sensor, humidity_sensor, light_sensor, energy_consume_sensor
from actuators                  import vent_actuator, pump_actuator

# ThermometerSensor(min_temp, max_temp, k, k_fan, act_threshold)
# HumiditySensor(min_hum, max_hum, evap_coeff, evap_offset, pump_gain, act_threshold)
# AirQualitySensor(min_ppm, max_ppm, k, k_fan, act_threshold)

# # # # 
# Zona A: coltivazione in piena luce (piante che amano tanto sole)
# ThermometerSensor(20.0, 40.0, 0.04, 0.02, 33.0)
# HumiditySensor(25.0, 70.0, 0.12, 1.0, 6.0, 50.0)
# AirQualitySensor(400.0, 1500.0, 0.03, 0.015, 1000.0)

sensors_A = [
    sensor_factory("thermometer"),
    sensor_factory("air_quality"),
    sensor_factory("humidity"),
    sensor_factory("light"),
    sensor_factory("energy_consume")
]

actuators_A = [
    actuator_factory("vent"),
    actuator_factory("pump")
]

zone_A = Zone(name="A", sensors=sensors_A, actuators=actuators_A, neighbors=["B", "D"])

# # # # 
# Zona B: coltivazione ombreggiata (piante più delicate)
# ThermometerSensor(15.0, 30.0, 0.03, 0.02, 28.0)
# HumiditySensor(40.0, 85.0, 0.08, 1.2, 5.5, 65.0)
# AirQualitySensor(400.0, 1400.0, 0.04, 0.02, 950.0)

sensors_B = [
    sensor_factory("thermometer"),
    sensor_factory("air_quality"),
    sensor_factory("humidity"),
    sensor_factory("light"),
    sensor_factory("energy_consume")
]

actuators_B = [
    actuator_factory("vent"),
    actuator_factory("pump")
]

zone_B = Zone(name="B", sensors=sensors_B, actuators=actuators_B, neighbors=["A", "E"])


# # # #
# Zona C: serre tropicali umide (orchidee, felci)
# ThermometerSensor(22.0, 35.0, 0.05, 0.02, 31.0)
# HumiditySensor(60.0, 95.0, 0.09, 1.0, 5.0, 75.0)
# AirQualitySensor(400.0, 1200.0, 0.02, 0.01, 850.0)

sensors_C = [
    sensor_factory("thermometer"),
    sensor_factory("air_quality"),
    sensor_factory("humidity"),
    sensor_factory("light"),
    sensor_factory("energy_consume")
]

actuators_C = [
    actuator_factory("vent"),
    actuator_factory("pump")
]

zone_C = Zone(name="C", sensors=sensors_C, actuators=actuators_C, neighbors=["D"])


# # # #
# Zona D: ortaggi da serra  (pomodori, insalate)
# ThermometerSensor(18.0, 32.0, 0.04, 0.02, 30.0)
# HumiditySensor(50.0, 80.0, 0.10, 1.5, 5.0, 60.0)
# AirQualitySensor(400.0, 1300.0, 0.03, 0.015, 900.0)

sensors_D = [
    sensor_factory("thermometer"),
    sensor_factory("air_quality"),
    sensor_factory("humidity"),
    sensor_factory("light"),
    sensor_factory("energy_consume")
]

actuators_D = [
    actuator_factory("vent"),
    actuator_factory("pump")
]

zone_D = Zone(name="D", sensors=sensors_D, actuators=actuators_D, neighbors=["A", "C"])

# # # #
# Zona E: vivaio per piante da fiore (rose, gerani)
# ThermometerSensor(16.0, 28.0, 0.035, 0.02, 26.0)
# HumiditySensor(45.0, 75.0, 0.07, 1.3, 5.5, 55.0)
# AirQualitySensor(400.0, 1400.0, 0.03, 0.015, 950.0)

sensors_E = [
    sensor_factory("thermometer"),
    sensor_factory("air_quality"),
    sensor_factory("humidity"),
    sensor_factory("light"),
    sensor_factory("energy_consume")
]

actuators_E = [
    actuator_factory("vent"),
    actuator_factory("pump")
]

zone_E = Zone(name="E", sensors=sensors_E, actuators=actuators_E, neighbors=["B"])




for i in range(50):
    zone_A.workflow()
    state = zone_A.get_state()  
    print(f"\n\nGiro numero {i}")
    for sensor_id, value in state.items():
        print(f"Sensor ID: {sensor_id} - Last Value: {value}")
