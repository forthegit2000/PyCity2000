import json
import math
import random
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import pygame

import avatars
from names import FIRST_NAME_DATA, FIRST_NAME_GENDERS, FIRST_NAMES, FIRST_NAMES_BY_GENDER, LAST_NAMES, gender_for_name
import shapes
import simulation_configs

if __name__ == "__main__":
    sys.modules.setdefault("pycity2000", sys.modules[__name__])


SCREEN_W, SCREEN_H = 1280, 820
FPS = 60
MAP_W, MAP_H = 48, 48
BASE_TILE_W, BASE_TILE_H = 56, 28
SIDEBAR_W = 292
TOPBAR_H = 46
PANEL_BG = (24, 28, 34)
PANEL_2 = (34, 40, 48)
PANEL_3 = (44, 52, 62)
TEXT = (226, 232, 240)
MUTED = (142, 153, 166)
ACCENT = (111, 179, 255)
GOOD = (112, 205, 132)
WARN = (240, 184, 83)
BAD = (235, 93, 93)
GROUND_COLOR = (113, 159, 91)
WATER_COLOR = (45, 107, 142)
TERRAIN_LEVEL_HEIGHT = 8
PLAY_SPEED = 0.5
FAST_SPEED = 1.5
FASTER_SPEED = 2.5
SAVE_PATH = Path("pycity2000_save.json")


class BuildKind(Enum):
    EMPTY = "Empty"
    ROAD = "Road"
    BRIDGE = "Bridge"
    RAIL = "Rail"
    RAIL_BRIDGE = "Rail Bridge"
    RAIL_CROSSING = "Rail Crossing"
    RAIL_STATION = "Railway Station"
    SEAPORT = "Seaport"
    AIRPORT = "Airport"
    POWERLINE = "Power Line"
    WATER = "Water Pipe"
    WATER_PUMP = "Water Pump"
    RES = "Residential Zone"
    COM = "Commercial Zone"
    IND = "Industrial Zone"
    GARBAGE = "Garbage Zone"
    PARK = "Park"
    LARGE_PARK = "Large Park"
    POLICE = "Police"
    FIRE = "Fire Station"
    CLINIC = "Clinic"
    SCHOOL = "School"
    LIBRARY = "Library"
    STADIUM = "Sports Stadium"
    COAL = "Coal Plant"
    SOLAR = "Solar Plant"
    RUBBLE = "Rubble"
    BURNING = "Fire"


class Tool(Enum):
    ROAD = "Road"
    BRIDGE = "Bridge"
    RAIL = "Rail"
    RAIL_BRIDGE = "Rail Bridge"
    RAIL_CROSSING = "Rail Crossing"
    RAIL_STATION = "Railway Station"
    SEAPORT = "Seaport"
    AIRPORT = "Airport"
    RES = "Residential"
    COM = "Commercial"
    IND = "Industrial"
    GARBAGE = "Garbage"
    POWERLINE = "Power Line"
    WATER = "Water Pipe"
    WATER_PUMP = "Water Pump"
    PARK = "Park"
    LARGE_PARK = "Large Park"
    POLICE = "Police"
    FIRE = "Fire Station"
    CLINIC = "Clinic"
    SCHOOL = "School"
    LIBRARY = "Library"
    STADIUM = "Sports Stadium"
    COAL = "Coal Plant"
    SOLAR = "Solar Plant"
    BULLDOZE = "Bulldoze"
    INSPECT = "Inspect"


class MapMode(Enum):
    STANDARD = "Standard Map"
    PIPES = "Water Pipe Map"
    TRAFFIC = "Traffic Map"
    LAND_VALUE = "Land Value Map"
    POLLUTION = "Pollution Map"
    CRIME = "Crime Map"
    FIRE_RISK = "Fire Risk Map"
    HEALTH = "Health Map"


TOOL_KEYS = {
    pygame.K_1: Tool.ROAD,
    pygame.K_2: Tool.RES,
    pygame.K_3: Tool.COM,
    pygame.K_4: Tool.IND,
    pygame.K_5: Tool.POWERLINE,
    pygame.K_6: Tool.WATER,
    pygame.K_7: Tool.PARK,
    pygame.K_8: Tool.POLICE,
    pygame.K_9: Tool.FIRE,
    pygame.K_0: Tool.CLINIC,
    pygame.K_MINUS: Tool.SCHOOL,
    pygame.K_EQUALS: Tool.COAL,
    pygame.K_p: Tool.SOLAR,
    pygame.K_b: Tool.RAIL,
    pygame.K_x: Tool.BULLDOZE,
}


TOOL_BUILD = {
    Tool.ROAD: BuildKind.ROAD,
    Tool.BRIDGE: BuildKind.BRIDGE,
    Tool.RAIL: BuildKind.RAIL,
    Tool.RAIL_BRIDGE: BuildKind.RAIL_BRIDGE,
    Tool.RAIL_CROSSING: BuildKind.RAIL_CROSSING,
    Tool.RAIL_STATION: BuildKind.RAIL_STATION,
    Tool.SEAPORT: BuildKind.SEAPORT,
    Tool.AIRPORT: BuildKind.AIRPORT,
    Tool.RES: BuildKind.RES,
    Tool.COM: BuildKind.COM,
    Tool.IND: BuildKind.IND,
    Tool.GARBAGE: BuildKind.GARBAGE,
    Tool.POWERLINE: BuildKind.POWERLINE,
    Tool.WATER: BuildKind.WATER,
    Tool.WATER_PUMP: BuildKind.WATER_PUMP,
    Tool.PARK: BuildKind.PARK,
    Tool.LARGE_PARK: BuildKind.LARGE_PARK,
    Tool.POLICE: BuildKind.POLICE,
    Tool.FIRE: BuildKind.FIRE,
    Tool.CLINIC: BuildKind.CLINIC,
    Tool.SCHOOL: BuildKind.SCHOOL,
    Tool.LIBRARY: BuildKind.LIBRARY,
    Tool.STADIUM: BuildKind.STADIUM,
    Tool.COAL: BuildKind.COAL,
    Tool.SOLAR: BuildKind.SOLAR,
}


def tool_keyed(values):
    return {Tool[key]: value for key, value in values.items()}


def build_kind_keyed(values):
    return {BuildKind[key]: value for key, value in values.items()}


COST = tool_keyed(simulation_configs.COST)
MAINTENANCE = build_kind_keyed(simulation_configs.MAINTENANCE)


ZONE_KINDS = {BuildKind.RES, BuildKind.COM, BuildKind.IND, BuildKind.GARBAGE}
ROAD_KINDS = {BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL_CROSSING}
RAIL_KINDS = {BuildKind.RAIL, BuildKind.RAIL_BRIDGE, BuildKind.RAIL_CROSSING}
RAIL_CONNECT_KINDS = RAIL_KINDS | {BuildKind.RAIL_STATION}
NETWORK_KINDS = {BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL_CROSSING, BuildKind.POWERLINE, BuildKind.WATER}
REGISTRY_EXCLUDED_KINDS = {
    BuildKind.EMPTY,
    BuildKind.ROAD,
    BuildKind.BRIDGE,
    BuildKind.RAIL,
    BuildKind.RAIL_BRIDGE,
    BuildKind.RAIL_CROSSING,
    BuildKind.POWERLINE,
    BuildKind.WATER,
}
PATH_TOOLS = {Tool.ROAD, Tool.RAIL, Tool.POWERLINE, Tool.WATER}
ZONE_TOOLS = {Tool.RES, Tool.COM, Tool.IND, Tool.GARBAGE}
SERVICE_KINDS = {
    BuildKind.PARK,
    BuildKind.LARGE_PARK,
    BuildKind.POLICE,
    BuildKind.FIRE,
    BuildKind.CLINIC,
    BuildKind.SCHOOL,
    BuildKind.LIBRARY,
    BuildKind.STADIUM,
    BuildKind.RAIL_STATION,
    BuildKind.SEAPORT,
    BuildKind.AIRPORT,
    BuildKind.WATER_PUMP,
    BuildKind.COAL,
    BuildKind.SOLAR,
}
INSPECTOR_AVATAR_KINDS = {
    BuildKind.PARK,
    BuildKind.LARGE_PARK,
    BuildKind.SCHOOL,
    BuildKind.CLINIC,
    BuildKind.POLICE,
    BuildKind.FIRE,
    BuildKind.LIBRARY,
    BuildKind.STADIUM,
    BuildKind.RAIL_STATION,
    BuildKind.SEAPORT,
    BuildKind.AIRPORT,
    BuildKind.WATER_PUMP,
    BuildKind.COAL,
    BuildKind.SOLAR,
}

CIVIC_JOB_CAPACITY = build_kind_keyed(simulation_configs.CIVIC_JOB_CAPACITY)
STUDENT_CAPACITY = build_kind_keyed(simulation_configs.STUDENT_CAPACITY)
RESIDENT_CAPACITY_BY_LEVEL = dict(simulation_configs.RESIDENT_CAPACITY_BY_LEVEL)
WORKING_AGE_MIN = simulation_configs.AGES["working_min"]
WORKING_AGE_MAX = simulation_configs.AGES["working_max"]
SCHOOL_AGE_MIN = simulation_configs.AGES["school_min"]
SCHOOL_AGE_MAX = simulation_configs.AGES["school_max"]
CITIZEN_POWER_USE = simulation_configs.CITIZEN_RESOURCE_USE["power"]
CITIZEN_WATER_USE = simulation_configs.CITIZEN_RESOURCE_USE["water"]
CITIZEN_GARBAGE_USE = simulation_configs.CITIZEN_RESOURCE_USE["garbage"]
WORKPLACE_GARBAGE_PER_WORKER = build_kind_keyed(simulation_configs.WORKPLACE_GARBAGE_PER_WORKER)
GARBAGE_ZONE_CAPACITY = simulation_configs.GARBAGE["zone_capacity"]
GARBAGE_FILL_DECAY_RATE = simulation_configs.GARBAGE["fill_decay_rate"]
EDUCATION_ABILITY_MIN = simulation_configs.EDUCATION["ability_min"]
EDUCATION_ABILITY_MAX = simulation_configs.EDUCATION["ability_max"]
MONTHLY_EDUCATION_GAIN = simulation_configs.EDUCATION["monthly_gain"]
HEALTH_TARGET = simulation_configs.HEALTH["target"]
BUILDING_OUTPUT_CAPACITY = build_kind_keyed(simulation_configs.BUILDING_OUTPUT_CAPACITY)
TILE_SCORE = dict(simulation_configs.TILE_SCORE)
TILE_SCORE_EFFECTS = build_kind_keyed(simulation_configs.TILE_SCORE_EFFECTS)
TILE_SCORE_FIELDS = ("pollution", "land_value", "crime", "health", "education", "fire_risk")
ZONE_GROWTH_BONUS = build_kind_keyed(simulation_configs.ZONE_GROWTH_BONUS)
RESOURCE_SHORTAGE_PENALTY = dict(simulation_configs.RESOURCE_SHORTAGE_PENALTY)
BUILDING_RESOURCE_USE = build_kind_keyed(simulation_configs.BUILDING_RESOURCE_USE)

FOOTPRINTS = {
    BuildKind.EMPTY: (1, 1),
    BuildKind.ROAD: (1, 1),
    BuildKind.BRIDGE: (1, 1),
    BuildKind.RAIL: (1, 1),
    BuildKind.RAIL_BRIDGE: (1, 1),
    BuildKind.RAIL_CROSSING: (1, 1),
    BuildKind.RAIL_STATION: (6, 3),
    BuildKind.SEAPORT: (4, 3),
    BuildKind.AIRPORT: (6, 4),
    BuildKind.POWERLINE: (1, 1),
    BuildKind.WATER: (1, 1),
    BuildKind.WATER_PUMP: (1, 1),
    BuildKind.RES: (1, 1),
    BuildKind.COM: (1, 1),
    BuildKind.IND: (1, 1),
    BuildKind.GARBAGE: (1, 1),
    BuildKind.PARK: (1, 1),
    BuildKind.LARGE_PARK: (3, 3),
    BuildKind.POLICE: (2, 2),
    BuildKind.FIRE: (2, 2),
    BuildKind.CLINIC: (2, 2),
    BuildKind.SCHOOL: (2, 2),
    BuildKind.LIBRARY: (2, 2),
    BuildKind.STADIUM: (4, 4),
    BuildKind.COAL: (3, 3),
    BuildKind.SOLAR: (2, 2),
    BuildKind.RUBBLE: (1, 1),
    BuildKind.BURNING: (1, 1),
}


@dataclass
class Tile:
    terrain: int = 0
    water: bool = False
    trees: bool = False
    pipe: bool = False
    build: BuildKind = BuildKind.EMPTY
    level: int = 0
    powered: bool = False
    watered: bool = False
    road_access: bool = False
    pollution: float = 0.0
    land_value: float = 0.0
    fire_risk: float = 0.0
    crime: float = 0.0
    health: float = 0.0
    education: float = 0.0
    garbage_fill: float = 0.0
    fire_timer: int = 0
    origin: tuple[int, int] | None = None
    footprint: tuple[int, int] = (1, 1)

    def is_buildable(self) -> bool:
        return not self.water and self.build not in {BuildKind.BURNING}

    def is_origin(self, x, y) -> bool:
        return self.origin in {None, (x, y)}


@dataclass
class Message:
    text: str
    color: tuple[int, int, int] = TEXT
    ttl: float = 8.0


@dataclass
class Citizen:
    id: int
    name: str = ""
    gender: str = "m"
    born: tuple[int, int, int] = (1, 1, 1900)
    household_id: int | None = None
    job_id: int | None = None
    school_id: int | None = None
    health: float = 70.0
    education: float = 0.0
    education_ability: float = 1.0
    happiness: float = 50.0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "born": self.born,
            "household_id": self.household_id,
            "job_id": self.job_id,
            "school_id": self.school_id,
            "health": self.health,
            "education": self.education,
            "education_ability": self.education_ability,
            "happiness": self.happiness,
        }

    @classmethod
    def from_dict(cls, data):
        citizen_id = data["id"]
        name = data.get("name") or f"Citizen {citizen_id}"
        return cls(
            id=citizen_id,
            name=name,
            gender=data.get("gender") or gender_for_name(name),
            born=tuple(data["born"]),
            household_id=data.get("household_id"),
            job_id=data.get("job_id"),
            school_id=data.get("school_id"),
            health=data.get("health", 70.0),
            education=data.get("education", 0.0),
            education_ability=data.get("education_ability", 1.0),
            happiness=data.get("happiness", 50.0),
        )


@dataclass
class Household:
    id: int
    home_building_id: int | None = None
    citizen_ids: list[int] = field(default_factory=list)
    income: float = 0.0

    def to_dict(self):
        return {
            "id": self.id,
            "home_building_id": self.home_building_id,
            "citizen_ids": self.citizen_ids,
            "income": self.income,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            home_building_id=data.get("home_building_id"),
            citizen_ids=list(data.get("citizen_ids", [])),
            income=data.get("income", 0.0),
        )


@dataclass
class BuildingInstance:
    id: int
    kind: BuildKind
    origin: tuple[int, int]
    footprint: tuple[int, int] = (1, 1)
    level: int = 0
    resident_capacity: int = 0
    job_capacity: int = 0
    student_capacity: int = 0
    resident_ids: list[int] = field(default_factory=list)
    worker_ids: list[int] = field(default_factory=list)
    student_ids: list[int] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "kind": self.kind.name,
            "origin": self.origin,
            "footprint": self.footprint,
            "level": self.level,
            "resident_capacity": self.resident_capacity,
            "job_capacity": self.job_capacity,
            "student_capacity": self.student_capacity,
            "resident_ids": self.resident_ids,
            "worker_ids": self.worker_ids,
            "student_ids": self.student_ids,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            kind=BuildKind[data["kind"]],
            origin=tuple(data["origin"]),
            footprint=tuple(data.get("footprint", (1, 1))),
            level=data.get("level", 0),
            resident_capacity=data.get("resident_capacity", 0),
            job_capacity=data.get("job_capacity", 0),
            student_capacity=data.get("student_capacity", 0),
            resident_ids=list(data.get("resident_ids", [])),
            worker_ids=list(data.get("worker_ids", [])),
            student_ids=list(data.get("student_ids", [])),
        )


@dataclass
class Trip:
    citizen_id: int
    from_building_id: int
    to_building_id: int
    purpose: str
    distance: int

    def to_dict(self):
        return {
            "citizen_id": self.citizen_id,
            "from_building_id": self.from_building_id,
            "to_building_id": self.to_building_id,
            "purpose": self.purpose,
            "distance": self.distance,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            citizen_id=data["citizen_id"],
            from_building_id=data["from_building_id"],
            to_building_id=data["to_building_id"],
            purpose=data["purpose"],
            distance=data["distance"],
        )


@dataclass
class CityStats:
    population: int = 0
    jobs: int = 0
    shops: int = 0
    demand_r: float = 0.0
    demand_c: float = 0.0
    demand_i: float = 0.0
    power_used: int = 0
    power_cap: int = 0
    water_used: int = 0
    water_cap: int = 0
    garbage_used: float = 0.0
    garbage_cap: float = 0.0
    income: float = 0.0
    expenses: float = 0.0
    mood: float = 50.0
    pollution: float = 0.0
    unemployment: float = 0.0
    traffic: float = 0.0


@dataclass
class City:
    width: int = MAP_W
    height: int = MAP_H
    tiles: list[list[Tile]] = field(default_factory=list)
    money: int = 20000
    day: int = 1
    month: int = 1
    year: int = 1900
    tax_rate: float = 8.0
    sim_speed: float = PLAY_SPEED
    paused: bool = False
    disasters_enabled: bool = True
    tick_accum: float = 0.0
    stats: CityStats = field(default_factory=CityStats)
    selected: tuple[int, int] | None = None
    messages: list[Message] = field(default_factory=list)
    citizens: dict[int, Citizen] = field(default_factory=dict)
    households: dict[int, Household] = field(default_factory=dict)
    buildings: dict[int, BuildingInstance] = field(default_factory=dict)
    trips: list[Trip] = field(default_factory=list)
    traffic_loads: dict[tuple[int, int], float] = field(default_factory=dict)
    next_sim_id: int = 1
    graphs: dict[str, list[float]] = field(default_factory=lambda: {
        "population": [],
        "money": [],
        "mood": [],
        "pollution": [],
    })

    def __post_init__(self):
        self.generate()

    def generate(self):
        rng = random.Random()
        self.tiles = [[Tile() for _ in range(self.height)] for _ in range(self.width)]
        cx = rng.randint(12, self.width - 13)
        cy = rng.randint(12, self.height - 13)
        river_width = rng.uniform(2.4, 4.2)
        river_phase = rng.random() * 10
        for x in range(self.width):
            for y in range(self.height):
                hill = (
                    math.sin(x * 0.23 + river_phase) * 0.7
                    + math.cos(y * 0.21) * 0.6
                    + math.sin((x + y) * 0.13) * 0.5
                )
                t = self.tiles[x][y]
                t.terrain = max(0, min(3, int(hill + 1.6)))
                river_y = cy + math.sin((x + river_phase) * 0.22) * 6
                lake = math.hypot(x - cx, y - cy) < 5.5
                t.water = abs(y - river_y) < river_width or lake
                t.trees = not t.water and rng.random() < 0.12 + 0.03 * t.terrain
        self.money = 20000
        self.day, self.month, self.year = 1, 1, 1900
        self.tax_rate = 8.0
        self.paused = False
        self.disasters_enabled = True
        self.sim_speed = PLAY_SPEED
        self.stats = CityStats()
        self.citizens = {}
        self.households = {}
        self.buildings = {}
        self.trips = []
        self.traffic_loads = {}
        self.next_sim_id = 1
        self.messages = [Message("New charter approved. Build roads, zones, power, and water.", ACCENT, 9)]
        self.graphs = {"population": [], "money": [], "mood": [], "pollution": []}

    def allocate_sim_id(self):
        sim_id = self.next_sim_id
        self.next_sim_id += 1
        return sim_id

    def building_resident_capacity(self, kind, level):
        if kind == BuildKind.RES:
            return RESIDENT_CAPACITY_BY_LEVEL.get(level, RESIDENT_CAPACITY_BY_LEVEL[max(RESIDENT_CAPACITY_BY_LEVEL)])
        return 0

    def building_job_capacity(self, kind, level):
        if kind == BuildKind.COM:
            return level * level * 5
        if kind == BuildKind.IND:
            return level * level * 14
        return CIVIC_JOB_CAPACITY.get(kind, 0)

    def building_student_capacity(self, kind, level):
        return STUDENT_CAPACITY.get(kind, 0)

    def citizen_age(self, citizen):
        birth_month, birth_day, birth_year = citizen.born
        age = self.year - birth_year
        if (self.month, self.day) < (birth_month, birth_day):
            age -= 1
        return max(0, age)

    def is_working_age(self, citizen):
        return WORKING_AGE_MIN <= self.citizen_age(citizen) <= WORKING_AGE_MAX

    def is_school_age(self, citizen):
        return SCHOOL_AGE_MIN <= self.citizen_age(citizen) <= SCHOOL_AGE_MAX

    def rebuild_building_registry(self):
        existing_by_origin = {
            building.origin: building
            for building in self.buildings.values()
        }
        rebuilt = {}
        for x, y, tile in self.footprint_origin_tiles():
            if tile.build in REGISTRY_EXCLUDED_KINDS:
                continue
            previous = existing_by_origin.get((x, y))
            if previous and previous.kind == tile.build:
                building = previous
                building.footprint = tile.footprint
                building.level = tile.level
            else:
                building = BuildingInstance(
                    id=self.allocate_sim_id(),
                    kind=tile.build,
                    origin=(x, y),
                    footprint=tile.footprint,
                    level=tile.level,
                )
            building.resident_capacity = self.building_resident_capacity(tile.build, tile.level)
            building.job_capacity = self.building_job_capacity(tile.build, tile.level)
            building.student_capacity = self.building_student_capacity(tile.build, tile.level)
            building.resident_ids = building.resident_ids[: building.resident_capacity]
            building.worker_ids = building.worker_ids[: building.job_capacity]
            building.student_ids = building.student_ids[: building.student_capacity]
            rebuilt[building.id] = building
        self.buildings = rebuilt
        self.sync_residential_population()
        self.sync_work_and_school_assignments()

    def household_seed(self, home_building_id, household_index=0):
        return home_building_id * 1009 + household_index * 9176 + self.year * 37

    def household_last_name(self, home_building_id, household_index=0):
        seed = self.household_seed(home_building_id, household_index)
        return LAST_NAMES[self.deterministic_int(seed, 81, 0, len(LAST_NAMES) - 1)]

    def deterministic_value(self, seed, salt):
        value = (seed ^ (salt * 0x9E3779B1)) & 0xFFFFFFFF
        value ^= value >> 16
        value = (value * 0x7FEB352D) & 0xFFFFFFFF
        value ^= value >> 15
        value = (value * 0x846CA68B) & 0xFFFFFFFF
        value ^= value >> 16
        return value

    def deterministic_ratio(self, seed, salt):
        return self.deterministic_value(seed, salt) / 0x100000000

    def deterministic_int(self, seed, salt, lo, hi):
        return lo + self.deterministic_value(seed, salt) % (hi - lo + 1)

    def generated_household_members(self, home_building_id, max_size, household_index=0):
        seed = self.household_seed(home_building_id, household_index)
        members = []
        if self.deterministic_ratio(seed, 1) < 0.72 and max_size >= 2:
            adult_a_age = self.deterministic_int(seed, 2, 24, 48)
            adult_b_age = clamp(adult_a_age + self.deterministic_int(seed, 3, -4, 5), 22, 52)
            members.extend((("m", adult_a_age), ("f", adult_b_age)))
            remaining = max_size - len(members)
            if remaining > 0:
                child_roll = self.deterministic_ratio(seed, 4)
                child_count = 0
                if child_roll < 0.42:
                    child_count = 1
                elif child_roll < 0.70:
                    child_count = 2
                elif child_roll < 0.78:
                    child_count = 3
                for i in range(min(remaining, child_count)):
                    gender = "m" if self.deterministic_ratio(seed, 10 + i) < 0.5 else "f"
                    age = self.deterministic_int(seed, 20 + i, 1, 17)
                    members.append((gender, age))
        else:
            gender = "m" if self.deterministic_ratio(seed, 5) < 0.5 else "f"
            age = self.deterministic_int(seed, 6, 21, 74)
            members.append((gender, age))
        return members[:max_size]

    def residential_population_target(self, building):
        if building.level <= 1:
            return len(self.generated_household_members(building.id, building.resident_capacity))
        return building.resident_capacity

    def create_household(self, home_building_id, max_size, household_index=0):
        household_id = self.allocate_sim_id()
        citizen_ids = []
        last_name = self.household_last_name(home_building_id, household_index)
        for gender, age in self.generated_household_members(home_building_id, max_size, household_index):
            citizen_id = self.allocate_sim_id()
            self.citizens[citizen_id] = Citizen(
                id=citizen_id,
                name=self.citizen_name(citizen_id, gender, last_name),
                gender=gender,
                born=self.citizen_birth_date(age),
                education_ability=self.citizen_education_ability(citizen_id),
                household_id=household_id,
            )
            citizen_ids.append(citizen_id)
        self.households[household_id] = Household(
            id=household_id,
            home_building_id=home_building_id,
            citizen_ids=citizen_ids,
        )
        return household_id

    def remove_household(self, household_id):
        household = self.households.pop(household_id, None)
        if not household:
            return
        for citizen_id in household.citizen_ids:
            self.citizens.pop(citizen_id, None)

    def remove_citizen_from_household(self, citizen_id):
        citizen = self.citizens.pop(citizen_id, None)
        if not citizen or citizen.household_id not in self.households:
            return
        household = self.households[citizen.household_id]
        household.citizen_ids = [cid for cid in household.citizen_ids if cid != citizen_id]
        if not household.citizen_ids:
            self.households.pop(household.id, None)

    def sync_residential_population(self):
        building_ids = set(self.buildings)
        valid_residents = set()
        for building in self.buildings.values():
            if building.kind != BuildKind.RES:
                continue
            target = self.residential_population_target(building)
            building.resident_ids = [
                cid
                for cid in building.resident_ids
                if cid in self.citizens and self.citizens[cid].household_id in self.households
            ][:target]
            valid_residents.update(building.resident_ids)

        for household_id, household in list(self.households.items()):
            if household.home_building_id not in building_ids:
                self.remove_household(household_id)
                continue
            household.citizen_ids = [cid for cid in household.citizen_ids if cid in self.citizens]
            if not household.citizen_ids:
                self.households.pop(household_id, None)

        for citizen_id in list(self.citizens):
            citizen = self.citizens[citizen_id]
            if citizen.household_id not in self.households or citizen_id not in valid_residents:
                self.remove_citizen_from_household(citizen_id)

        for building in self.buildings.values():
            if building.kind != BuildKind.RES:
                continue
            target = self.residential_population_target(building)
            household_index = len({
                self.citizens[cid].household_id
                for cid in building.resident_ids
                if cid in self.citizens
            })
            while len(building.resident_ids) < target:
                open_slots = target - len(building.resident_ids)
                household_id = self.create_household(building.id, min(4, open_slots), household_index)
                resident_ids = self.households[household_id].citizen_ids
                building.resident_ids.extend(resident_ids)
                household_index += 1

    def sorted_buildings_with_capacity(self, attr):
        return sorted(
            (building for building in self.buildings.values() if getattr(building, attr) > 0),
            key=lambda building: (building.origin[0], building.origin[1], building.id),
        )

    def commercial_shop_output(self, building):
        if not building or building.kind != BuildKind.COM:
            return 0.0
        return building.level * building.level * 8 * self.zone_fill_ratio(building, "worker_ids", "job_capacity")

    def commercial_shop_gap(self):
        needed = len(self.citizens) * 0.18
        shops = sum(self.commercial_shop_output(building) for building in self.buildings.values())
        return max(0.0, (needed - shops) / max(1.0, needed))

    def industrial_job_gap(self):
        working_age = len(self.working_age_citizens())
        needed = working_age * 0.55
        capacity = sum(building.job_capacity for building in self.buildings.values() if building.kind == BuildKind.IND)
        return max(0.0, (needed - capacity) / max(1.0, needed))

    def worker_assignment_priority(self, building):
        if building.kind == BuildKind.COM:
            return 45 + self.commercial_shop_gap() * 160 + self.commercial_customer_support() * 25
        if building.kind == BuildKind.IND:
            return 45 + self.industrial_job_gap() * 120 + self.industrial_labor_support() * 25
        return 50

    def worker_assignment_buildings(self, buildings):
        sector_rank = {BuildKind.COM: 0, BuildKind.IND: 1}
        return sorted(
            buildings,
            key=lambda building: (
                -self.worker_assignment_priority(building),
                sector_rank.get(building.kind, 2),
                building.origin[0],
                building.origin[1],
                building.id,
            ),
        )

    def sync_work_assignments(self):
        job_buildings = self.worker_assignment_buildings(self.sorted_buildings_with_capacity("job_capacity"))

        for building in job_buildings:
            building.worker_ids = []

        for citizen in self.citizens.values():
            citizen.job_id = None

        for citizen_id in sorted(self.citizens):
            citizen = self.citizens[citizen_id]
            if not self.is_working_age(citizen) or citizen.job_id is not None:
                continue
            for building in job_buildings:
                if len(building.worker_ids) < building.job_capacity:
                    building.worker_ids.append(citizen_id)
                    citizen.job_id = building.id
                    break

    def sync_school_assignments(self):
        school_buildings = self.sorted_buildings_with_capacity("student_capacity")
        valid_school_ids = {building.id for building in school_buildings}
        assigned = set()

        for building in school_buildings:
            kept = []
            for citizen_id in building.student_ids:
                citizen = self.citizens.get(citizen_id)
                if not citizen or not self.is_school_age(citizen) or citizen.school_id != building.id or citizen_id in assigned:
                    continue
                kept.append(citizen_id)
                assigned.add(citizen_id)
                if len(kept) >= building.student_capacity:
                    break
            building.student_ids = kept

        for citizen in self.citizens.values():
            if not self.is_school_age(citizen) or citizen.school_id not in valid_school_ids or citizen.id not in assigned:
                citizen.school_id = None

        for citizen_id in sorted(self.citizens):
            citizen = self.citizens[citizen_id]
            if not self.is_school_age(citizen) or citizen.school_id is not None:
                continue
            for building in school_buildings:
                if len(building.student_ids) < building.student_capacity:
                    building.student_ids.append(citizen_id)
                    citizen.school_id = building.id
                    assigned.add(citizen_id)
                    break

    def sync_work_and_school_assignments(self):
        self.sync_work_assignments()
        self.sync_school_assignments()
        self.recompute_trips()

    def working_age_citizens(self):
        return [citizen for citizen in self.citizens.values() if self.is_working_age(citizen)]

    def school_age_citizens(self):
        return [citizen for citizen in self.citizens.values() if self.is_school_age(citizen)]

    def building_at_origin(self, origin):
        for building in self.buildings.values():
            if building.origin == origin:
                return building
        return None

    def citizen_name(self, citizen_id, gender=None, last_name=None):
        first_names = FIRST_NAMES_BY_GENDER.get(gender, FIRST_NAMES)
        first = first_names[citizen_id % len(first_names)]
        last = last_name or LAST_NAMES[(citizen_id // len(FIRST_NAMES)) % len(LAST_NAMES)]
        return f"{first} {last}"

    def citizen_gender(self, citizen_id):
        first = FIRST_NAMES[citizen_id % len(FIRST_NAMES)]
        return FIRST_NAME_GENDERS[first]

    def citizen_birth_date(self, age):
        return self.month, self.day, max(1, self.year - age)

    def citizen_education_ability(self, citizen_id):
        steps = 20
        ratio = ((citizen_id * 37) % (steps + 1)) / steps
        return round(EDUCATION_ABILITY_MIN + (EDUCATION_ABILITY_MAX - EDUCATION_ABILITY_MIN) * ratio, 2)

    def format_date(self, date):
        month, day, year = date
        return f"{month:02d}/{day:02d}/{year}"

    def building_resource_use(self, building):
        base_power, base_water, base_garbage = BUILDING_RESOURCE_USE.get(building.kind, (0, 0, 0))
        if building.kind == BuildKind.COM:
            workers = sum(1 for citizen_id in building.worker_ids if citizen_id in self.citizens)
            return (
                building.job_capacity,
                max(1, math.ceil(building.job_capacity * 0.6)),
                workers * WORKPLACE_GARBAGE_PER_WORKER[BuildKind.COM],
            )
        if building.kind == BuildKind.IND:
            workers = sum(1 for citizen_id in building.worker_ids if citizen_id in self.citizens)
            return (
                building.job_capacity * 2,
                math.ceil(building.job_capacity * 0.7),
                workers * WORKPLACE_GARBAGE_PER_WORKER[BuildKind.IND],
            )
        return base_power, base_water, base_garbage

    def resource_usage(self):
        power_used = len(self.citizens) * CITIZEN_POWER_USE
        water_used = len(self.citizens) * CITIZEN_WATER_USE
        garbage_used = len(self.citizens) * CITIZEN_GARBAGE_USE
        garbage_cap = 0
        for building in self.buildings.values():
            power, water, garbage = self.building_resource_use(building)
            power_used += power
            water_used += water
            garbage_used += garbage
            if building.kind == BuildKind.GARBAGE:
                tile = self.tiles[building.origin[0]][building.origin[1]]
                garbage_cap += max(0.0, GARBAGE_ZONE_CAPACITY - tile.garbage_fill)
        return power_used, water_used, garbage_used, garbage_cap

    def citizen_home_building_id(self, citizen):
        household = self.households.get(citizen.household_id)
        return household.home_building_id if household else None

    def building_distance(self, from_building_id, to_building_id):
        start = self.buildings[from_building_id].origin
        end = self.buildings[to_building_id].origin
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def building_road_access_tiles(self, building_id, radius=1):
        building = self.buildings.get(building_id)
        if not building:
            return []
        roads = set()
        for tx, ty in self.building_tiles(*building.origin):
            for nx, ny, _ in self.neighbors_radius(tx, ty, radius):
                if self.tiles[nx][ny].build in ROAD_KINDS:
                    roads.add((nx, ny))
        return sorted(roads)

    def road_path_between_buildings(self, from_building_id, to_building_id):
        starts = self.building_road_access_tiles(from_building_id)
        goals = set(self.building_road_access_tiles(to_building_id))
        if not starts or not goals:
            return []
        queue = list(starts)
        parents = {start: None for start in starts}
        idx = 0
        while idx < len(queue):
            current = queue[idx]
            idx += 1
            if current in goals:
                path = []
                while current is not None:
                    path.append(current)
                    current = parents[current]
                return list(reversed(path))
            x, y = current
            for nx, ny in self.neighbors4(x, y):
                if (nx, ny) in parents or self.tiles[nx][ny].build not in ROAD_KINDS:
                    continue
                parents[(nx, ny)] = current
                queue.append((nx, ny))
        return []

    def trip_distance_and_route(self, from_building_id, to_building_id):
        route = self.road_path_between_buildings(from_building_id, to_building_id)
        if route:
            return len(route), route
        return max(1, self.building_distance(from_building_id, to_building_id) * 3), []

    def add_trip_traffic(self, route):
        for x, y in route:
            self.traffic_loads[(x, y)] = self.traffic_loads.get((x, y), 0.0) + 1.0

    def recompute_trips(self):
        trips = []
        self.traffic_loads = {}
        for citizen_id in sorted(self.citizens):
            citizen = self.citizens[citizen_id]
            home_id = self.citizen_home_building_id(citizen)
            if home_id not in self.buildings:
                continue
            for purpose, destination_id in (("work", citizen.job_id), ("school", citizen.school_id)):
                if destination_id not in self.buildings:
                    continue
                distance, route = self.trip_distance_and_route(home_id, destination_id)
                trip = Trip(
                    citizen_id=citizen_id,
                    from_building_id=home_id,
                    to_building_id=destination_id,
                    purpose=purpose,
                    distance=distance,
                )
                trips.append(trip)
                self.add_trip_traffic(route)
        self.trips = trips

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "money": self.money,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "tax_rate": self.tax_rate,
            "sim_speed": self.sim_speed,
            "paused": self.paused,
            "disasters_enabled": self.disasters_enabled,
            "tick_accum": self.tick_accum,
            "selected": self.selected,
            "citizens": [self.citizens[cid].to_dict() for cid in sorted(self.citizens)],
            "households": [self.households[hid].to_dict() for hid in sorted(self.households)],
            "buildings": [self.buildings[bid].to_dict() for bid in sorted(self.buildings)],
            "trips": [trip.to_dict() for trip in self.trips],
            "next_sim_id": self.next_sim_id,
            "graphs": self.graphs,
            "tiles": [[self.tile_to_dict(self.tiles[x][y]) for y in range(self.height)] for x in range(self.width)],
        }

    def tile_to_dict(self, tile):
        return {
            "terrain": tile.terrain,
            "water": tile.water,
            "trees": tile.trees,
            "pipe": tile.pipe,
            "build": tile.build.name,
            "level": tile.level,
            "garbage_fill": tile.garbage_fill,
            "fire_timer": tile.fire_timer,
            "origin": tile.origin,
            "footprint": tile.footprint,
        }

    @classmethod
    def from_dict(cls, data):
        city = cls(data["width"], data["height"])
        city.money = data["money"]
        city.day = data["day"]
        city.month = data["month"]
        city.year = data["year"]
        city.tax_rate = data["tax_rate"]
        city.sim_speed = data["sim_speed"]
        city.paused = data["paused"]
        city.disasters_enabled = data.get("disasters_enabled", True)
        city.tick_accum = data.get("tick_accum", 0.0)
        city.selected = tuple(data["selected"]) if data.get("selected") else None
        city.graphs = data.get("graphs", {"population": [], "money": [], "mood": [], "pollution": []})
        city.citizens = {citizen.id: citizen for citizen in (Citizen.from_dict(item) for item in data.get("citizens", []))}
        city.households = {household.id: household for household in (Household.from_dict(item) for item in data.get("households", []))}
        city.buildings = {building.id: building for building in (BuildingInstance.from_dict(item) for item in data.get("buildings", []))}
        city.trips = [Trip.from_dict(item) for item in data.get("trips", [])]
        city.traffic_loads = {}
        highest_id = max([0, *city.citizens, *city.households, *city.buildings])
        city.next_sim_id = max(data.get("next_sim_id", 1), highest_id + 1)
        city.tiles = [[cls.tile_from_dict(data["tiles"][x][y]) for y in range(city.height)] for x in range(city.width)]
        city.messages = []
        city.rebuild_building_registry()
        city.recompute_networks()
        city.recompute_tile_scores()
        city.recompute_stats()
        return city

    @staticmethod
    def tile_from_dict(data):
        return Tile(
            terrain=data["terrain"],
            water=data["water"],
            trees=data["trees"],
            pipe=data.get("pipe", False),
            build=BuildKind[data["build"]],
            level=data["level"],
            garbage_fill=data.get("garbage_fill", 0.0),
            fire_timer=data.get("fire_timer", 0),
            origin=tuple(data["origin"]) if data.get("origin") else None,
            footprint=tuple(data.get("footprint", (1, 1))),
        )

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors4(self, x, y):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield nx, ny

    def neighbors_radius(self, x, y, radius):
        r = int(radius)
        for nx in range(max(0, x - r), min(self.width, x + r + 1)):
            for ny in range(max(0, y - r), min(self.height, y + r + 1)):
                d = abs(nx - x) + abs(ny - y)
                if d <= radius:
                    yield nx, ny, d

    def footprint_tiles(self, kind, x, y):
        fw, fh = FOOTPRINTS[kind]
        for ox in range(fw):
            for oy in range(fh):
                yield x + ox, y + oy

    def building_origin(self, x, y):
        tile = self.tiles[x][y]
        return tile.origin or (x, y)

    def building_tiles(self, x, y):
        ox, oy = self.building_origin(x, y)
        footprint = self.tiles[ox][oy].footprint if self.in_bounds(ox, oy) else self.tiles[x][y].footprint
        seen = set()
        for tx in range(ox, ox + footprint[0]):
            for ty in range(oy, oy + footprint[1]):
                if self.in_bounds(tx, ty) and self.tiles[tx][ty].origin == (ox, oy):
                    seen.add((tx, ty))
                    yield tx, ty
        if not seen:
            yield x, y

    def footprint_origin_tiles(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                if tile.build != BuildKind.EMPTY and tile.origin in {None, (x, y)}:
                    yield x, y, tile

    def footprint_has_adjacent(self, x, y, kind):
        for tx, ty in self.building_tiles(x, y):
            for nx, ny in self.neighbors4(tx, ty):
                if self.tiles[nx][ny].build == kind:
                    return True
        return False

    def rail_station_track_tile(self, x, y, tx, ty):
        return y <= ty < y + FOOTPRINTS[BuildKind.RAIL_STATION][1] and ty == y + 1

    def is_rail_station_track(self, x, y):
        tile = self.tiles[x][y]
        return tile.build == BuildKind.RAIL_STATION and tile.origin is not None and y == tile.origin[1] + 1

    def footprint_touches_water(self, kind, x, y):
        tiles = set(self.footprint_tiles(kind, x, y))
        for tx, ty in tiles:
            for nx, ny in self.neighbors4(tx, ty):
                if (nx, ny) not in tiles and self.tiles[nx][ny].water:
                    return True
        return False

    def footprint_is_flat(self, kind, x, y):
        levels = {self.tiles[tx][ty].terrain for tx, ty in self.footprint_tiles(kind, x, y)}
        return len(levels) == 1

    def pump_has_water_neighbor(self, x, y):
        return any(self.tiles[nx][ny].water for nx, ny in self.neighbors4(x, y))

    def water_pump_capacity(self, x, y):
        if not self.pump_has_water_neighbor(x, y):
            return 0
        return BUILDING_OUTPUT_CAPACITY[BuildKind.WATER_PUMP]["water"]

    def power_source_capacity(self, kind):
        return BUILDING_OUTPUT_CAPACITY.get(kind, {}).get("power", 0)

    def building_boundary(self, x, y):
        tiles = set(self.building_tiles(x, y))
        for tx, ty in tiles:
            for nx, ny in self.neighbors4(tx, ty):
                if (nx, ny) not in tiles:
                    yield nx, ny

    def can_build(self, tool, x, y):
        if not self.in_bounds(x, y):
            return False, "Outside map"
        tile = self.tiles[x][y]
        if tool == Tool.BULLDOZE:
            if tile.build == BuildKind.GARBAGE:
                return False, "Garbage zones cannot be bulldozed"
            return tile.build != BuildKind.EMPTY or tile.trees or tile.pipe, "Nothing to clear"
        kind = TOOL_BUILD[tool]
        if tool in {Tool.BRIDGE, Tool.RAIL_BRIDGE}:
            if not tile.water:
                return False, f"{TOOL_BUILD[tool].value}s must be built on water"
            if tile.build != BuildKind.EMPTY:
                return False, "Occupied"
            anchor_kinds = ROAD_KINDS if tool == Tool.BRIDGE else RAIL_CONNECT_KINDS
            network_name = "road" if tool == Tool.BRIDGE else "rail"
            if not any(self.tiles[nx][ny].build in anchor_kinds or not self.tiles[nx][ny].water for nx, ny in self.neighbors4(x, y)):
                return False, f"{TOOL_BUILD[tool].value} must touch land, {network_name}, or another bridge"
            return True, ""
        if tool == Tool.WATER:
            if tile.water:
                return False, "Water pipes need land"
            if tile.build == BuildKind.BURNING:
                return False, "Cannot build there"
            if tile.pipe:
                return False, "Pipe already there"
            return True, ""
        if tool in {Tool.ROAD, Tool.RAIL, Tool.POWERLINE}:
            if not tile.is_buildable():
                return False, "Cannot build there"
            if tile.build in SERVICE_KINDS or tile.build in ZONE_KINDS:
                return False, "Occupied"
            if tool == Tool.ROAD and tile.water:
                return False, "Drag roads across water to bridge automatically"
            if tool == Tool.RAIL and tile.water:
                return False, "Drag rails across water to bridge automatically"
            if tool == Tool.ROAD and tile.build not in {BuildKind.EMPTY, BuildKind.ROAD, BuildKind.RAIL, BuildKind.RAIL_CROSSING}:
                return False, "Road path is blocked"
            if tool == Tool.RAIL and tile.build not in {BuildKind.EMPTY, BuildKind.RAIL, BuildKind.ROAD, BuildKind.RAIL_CROSSING}:
                return False, "Rail path is blocked"
            return True, ""
        fw, fh = FOOTPRINTS[kind]
        if not self.in_bounds(x + fw - 1, y + fh - 1):
            return False, f"{kind.value} needs {fw}x{fh} tiles"
        for tx, ty in self.footprint_tiles(kind, x, y):
            ftile = self.tiles[tx][ty]
            if not ftile.is_buildable():
                return False, f"{kind.value} needs clear land"
            if kind == BuildKind.RAIL_STATION and self.rail_station_track_tile(x, y, tx, ty):
                if ftile.build not in {BuildKind.EMPTY, BuildKind.RAIL, BuildKind.RAIL_CROSSING}:
                    return False, "Railway Station needs clear platforms and a pass-through rail"
            elif ftile.build != BuildKind.EMPTY:
                return False, f"{kind.value} needs an empty {fw}x{fh} footprint"
        if kind == BuildKind.SEAPORT and not self.footprint_touches_water(kind, x, y):
            return False, "Seaport needs a clear shoreline"
        if kind == BuildKind.AIRPORT and not self.footprint_is_flat(kind, x, y):
            return False, "Airport needs a flat clear footprint"
        return True, ""

    def build(self, tool, x, y):
        ok, reason = self.can_build(tool, x, y)
        if not ok:
            self.add_message(reason, WARN)
            return
        price = COST[tool]
        if self.money < price:
            self.add_message("Not enough funds.", BAD)
            return
        self.money -= price
        tile = self.tiles[x][y]
        if tool == Tool.BULLDOZE:
            pipe_only = tile.build == BuildKind.EMPTY and not tile.trees and tile.pipe
            for tx, ty in list(self.building_tiles(x, y)):
                target = self.tiles[tx][ty]
                target.build = BuildKind.EMPTY
                target.level = 0
                target.trees = False
                if pipe_only:
                    target.pipe = False
                target.fire_timer = 0
                target.origin = None
                target.footprint = (1, 1)
                target.garbage_fill = 0.0
            self.add_message(f"Cleared tile for ${price}.", MUTED, 3)
        elif tool == Tool.WATER:
            tile.pipe = True
            self.add_message(f"Built {tool.value} for ${price}.", TEXT, 3)
        else:
            kind = TOOL_BUILD[tool]
            footprint = FOOTPRINTS[kind]
            for tx, ty in self.footprint_tiles(kind, x, y):
                target = self.tiles[tx][ty]
                target.build = kind
                target.level = 0
                target.trees = False
                target.fire_timer = 0
                target.origin = (x, y)
                target.footprint = footprint
                target.garbage_fill = 0.0
                if kind in ZONE_KINDS:
                    target.level = 1
            self.add_message(f"Built {tool.value} for ${price}.", TEXT, 3)
        self.rebuild_building_registry()
        self.recompute_networks()
        self.recompute_stats()

    def build_path(self, steps, total_cost):
        if not steps:
            self.add_message("No path to build.", WARN, 3)
            return
        if self.money < total_cost:
            self.add_message("Not enough funds for that path.", BAD)
            return
        self.money -= total_cost
        built = 0
        for tool, x, y in steps:
            kind = TOOL_BUILD[tool]
            tile = self.tiles[x][y]
            if tool == Tool.WATER:
                if tile.pipe:
                    continue
                tile.pipe = True
                built += 1
                continue
            if tile.build == kind:
                continue
            tile.build = kind
            tile.level = 0
            tile.trees = False
            tile.fire_timer = 0
            tile.origin = (x, y)
            tile.footprint = FOOTPRINTS[kind]
            tile.garbage_fill = 0.0
            built += 1
        self.add_message(f"Built {built} path tiles for ${total_cost}.", TEXT, 4)
        self.rebuild_building_registry()
        self.recompute_networks()
        self.recompute_stats()

    def build_zone_area(self, tool, tiles, total_cost):
        if not tiles:
            self.add_message("No zone area to build.", WARN, 3)
            return
        if self.money < total_cost:
            self.add_message("Not enough funds for that zone.", BAD)
            return
        kind = TOOL_BUILD[tool]
        self.money -= total_cost
        built = 0
        for x, y in tiles:
            tile = self.tiles[x][y]
            tile.build = kind
            tile.level = 1
            tile.trees = False
            tile.fire_timer = 0
            tile.origin = (x, y)
            tile.footprint = FOOTPRINTS[kind]
            tile.garbage_fill = 0.0
            built += 1
        self.add_message(f"Zoned {built} tiles for ${total_cost}.", TEXT, 4)
        self.rebuild_building_registry()
        self.recompute_networks()
        self.recompute_stats()

    def add_message(self, text, color=TEXT, ttl=7.0):
        if self.messages and self.messages[0].text == text:
            self.messages[0].ttl = ttl
            return
        self.messages.insert(0, Message(text, color, ttl))
        self.messages = self.messages[:6]

    def ignite_building(self, x, y):
        timer = random.randint(10, 18)
        for tx, ty in self.building_tiles(x, y):
            tile = self.tiles[tx][ty]
            tile.build = BuildKind.BURNING
            tile.fire_timer = timer
            tile.level = 0
        self.rebuild_building_registry()

    def trigger_fire(self):
        if not self.disasters_enabled:
            self.add_message("Disasters are off.", WARN, 4)
            return
        candidates = [
            (x, y)
            for x, y, tile in self.footprint_origin_tiles()
            if tile.build not in {BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL, BuildKind.RAIL_BRIDGE, BuildKind.RAIL_CROSSING, BuildKind.WATER, BuildKind.POWERLINE, BuildKind.BURNING, BuildKind.RUBBLE}
        ]
        if not candidates:
            self.add_message("No buildings to burn.", WARN)
            return
        x, y = random.choice(candidates)
        self.ignite_building(x, y)
        self.add_message("Fire reported. Build fire coverage or bulldoze fast.", BAD, 9)

    def update(self, dt):
        self.messages = [m for m in self.messages if m.ttl > 0]
        for m in self.messages:
            m.ttl -= dt
        if self.paused:
            return
        self.tick_accum += dt * self.sim_speed
        while self.tick_accum >= 0.32:
            self.tick_accum -= 0.32
            self.advance_day()

    def advance_day(self):
        self.day += 1
        if self.day <= 30:
            return
        self.day = 1
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.recompute_networks()
        self.recompute_tile_scores()
        self.grow_city()
        self.update_fires()
        self.recompute_stats()
        self.update_landfills()
        self.recompute_tile_scores()
        self.recompute_stats()
        self.update_citizen_health()
        self.update_citizen_education()
        self.recompute_stats()
        self.monthly_budget()
        self.record_graphs()

    def monthly_budget(self):
        taxable = self.stats.population * 0.8 + self.stats.jobs * 0.55 + self.stats.shops * 0.75
        income = taxable * (self.tax_rate / 100.0) * 5.0
        expenses = 0.0
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                if tile.build in SERVICE_KINDS and not tile.is_origin(x, y):
                    if tile.pipe:
                        expenses += MAINTENANCE[BuildKind.WATER]
                    continue
                if tile.pipe:
                    expenses += MAINTENANCE[BuildKind.WATER]
                expenses += MAINTENANCE.get(tile.build, 0.0)
                if tile.build in ZONE_KINDS:
                    expenses += tile.level * 0.04
        self.stats.income = income
        self.stats.expenses = expenses
        self.money += int(income - expenses)
        if self.money < 0:
            self.add_message("City is running a deficit. Raise taxes or slow expansion.", BAD, 8)
        elif income < expenses:
            self.add_message("Monthly budget is negative.", WARN, 6)

    def garbage_tiles(self):
        for x, y, tile in self.footprint_origin_tiles():
            if tile.build == BuildKind.GARBAGE:
                yield x, y, tile

    def landfill_garbage_generated(self):
        garbage = len(self.citizens) * CITIZEN_GARBAGE_USE
        for building in self.buildings.values():
            if building.kind == BuildKind.GARBAGE:
                continue
            _, _, building_garbage = self.building_resource_use(building)
            garbage += building_garbage
        return garbage

    def update_landfills(self):
        garbage_tiles = list(self.garbage_tiles())
        total_fill = sum(tile.garbage_fill for _, _, tile in garbage_tiles)
        total_fill = max(0.0, total_fill * (1.0 - GARBAGE_FILL_DECAY_RATE))
        total_fill += self.landfill_garbage_generated()
        if total_fill < 0.05:
            total_fill = 0.0

        remaining = total_fill
        ordered_tiles = sorted(
            garbage_tiles,
            key=lambda item: (item[2].garbage_fill <= 0, -item[2].garbage_fill, item[0], item[1]),
        )
        for _, _, tile in ordered_tiles:
            accepted = min(GARBAGE_ZONE_CAPACITY, remaining)
            tile.garbage_fill = accepted
            remaining -= accepted

    def school_trip_distance(self, citizen_id):
        for trip in self.trips:
            if trip.citizen_id == citizen_id and trip.purpose == "school":
                return trip.distance
        return 0

    def commute_distance(self, citizen_id):
        return sum(trip.distance for trip in self.trips if trip.citizen_id == citizen_id)

    def citizen_age_vulnerability(self, citizen):
        age = self.citizen_age(citizen)
        if age < 5:
            return 1.25
        if age <= 20:
            return 1.10
        if age <= 64:
            return 1.0
        elder_years = age - 65
        return 1.15 + elder_years ** 2 * 0.002 + elder_years ** 3 * 0.00007

    def clinic_coverage(self, origin):
        best = 0.0
        for nx, ny, distance in self.neighbors_radius(origin[0], origin[1], 8):
            tile = self.tiles[nx][ny]
            if tile.build == BuildKind.CLINIC and tile.is_origin(nx, ny):
                best = max(best, (8 - distance) / 8)
        return best

    def police_coverage(self, origin):
        best = 0.0
        for nx, ny, distance in self.neighbors_radius(origin[0], origin[1], 8):
            tile = self.tiles[nx][ny]
            if tile.build == BuildKind.POLICE and tile.is_origin(nx, ny):
                best = max(best, (8 - distance) / 8)
        return best

    def fire_coverage(self, origin):
        best = 0.0
        for nx, ny, distance in self.neighbors_radius(origin[0], origin[1], 8):
            tile = self.tiles[nx][ny]
            if tile.build == BuildKind.FIRE and tile.is_origin(nx, ny):
                best = max(best, (8 - distance) / 8)
        return best

    def library_coverage(self, origin):
        best = 0.0
        for nx, ny, distance in self.neighbors_radius(origin[0], origin[1], 8):
            tile = self.tiles[nx][ny]
            if tile.build == BuildKind.LIBRARY and tile.is_origin(nx, ny):
                best = max(best, (8 - distance) / 8)
        return best

    def stadium_coverage(self, origin):
        best = 0.0
        for nx, ny, distance in self.neighbors_radius(origin[0], origin[1], 8):
            tile = self.tiles[nx][ny]
            if tile.build == BuildKind.STADIUM and tile.is_origin(nx, ny):
                best = max(best, (8 - distance) / 8)
        return best

    def health_delta(self, citizen):
        home_id = self.citizen_home_building_id(citizen)
        if home_id not in self.buildings:
            return 0.0
        home = self.buildings[home_id]
        home_tile = self.tiles[home.origin[0]][home.origin[1]]
        positive = (HEALTH_TARGET - citizen.health) * 0.03
        positive += self.clinic_coverage(home.origin) * 1.2
        positive += (home_tile.health - 50) / 80

        negative = 0.0
        if not home_tile.watered:
            negative += 0.8
        if not home_tile.powered:
            negative += 0.4
        negative += home_tile.pollution / 80
        negative += home_tile.crime / 160
        if self.stats.garbage_used > self.stats.garbage_cap:
            negative += 0.8
        negative += self.commute_distance(citizen.id) / 80
        negative *= self.citizen_age_vulnerability(citizen)
        return positive - negative

    def update_citizen_health(self):
        dead_ids = [citizen.id for citizen in self.citizens.values() if citizen.health <= 0]
        for citizen_id in dead_ids:
            self.remove_citizen_from_household(citizen_id)
        for citizen in list(self.citizens.values()):
            citizen.health = clamp(citizen.health + self.health_delta(citizen), 0, 100)
        dead_ids.extend(citizen.id for citizen in self.citizens.values() if citizen.health <= 0)
        for citizen_id in dead_ids:
            self.remove_citizen_from_household(citizen_id)
        if dead_ids:
            self.rebuild_building_registry()
            count = len(dead_ids)
            self.add_message(f"{count} citizen{'s' if count != 1 else ''} died from poor health.", BAD, 7)

    def education_gain(self, citizen):
        home_id = self.citizen_home_building_id(citizen)
        school_id = citizen.school_id
        if home_id not in self.buildings or school_id not in self.buildings:
            return 0.0

        home = self.buildings[home_id]
        school = self.buildings[school_id]
        home_tile = self.tiles[home.origin[0]][home.origin[1]]
        school_tile = self.tiles[school.origin[0]][school.origin[1]]
        school_quality = clamp(0.60 + school_tile.education / 100.0 * 0.80, 0.60, 1.40)
        health_factor = clamp(0.50 + citizen.health / 100.0 * 0.70, 0.50, 1.20)
        commute_factor = clamp(1.08 - self.school_trip_distance(citizen.id) / 45.0, 0.50, 1.08)
        utility_factor = 1.0
        for tile in (home_tile, school_tile):
            if not tile.watered:
                utility_factor -= 0.12
            if not tile.powered:
                utility_factor -= 0.10
        if self.stats.garbage_used > self.stats.garbage_cap:
            utility_factor -= 0.10
        utility_factor = clamp(utility_factor, 0.45, 1.0)
        environment_factor = clamp(1.0 - (home_tile.pollution + school_tile.pollution) / 260.0 - (home_tile.crime + school_tile.crime) / 360.0, 0.45, 1.0)
        return MONTHLY_EDUCATION_GAIN * citizen.education_ability * school_quality * health_factor * commute_factor * utility_factor * environment_factor

    def update_citizen_education(self):
        self.sync_work_and_school_assignments()
        for citizen in self.citizens.values():
            if not self.is_school_age(citizen) or citizen.school_id not in self.buildings:
                continue
            citizen.education = clamp(citizen.education + self.education_gain(citizen), 0, 100)

    def record_graphs(self):
        for key, value in (
            ("population", self.stats.population),
            ("money", self.money),
            ("mood", self.stats.mood),
            ("pollution", self.stats.pollution),
        ):
            self.graphs[key].append(float(value))
            self.graphs[key] = self.graphs[key][-48:]

    def recompute_networks(self):
        for col in self.tiles:
            for tile in col:
                tile.powered = False
                tile.watered = False
                tile.road_access = False

        power_sources = []
        water_sources = []
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                b = tile.build
                if b in SERVICE_KINDS and not tile.is_origin(x, y):
                    continue
                if b in {BuildKind.COAL, BuildKind.SOLAR}:
                    power_sources.append((x, y, self.power_source_capacity(b)))
                elif b == BuildKind.WATER_PUMP:
                    capacity = self.water_pump_capacity(x, y)
                    if capacity:
                        water_sources.append((x, y, capacity))

        self._flood_network(power_sources, "powered", {BuildKind.POWERLINE, BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL_CROSSING})
        self._flood_network(water_sources, "watered", set(), use_pipes=True)
        self.apply_powerline_coverage(3)
        self.apply_pipe_coverage(3)
        self.apply_road_coverage(3)

        for x, y, tile in self.footprint_origin_tiles():
            if tile.build in ZONE_KINDS | SERVICE_KINDS:
                road_access = tile.road_access or any(self.tiles[nx][ny].build in ROAD_KINDS for nx, ny in self.building_boundary(x, y))
                powered = tile.powered or any(self.tiles[nx][ny].powered for nx, ny in self.building_boundary(x, y))
                watered = tile.watered or any(self.tiles[nx][ny].watered for nx, ny in self.building_boundary(x, y))
                for tx, ty in self.building_tiles(x, y):
                    self.tiles[tx][ty].road_access = road_access
                    self.tiles[tx][ty].powered = powered
                    self.tiles[tx][ty].watered = watered

    def apply_pipe_coverage(self, radius):
        covered = set()
        for x in range(self.width):
            for y in range(self.height):
                if not self.tiles[x][y].pipe or not self.tiles[x][y].watered:
                    continue
                for nx, ny, _ in self.neighbors_radius(x, y, radius):
                    tile = self.tiles[nx][ny]
                    if not tile.water and tile.build in ZONE_KINDS | SERVICE_KINDS:
                        covered.add(self.building_origin(nx, ny))
        for ox, oy in covered:
                for tx, ty in self.building_tiles(ox, oy):
                    self.tiles[tx][ty].watered = True

    def apply_powerline_coverage(self, radius):
        covered = set()
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                if tile.build != BuildKind.POWERLINE or not tile.powered:
                    continue
                for nx, ny, _ in self.neighbors_radius(x, y, radius):
                    target = self.tiles[nx][ny]
                    if not target.water and target.build in ZONE_KINDS | SERVICE_KINDS:
                        covered.add(self.building_origin(nx, ny))
        for ox, oy in covered:
            for tx, ty in self.building_tiles(ox, oy):
                self.tiles[tx][ty].powered = True

    def apply_road_coverage(self, radius):
        covered = set()
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].build not in ROAD_KINDS:
                    continue
                for nx, ny, _ in self.neighbors_radius(x, y, radius):
                    tile = self.tiles[nx][ny]
                    if not tile.water and tile.build in ZONE_KINDS | SERVICE_KINDS:
                        covered.add(self.building_origin(nx, ny))
        for ox, oy in covered:
            for tx, ty in self.building_tiles(ox, oy):
                self.tiles[tx][ty].road_access = True

    def _flood_network(self, sources, attr, carriers, use_pipes=False):
        queue = []
        capacity = 0
        for sx, sy, cap in sources:
            setattr(self.tiles[sx][sy], attr, True)
            queue.append((sx, sy))
            capacity += cap
        idx = 0
        while idx < len(queue):
            x, y = queue[idx]
            idx += 1
            for nx, ny in self.neighbors4(x, y):
                nt = self.tiles[nx][ny]
                if getattr(nt, attr):
                    continue
                if nt.build in carriers or (use_pipes and nt.pipe) or nt.build in ZONE_KINDS or nt.build in SERVICE_KINDS:
                    setattr(nt, attr, True)
                    queue.append((nx, ny))
        if attr == "powered":
            self.stats.power_cap = capacity
        else:
            self.stats.water_cap = capacity

    def recompute_tile_scores(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                scores = dict(TILE_SCORE["base"])
                scores["land_value"] += tile.terrain * TILE_SCORE["terrain_land_value"]
                if tile.water:
                    scores["land_value"] += TILE_SCORE["water_land_value"]
                if tile.trees:
                    scores["land_value"] += TILE_SCORE["trees_land_value"]
                radius = TILE_SCORE["radius"]
                for nx, ny, d in self.neighbors_radius(x, y, radius):
                    other = self.tiles[nx][ny]
                    if other.build in SERVICE_KINDS and not other.is_origin(nx, ny):
                        continue
                    weight = max(0.0, (radius - d) / radius)
                    effect = TILE_SCORE_EFFECTS.get(other.build)
                    if other.build in ROAD_KINDS:
                        effect = TILE_SCORE["road_effect"]
                    if not effect:
                        continue
                    fill_ratio = clamp(other.garbage_fill / GARBAGE_ZONE_CAPACITY, 0.0, 1.0)
                    for field in TILE_SCORE_FIELDS:
                        scores[field] += (
                            effect.get(field, 0.0)
                            + effect.get(f"{field}_per_level", 0.0) * other.level
                            + effect.get(f"{field}_per_fill", 0.0) * fill_ratio
                        ) * weight

                pollution = scores["pollution"]
                tile.pollution = clamp(pollution, 0, 100)
                tile.land_value = clamp(scores["land_value"] - pollution * TILE_SCORE["pollution_land_value_penalty"], 0, 100)
                tile.crime = clamp(
                    scores["crime"]
                    + max(0, tile.level - TILE_SCORE["level_crime_penalty_after"]) * TILE_SCORE["level_crime_penalty"],
                    0,
                    100,
                )
                tile.health = clamp(scores["health"] - pollution * TILE_SCORE["pollution_health_penalty"], 0, 100)
                tile.education = clamp(scores["education"], 0, 100)
                tile.fire_risk = clamp(
                    scores["fire_risk"]
                    + pollution * TILE_SCORE["pollution_fire_risk_penalty"]
                    + tile.level * TILE_SCORE["level_fire_risk"],
                    0,
                    100,
                )

    def grow_city(self):
        self.calculate_demand()
        origin_buildings = {building.origin: building for building in self.buildings.values()}
        zones = []
        for x in range(self.width):
            for y in range(self.height):
                t = self.tiles[x][y]
                if t.build in {BuildKind.RES, BuildKind.COM, BuildKind.IND}:
                    zones.append((x, y, t, origin_buildings.get((x, y))))
        for x, y, t, building in zones:
            pressure = self.zone_growth_pressure(t, building)
            score = self.zone_score(t)
            can_grow = t.powered and t.watered and t.road_access
            score_threshold = 50 if t.build == BuildKind.COM else 55
            if can_grow and pressure >= 70 and score >= score_threshold and t.level < 5:
                t.level += 1
            elif (pressure <= -25 or score < 25) and t.level > 1:
                t.level -= 1

        self.rebuild_building_registry()
        self.calculate_demand()
        if self.disasters_enabled and random.random() < 0.002 + self.stats.pollution / 70000:
            self.trigger_fire()

    def zone_fill_ratio(self, building, filled_attr, capacity_attr):
        if not building:
            return 0.0
        capacity = getattr(building, capacity_attr)
        if capacity <= 0:
            return 1.0
        return clamp(len(getattr(building, filled_attr)) / capacity, 0.0, 1.0)

    def resource_shortage_penalty(self):
        penalty = 0
        if self.stats.power_used > self.stats.power_cap:
            penalty += RESOURCE_SHORTAGE_PENALTY["power"]
        if self.stats.water_used > self.stats.water_cap:
            penalty += RESOURCE_SHORTAGE_PENALTY["water"]
        if self.stats.garbage_used > self.stats.garbage_cap:
            penalty += RESOURCE_SHORTAGE_PENALTY["garbage"]
        return penalty

    def commercial_customer_support(self):
        return clamp(len(self.citizens) / 12.0, 0.0, 1.0)

    def industrial_labor_support(self, building=None):
        working_age = len(self.working_age_citizens())
        if building and building.job_capacity > 0:
            return clamp(working_age / building.job_capacity, 0.0, 1.0)
        return clamp(working_age / 10.0, 0.0, 1.0)

    def zone_growth_pressure(self, tile, building):
        demand = {
            BuildKind.RES: self.stats.demand_r,
            BuildKind.COM: self.stats.demand_c,
            BuildKind.IND: self.stats.demand_i,
        }.get(tile.build, 0.0)
        score = self.zone_score(tile)
        pressure = demand + (score - 50) * 0.45
        if tile.build == BuildKind.RES:
            pressure += (self.zone_fill_ratio(building, "resident_ids", "resident_capacity") - 0.80) * 45
        elif tile.build == BuildKind.COM:
            pressure += (self.zone_fill_ratio(building, "worker_ids", "job_capacity") - 0.75) * 85
            customer_support = self.commercial_customer_support()
            pressure += customer_support * 30
            if building and building.level <= 1:
                pressure += customer_support * 20
        elif tile.build == BuildKind.IND:
            pressure += (self.zone_fill_ratio(building, "worker_ids", "job_capacity") - 0.70) * 70
            labor_support = self.industrial_labor_support(building)
            pressure += labor_support * 42
            if building and building.level <= 1:
                pressure += self.industrial_labor_support() * 16
        pressure += self.zone_growth_bonus(tile.build) * 100
        pressure -= self.tax_growth_penalty() * 100
        pressure -= self.resource_shortage_penalty() * 0.35
        return pressure

    def zone_growth_bonus(self, build):
        return ZONE_GROWTH_BONUS.get(build, 0.0)

    def tax_growth_penalty(self):
        return max(0.0, self.tax_rate - 8.0) * 0.006

    def zone_score(self, tile):
        utility = 0
        utility += 24 if tile.powered else -24
        utility += 18 if tile.watered else -18
        utility += 22 if tile.road_access else -28
        if tile.build == BuildKind.RES:
            utility += tile.land_value * 0.45 + tile.health * 0.18 + tile.education * 0.12
            utility -= tile.pollution * 0.4 + tile.crime * 0.16
        elif tile.build == BuildKind.COM:
            utility += tile.land_value * 0.25 + tile.education * 0.14
            utility -= tile.pollution * 0.15 + tile.crime * 0.2
        elif tile.build == BuildKind.IND:
            utility += 30 if tile.road_access else -20
            utility += 8 if tile.powered else -25
            utility -= tile.land_value * 0.04
        utility -= max(0, self.tax_rate - 8) * 4
        return clamp(utility, 0, 100)

    def calculate_demand(self):
        self.sync_work_and_school_assignments()
        housing_capacity = shops = 0
        pollution_sum = 0.0
        built = 0
        origin_buildings = {building.origin: building for building in self.buildings.values()}
        for x in range(self.width):
            for y in range(self.height):
                t = self.tiles[x][y]
                if t.build == BuildKind.RES:
                    housing_capacity += self.building_resident_capacity(t.build, t.level)
                    built += 1
                elif t.build == BuildKind.COM:
                    shops += self.commercial_shop_output(origin_buildings.get((x, y)))
                    built += 1
                elif t.build == BuildKind.IND:
                    built += 1
                elif t.build == BuildKind.GARBAGE:
                    built += 1
                elif t.build in SERVICE_KINDS:
                    if not t.is_origin(x, y):
                        continue
                pollution_sum += t.pollution

        power_used, water_used, garbage_used, garbage_cap = self.resource_usage()
        population = len(self.citizens)
        working_age = len(self.working_age_citizens())
        assigned_workers = sum(1 for citizen in self.citizens.values() if citizen.job_id is not None)
        job_capacity = sum(building.job_capacity for building in self.buildings.values())
        job_fill = assigned_workers / max(1, job_capacity) if job_capacity else 0.0
        school_age = len(self.school_age_citizens())
        assigned_students = sum(1 for citizen in self.citizens.values() if citizen.school_id is not None)
        education_coverage = assigned_students / max(1, school_age) if school_age else 1.0
        housing_fill = population / max(1, housing_capacity) if housing_capacity else 0.0
        unemployment = max(0.0, (working_age - assigned_workers) / max(1.0, working_age))
        worker_gap = max(0.0, (job_capacity - assigned_workers) / max(1.0, job_capacity))
        shop_gap = max(0.0, (population * 0.18 - shops) / max(1.0, population * 0.18))
        customer_signal = clamp(population / 30.0, 0.0, 1.0)
        labor_signal = clamp(working_age / 30.0, 0.0, 1.0)
        infrastructure_penalty = 0
        if power_used > self.stats.power_cap:
            infrastructure_penalty += RESOURCE_SHORTAGE_PENALTY["power"]
        if water_used > self.stats.water_cap:
            infrastructure_penalty += RESOURCE_SHORTAGE_PENALTY["water"]
        if garbage_used > garbage_cap:
            infrastructure_penalty += RESOURCE_SHORTAGE_PENALTY["garbage"]
        tax_penalty = max(0.0, self.tax_rate - 7.0) * 5.5
        cash_pressure = -8 if self.money < 0 else 0
        self.stats.population = int(population)
        self.stats.jobs = int(assigned_workers)
        self.stats.shops = int(shops)
        self.stats.power_used = int(power_used)
        self.stats.water_used = int(water_used)
        self.stats.garbage_used = garbage_used
        self.stats.garbage_cap = garbage_cap
        self.stats.unemployment = unemployment
        garbage_overflow = max(0, garbage_used - garbage_cap)
        self.stats.pollution = clamp(pollution_sum / max(1, self.width * self.height) + garbage_overflow * 0.02, 0, 100)
        self.stats.traffic = min(100, sum(trip.distance for trip in self.trips) * 0.35)
        service_score = self.average_services()
        self.stats.demand_r = clamp(24 + worker_gap * 80 + housing_fill * 24 + service_score * 0.16 - unemployment * 72 - tax_penalty * 1.05 - infrastructure_penalty + cash_pressure, -80, 100)
        self.stats.demand_c = clamp(20 + shop_gap * 86 + job_fill * 32 + customer_signal * 14 + population / 900 - tax_penalty * 0.9 - infrastructure_penalty * 0.8, -80, 100)
        self.stats.demand_i = clamp(18 + unemployment * 84 + job_fill * 28 + labor_signal * 18 - housing_capacity / 2000 - tax_penalty * 0.7 - infrastructure_penalty * 0.75, -80, 100)
        utility_score = 100
        if power_used > self.stats.power_cap:
            utility_score -= 32
        if water_used > self.stats.water_cap:
            utility_score -= 22
        if garbage_used > garbage_cap:
            utility_score -= 12
        self.stats.mood = clamp(
            55 + service_score * 0.24 + education_coverage * 6 - unemployment * 32 - self.stats.pollution * 0.35 - max(0, self.tax_rate - 8) * 4 + utility_score * 0.18,
            0,
            100,
        )

    def road_traffic_neighbors(self, x, y):
        return sum(1 for nx, ny in self.neighbors4(x, y) if self.tiles[nx][ny].build in ZONE_KINDS)

    def road_congestion(self, x, y):
        if self.tiles[x][y].build not in ROAD_KINDS:
            return 0
        return min(100, self.traffic_loads.get((x, y), 0.0) * 8.0)

    def average_services(self):
        total = count = 0
        for col in self.tiles:
            for t in col:
                if t.build in ZONE_KINDS:
                    total += (100 - t.crime) * 0.22 + t.health * 0.26 + t.education * 0.18 + (100 - t.fire_risk) * 0.18 + t.land_value * 0.16
                    count += 1
        return total / max(1, count)

    def recompute_stats(self):
        self.calculate_demand()

    def update_fires(self):
        burning = []
        changed = False
        for x in range(self.width):
            for y in range(self.height):
                t = self.tiles[x][y]
                if t.build == BuildKind.BURNING and t.is_origin(x, y):
                    burning.append((x, y, t))
        for x, y, t in burning:
            nearby_fire_station = any(self.tiles[nx][ny].build == BuildKind.FIRE for nx, ny, d in self.neighbors_radius(x, y, 7))
            t.fire_timer -= 2 if nearby_fire_station else 1
            if t.fire_timer <= 0:
                if nearby_fire_station and random.random() < 0.72:
                    for tx, ty in self.building_tiles(x, y):
                        self.tiles[tx][ty].build = BuildKind.RUBBLE
                        self.tiles[tx][ty].fire_timer = 0
                    self.add_message("Fire contained. Rubble remains.", WARN, 5)
                    changed = True
                else:
                    for tx, ty in self.building_tiles(x, y):
                        self.tiles[tx][ty].build = BuildKind.RUBBLE
                        self.tiles[tx][ty].fire_timer = 0
                    self.add_message("A building burned down.", BAD, 5)
                    changed = True
                    for tx, ty in self.building_tiles(x, y):
                        for nx, ny in self.neighbors4(tx, ty):
                            nt = self.tiles[nx][ny]
                            if nt.build not in {BuildKind.EMPTY, BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL, BuildKind.RAIL_BRIDGE, BuildKind.RAIL_CROSSING, BuildKind.WATER, BuildKind.POWERLINE, BuildKind.BURNING, BuildKind.RUBBLE} and random.random() < 0.08:
                                self.ignite_building(nx, ny)
        if changed:
            self.rebuild_building_registry()


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


class Button:
    def __init__(self, rect, label, tool=None, hotkey="", menu=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.tool = tool
        self.hotkey = hotkey
        self.menu = menu


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyCity 2000")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 15)
        self.small = pygame.font.SysFont("arial", 12)
        self.big = pygame.font.SysFont("arial", 22, bold=True)
        self.ui = UI(self)
        self.city = City()
        self.camera = Camera()
        self.tool = Tool.ROAD
        self.hover = None
        self.running = True
        self.dragging_map = False
        self.last_mouse = (0, 0)
        self.auto_build = False
        self.dragging_tax = False
        self.dragging_path = False
        self.path_start = None
        self.path_first_axis = None
        self.path_plan = []
        self.path_cost = 0
        self.path_error = ""
        self.dragging_zone = False
        self.zone_start = None
        self.zone_plan = []
        self.zone_cost = 0
        self.zone_error = ""
        self.movement_auto_pause_active = False
        self.movement_auto_pause_previous = False
        self.rotation_pause_timer = 0.0

    def save_game(self, path=SAVE_PATH):
        path = Path(path)
        path.write_text(json.dumps(self.city.to_dict(), indent=2), encoding="utf-8")
        self.city.add_message(f"Game saved to {path.name}.", GOOD, 5)

    def load_game(self, path=SAVE_PATH):
        path = Path(path)
        if not path.exists():
            self.city.add_message(f"No save file found: {path.name}.", WARN, 5)
            return False
        self.city = City.from_dict(json.loads(path.read_text(encoding="utf-8")))
        self.city.add_message(f"Game loaded from {path.name}.", GOOD, 5)
        self.hover = None
        self.dragging_path = False
        self.dragging_zone = False
        self.ui.selected_citizen_id = None
        self.path_plan = []
        self.zone_plan = []
        return True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.handle_keys(dt)
            self.city.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key, event.mod)
            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                if self.ui.handle_wheel(mx, my, event.y):
                    continue
                if mx < SCREEN_W - SIDEBAR_W:
                    old = self.camera.zoom
                    self.camera.zoom = clamp(self.camera.zoom + event.y * 0.08, 0.62, 1.55)
                    ratio = self.camera.zoom / old
                    self.camera.x = mx - (mx - self.camera.x) * ratio
                    self.camera.y = my - (my - self.camera.y) * ratio
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging_tax = False
                    self.ui.avatar_slider_dragging = None
                    if self.dragging_path:
                        self.commit_path()
                    if self.dragging_zone:
                        self.commit_zone_area()
                    self.auto_build = False
                    self.dragging_path = False
                    self.path_start = None
                    self.path_first_axis = None
                    self.path_plan = []
                    self.path_cost = 0
                    self.path_error = ""
                    self.dragging_zone = False
                    self.zone_start = None
                    self.zone_plan = []
                    self.zone_cost = 0
                    self.zone_error = ""
                if event.button == 2:
                    self.dragging_map = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_tax:
                    self.ui.set_tax_from_slider(event.pos[0])
                if self.ui.avatar_slider_dragging:
                    self.ui.set_avatar_editor_slider_from_mouse(self.ui.avatar_slider_dragging, event.pos[0])
                if self.dragging_map:
                    dx, dy = event.rel
                    self.camera.x += dx
                    self.camera.y += dy
                if self.dragging_path:
                    self.update_path_plan()
                if self.dragging_zone:
                    self.update_zone_plan()
                if self.auto_build:
                    self.use_tool_at_mouse()

    def handle_keydown(self, key, mod=0):
        ctrl = mod & pygame.KMOD_CTRL
        if ctrl and key == pygame.K_s:
            self.save_game()
            return
        if ctrl and key == pygame.K_l:
            self.load_game()
            return

        if key == pygame.K_ESCAPE:
            self.running = False
        elif key in TOOL_KEYS:
            self.tool = TOOL_KEYS[key]
        elif key == pygame.K_SPACE:
            self.city.paused = not self.city.paused
        elif key == pygame.K_LEFTBRACKET:
            self.city.sim_speed = max(0.25, self.city.sim_speed - 0.25)
        elif key == pygame.K_RIGHTBRACKET:
            self.city.sim_speed = min(FASTER_SPEED, self.city.sim_speed + 0.25)
        elif key == pygame.K_t:
            self.city.tax_rate = max(0.0, self.city.tax_rate - 0.5)
            self.city.add_message(f"Tax rate lowered to {self.city.tax_rate:.1f}%.", TEXT, 4)
        elif key == pygame.K_y:
            self.city.tax_rate = min(20.0, self.city.tax_rate + 0.5)
            self.city.add_message(f"Tax rate raised to {self.city.tax_rate:.1f}%.", TEXT, 4)
        elif key == pygame.K_f:
            self.city.trigger_fire()
        elif key == pygame.K_n:
            self.city.generate()
        elif key == pygame.K_i:
            self.tool = Tool.INSPECT
        elif key == pygame.K_q:
            self.rotate_map(-1)
        elif key == pygame.K_e:
            self.rotate_map(1)

    def handle_keys(self, dt):
        keys = pygame.key.get_pressed()
        speed = 520 * dt
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed *= 1.8
        if self.rotation_pause_timer > 0:
            self.rotation_pause_timer = max(0.0, self.rotation_pause_timer - dt)
        moving_camera = self.dragging_map or self.dragging_path or self.dragging_zone or self.rotation_pause_timer > 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.camera.x += speed
            moving_camera = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.camera.x -= speed
            moving_camera = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.camera.y += speed
            moving_camera = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.camera.y -= speed
            moving_camera = True
        self.update_movement_auto_pause(moving_camera)

    def rotate_map(self, turns):
        view_w = SCREEN_W - SIDEBAR_W
        view_h = SCREEN_H - TOPBAR_H
        self.camera.rotate(turns, view_w / 2, TOPBAR_H + view_h / 2)
        self.rotation_pause_timer = 0.28

    def update_movement_auto_pause(self, moving_camera):
        if moving_camera and not self.movement_auto_pause_active:
            self.movement_auto_pause_previous = self.city.paused
            self.city.paused = True
            self.movement_auto_pause_active = True
        elif not moving_camera and self.movement_auto_pause_active:
            self.city.paused = self.movement_auto_pause_previous
            self.movement_auto_pause_active = False

    def mouse_down(self, event):
        mx, my = event.pos
        if event.button == 2:
            self.dragging_map = True
            return
        clicked_ui = self.ui.handle_click(mx, my)
        if clicked_ui:
            return
        if mx >= SCREEN_W - SIDEBAR_W or my < TOPBAR_H:
            return
        if event.button == 1:
            if self.tool in PATH_TOOLS:
                tx, ty = self.camera.screen_to_world(mx, my)
                if self.city.in_bounds(tx, ty):
                    self.dragging_path = True
                    self.path_start = (tx, ty)
                    self.path_first_axis = None
                    self.update_path_plan()
            elif self.tool in ZONE_TOOLS:
                tx, ty = self.camera.screen_to_world(mx, my)
                if self.city.in_bounds(tx, ty):
                    self.dragging_zone = True
                    self.zone_start = (tx, ty)
                    self.update_zone_plan()
            else:
                self.use_tool_at_mouse()
                self.auto_build = self.tool == Tool.BULLDOZE
        elif event.button == 3:
            tx, ty = self.camera.screen_to_world(mx, my)
            if self.city.in_bounds(tx, ty):
                self.city.selected = (tx, ty)

    def update_path_plan(self):
        if not self.path_start or self.tool not in PATH_TOOLS:
            self.path_plan = []
            self.path_cost = 0
            return
        mx, my = pygame.mouse.get_pos()
        if mx >= SCREEN_W - SIDEBAR_W or my < TOPBAR_H:
            return
        end = self.camera.screen_to_world(mx, my)
        if not self.city.in_bounds(end[0], end[1]):
            return
        self.update_path_first_axis(end)
        self.path_plan, self.path_cost, self.path_error = self.plan_path(self.path_start, end, self.tool, self.path_first_axis)

    def update_path_first_axis(self, end):
        if end == self.path_start:
            self.path_first_axis = None
            return
        if self.path_first_axis:
            return
        dx = end[0] - self.path_start[0]
        dy = end[1] - self.path_start[1]
        if dx and not dy:
            self.path_first_axis = "x"
        elif dy and not dx:
            self.path_first_axis = "y"
        elif dx or dy:
            self.path_first_axis = "x" if abs(dx) >= abs(dy) else "y"

    def make_path_tiles(self, start, end, first_axis=None):
        x1, y1 = start
        x2, y2 = end
        path = []

        def add_line(ax, ay, bx, by):
            if ax != bx:
                step = 1 if bx > ax else -1
                for x in range(ax, bx + step, step):
                    if not path or path[-1] != (x, ay):
                        path.append((x, ay))
            if ay != by:
                step = 1 if by > ay else -1
                for y in range(ay, by + step, step):
                    if not path or path[-1] != (bx, y):
                        path.append((bx, y))

        if first_axis is None:
            first_axis = "x" if abs(x2 - x1) >= abs(y2 - y1) else "y"

        if first_axis == "x":
            add_line(x1, y1, x2, y1)
            add_line(x2, y1, x2, y2)
        else:
            add_line(x1, y1, x1, y2)
            add_line(x1, y2, x2, y2)
        return path

    def plan_path(self, start, end, tool, first_axis=None):
        raw_tiles = self.make_path_tiles(start, end, first_axis)
        planned = []
        planned_roads = set()
        planned_bridges = set()
        planned_rails = set()
        planned_rail_bridges = set()
        total = 0
        error = ""
        for x, y in raw_tiles:
            tile = self.city.tiles[x][y]
            step_tool = tool
            if tool == Tool.ROAD and tile.water:
                step_tool = Tool.BRIDGE
            elif tool == Tool.RAIL and tile.water:
                step_tool = Tool.RAIL_BRIDGE
            elif tool == Tool.ROAD and tile.build in RAIL_KINDS:
                step_tool = Tool.RAIL_CROSSING
            elif tool == Tool.RAIL and tile.build in ROAD_KINDS:
                step_tool = Tool.RAIL_CROSSING
            kind = TOOL_BUILD[step_tool]
            valid = True
            reason = ""
            existing = tile.pipe if step_tool == Tool.WATER else tile.build == kind
            if step_tool == Tool.RAIL and self.city.is_rail_station_track(x, y):
                existing = True
            if existing:
                pass
            elif step_tool in {Tool.BRIDGE, Tool.RAIL_BRIDGE}:
                if not tile.water:
                    valid = False
                    reason = f"{kind.value}s must stay on water"
                elif tile.build != BuildKind.EMPTY:
                    valid = False
                    reason = f"{kind.value} path is blocked"
            elif step_tool == Tool.RAIL_CROSSING:
                if tile.water:
                    valid = False
                    reason = "Rail crossing needs land"
                elif tool == Tool.ROAD and tile.build not in RAIL_KINDS:
                    valid = False
                    reason = "Road crossing needs an existing rail"
                elif tool == Tool.RAIL and tile.build not in ROAD_KINDS:
                    valid = False
                    reason = "Rail crossing needs an existing road"
            elif step_tool == Tool.ROAD:
                if tile.water:
                    valid = False
                    reason = "Road path needs bridge over water"
                elif tile.build in SERVICE_KINDS or tile.build in ZONE_KINDS or tile.build not in {BuildKind.EMPTY, BuildKind.ROAD}:
                    valid = False
                    reason = "Road path is blocked"
            elif step_tool == Tool.WATER:
                if tile.water:
                    valid = False
                    reason = "Water pipe needs land"
                elif tile.build == BuildKind.BURNING:
                    valid = False
                    reason = "Water pipe path is blocked"
            else:
                if tile.water:
                    valid = False
                    reason = f"{step_tool.value} path needs land"
                elif tile.build != BuildKind.EMPTY:
                    valid = False
                    reason = f"{step_tool.value} path is blocked"
            if valid and not existing:
                total += COST[step_tool]
            if valid and kind in ROAD_KINDS and kind != BuildKind.BRIDGE:
                planned_roads.add((x, y))
            if valid and kind == BuildKind.BRIDGE:
                planned_bridges.add((x, y))
            if valid and kind in RAIL_KINDS and kind != BuildKind.RAIL_BRIDGE:
                planned_rails.add((x, y))
            if valid and kind == BuildKind.RAIL_BRIDGE:
                planned_rail_bridges.add((x, y))
            if not valid and not error:
                error = reason
            planned.append({"x": x, "y": y, "tool": step_tool, "kind": kind, "valid": valid, "existing": existing})

        bridge_error = self.validate_bridge_components(planned_bridges, planned_roads, ROAD_KINDS, "Bridge path must connect to land or road")
        if bridge_error:
            error = error or bridge_error
            for step in planned:
                if (step["x"], step["y"]) in planned_bridges:
                    step["valid"] = False
        rail_bridge_error = self.validate_bridge_components(planned_rail_bridges, planned_rails, RAIL_CONNECT_KINDS, "Rail bridge path must connect to land or rail")
        if rail_bridge_error:
            error = error or rail_bridge_error
            for step in planned:
                if (step["x"], step["y"]) in planned_rail_bridges:
                    step["valid"] = False
        return planned, total, error

    def validate_bridge_components(self, planned_bridges, planned_land_paths, anchor_kinds, error_message):
        remaining = set(planned_bridges)
        while remaining:
            start = remaining.pop()
            stack = [start]
            component = {start}
            anchored = False
            while stack:
                x, y = stack.pop()
                for nx, ny in self.city.neighbors4(x, y):
                    if (nx, ny) in planned_bridges and (nx, ny) not in component:
                        component.add((nx, ny))
                        remaining.discard((nx, ny))
                        stack.append((nx, ny))
                    elif self.city.tiles[nx][ny].build in anchor_kinds or (nx, ny) in planned_land_paths or not self.city.tiles[nx][ny].water:
                        anchored = True
            if not anchored:
                return error_message
        return ""

    def commit_path(self):
        if not self.path_plan:
            return
        invalid = [step for step in self.path_plan if not step["valid"]]
        if invalid:
            self.city.add_message(self.path_error or "Path is blocked.", WARN, 5)
            return
        steps = [
            (step["tool"], step["x"], step["y"])
            for step in self.path_plan
            if not step["existing"]
        ]
        self.city.build_path(steps, self.path_cost)

    def update_zone_plan(self):
        if not self.zone_start or self.tool not in ZONE_TOOLS:
            self.zone_plan = []
            self.zone_cost = 0
            return
        mx, my = pygame.mouse.get_pos()
        if mx >= SCREEN_W - SIDEBAR_W or my < TOPBAR_H:
            return
        end = self.camera.screen_to_world(mx, my)
        if not self.city.in_bounds(end[0], end[1]):
            return
        self.zone_plan, self.zone_cost, self.zone_error = self.plan_zone_area(self.zone_start, end, self.tool)

    def make_area_tiles(self, start, end):
        x1, y1 = start
        x2, y2 = end
        left, right = sorted((x1, x2))
        top, bottom = sorted((y1, y2))
        return [(x, y) for x in range(left, right + 1) for y in range(top, bottom + 1)]

    def plan_zone_area(self, start, end, tool):
        planned = []
        total = 0
        error = ""
        kind = TOOL_BUILD[tool]
        for x, y in self.make_area_tiles(start, end):
            tile = self.city.tiles[x][y]
            existing = tile.build == kind
            valid = True
            reason = ""
            if existing:
                pass
            elif tile.water:
                valid = False
                reason = "Zone area needs land"
            elif tile.build != BuildKind.EMPTY:
                valid = False
                reason = "Zone area is blocked"
            if valid and not existing:
                total += COST[tool]
            if not valid and not error:
                error = reason
            planned.append({"x": x, "y": y, "tool": tool, "kind": kind, "valid": valid, "existing": existing})
        return planned, total, error

    def commit_zone_area(self):
        if not self.zone_plan:
            return
        invalid = [step for step in self.zone_plan if not step["valid"]]
        if invalid:
            self.city.add_message(self.zone_error or "Zone area is blocked.", WARN, 5)
            return
        tiles = [(step["x"], step["y"]) for step in self.zone_plan if not step["existing"]]
        self.city.build_zone_area(self.tool, tiles, self.zone_cost)

    def use_tool_at_mouse(self):
        mx, my = pygame.mouse.get_pos()
        if mx >= SCREEN_W - SIDEBAR_W or my < TOPBAR_H:
            return
        tx, ty = self.camera.screen_to_world(mx, my)
        if not self.city.in_bounds(tx, ty):
            return
        if self.tool == Tool.INSPECT:
            self.city.selected = (tx, ty)
            return
        self.city.build(self.tool, tx, ty)

    def draw(self):
        self.screen.fill((12, 17, 22))
        self.update_hover()
        self.draw_map()
        self.ui.draw()
        pygame.display.flip()

    def update_hover(self):
        mx, my = pygame.mouse.get_pos()
        tx, ty = self.camera.screen_to_world(mx, my)
        self.hover = (tx, ty) if self.city.in_bounds(tx, ty) and mx < SCREEN_W - SIDEBAR_W and my >= TOPBAR_H else None

    def draw_map(self):
        pipe_build_view = self.pipe_build_view_active()
        analysis_view = self.analysis_map_active()
        visible = []
        for x in range(self.city.width):
            for y in range(self.city.height):
                sx, sy = self.camera.world_to_screen(x, y)
                if -100 < sx < SCREEN_W - SIDEBAR_W + 100 and -80 < sy < SCREEN_H + 160:
                    rx, ry = self.camera.rotate_world(x, y)
                    visible.append((rx + ry, x, y, sx, sy))
        visible.sort()
        for _, x, y, sx, sy in visible:
            self.draw_tile(x, y, sx, sy, underground=pipe_build_view)
        if analysis_view:
            self.draw_analysis_map_layer(visible)
        if pipe_build_view:
            self.draw_underground_surface_markers(visible)
        elif not analysis_view:
            for _, x, y, sx, sy in visible:
                self.draw_building(x, y, sx, sy, services=False)
            for _, x, y, sx, sy in visible:
                self.draw_building(x, y, sx, sy, services=True)
        if self.water_layer_visible():
            self.draw_water_pipe_layer(visible)

        if self.dragging_path and self.path_plan:
            self.draw_path_preview()
        elif self.dragging_zone and self.zone_plan:
            self.draw_zone_area_preview()
        elif self.hover:
            self.draw_tool_preview()
        if self.city.selected:
            self.draw_tile_overlay(self.city.selected[0], self.city.selected[1], (255, 237, 135), 2)

    def water_layer_visible(self):
        selected_pipe = self.city.selected and self.city.tiles[self.city.selected[0]][self.city.selected[1]].pipe
        return self.tool == Tool.WATER or self.ui.map_mode == MapMode.PIPES or selected_pipe

    def pipe_build_view_active(self):
        return self.tool == Tool.WATER or self.ui.map_mode == MapMode.PIPES

    def analysis_map_active(self):
        return self.ui.map_mode in {MapMode.TRAFFIC, MapMode.LAND_VALUE, MapMode.POLLUTION, MapMode.CRIME, MapMode.FIRE_RISK, MapMode.HEALTH}

    def draw_analysis_map_layer(self, visible):
        for _, x, y, _, _ in visible:
            color = self.analysis_tile_color(x, y)
            if not color:
                continue
            poly = self.tile_base_poly(x, y) if self.city.tiles[x][y].water else self.tile_top_poly(x, y)
            pygame.draw.polygon(self.screen, color, poly)
            pygame.draw.polygon(self.screen, darken(color, 0.55), poly, max(1, int(self.camera.zoom)))

    def analysis_tile_color(self, x, y):
        tile = self.city.tiles[x][y]
        if self.ui.map_mode == MapMode.TRAFFIC:
            if tile.build in ROAD_KINDS:
                return risk_color(self.city.road_congestion(x, y))
            if tile.build in ZONE_KINDS:
                return (76, 70, 62)
            return None
        if self.ui.map_mode == MapMode.LAND_VALUE and tile.build in ZONE_KINDS:
            return heat_color(tile.land_value)
        if self.ui.map_mode == MapMode.POLLUTION:
            return risk_color(tile.pollution)
        if self.ui.map_mode == MapMode.CRIME:
            return risk_color(tile.crime)
        if self.ui.map_mode == MapMode.FIRE_RISK:
            return risk_color(tile.fire_risk)
        if self.ui.map_mode == MapMode.HEALTH:
            return heat_color(tile.health)
        return None

    def draw_water_pipe_layer(self, visible):
        for _, x, y, _, _ in visible:
            if self.city.tiles[x][y].pipe:
                sx, sy = self.tile_screen(x, y)
                self.draw_pipe(x, y, sx, sy)

    def tile_poly(self, sx, sy):
        tw, th = self.camera.tile_w, self.camera.tile_h
        return [(sx, sy - th / 2), (sx + tw / 2, sy), (sx, sy + th / 2), (sx - tw / 2, sy)]

    def terrain_level_at(self, x, y):
        if not self.city.in_bounds(x, y):
            return 0
        tile = self.city.tiles[x][y]
        return 0 if tile.water else tile.terrain

    def terrain_vertex_level(self, gx, gy):
        coords = [(gx, gy), (gx - 1, gy), (gx, gy - 1), (gx - 1, gy - 1)]
        for tx, ty in coords:
            if self.city.in_bounds(tx, ty) and self.city.tiles[tx][ty].water:
                return 0
        samples = [self.terrain_level_at(tx, ty) for tx, ty in coords]
        return sum(samples) / len(samples)

    def tile_corner_lifts(self, x, y):
        z = TERRAIN_LEVEL_HEIGHT * self.camera.zoom
        return [
            self.terrain_vertex_level(x, y) * z,
            self.terrain_vertex_level(x + 1, y) * z,
            self.terrain_vertex_level(x + 1, y + 1) * z,
            self.terrain_vertex_level(x, y + 1) * z,
        ]

    def tile_top_poly(self, x, y):
        base = self.tile_base_poly(x, y)
        lifts = self.tile_corner_lifts(x, y)
        return [(px, py - lift) for (px, py), lift in zip(base, lifts)]

    def tile_base_poly(self, x, y):
        return [
            self.camera.world_to_screen(x - 0.5, y - 0.5),
            self.camera.world_to_screen(x + 0.5, y - 0.5),
            self.camera.world_to_screen(x + 0.5, y + 0.5),
            self.camera.world_to_screen(x - 0.5, y + 0.5),
        ]

    def tile_lift(self, x, y):
        if not self.city.in_bounds(x, y):
            return 0
        if self.city.tiles[x][y].water:
            return 0
        lifts = self.tile_corner_lifts(x, y)
        return sum(lifts) / len(lifts)

    def tile_screen(self, x, y):
        sx, sy = self.camera.world_to_screen(x, y)
        return sx, sy - self.tile_lift(x, y)

    def draw_tile(self, x, y, sx, sy, underground=False):
        t = self.city.tiles[x][y]
        color = WATER_COLOR if t.water else GROUND_COLOR
        if t.build == BuildKind.RUBBLE:
            color = (98, 92, 84)
        poly = self.tile_base_poly(x, y) if t.water else self.tile_top_poly(x, y)
        pygame.draw.polygon(self.screen, color, poly)
        pygame.draw.polygon(self.screen, (27, 52, 52), poly, 1)
        cx = sum(p[0] for p in poly) / len(poly)
        cy = sum(p[1] for p in poly) / len(poly)
        if underground:
            return
        if t.trees:
            self.draw_tree(cx, cy - 4 * self.camera.zoom)
        if t.powered and not t.water and t.build in ZONE_KINDS:
            self.draw_dot(cx - 13 * self.camera.zoom, cy - 1 * self.camera.zoom, (255, 224, 97))
        if t.watered and not t.water and t.build in ZONE_KINDS:
            self.draw_dot(cx + 13 * self.camera.zoom, cy - 1 * self.camera.zoom, (101, 183, 255))

    def draw_dot(self, x, y, color):
        pygame.draw.circle(self.screen, color, (int(x), int(y)), max(2, int(2.5 * self.camera.zoom)))

    def underground_marker_color(self, tile):
        if tile.water or tile.build in {BuildKind.EMPTY, BuildKind.WATER}:
            return None
        if tile.build in ZONE_KINDS:
            return (198, 174, 85)
        if tile.build in ROAD_KINDS or tile.build in RAIL_KINDS or tile.build == BuildKind.POWERLINE:
            return (140, 146, 150)
        return (172, 101, 92)

    def draw_underground_surface_markers(self, visible):
        for _, x, y, _, _ in visible:
            color = self.underground_marker_color(self.city.tiles[x][y])
            if not color:
                continue
            poly = self.tile_top_poly(x, y)
            cx = sum(p[0] for p in poly) / len(poly)
            cy = sum(p[1] for p in poly) / len(poly)
            marker = [(cx + (px - cx) * 0.58, cy + (py - cy) * 0.58) for px, py in poly]
            pygame.draw.polygon(self.screen, color, marker)
            pygame.draw.polygon(self.screen, darken(color, 0.55), marker, max(1, int(self.camera.zoom)))

    def draw_tile_overlay(self, x, y, color, width):
        poly = self.tile_base_poly(x, y) if self.city.tiles[x][y].water else self.tile_top_poly(x, y)
        pygame.draw.polygon(self.screen, color, poly, width)

    def draw_tool_preview(self):
        x, y = self.hover
        if self.tool == Tool.BULLDOZE:
            ok, _ = self.city.can_build(self.tool, x, y)
            color = BAD if ok else MUTED
            for tx, ty in self.city.building_tiles(x, y):
                self.draw_tile_overlay(tx, ty, color, 2)
        elif self.tool in TOOL_BUILD:
            kind = TOOL_BUILD[self.tool]
            ok, _ = self.city.can_build(self.tool, x, y)
            color = ACCENT if ok else BAD
            for tx, ty in self.city.footprint_tiles(kind, x, y):
                if self.city.in_bounds(tx, ty):
                    self.draw_tile_overlay(tx, ty, color, 2)
        else:
            for tx, ty in self.city.building_tiles(x, y):
                self.draw_tile_overlay(tx, ty, ACCENT, 2)

    def draw_path_preview(self):
        preview = {
            (step["x"], step["y"]): step["kind"]
            for step in self.path_plan
            if step["valid"]
        }
        for step in self.path_plan:
            if not step["valid"]:
                continue
            sx, sy = self.tile_screen(step["x"], step["y"])
            if step["kind"] == BuildKind.RAIL_CROSSING:
                self.draw_road(step["x"], step["y"], sx, sy, preview)
                self.draw_rail(step["x"], step["y"], sx, sy, preview)
                self.draw_rail_crossing_mark(sx, sy)
            elif step["kind"] in ROAD_KINDS:
                self.draw_road(step["x"], step["y"], sx, sy, preview)
            elif step["kind"] in RAIL_KINDS:
                self.draw_rail(step["x"], step["y"], sx, sy, preview)
            elif step["kind"] == BuildKind.POWERLINE:
                self.draw_powerline(step["x"], step["y"], sx, sy, preview)
            elif step["kind"] == BuildKind.WATER:
                self.draw_pipe(step["x"], step["y"], sx, sy, preview)
        for step in self.path_plan:
            color = ACCENT if step["valid"] else BAD
            if step["existing"]:
                color = MUTED
            self.draw_tile_overlay(step["x"], step["y"], color, 3)

    def draw_zone_area_preview(self):
        for step in self.zone_plan:
            color = ACCENT if step["valid"] else BAD
            if step["existing"]:
                color = MUTED
            self.draw_tile_overlay(step["x"], step["y"], color, 3)

    def draw_tree(self, sx, sy):
        z = self.camera.zoom
        pygame.draw.rect(self.screen, (82, 64, 38), (sx - 1 * z, sy, 3 * z, 8 * z))
        pygame.draw.circle(self.screen, (33, 98, 58), (int(sx), int(sy - 2 * z)), max(3, int(6 * z)))

    def draw_building(self, x, y, sx, sy, services=None):
        t = self.city.tiles[x][y]
        z = self.camera.zoom
        sx, sy = self.tile_screen(x, y)
        if t.build == BuildKind.EMPTY:
            return
        is_service = t.build in SERVICE_KINDS
        if services is not None and is_service != services:
            return
        if t.build == BuildKind.RAIL_CROSSING:
            self.draw_road(x, y, sx, sy)
            self.draw_rail(x, y, sx, sy)
            self.draw_rail_crossing_mark(sx, sy)
        elif t.build in ROAD_KINDS:
            self.draw_road(x, y, sx, sy)
        elif t.build in RAIL_KINDS:
            self.draw_rail(x, y, sx, sy)
        elif t.build == BuildKind.POWERLINE:
            self.draw_powerline(x, y, sx, sy)
        elif t.build == BuildKind.WATER:
            self.draw_pipe(x, y, sx, sy)
        elif t.build in ZONE_KINDS:
            self.draw_zone(t, x, y, sx, sy)
        elif t.build == BuildKind.PARK:
            self.draw_park(x, y, sx, sy)
        elif t.build in {BuildKind.POLICE, BuildKind.FIRE, BuildKind.CLINIC, BuildKind.SCHOOL, BuildKind.LIBRARY, BuildKind.STADIUM, BuildKind.RAIL_STATION, BuildKind.SEAPORT, BuildKind.AIRPORT, BuildKind.WATER_PUMP, BuildKind.LARGE_PARK, BuildKind.COAL, BuildKind.SOLAR}:
            if not t.is_origin(x, y):
                return
            fw, fh = t.footprint
            self.draw_service(t, x, y, fw, fh)
        elif t.build == BuildKind.RUBBLE:
            for i in range(5):
                ox = (i - 2) * 5 * z
                pygame.draw.rect(self.screen, (75, 68, 61), (sx + ox - 3 * z, sy - 4 * z, 7 * z, 5 * z))
        elif t.build == BuildKind.BURNING:
            self.draw_fire(sx, sy)

    def preview_build_kind(self, x, y, preview=None):
        if preview and (x, y) in preview:
            return preview[(x, y)]
        return self.city.tiles[x][y].build

    def preview_has_pipe(self, x, y, preview=None):
        return (preview and preview.get((x, y)) == BuildKind.WATER) or self.city.tiles[x][y].pipe

    def draw_road(self, x, y, sx, sy, preview=None):
        z = self.camera.zoom
        is_bridge = self.preview_build_kind(x, y, preview) == BuildKind.BRIDGE
        dark = (91, 82, 72) if is_bridge else (57, 61, 65)
        line = (204, 198, 126)
        road_poly = self.tile_base_poly(x, y) if is_bridge else self.tile_top_poly(x, y)
        pygame.draw.polygon(self.screen, dark, road_poly)
        if is_bridge:
            pygame.draw.line(self.screen, (43, 36, 31), (sx - 18 * z, sy + 7 * z), (sx + 18 * z, sy + 7 * z), max(2, int(3 * z)))
            pygame.draw.line(self.screen, (180, 165, 134), (sx - 19 * z, sy - 5 * z), (sx + 19 * z, sy - 5 * z), max(1, int(2 * z)))
        for nx, ny in self.city.neighbors4(x, y):
            if self.preview_build_kind(nx, ny, preview) in ROAD_KINDS:
                ex, ey = self.camera.world_to_screen((x + nx) / 2, (y + ny) / 2)
                ey -= (self.tile_lift(x, y) + self.tile_lift(nx, ny)) / 2
                pygame.draw.line(self.screen, dark, (sx, sy), (ex, ey), max(5, int(11 * z)))
                pygame.draw.line(self.screen, line, (sx, sy), (ex, ey), max(1, int(2 * z)))

    def draw_rail(self, x, y, sx, sy, preview=None):
        z = self.camera.zoom
        kind = self.preview_build_kind(x, y, preview)
        is_bridge = kind == BuildKind.RAIL_BRIDGE
        is_crossing = kind == BuildKind.RAIL_CROSSING
        bed = self.tile_base_poly(x, y) if is_bridge else self.tile_top_poly(x, y)
        if not is_crossing:
            pygame.draw.polygon(self.screen, (82, 68, 56) if is_bridge else (67, 63, 57), bed)
        if is_bridge:
            pygame.draw.line(self.screen, (43, 36, 31), (sx - 22 * z, sy + 9 * z), (sx + 22 * z, sy + 9 * z), max(2, int(4 * z)))
            pygame.draw.line(self.screen, (168, 139, 96), (sx - 23 * z, sy - 7 * z), (sx + 23 * z, sy - 7 * z), max(1, int(2 * z)))
        connected = False
        for nx, ny in self.city.neighbors4(x, y):
            if self.preview_build_kind(nx, ny, preview) in RAIL_CONNECT_KINDS:
                ex, ey = self.camera.world_to_screen((x + nx) / 2, (y + ny) / 2)
                ey -= (self.tile_lift(x, y) + self.tile_lift(nx, ny)) / 2
                self.draw_double_rail_segment((sx, sy), (ex, ey), z)
                connected = True
        if not connected:
            ax, ay = self.camera.world_to_screen(x - 0.45, y)
            bx, by = self.camera.world_to_screen(x + 0.45, y)
            ay -= self.tile_lift(x, y)
            by -= self.tile_lift(x, y)
            self.draw_double_rail_segment((ax, ay), (bx, by), z)

    def draw_double_rail_segment(self, start, end, z):
        sx, sy = start
        ex, ey = end
        dx, dy = ex - sx, ey - sy
        length = max(1.0, math.hypot(dx, dy))
        nx, ny = -dy / length, dx / length
        tx, ty = dx / length, dy / length
        ballast = (65, 60, 54)
        ballast_edge = (46, 43, 39)
        sleeper = (93, 68, 44)
        sleeper_edge = (54, 43, 34)
        rail_shadow = (66, 68, 66)
        rail = (164, 166, 158)
        rail_highlight = (218, 216, 202)
        track_centers = (-4.4 * z, 4.4 * z)
        rail_gap = 1.55 * z

        pygame.draw.line(self.screen, (42, 39, 36), start, end, max(7, int(10 * z)))
        for center in track_centers:
            bed_start = (sx + nx * center, sy + ny * center)
            bed_end = (ex + nx * center, ey + ny * center)
            pygame.draw.line(self.screen, ballast_edge, bed_start, bed_end, max(5, int(8 * z)))
            pygame.draw.line(self.screen, ballast, bed_start, bed_end, max(4, int(6 * z)))

        sleeper_count = max(2, int(length / max(10 * z, 1)))
        for i in range(1, sleeper_count + 1):
            t = i / (sleeper_count + 1)
            cx = sx + dx * t
            cy = sy + dy * t
            for center in track_centers:
                mid = (cx + nx * center, cy + ny * center)
                half = 3.8 * z
                a = (mid[0] - nx * half, mid[1] - ny * half)
                b = (mid[0] + nx * half, mid[1] + ny * half)
                pygame.draw.line(self.screen, sleeper_edge, (a[0], a[1] + z), (b[0], b[1] + z), max(1, int(3 * z)))
                pygame.draw.line(self.screen, sleeper, a, b, max(1, int(2 * z)))

        for center in track_centers:
            for side in (-rail_gap, rail_gap):
                offset = center + side
                a = (sx + nx * offset, sy + ny * offset)
                b = (ex + nx * offset, ey + ny * offset)
                pygame.draw.line(self.screen, rail_shadow, (a[0], a[1] + 1.4 * z), (b[0], b[1] + 1.4 * z), max(1, int(3 * z)))
                pygame.draw.line(self.screen, rail, a, b, max(1, int(2 * z)))
                pygame.draw.line(
                    self.screen,
                    rail_highlight,
                    (a[0] - tx * z * 0.4, a[1] - ty * z * 0.4),
                    (b[0] - tx * z * 0.4, b[1] - ty * z * 0.4),
                    max(1, int(z)),
                )

    def draw_rail_crossing_mark(self, sx, sy):
        z = self.camera.zoom
        paint = (236, 224, 132)
        dark = (52, 45, 38)
        width = max(1, int(2 * z))
        pygame.draw.line(self.screen, dark, (sx - 13 * z, sy - 10 * z), (sx + 13 * z, sy + 10 * z), width + 2)
        pygame.draw.line(self.screen, dark, (sx - 13 * z, sy + 10 * z), (sx + 13 * z, sy - 10 * z), width + 2)
        pygame.draw.line(self.screen, paint, (sx - 13 * z, sy - 10 * z), (sx + 13 * z, sy + 10 * z), width)
        pygame.draw.line(self.screen, paint, (sx - 13 * z, sy + 10 * z), (sx + 13 * z, sy - 10 * z), width)

    def draw_powerline(self, x, y, sx, sy, preview=None):
        z = self.camera.zoom
        pole_top = (sx, sy - 18 * z)
        pygame.draw.line(self.screen, (73, 52, 37), (sx, sy + 4 * z), pole_top, max(2, int(3 * z)))
        connected = False
        for nx, ny in self.city.neighbors4(x, y):
            if self.preview_build_kind(nx, ny, preview) == BuildKind.POWERLINE:
                ex, ey = self.camera.world_to_screen((x + nx) / 2, (y + ny) / 2)
                ey -= (self.tile_lift(x, y) + self.tile_lift(nx, ny)) / 2
                end = (ex, ey - 18 * z)
                pygame.draw.line(self.screen, (65, 52, 44), pole_top, end, max(2, int(3 * z)))
                pygame.draw.line(self.screen, (235, 205, 75), (pole_top[0], pole_top[1] - 4 * z), (end[0], end[1] - 4 * z), max(1, int(2 * z)))
                connected = True
        if not connected:
            pygame.draw.line(self.screen, (65, 52, 44), (sx - 10 * z, sy + 3 * z), (sx + 10 * z, sy - 3 * z), max(2, int(3 * z)))
            pygame.draw.line(self.screen, (235, 205, 75), (sx - 12 * z, sy - 3 * z), (sx + 12 * z, sy - 9 * z), max(1, int(2 * z)))

    def draw_pipe(self, x, y, sx, sy, preview=None):
        z = self.camera.zoom
        connected = False
        for nx, ny in self.city.neighbors4(x, y):
            if self.preview_has_pipe(nx, ny, preview):
                ex, ey = self.camera.world_to_screen((x + nx) / 2, (y + ny) / 2)
                ey -= (self.tile_lift(x, y) + self.tile_lift(nx, ny)) / 2
                pygame.draw.line(self.screen, (30, 82, 128), (sx, sy), (ex, ey), max(5, int(7 * z)))
                pygame.draw.line(self.screen, (89, 174, 233), (sx, sy), (ex, ey), max(2, int(3 * z)))
                connected = True
        if not connected:
            pygame.draw.line(self.screen, (30, 82, 128), (sx - 18 * z, sy), (sx + 18 * z, sy), max(5, int(7 * z)))
            pygame.draw.line(self.screen, (89, 174, 233), (sx - 18 * z, sy), (sx + 18 * z, sy), max(2, int(3 * z)))
        pygame.draw.circle(self.screen, (89, 174, 233), (int(sx), int(sy)), max(3, int(4 * z)))

    def draw_zone(self, tile, x, y, sx, sy):
        z = self.camera.zoom
        palette = {
            BuildKind.RES: ((95, 177, 111), (56, 110, 82)),
            BuildKind.COM: ((87, 139, 217), (52, 82, 141)),
            BuildKind.IND: ((205, 154, 83), (124, 94, 62)),
            BuildKind.GARBAGE: ((104, 116, 89), (67, 75, 58)),
        }
        top, side = palette[tile.build]
        if not tile.powered or not tile.watered or not tile.road_access:
            top = tuple(int(c * 0.68) for c in top)
            side = tuple(int(c * 0.68) for c in side)
        if tile.build == BuildKind.RES and tile.level == 2:
            self.draw_residential_house(x, y, sx, sy, top)
            return
        if tile.build == BuildKind.COM and tile.level == 2:
            self.draw_commercial_shop(x, y, sx, sy, top)
            return
        if tile.build == BuildKind.IND and tile.level == 2:
            self.draw_industrial_workshop(x, y, sx, sy, top)
            return
        if tile.build == BuildKind.GARBAGE:
            self.draw_garbage_zone(x, y, sx, sy, top)
            return
        if tile.level <= 1:
            self.draw_zone_lot(x, y, sx, sy, top)
            return
        floors = max(1, tile.level)
        w = (18 + floors * 3) * z
        h = (12 + floors * 9) * z
        base_y = sy - 3 * z
        front = [(sx - w, base_y), (sx, base_y + w * 0.42), (sx, base_y + w * 0.42 - h), (sx - w, base_y - h)]
        right = [(sx, base_y + w * 0.42), (sx + w, base_y), (sx + w, base_y - h), (sx, base_y + w * 0.42 - h)]
        roof = [(sx - w, base_y - h), (sx, base_y - h - w * 0.42), (sx + w, base_y - h), (sx, base_y + w * 0.42 - h)]
        pygame.draw.polygon(self.screen, side, front)
        pygame.draw.polygon(self.screen, darken(side, 0.8), right)
        pygame.draw.polygon(self.screen, top, roof)
        pygame.draw.polygon(self.screen, (30, 35, 38), front, 1)
        pygame.draw.polygon(self.screen, (30, 35, 38), right, 1)
        if tile.level >= 3:
            for i in range(tile.level):
                pygame.draw.rect(self.screen, (226, 232, 174), (sx - w * 0.65, base_y - h + (i + 1) * 7 * z, 4 * z, 3 * z))
                pygame.draw.rect(self.screen, (202, 225, 246), (sx + w * 0.28, base_y - h + (i + 1) * 7 * z, 4 * z, 3 * z))

    def draw_zone_lot(self, x, y, sx, sy, color):
        return shapes.draw_zone_lot(self, x, y, sx, sy, color)

    def draw_residential_house(self, x, y, sx, sy, lot_color):
        return shapes.draw_residential_house(self, x, y, sx, sy, lot_color)

    def draw_commercial_shop(self, x, y, sx, sy, lot_color):
        return shapes.draw_commercial_shop(self, x, y, sx, sy, lot_color)

    def draw_industrial_workshop(self, x, y, sx, sy, lot_color):
        return shapes.draw_industrial_workshop(self, x, y, sx, sy, lot_color)

    def garbage_visual_fill_ratio(self, x, y):
        tile = self.city.tiles[x][y]
        if tile.build != BuildKind.GARBAGE:
            return 0.0
        return clamp(tile.garbage_fill / GARBAGE_ZONE_CAPACITY, 0.0, 1.0)

    def draw_garbage_zone(self, x, y, sx, sy, lot_color):
        return shapes.draw_garbage_zone(self, x, y, sx, sy, lot_color, self.garbage_visual_fill_ratio(x, y))

    def draw_park(self, x, y, sx, sy):
        z = self.camera.zoom
        grass = self.iso_rect_poly(x, y, 1, 1, 0.08, base_lift=self.tile_lift(x, y))
        pygame.draw.polygon(self.screen, (73, 156, 86), grass)
        pygame.draw.polygon(self.screen, (42, 104, 58), grass, max(1, int(2 * z)))

        west = shapes.lerp_point(grass[3], grass[0], 0.52)
        east = shapes.lerp_point(grass[1], grass[2], 0.58)
        north = shapes.lerp_point(grass[0], grass[1], 0.55)
        center = (sx, sy - 2 * z)
        path_color = (219, 202, 143)
        path_shadow = (151, 132, 91)
        for a, b in ((west, center), (center, east), (north, center)):
            pygame.draw.line(self.screen, path_shadow, a, b, max(3, int(5 * z)))
            pygame.draw.line(self.screen, path_color, a, b, max(2, int(3 * z)))

        pond = pygame.Rect(0, 0, int(20 * z), int(9 * z))
        pond.center = (sx + 7 * z, sy + 3 * z)
        pygame.draw.ellipse(self.screen, (52, 132, 154), pond)
        pygame.draw.ellipse(self.screen, (132, 197, 203), pond.inflate(-5 * z, -3 * z), max(1, int(z)))

        bench_a = (sx - 14 * z, sy + 2 * z)
        bench_b = (sx - 4 * z, sy - 1 * z)
        pygame.draw.line(self.screen, (94, 62, 43), bench_a, bench_b, max(2, int(3 * z)))
        pygame.draw.line(self.screen, (58, 45, 38), (bench_a[0], bench_a[1] + 3 * z), (bench_b[0], bench_b[1] + 3 * z), max(1, int(2 * z)))

        for px, py, color in [(-6, -8, (225, 92, 108)), (0, -10, (248, 220, 95)), (6, -8, (214, 125, 218))]:
            pygame.draw.circle(self.screen, color, (int(sx + px * z), int(sy + py * z)), max(1, int(2 * z)))
        for ox, oy in [(-13, -5), (9, -8), (15, 0), (-2, 6)]:
            self.draw_tree(sx + ox * z, sy + oy * z)

    def draw_large_park(self, x, y, fw, fh):
        return shapes.draw_large_park(self, x, y, fw, fh)

    def iso_rect_poly(self, x, y, fw, fh, inset=0.0, y_offset=0.0, base_lift=0.0):
        x0 = x - 0.5 + inset
        y0 = y - 0.5 + inset
        x1 = x + fw - 0.5 - inset
        y1 = y + fh - 0.5 - inset
        offset = y_offset - base_lift
        return [
            offset_point(self.camera.world_to_screen(x0, y0), 0, offset),
            offset_point(self.camera.world_to_screen(x1, y0), 0, offset),
            offset_point(self.camera.world_to_screen(x1, y1), 0, offset),
            offset_point(self.camera.world_to_screen(x0, y1), 0, offset),
        ]

    def draw_iso_prism(self, x, y, fw, fh, height, top_color, side_color, inset=0.08, base_lift=None):
        if base_lift is None:
            base_lift = self.tile_lift(x, y)
        base = self.iso_rect_poly(x, y, fw, fh, inset, base_lift=base_lift)
        roof = self.iso_rect_poly(x, y, fw, fh, inset, -height, base_lift)
        back = [base[0], base[1], roof[1], roof[0]]
        right = [base[1], base[2], roof[2], roof[1]]
        front = [base[2], base[3], roof[3], roof[2]]
        left = [base[3], base[0], roof[0], roof[3]]
        pygame.draw.polygon(self.screen, darken(side_color, 0.80), back)
        pygame.draw.polygon(self.screen, darken(side_color, 0.72), left)
        pygame.draw.polygon(self.screen, side_color, right)
        pygame.draw.polygon(self.screen, darken(side_color, 0.86), front)
        pygame.draw.polygon(self.screen, top_color, roof)
        outline = (30, 35, 38)
        pygame.draw.polygon(self.screen, outline, back, 1)
        pygame.draw.polygon(self.screen, outline, right, 1)
        pygame.draw.polygon(self.screen, outline, front, 1)
        pygame.draw.polygon(self.screen, outline, roof, 1)
        cx = sum(p[0] for p in roof) / len(roof)
        cy = sum(p[1] for p in roof) / len(roof)
        return cx, cy, roof, base

    def draw_service(self, tile, x, y, fw=1, fh=1):
        z = self.camera.zoom
        colors = {
            BuildKind.POLICE: ((71, 99, 180), "P"),
            BuildKind.FIRE: ((198, 61, 55), "F"),
            BuildKind.LARGE_PARK: ((74, 153, 86), "P"),
            BuildKind.CLINIC: ((235, 235, 239), "+"),
            BuildKind.SCHOOL: ((193, 175, 94), "S"),
            BuildKind.LIBRARY: ((154, 118, 83), "L"),
            BuildKind.STADIUM: ((94, 142, 96), "S"),
            BuildKind.RAIL_STATION: ((118, 102, 82), "R"),
            BuildKind.SEAPORT: ((82, 116, 126), "P"),
            BuildKind.AIRPORT: ((90, 103, 113), "A"),
            BuildKind.WATER_PUMP: ((78, 145, 173), "W"),
            BuildKind.COAL: ((78, 75, 70), "C"),
            BuildKind.SOLAR: ((75, 154, 199), "*"),
        }
        color, label = colors[tile.build]
        h = 27 * z
        if tile.build == BuildKind.COAL:
            h = 42 * z
        elif tile.build == BuildKind.SOLAR:
            h = 10 * z
        elif tile.build == BuildKind.POLICE:
            self.draw_police_station(x, y, fw, fh)
            return
        elif tile.build == BuildKind.FIRE:
            self.draw_fire_station(x, y, fw, fh)
            return
        elif tile.build == BuildKind.LARGE_PARK:
            self.draw_large_park(x, y, fw, fh)
            return
        elif tile.build == BuildKind.CLINIC:
            self.draw_clinic(x, y, fw, fh)
            return
        elif tile.build == BuildKind.SCHOOL:
            self.draw_school(x, y, fw, fh)
            return
        elif tile.build == BuildKind.LIBRARY:
            self.draw_library(x, y, fw, fh)
            return
        elif tile.build == BuildKind.STADIUM:
            self.draw_stadium(x, y, fw, fh)
            return
        elif tile.build == BuildKind.RAIL_STATION:
            self.draw_rail_station(x, y, fw, fh)
            return
        elif tile.build == BuildKind.SEAPORT:
            self.draw_seaport(x, y, fw, fh)
            return
        elif tile.build == BuildKind.AIRPORT:
            self.draw_airport(x, y, fw, fh)
            return
        elif tile.build == BuildKind.WATER_PUMP:
            self.draw_water_pump(x, y, fw, fh)
            return
        cx, cy, roof, _ = self.draw_iso_prism(x, y, fw, fh, h, color, darken(color, 0.78))
        if tile.build == BuildKind.COAL:
            self.draw_smokestack(x + fw - 0.82, y + 0.15, h, 48 * z)
            self.draw_smokestack(x + 0.55, y + fh - 0.62, h, 35 * z)
        elif tile.build == BuildKind.SOLAR:
            panel = self.iso_rect_poly(x, y, fw, fh, 0.18, -h - 3 * z, self.tile_lift(x, y))
            pygame.draw.polygon(self.screen, (35, 76, 112), panel)
            pygame.draw.polygon(self.screen, (103, 176, 222), panel, 1)
            for i in range(1, fw + fh + 1):
                a = i / (fw + fh + 1)
                p1 = lerp_point(panel[0], panel[1], a)
                p2 = lerp_point(panel[3], panel[2], a)
                pygame.draw.line(self.screen, (75, 135, 178), p1, p2, max(1, int(z)))
        else:
            surf = self.small.render(label, True, (20, 24, 28))
            self.screen.blit(surf, surf.get_rect(center=(cx, cy)))

    def draw_police_station(self, x, y, fw, fh):
        return shapes.draw_police_station(self, x, y, fw, fh)

    def draw_fire_station(self, x, y, fw, fh):
        return shapes.draw_fire_station(self, x, y, fw, fh)

    def draw_school(self, x, y, fw, fh):
        return shapes.draw_school(self, x, y, fw, fh)

    def draw_clinic(self, x, y, fw, fh):
        return shapes.draw_clinic(self, x, y, fw, fh)

    def draw_library(self, x, y, fw, fh):
        return shapes.draw_library(self, x, y, fw, fh)

    def draw_rail_station(self, x, y, fw, fh):
        return shapes.draw_rail_station(self, x, y, fw, fh)

    def draw_stadium(self, x, y, fw, fh):
        return shapes.draw_stadium(self, x, y, fw, fh)

    def draw_seaport(self, x, y, fw, fh):
        return shapes.draw_seaport(self, x, y, fw, fh)

    def draw_airport(self, x, y, fw, fh):
        return shapes.draw_airport(self, x, y, fw, fh)

    def draw_water_pump(self, x, y, fw, fh):
        return shapes.draw_water_pump(self, x, y, fw, fh)

    def draw_smokestack(self, wx, wy, roof_height, stack_height):
        return shapes.draw_smokestack(self, wx, wy, roof_height, stack_height)

    def draw_fire(self, sx, sy):
        z = self.camera.zoom
        pygame.draw.polygon(self.screen, (126, 83, 60), self.tile_poly(sx, sy))
        for i in range(5):
            ox = (i - 2) * 5 * z
            flame = [(sx + ox, sy - 2 * z), (sx + ox + 5 * z, sy - 22 * z - random.random() * 8 * z), (sx + ox + 10 * z, sy - 2 * z)]
            pygame.draw.polygon(self.screen, (238, 74, 43), flame)
            pygame.draw.polygon(self.screen, (255, 189, 61), [(p[0], p[1] + 4 * z) for p in flame])


def darken(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color)


def offset_point(point, dx, dy):
    return point[0] + dx, point[1] + dy


def lerp_point(a, b, t):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def meter_color(value):
    if value >= 70:
        return GOOD
    if value >= 42:
        return WARN
    return BAD


def heat_color(value):
    ratio = clamp(value / 100.0, 0.0, 1.0)
    if ratio < 0.5:
        t = ratio * 2
        return (
            int(BAD[0] + (WARN[0] - BAD[0]) * t),
            int(BAD[1] + (WARN[1] - BAD[1]) * t),
            int(BAD[2] + (WARN[2] - BAD[2]) * t),
        )
    t = (ratio - 0.5) * 2
    return (
        int(WARN[0] + (GOOD[0] - WARN[0]) * t),
        int(WARN[1] + (GOOD[1] - WARN[1]) * t),
        int(WARN[2] + (GOOD[2] - WARN[2]) * t),
    )


def risk_color(value):
    return heat_color(100 - value)



from camera import Camera
from ui import UI

def main():
    Game().run()


if __name__ == "__main__":
    main()
