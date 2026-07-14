from .orchid_data import care_for, display_name


def _check(value, low, high, unit, name):
    if value < low:
        msg, level = f"{name} is low ({value}{unit}). Ideal: {low}-{high}{unit}.", "warning"
    elif value > high:
        msg, level = f"{name} is high ({value}{unit}). Ideal: {low}-{high}{unit}.", "warning"
    else:
        msg, level = f"{name} is optimal ({value}{unit}).", "ok"
    return {"metric": name, "level": level, "value": value, "unit": unit, "message": msg}


def evaluate(species_name, sensors):
    care = care_for(species_name)
    checks = [
        _check(sensors["temp_c"], *care["temp_c"], "°C", "Temperature"),
        _check(sensors["humidity_pct"], *care["humidity_pct"], "%", "Humidity"),
        _check(sensors["light_lux"], *care["light_lux"], " lux", "Light"),
    ]
    warnings = [c for c in checks if c["level"] == "warning"]
    status = "healthy" if not warnings else ("attention" if len(warnings) == 1 else "critical")
    return {
        "species": species_name,
        "display_name": display_name(species_name),
        "description": care.get("desc", ""),
        "difficulty": care["difficulty"],
        "status": status,
        "checks": checks,
        "warnings": warnings,
        "tips": care["tips"],
        "water_days": care["water_days"],
        "ideal": {"temp_c": care["temp_c"], "humidity_pct": care["humidity_pct"], "light_lux": care["light_lux"]},
    }
