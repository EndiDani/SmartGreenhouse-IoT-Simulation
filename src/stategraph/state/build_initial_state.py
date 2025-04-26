from stategraph.state.load_zones import load_zones_data

def build_initial_state(zone_name: str) -> dict: 
    zones_data = load_zones_data(zone_name)
    sensors    = zones_data["sensors"]
    actuators  = zones_data["actuators"]
    neighbors  = zones_data["neighbors"]

    initial_state = {
        "zone":             zones_data["name"],
        "light":            sensors["light"]["state"],
        "light_delta":      0.,
        "thermometer":      sensors["thermometer"]["state"],
        "delta_temp":       0., 
        "air_quality":      sensors["air_quality"]["state"],
        "humidity":         sensors["humidity"]["state"],
        "evaporation_rate": 0., 
        "energy_consume":   sensors["energy_consume"]["state"],
        "vent_on":          actuators["vent"]["powered"],
        "pump_on":          actuators["pump"]["powered"],
        "neighbors":        neighbors,
        "env": {
            # Termometro
            "k_temp":                 sensors["thermometer"]["k"],
            "min_temp":               sensors["thermometer"]["min_temp"],
            "max_temp":               sensors["thermometer"]["max_temp"],
            "k_fan_temp":             sensors["thermometer"]["k_fan"],
            "act_threshold_temp":     sensors["thermometer"]["act_threshold"],
            # Umidità
            "min_hum":                sensors["humidity"]["min_hum"],
            "max_hum":                sensors["humidity"]["max_hum"],
            "evap_coeff":             sensors["humidity"]["evap_coeff"],
            "evap_offset":            sensors["humidity"]["evap_offset"],
            "pump_gain":              sensors["humidity"]["pump_gain"],
            "act_threshold_humidity": sensors["humidity"]["act_threshold"],
            # Qualità aria
            "min_ppm":                sensors["air_quality"]["min_ppm"],
            "max_ppm":                sensors["air_quality"]["max_ppm"],
            "k_air":                  sensors["air_quality"]["k"],
            "k_fan_air":              sensors["air_quality"]["k_fan"],
            "act_threshold_air":      sensors["air_quality"]["act_threshold"],
            # Energia
            "idle_power":             sensors["energy_consume"]["idle_power"],
            # Ventola
            "power_rating_vent":      actuators["vent"]["power_rating"],
            # Pompa
            "power_rating_pump":      actuators["pump"]["power_rating"]
        },
        "steps": [],
        "events": [],
    }
    return initial_state
