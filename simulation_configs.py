COST = {
    "ROAD": 8,
    "BRIDGE": 35,
    "RAIL": 12,
    "RAIL_BRIDGE": 45,
    "RAIL_CROSSING": 20,
    "RAIL_STATION": 950,
    "SEAPORT": 1600,
    "AIRPORT": 2200,
    "RES": 20,
    "COM": 24,
    "IND": 22,
    "GARBAGE": 14,
    "POWERLINE": 6,
    "WATER": 7,
    "WATER_PUMP": 350,
    "PARK": 60,
    "LARGE_PARK": 320,
    "POLICE": 450,
    "FIRE": 420,
    "CLINIC": 520,
    "SCHOOL": 650,
    "LIBRARY": 380,
    "STADIUM": 1800,
    "COAL": 1400,
    "SOLAR": 900,
    "BULLDOZE": 3,
}

MAINTENANCE = {
    "ROAD": 0.02,
    "BRIDGE": 0.08,
    "RAIL": 0.03,
    "RAIL_BRIDGE": 0.10,
    "RAIL_CROSSING": 0.05,
    "RAIL_STATION": 2.8,
    "SEAPORT": 3.6,
    "AIRPORT": 5.2,
    "POWERLINE": 0.01,
    "WATER": 0.01,
    "WATER_PUMP": 0.8,
    "PARK": 0.18,
    "LARGE_PARK": 0.55,
    "POLICE": 2.4,
    "FIRE": 2.2,
    "CLINIC": 2.8,
    "SCHOOL": 3.2,
    "LIBRARY": 1.4,
    "STADIUM": 4.5,
    "COAL": 5.0,
    "SOLAR": 1.2,
}

CIVIC_JOB_CAPACITY = {
    "GARBAGE": 1,
    "PARK": 2,
    "LARGE_PARK": 6,
    "POLICE": 18,
    "FIRE": 16,
    "CLINIC": 24,
    "SCHOOL": 35,
    "LIBRARY": 12,
    "STADIUM": 30,
    "RAIL_STATION": 10,
    "SEAPORT": 40,
    "AIRPORT": 80,
    "WATER_PUMP": 3,
    "COAL": 20,
    "SOLAR": 6,
}

STUDENT_CAPACITY = {
    "SCHOOL": 120,
}

RESIDENT_CAPACITY_BY_LEVEL = {
    1: 4,
    2: 10,
    3: 24,
    4: 60,
    5: 120,
}

AGES = {
    "working_min": 21,
    "working_max": 64,
    "school_min": 5,
    "school_max": 20,
}

CITIZEN_RESOURCE_USE = {
    "power": 1,
    "water": 1,
    "garbage": 0.01,
}

WORKPLACE_GARBAGE_PER_WORKER = {
    "COM": 0.003,
    "IND": 0.006,
}

GARBAGE = {
    "zone_capacity": 100,
    "fill_decay_rate": 0.01,
}

EDUCATION = {
    "ability_min": 0.75,
    "ability_max": 1.25,
    "monthly_gain": 1.2,
}

HEALTH = {
    "target": 70.0,
}

BUILDING_OUTPUT_CAPACITY = {
    "WATER_PUMP": {"water": 90},
    "COAL": {"power": 450},
    "SOLAR": {"power": 110},
}

TILE_SCORE = {
    "radius": 8,
    "base": {
        "pollution": 0.0,
        "land_value": 45.0,
        "crime": 50.0,
        "health": 40.0,
        "education": 35.0,
        "fire_risk": 40.0,
    },
    "terrain_land_value": 3.0,
    "water_land_value": 16.0,
    "trees_land_value": 4.0,
    "pollution_land_value_penalty": 0.3,
    "pollution_health_penalty": 0.25,
    "pollution_fire_risk_penalty": 0.15,
    "level_crime_penalty_after": 2,
    "level_crime_penalty": 5.0,
    "level_fire_risk": 6.0,
    "road_effect": {
        "land_value": 1.5,
    },
}

TILE_SCORE_EFFECTS = {
    "IND": {
        "pollution": 8.0,
        "pollution_per_level": 10.0,
        "land_value": -5.0,
        "land_value_per_level": -4.0,
    },
    "GARBAGE": {
        "pollution": 12.0,
        "pollution_per_fill": 34.0,
        "land_value": -10.0,
        "land_value_per_fill": -26.0,
        "health": -4.0,
        "health_per_fill": -16.0,
    },
    "COAL": {
        "pollution": 35.0,
        "land_value": -15.0,
    },
    "PARK": {
        "land_value": 12.0,
        "health": 8.0,
    },
    "LARGE_PARK": {
        "land_value": 24.0,
        "health": 16.0,
    },
    "POLICE": {
        "crime": -34.0,
    },
    "FIRE": {
        "fire_risk": -42.0,
    },
    "CLINIC": {
        "health": 45.0,
    },
    "SCHOOL": {
        "education": 42.0,
    },
    "LIBRARY": {
        "education": 24.0,
        "land_value": 5.0,
    },
    "STADIUM": {
        "land_value": 14.0,
        "crime": 3.0,
    },
    "RAIL_STATION": {
        "land_value": 9.0,
        "pollution": -2.0,
    },
    "SEAPORT": {
        "land_value": 8.0,
        "pollution": 4.0,
    },
    "AIRPORT": {
        "land_value": 10.0,
        "pollution": 6.0,
    },
}

ZONE_GROWTH_BONUS = {
    "RES": 0.010,
    "COM": 0.008,
    "IND": 0.012,
}

RESOURCE_SHORTAGE_PENALTY = {
    "power": 25,
    "water": 16,
    "garbage": 10,
}

BUILDING_RESOURCE_USE = {
    "COM": (5, 3, 4),
    "IND": (12, 5, 8),
    "GARBAGE": (1, 1, 0),
    "PARK": (0, 1, 0),
    "LARGE_PARK": (1, 3, 1),
    "POLICE": (8, 4, 2),
    "FIRE": (8, 4, 2),
    "CLINIC": (10, 6, 4),
    "SCHOOL": (10, 8, 5),
    "LIBRARY": (6, 3, 2),
    "STADIUM": (18, 10, 12),
    "RAIL_STATION": (8, 4, 5),
    "SEAPORT": (20, 8, 14),
    "AIRPORT": (30, 14, 20),
    "WATER_PUMP": (3, 0, 1),
}
