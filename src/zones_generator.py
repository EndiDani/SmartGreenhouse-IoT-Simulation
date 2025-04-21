from factories.sensor_factory   import sensor_factory
from factories.actuator_factory import actuator_factory
from zones.zone                 import Zone 
from sensors                    import thermometer_sensor, airquality_sensor, humidity_sensor, light_sensor, energy_consume_sensor
from actuators                  import vent_actuator, pump_actuator

# ThermometerSensor(min_temp, max_temp, k, k_fan, act_threshold)
# HumiditySensor(min_hum, max_hum, evap_coeff, evap_offset, pump_gain, act_threshold)
# AirQualitySensor(min_ppm, max_ppm, k, k_fan, act_threshold)


def create_zones():
    # # # # 
    # Zona A: coltivazione in piena luce (piante che amano tanto sole)
    # ThermometerSensor(20.0, 40.0, 0.04, 0.02, 33.0)
    # HumiditySensor(25.0, 70.0, 0.12, 1.0, 6.0, 50.0)
    # AirQualitySensor(400.0, 1500.0, 0.03, 0.015, 1000.0)

    zone_A = Zone(
        name="A",
        sensors=[
            sensor_factory("thermometer", min_temp=20.0, max_temp=40.0, k=0.04, k_fan=0.02, act_threshold=33.0),
            sensor_factory("humidity", min_hum=25.0, max_hum=70.0, evap_coeff=0.12, evap_offset=1.0, pump_gain=6.0, act_threshold=50.0),
            sensor_factory("air_quality", min_ppm=400.0, max_ppm=1500.0, k=0.03, k_fan=0.015, act_threshold=1000.0),
            sensor_factory("light"),
            sensor_factory("energy_consume")
        ],
        actuators=[
            actuator_factory("vent"),
            actuator_factory("pump")
        ],
        neighbors=["B", "D"]
    )

    # # # # 
    # Zona B: coltivazione ombreggiata (piante più delicate)
    # ThermometerSensor(15.0, 30.0, 0.03, 0.02, 28.0)
    # HumiditySensor(40.0, 85.0, 0.08, 1.2, 5.5, 65.0)
    # AirQualitySensor(400.0, 1400.0, 0.04, 0.02, 950.0)

    zone_B = Zone(
        name="B",
        sensors=[
            sensor_factory("thermometer", min_temp=15.0, max_temp=30.0, k=0.03, k_fan=0.02, act_threshold=28.0),
            sensor_factory("humidity", min_hum=40.0, max_hum=85.0, evap_coeff=0.08, evap_offset=1.2, pump_gain=5.5, act_threshold=65.0),  
            sensor_factory("air_quality", min_ppm=400.0, max_ppm=1400.0, k=0.04, k_fan=0.02, act_threshold=950.0),
            sensor_factory("light"),
            sensor_factory("energy_consume")
        ],
        actuators=[
            actuator_factory("vent"),
            actuator_factory("pump")
        ],
        neighbors=["A", "E"]
    )   

    # # # #
    # Zona C: serre tropicali umide (orchidee, felci)
    # ThermometerSensor(22.0, 35.0, 0.05, 0.02, 31.0)
    # HumiditySensor(60.0, 95.0, 0.09, 1.0, 5.0, 75.0)
    # AirQualitySensor(400.0, 1200.0, 0.02, 0.01, 850.0)

    zone_C = Zone(
        name="C",
        sensors=[
            sensor_factory("thermometer", min_temp=22.0, max_temp=35.0, k=0.05, k_fan=0.02, act_threshold=31.0),
            sensor_factory("humidity", min_hum=60.0, max_hum=95.0, evap_coeff=0.09, evap_offset=1.0, pump_gain=5.0, act_threshold=75.0),
            sensor_factory("air_quality", min_ppm=400.0, max_ppm=1200.0, k=0.02, k_fan=0.01, act_threshold=850.0),
            sensor_factory("light"),
            sensor_factory("energy_consume")
        ],
        actuators=[
            actuator_factory("vent"),
            actuator_factory("pump")
        ],
        neighbors=["D"]
    )

    # # # #
    # Zona D: ortaggi da serra  (pomodori, insalate)
    # ThermometerSensor(18.0, 32.0, 0.04, 0.02, 30.0)
    # HumiditySensor(50.0, 80.0, 0.10, 1.5, 5.0, 60.0)
    # AirQualitySensor(400.0, 1300.0, 0.03, 0.015, 900.0)

    zone_D = Zone(
        name="D",
        sensors=[
            sensor_factory("thermometer", min_temp=18.0, max_temp=32.0, k=0.04, k_fan=0.02, act_threshold=30.0),
            sensor_factory("humidity", min_hum=50.0, max_hum=80.0, evap_coeff=0.10, evap_offset=1.5, pump_gain=5.0, act_threshold=60.0),
            sensor_factory("air_quality", min_ppm=400.0, max_ppm=1300.0, k=0.03, k_fan=0.015, act_threshold=900.0),
            sensor_factory("light"),
            sensor_factory("energy_consume")
        ],
        actuators=[
            actuator_factory("vent"),
            actuator_factory("pump")
        ],
        neighbors=["A", "C"]
    )

    # # # #
    # Zona E: vivaio per piante da fiore (rose, gerani)
    # ThermometerSensor(16.0, 28.0, 0.035, 0.02, 26.0)
    # HumiditySensor(45.0, 75.0, 0.07, 1.3, 5.5, 55.0)
    # AirQualitySensor(400.0, 1400.0, 0.03, 0.015, 950.0)

    zone_E = Zone(
        name="E",
        sensors=[
            sensor_factory("thermometer", min_temp=16.0, max_temp=28.0, k=0.035, k_fan=0.02, act_threshold=26.0),
            sensor_factory("humidity", min_hum=45.0, max_hum=75.0, evap_coeff=0.07, evap_offset=1.3, pump_gain=5.5, act_threshold=55.0),
            sensor_factory("air_quality", min_ppm=400.0, max_ppm=1400.0, k=0.03, k_fan=0.015, act_threshold=950.0),
            sensor_factory("light"),
            sensor_factory("energy_consume")
        ],
        actuators=[
            actuator_factory("vent"),
            actuator_factory("pump")
        ],
        neighbors=["B"]
    )

    return {"A": zone_A, "B": zone_B, "C": zone_C, "D": zone_D, "E": zone_E}
