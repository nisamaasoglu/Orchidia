# Care knowledge base for common orchid genera.
# Species folder names are matched against these keys by substring,
# so "Phalaenopsis amabilis" resolves to the "phalaenopsis" profile.

CARE_DB = {
    "phalaenopsis": {"difficulty": "Beginner", "temp_c": (18, 28), "humidity_pct": (50, 70), "light_lux": (10000, 20000), "water_days": 7,
        "tips": ["Water weekly; let roots dry between waterings.", "Bright indirect light — avoid direct midday sun.", "Silver-green roots mean it's time to water."]},
    "cattleya": {"difficulty": "Intermediate", "temp_c": (20, 30), "humidity_pct": (40, 70), "light_lux": (20000, 30000), "water_days": 6,
        "tips": ["Loves bright light with some gentle direct sun.", "Let the mix dry out fully before watering.", "Needs a day/night temperature drop to bloom."]},
    "dendrobium": {"difficulty": "Intermediate", "temp_c": (18, 30), "humidity_pct": (50, 70), "light_lux": (15000, 25000), "water_days": 5,
        "tips": ["Water more in growth season, far less in winter.", "Bright light drives strong cane growth.", "Don't cut leafless canes — they store energy."]},
    "vanda": {"difficulty": "Advanced", "temp_c": (20, 32), "humidity_pct": (60, 80), "light_lux": (25000, 35000), "water_days": 2,
        "tips": ["Loves very high light and humidity.", "Often grown bare-root; water roots daily.", "Feed frequently during active growth."]},
    "oncidium": {"difficulty": "Intermediate", "temp_c": (18, 28), "humidity_pct": (40, 70), "light_lux": (15000, 25000), "water_days": 5,
        "tips": ["Keep evenly moist during growth.", "Bright, filtered light suits it well.", "Pseudobulbs shrivel when under-watered."]},
    "cymbidium": {"difficulty": "Intermediate", "temp_c": (10, 28), "humidity_pct": (40, 60), "light_lux": (20000, 30000), "water_days": 5,
        "tips": ["Tolerates cooler temperatures than most orchids.", "Needs cool autumn nights to set flower spikes.", "Keep well watered in summer."]},
    "paphiopedilum": {"difficulty": "Intermediate", "temp_c": (16, 27), "humidity_pct": (50, 70), "light_lux": (8000, 15000), "water_days": 5,
        "tips": ["Lower light — thrives away from direct sun.", "Keep the mix lightly moist, never soggy.", "No pseudobulbs, so don't let it dry out fully."]},
    "miltonia": {"difficulty": "Intermediate", "temp_c": (16, 26), "humidity_pct": (60, 80), "light_lux": (10000, 18000), "water_days": 4,
        "tips": ["Prefers cooler, humid, shaded conditions.", "Keep evenly moist.", "Pleated leaves signal watering stress."]},
    "masdevallia": {"difficulty": "Advanced", "temp_c": (12, 24), "humidity_pct": (70, 90), "light_lux": (8000, 15000), "water_days": 3,
        "tips": ["Needs cool, very humid, shaded air.", "Never let roots dry out.", "Good air movement prevents rot."]},
    "bulbophyllum": {"difficulty": "Advanced", "temp_c": (18, 30), "humidity_pct": (60, 85), "light_lux": (10000, 18000), "water_days": 3,
        "tips": ["High humidity and steady moisture.", "Moderate, filtered light.", "Best mounted or in shallow pots."]},
    "brassia": {"difficulty": "Intermediate", "temp_c": (18, 29), "humidity_pct": (50, 70), "light_lux": (15000, 22000), "water_days": 5,
        "tips": ["Bright, filtered light.", "Keep moist during active growth.", "Allow slight drying between waterings."]},
    "zygopetalum": {"difficulty": "Intermediate", "temp_c": (15, 27), "humidity_pct": (50, 70), "light_lux": (15000, 22000), "water_days": 5,
        "tips": ["Moderate light, cooler nights.", "Keep evenly moist in growth.", "Avoid wetting foliage to prevent spotting."]},
    "phragmipedium": {"difficulty": "Advanced", "temp_c": (16, 29), "humidity_pct": (60, 80), "light_lux": (10000, 18000), "water_days": 2,
        "tips": ["Loves constantly wet roots — even standing water.", "Moderate light.", "Use pure water; sensitive to salts."]},
    "ludisia": {"difficulty": "Beginner", "temp_c": (18, 28), "humidity_pct": (50, 70), "light_lux": (5000, 12000), "water_days": 4,
        "tips": ["A jewel orchid grown for its foliage.", "Low, indirect light.", "Keep lightly moist, never soggy."]},
    "encyclia": {"difficulty": "Intermediate", "temp_c": (18, 30), "humidity_pct": (40, 65), "light_lux": (20000, 30000), "water_days": 6,
        "tips": ["High light, good air flow.", "Dry out between waterings.", "Reduce water in winter rest."]},
    "epidendrum": {"difficulty": "Beginner", "temp_c": (16, 30), "humidity_pct": (40, 70), "light_lux": (20000, 30000), "water_days": 5,
        "tips": ["Very tough and sun-tolerant.", "Keep moist in growth.", "Great beginner reed-stem orchid."]},
    "maxillaria": {"difficulty": "Intermediate", "temp_c": (16, 28), "humidity_pct": (50, 75), "light_lux": (12000, 20000), "water_days": 4,
        "tips": ["Moderate, filtered light.", "Keep evenly moist.", "Diverse genus — conditions vary by species."]},
    "coelogyne": {"difficulty": "Intermediate", "temp_c": (14, 26), "humidity_pct": (50, 75), "light_lux": (12000, 20000), "water_days": 4,
        "tips": ["Cooler growing, moderate light.", "Water freely in growth, rest in winter.", "Dislikes root disturbance."]},
    "lycaste": {"difficulty": "Intermediate", "temp_c": (14, 26), "humidity_pct": (50, 70), "light_lux": (12000, 20000), "water_days": 5,
        "tips": ["Bright shade, cooler nights.", "Water well in growth, dry rest after leaf drop.", "Deciduous — reduce water when dormant."]},
    "vanilla": {"difficulty": "Advanced", "temp_c": (21, 32), "humidity_pct": (60, 80), "light_lux": (15000, 22000), "water_days": 4,
        "tips": ["A climbing vine orchid — give it support.", "Warm, humid, filtered light.", "Needs space and time to flower."]},
}

DEFAULT_CARE = {"difficulty": "Intermediate", "temp_c": (18, 28), "humidity_pct": (50, 70),
                "light_lux": (12000, 22000), "water_days": 5,
                "tips": ["Bright, indirect light suits most orchids.",
                         "Let roots approach dryness before watering.",
                         "Good air movement helps prevent rot."]}


def care_for(species_name):
    key = species_name.lower().replace("_", " ").strip()
    for genus, profile in CARE_DB.items():
        if genus in key:
            return {"matched_genus": genus, **profile}
    return {"matched_genus": None, **DEFAULT_CARE}


def display_name(species_name):
    return species_name.replace("_", " ").replace("-", " ").title()
