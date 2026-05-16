import json
import math
import random
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import pygame

import shapes


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


COST = {
    Tool.ROAD: 8,
    Tool.BRIDGE: 35,
    Tool.RAIL: 12,
    Tool.RAIL_BRIDGE: 45,
    Tool.RAIL_CROSSING: 20,
    Tool.RAIL_STATION: 950,
    Tool.SEAPORT: 1600,
    Tool.AIRPORT: 2200,
    Tool.RES: 20,
    Tool.COM: 24,
    Tool.IND: 22,
    Tool.GARBAGE: 14,
    Tool.POWERLINE: 6,
    Tool.WATER: 7,
    Tool.WATER_PUMP: 350,
    Tool.PARK: 60,
    Tool.LARGE_PARK: 320,
    Tool.POLICE: 450,
    Tool.FIRE: 420,
    Tool.CLINIC: 520,
    Tool.SCHOOL: 650,
    Tool.LIBRARY: 380,
    Tool.STADIUM: 1800,
    Tool.COAL: 1400,
    Tool.SOLAR: 900,
    Tool.BULLDOZE: 3,
}


MAINTENANCE = {
    BuildKind.ROAD: 0.02,
    BuildKind.BRIDGE: 0.08,
    BuildKind.RAIL: 0.03,
    BuildKind.RAIL_BRIDGE: 0.10,
    BuildKind.RAIL_CROSSING: 0.05,
    BuildKind.RAIL_STATION: 2.8,
    BuildKind.SEAPORT: 3.6,
    BuildKind.AIRPORT: 5.2,
    BuildKind.POWERLINE: 0.01,
    BuildKind.WATER: 0.01,
    BuildKind.WATER_PUMP: 0.8,
    BuildKind.PARK: 0.18,
    BuildKind.LARGE_PARK: 0.55,
    BuildKind.POLICE: 2.4,
    BuildKind.FIRE: 2.2,
    BuildKind.CLINIC: 2.8,
    BuildKind.SCHOOL: 3.2,
    BuildKind.LIBRARY: 1.4,
    BuildKind.STADIUM: 4.5,
    BuildKind.COAL: 5.0,
    BuildKind.SOLAR: 1.2,
}


ZONE_KINDS = {BuildKind.RES, BuildKind.COM, BuildKind.IND, BuildKind.GARBAGE}
ROAD_KINDS = {BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL_CROSSING}
RAIL_KINDS = {BuildKind.RAIL, BuildKind.RAIL_BRIDGE, BuildKind.RAIL_CROSSING}
RAIL_CONNECT_KINDS = RAIL_KINDS | {BuildKind.RAIL_STATION}
NETWORK_KINDS = {BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL_CROSSING, BuildKind.POWERLINE, BuildKind.WATER}
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
    age: int = 0
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
        self.messages = [Message("New charter approved. Build roads, zones, power, and water.", ACCENT, 9)]
        self.graphs = {"population": [], "money": [], "mood": [], "pollution": []}

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
            "age": tile.age,
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
        city.tiles = [[cls.tile_from_dict(data["tiles"][x][y]) for y in range(city.height)] for x in range(city.width)]
        city.messages = []
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
            age=data.get("age", 0),
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
                target.age = 0
                target.trees = False
                target.fire_timer = 0
                target.origin = (x, y)
                target.footprint = footprint
                if kind in ZONE_KINDS:
                    target.level = 1
            self.add_message(f"Built {tool.value} for ${price}.", TEXT, 3)
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
            tile.age = 0
            tile.trees = False
            tile.fire_timer = 0
            tile.origin = (x, y)
            tile.footprint = FOOTPRINTS[kind]
            built += 1
        self.add_message(f"Built {built} path tiles for ${total_cost}.", TEXT, 4)
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
            tile.age = 0
            tile.trees = False
            tile.fire_timer = 0
            tile.origin = (x, y)
            tile.footprint = FOOTPRINTS[kind]
            built += 1
        self.add_message(f"Zoned {built} tiles for ${total_cost}.", TEXT, 4)
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
                if b == BuildKind.COAL:
                    power_sources.append((x, y, 450))
                elif b == BuildKind.SOLAR:
                    power_sources.append((x, y, 110))
                elif b == BuildKind.WATER_PUMP and self.pump_has_water_neighbor(x, y):
                    water_sources.append((x, y, 90))

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
                pollution = 0.0
                land = 45.0 + tile.terrain * 3.0
                crime = 50.0
                health = 40.0
                education = 35.0
                fire_risk = 40.0
                if tile.water:
                    land += 16.0
                if tile.trees:
                    land += 4.0
                for nx, ny, d in self.neighbors_radius(x, y, 8):
                    other = self.tiles[nx][ny]
                    if other.build in SERVICE_KINDS and not other.is_origin(nx, ny):
                        continue
                    weight = max(0.0, (8 - d) / 8)
                    if other.build == BuildKind.IND:
                        pollution += (8 + other.level * 10) * weight
                        land -= (5 + other.level * 4) * weight
                    elif other.build == BuildKind.GARBAGE:
                        pollution += 22 * weight
                        land -= 18 * weight
                        health -= 8 * weight
                    elif other.build == BuildKind.COAL:
                        pollution += 35 * weight
                        land -= 15 * weight
                    elif other.build == BuildKind.PARK:
                        land += 12 * weight
                        health += 8 * weight
                    elif other.build == BuildKind.LARGE_PARK:
                        land += 24 * weight
                        health += 16 * weight
                    elif other.build == BuildKind.POLICE:
                        crime -= 34 * weight
                    elif other.build == BuildKind.FIRE:
                        fire_risk -= 42 * weight
                    elif other.build == BuildKind.CLINIC:
                        health += 45 * weight
                    elif other.build == BuildKind.SCHOOL:
                        education += 42 * weight
                    elif other.build == BuildKind.LIBRARY:
                        education += 24 * weight
                        land += 5 * weight
                    elif other.build == BuildKind.STADIUM:
                        land += 14 * weight
                        crime += 3 * weight
                    elif other.build == BuildKind.RAIL_STATION:
                        land += 9 * weight
                        pollution -= 2 * weight
                    elif other.build == BuildKind.SEAPORT:
                        land += 8 * weight
                        pollution += 4 * weight
                    elif other.build == BuildKind.AIRPORT:
                        land += 10 * weight
                        pollution += 6 * weight
                    elif other.build in ROAD_KINDS:
                        land += 1.5 * weight
                tile.pollution = clamp(pollution, 0, 100)
                tile.land_value = clamp(land - pollution * 0.3, 0, 100)
                tile.crime = clamp(crime + max(0, tile.level - 2) * 5, 0, 100)
                tile.health = clamp(health - pollution * 0.25, 0, 100)
                tile.education = clamp(education, 0, 100)
                tile.fire_risk = clamp(fire_risk + pollution * 0.15 + tile.level * 6, 0, 100)

    def grow_city(self):
        self.calculate_demand()
        zones = []
        for x in range(self.width):
            for y in range(self.height):
                t = self.tiles[x][y]
                if t.build in {BuildKind.RES, BuildKind.COM, BuildKind.IND}:
                    zones.append((x, y, t))
        random.shuffle(zones)
        for x, y, t in zones[: max(12, len(zones) // 3)]:
            demand = {
                BuildKind.RES: self.stats.demand_r,
                BuildKind.COM: self.stats.demand_c,
                BuildKind.IND: self.stats.demand_i,
            }[t.build]
            score = self.zone_score(t)
            grow_chance = max(0.0, (demand + score - 120) / 260.0)
            shrink_chance = max(0.0, (42 - demand + (38 - score)) / 220.0)
            grow_chance += self.zone_growth_bonus(t.build)
            grow_chance -= self.tax_growth_penalty()
            if t.powered and t.watered and t.road_access and random.random() < grow_chance:
                if t.level < 5:
                    t.level += 1
                    t.age = 0
            elif random.random() < shrink_chance:
                t.level = max(1, t.level - 1)
            t.age += 1

        if self.disasters_enabled and random.random() < 0.002 + self.stats.pollution / 70000:
            self.trigger_fire()

    def zone_growth_bonus(self, build):
        return {
            BuildKind.RES: 0.010,
            BuildKind.COM: 0.008,
            BuildKind.IND: 0.012,
        }.get(build, 0.0)

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
        population = jobs = shops = 0
        power_used = water_used = 0
        traffic_tiles = 0
        pollution_sum = 0.0
        built = 0
        for x in range(self.width):
            for y in range(self.height):
                t = self.tiles[x][y]
                if t.build == BuildKind.RES:
                    population += t.level * t.level * 12
                    power_used += t.level * 4
                    water_used += t.level * 5
                    built += 1
                elif t.build == BuildKind.COM:
                    shops += t.level * t.level * 8
                    jobs += t.level * t.level * 5
                    power_used += t.level * 5
                    water_used += t.level * 3
                    built += 1
                elif t.build == BuildKind.IND:
                    jobs += t.level * t.level * 14
                    power_used += t.level * 8
                    water_used += t.level * 4
                    built += 1
                elif t.build == BuildKind.GARBAGE:
                    jobs += 1
                    power_used += 1
                    built += 1
                elif t.build in SERVICE_KINDS:
                    if not t.is_origin(x, y):
                        continue
                    power_used += 8 if t.build not in {BuildKind.COAL, BuildKind.SOLAR} else 0
                    water_used += 4 if t.build in {BuildKind.POLICE, BuildKind.FIRE, BuildKind.CLINIC, BuildKind.SCHOOL, BuildKind.LIBRARY, BuildKind.RAIL_STATION, BuildKind.STADIUM, BuildKind.SEAPORT, BuildKind.AIRPORT, BuildKind.WATER_PUMP} else 0
                if t.build in ROAD_KINDS:
                    traffic_tiles += self.road_traffic_neighbors(x, y)
                pollution_sum += t.pollution

        unemployment = max(0.0, (population * 0.42 - jobs) / max(1.0, population * 0.42))
        worker_gap = max(0.0, (jobs - population * 0.42) / max(1.0, jobs))
        shop_gap = max(0.0, (population * 0.18 - shops) / max(1.0, population * 0.18))
        infrastructure_penalty = 0
        if power_used > self.stats.power_cap:
            infrastructure_penalty += 25
        if water_used > self.stats.water_cap:
            infrastructure_penalty += 16
        tax_penalty = max(0.0, self.tax_rate - 7.0) * 5.5
        cash_pressure = -8 if self.money < 0 else 0
        self.stats.population = int(population)
        self.stats.jobs = int(jobs)
        self.stats.shops = int(shops)
        self.stats.power_used = int(power_used)
        self.stats.water_used = int(water_used)
        self.stats.unemployment = unemployment
        self.stats.pollution = pollution_sum / max(1, self.width * self.height)
        self.stats.traffic = min(100, traffic_tiles * 1.7)
        self.stats.demand_r = clamp(36 + worker_gap * 55 - unemployment * 60 - tax_penalty * 1.1 - infrastructure_penalty * 1.15 + cash_pressure, -80, 100)
        self.stats.demand_c = clamp(28 + shop_gap * 62 + population / 800 - tax_penalty * 0.95 - infrastructure_penalty * 1.1, -80, 100)
        self.stats.demand_i = clamp(34 + unemployment * 55 - population / 1800 - tax_penalty * 0.75 - infrastructure_penalty, -80, 100)
        service_score = self.average_services()
        utility_score = 100
        if power_used > self.stats.power_cap:
            utility_score -= 32
        if water_used > self.stats.water_cap:
            utility_score -= 22
        self.stats.mood = clamp(
            55 + service_score * 0.24 - unemployment * 32 - self.stats.pollution * 0.35 - max(0, self.tax_rate - 8) * 4 + utility_score * 0.18,
            0,
            100,
        )

    def road_traffic_neighbors(self, x, y):
        return sum(1 for nx, ny in self.neighbors4(x, y) if self.tiles[nx][ny].build in ZONE_KINDS)

    def road_congestion(self, x, y):
        if self.tiles[x][y].build not in ROAD_KINDS:
            return 0
        return min(100, self.road_traffic_neighbors(x, y) * 1.7)

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
                else:
                    for tx, ty in self.building_tiles(x, y):
                        self.tiles[tx][ty].build = BuildKind.RUBBLE
                        self.tiles[tx][ty].fire_timer = 0
                    self.add_message("A building burned down.", BAD, 5)
                    for tx, ty in self.building_tiles(x, y):
                        for nx, ny in self.neighbors4(tx, ty):
                            nt = self.tiles[nx][ny]
                            if nt.build not in {BuildKind.EMPTY, BuildKind.ROAD, BuildKind.BRIDGE, BuildKind.RAIL, BuildKind.RAIL_BRIDGE, BuildKind.RAIL_CROSSING, BuildKind.WATER, BuildKind.POWERLINE, BuildKind.BURNING, BuildKind.RUBBLE} and random.random() < 0.08:
                                self.ignite_building(nx, ny)


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


class Camera:
    def __init__(self):
        self.x = SCREEN_W * 0.46
        self.y = 116
        self.zoom = 1.0
        self.rotation = 0

    @property
    def tile_w(self):
        return BASE_TILE_W * self.zoom

    @property
    def tile_h(self):
        return BASE_TILE_H * self.zoom

    def rotate_world(self, tx, ty):
        if self.rotation == 1:
            return ty, MAP_W - 1 - tx
        if self.rotation == 2:
            return MAP_W - 1 - tx, MAP_H - 1 - ty
        if self.rotation == 3:
            return MAP_H - 1 - ty, tx
        return tx, ty

    def unrotate_world(self, rx, ry):
        if self.rotation == 1:
            return MAP_W - 1 - ry, rx
        if self.rotation == 2:
            return MAP_W - 1 - rx, MAP_H - 1 - ry
        if self.rotation == 3:
            return ry, MAP_H - 1 - rx
        return rx, ry

    def iso_offset(self, tx, ty):
        rx, ry = self.rotate_world(tx, ty)
        return (rx - ry) * self.tile_w / 2, (rx + ry) * self.tile_h / 2

    def world_to_screen(self, tx, ty, z=0):
        ox, oy = self.iso_offset(tx, ty)
        sx = ox + self.x
        sy = oy + self.y - z * 7 * self.zoom
        return sx, sy

    def screen_to_world(self, sx, sy):
        sx -= self.x
        sy -= self.y
        rx = sy / self.tile_h + sx / self.tile_w
        ry = sy / self.tile_h - sx / self.tile_w
        tx, ty = self.unrotate_world(rx, ry)
        return int(math.floor(tx + 0.5)), int(math.floor(ty + 0.5))

    def center_on(self, tx, ty, screen_x, screen_y):
        iso_x, iso_y = self.iso_offset(tx, ty)
        self.x = screen_x - iso_x
        self.y = screen_y - iso_y

    def rotate(self, turns, screen_x, screen_y):
        tx, ty = self.screen_to_world(screen_x, screen_y)
        self.rotation = (self.rotation + turns) % 4
        self.center_on(tx, ty, screen_x, screen_y)


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
                self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
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

    def handle_keydown(self, key):
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
        return self.ui.map_mode in {MapMode.TRAFFIC, MapMode.LAND_VALUE}

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
                return heat_color(self.city.road_congestion(x, y))
            if tile.build in ZONE_KINDS:
                return (76, 70, 62)
            return None
        if self.ui.map_mode == MapMode.LAND_VALUE and tile.build in ZONE_KINDS:
            return heat_color(tile.land_value)
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
        if self.tool in TOOL_BUILD:
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

    def draw_garbage_zone(self, x, y, sx, sy, lot_color):
        return shapes.draw_garbage_zone(self, x, y, sx, sy, lot_color)

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


class UI:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.menu_buttons = []
        self.time_buttons = []
        self.build_menus = []
        self.open_menu = None
        self.game_menu_open = False
        self.map_menu_open = False
        self.map_mode = MapMode.STANDARD
        self.budget_open = False
        self.make_buttons()

    def make_buttons(self):
        x = SCREEN_W - SIDEBAR_W + 14
        y = TOPBAR_H + 28
        self.build_menus = [
            ("Transport", [("Road", Tool.ROAD, "1"), ("Rail", Tool.RAIL, "B"), ("Railway Station", Tool.RAIL_STATION, ""), ("Seaport", Tool.SEAPORT, ""), ("Airport", Tool.AIRPORT, "")]),
            ("Zones", [("Res", Tool.RES, "2"), ("Com", Tool.COM, "3"), ("Ind", Tool.IND, "4"), ("Garbage", Tool.GARBAGE, "")]),
            ("Utilities", [("Power Line", Tool.POWERLINE, "5"), ("Pipes", Tool.WATER, "6"), ("Pump", Tool.WATER_PUMP, ""), ("Solar", Tool.SOLAR, "P"), ("Coal", Tool.COAL, "=")]),
            ("Services", [("Park", Tool.PARK, "7"), ("Large Park", Tool.LARGE_PARK, ""), ("Police", Tool.POLICE, "8"), ("Fire", Tool.FIRE, "9"), ("Clinic", Tool.CLINIC, "0"), ("School", Tool.SCHOOL, "-"), ("Library", Tool.LIBRARY, ""), ("Stadium", Tool.STADIUM, "")]),
            ("Tools", [("Doze", Tool.BULLDOZE, "X"), ("Info", Tool.INSPECT, "I")]),
        ]
        self.menu_buttons = []
        for i, (label, _) in enumerate(self.build_menus):
            self.menu_buttons.append(Button((x, y + i * 40, 260, 32), label, menu=i))
        self.buttons = self.menu_buttons

        tx = 716
        self.time_buttons = [
            Button((tx, 8, 38, 30), "||", hotkey="Space"),
            Button((tx + 42, 8, 38, 30), ">", hotkey="0.5x"),
            Button((tx + 84, 8, 42, 30), ">>", hotkey="1.5x"),
            Button((tx + 130, 8, 46, 30), ">>>", hotkey="2.5x"),
        ]

    def menu_tools(self, menu_index):
        return [tool for _, tool, _ in self.build_menus[menu_index][1]]

    def menu_item_buttons(self, menu_index):
        menu_button = self.menu_buttons[menu_index]
        items = self.build_menus[menu_index][1]
        width = 172
        x = SCREEN_W - SIDEBAR_W - width - 8
        y = menu_button.rect.y
        return [
            Button((x, y + i * 36, width, 32), label, tool, hotkey)
            for i, (label, tool, hotkey) in enumerate(items)
        ]

    def menu_popup_rect(self, menu_index):
        buttons = self.menu_item_buttons(menu_index)
        rect = buttons[0].rect.copy()
        for b in buttons[1:]:
            rect.union_ip(b.rect)
        rect.inflate_ip(10, 10)
        return rect

    def minimap_rect(self):
        return pygame.Rect(SCREEN_W - SIDEBAR_W + 16, SCREEN_H - 115, 112, 112)

    def minimap_to_tile(self, mx, my):
        rect = self.minimap_rect()
        c = self.game.city
        tx = int((mx - rect.x) / rect.width * c.width)
        ty = int((my - rect.y) / rect.height * c.height)
        return int(clamp(tx, 0, c.width - 1)), int(clamp(ty, 0, c.height - 1))

    def center_camera_on_tile(self, tx, ty):
        view_w = SCREEN_W - SIDEBAR_W
        view_h = SCREEN_H - TOPBAR_H
        self.game.camera.center_on(tx, ty, view_w / 2, TOPBAR_H + view_h / 2)

    def handle_click(self, mx, my):
        if self.game_menu_open:
            for action, rect in self.game_menu_items():
                if rect.collidepoint(mx, my):
                    self.game_menu_open = False
                    if action == "save":
                        self.game.save_game()
                    elif action == "load":
                        self.game.load_game()
                    elif action == "disasters":
                        c = self.game.city
                        c.disasters_enabled = not c.disasters_enabled
                        state = "on" if c.disasters_enabled else "off"
                        c.add_message(f"Disasters turned {state}.", TEXT, 4)
                    elif action == "quit":
                        self.game.running = False
                    return True
            if self.game_menu_rect().collidepoint(mx, my):
                return True
            self.game_menu_open = False
            return True
        if self.map_menu_open:
            for mode, rect in self.map_menu_items():
                if rect.collidepoint(mx, my):
                    self.map_mode = mode
                    self.map_menu_open = False
                    return True
            if self.map_menu_rect().collidepoint(mx, my):
                return True
            self.map_menu_open = False
            return True
        if my < TOPBAR_H:
            if self.game_menu_button_rect().collidepoint(mx, my):
                self.game_menu_open = not self.game_menu_open
                self.open_menu = None
                self.map_menu_open = False
                return True
            self.game_menu_open = False
            for i, b in enumerate(self.time_buttons):
                if b.rect.collidepoint(mx, my):
                    c = self.game.city
                    if i == 0:
                        c.paused = True
                    elif i == 1:
                        c.paused = False
                        c.sim_speed = PLAY_SPEED
                    elif i == 2:
                        c.paused = False
                        c.sim_speed = FAST_SPEED
                    elif i == 3:
                        c.paused = False
                        c.sim_speed = FASTER_SPEED
                    return True
            return True

        if self.game.city.selected and self.inspector_popup_rect().collidepoint(mx, my):
            if self.inspector_close_rect().collidepoint(mx, my):
                self.game.city.selected = None
            return True
        if self.budget_open and self.budget_popup_rect().collidepoint(mx, my):
            if self.budget_close_rect().collidepoint(mx, my):
                self.budget_open = False
            elif self.tax_slider_hit_rect().collidepoint(mx, my):
                self.set_tax_from_slider(mx)
                self.game.dragging_tax = True
            return True

        if self.open_menu is not None:
            for b in self.menu_item_buttons(self.open_menu):
                if b.rect.collidepoint(mx, my):
                    self.game.tool = b.tool
                    self.open_menu = None
                    return True
            if self.menu_popup_rect(self.open_menu).collidepoint(mx, my):
                return True
            if mx < SCREEN_W - SIDEBAR_W:
                self.open_menu = None
                return True

        for b in self.menu_buttons:
            if b.rect.collidepoint(mx, my):
                self.game_menu_open = False
                self.map_menu_open = False
                self.open_menu = None if self.open_menu == b.menu else b.menu
                return True
        if self.map_title_rect().collidepoint(mx, my):
            self.game_menu_open = False
            self.open_menu = None
            self.map_menu_open = not self.map_menu_open
            return True
        if self.minimap_rect().collidepoint(mx, my):
            tx, ty = self.minimap_to_tile(mx, my)
            self.center_camera_on_tile(tx, ty)
            self.open_menu = None
            self.map_menu_open = False
            return True
        if self.budget_button_rect().collidepoint(mx, my):
            self.game_menu_open = False
            self.map_menu_open = False
            self.budget_open = not self.budget_open
            return True
        if mx >= SCREEN_W - SIDEBAR_W:
            self.open_menu = None
            self.map_menu_open = False
            return True
        return False

    def draw(self):
        self.draw_topbar()
        self.draw_sidebar()
        self.draw_game_menu()
        self.draw_messages()
        self.draw_budget_popup()
        self.draw_inspector_popup()
        self.draw_tooltip()

    def draw_topbar(self):
        g, c = self.game, self.game.city
        pygame.draw.rect(g.screen, PANEL_BG, (0, 0, SCREEN_W, TOPBAR_H))
        pygame.draw.line(g.screen, (57, 64, 74), (0, TOPBAR_H - 1), (SCREEN_W, TOPBAR_H - 1))
        title = g.big.render("PyCity 2000", True, TEXT)
        g.screen.blit(title, (15, 11))
        date = f"{c.month:02d}/{c.day:02d}/{c.year}"
        paused = "PAUSED" if c.paused else f"{c.sim_speed:.1f}x"
        items = [
            (f"${c.money:,}", GOOD if c.money >= 0 else BAD),
            (date, TEXT),
            (paused, WARN if c.paused else ACCENT),
            (f"Pop {c.stats.population:,}", TEXT),
            (f"Mood {c.stats.mood:.0f}", meter_color(c.stats.mood)),
            (f"Tax {c.tax_rate:.1f}%", TEXT),
        ]
        x = 190
        for text, color in items:
            surf = g.font.render(text, True, color)
            g.screen.blit(surf, (x, 14))
            x += surf.get_width() + 24
        self.draw_time_buttons()
        tool = g.font.render(f"Tool {g.tool.value}", True, ACCENT)
        g.screen.blit(tool, (960, 14))
        self.draw_game_menu_button()

    def draw_time_buttons(self):
        g, c = self.game, self.game.city
        for i, b in enumerate(self.time_buttons):
            active = (
                (i == 0 and c.paused)
                or (i == 1 and not c.paused and c.sim_speed == PLAY_SPEED)
                or (i == 2 and not c.paused and c.sim_speed == FAST_SPEED)
                or (i == 3 and not c.paused and c.sim_speed == FASTER_SPEED)
            )
            pygame.draw.rect(g.screen, ACCENT if active else PANEL_2, b.rect, border_radius=6)
            pygame.draw.rect(g.screen, (75, 86, 99), b.rect, 1, border_radius=6)
            color = (15, 20, 25) if active else TEXT
            label = g.small.render(b.label, True, color)
            g.screen.blit(label, label.get_rect(center=b.rect.center))

    def game_menu_button_rect(self):
        return pygame.Rect(SCREEN_W - 88, 8, 74, 30)

    def game_menu_rect(self):
        button = self.game_menu_button_rect()
        width = 162
        return pygame.Rect(button.right - width, TOPBAR_H - 2, width, 136)

    def game_menu_items(self):
        rect = self.game_menu_rect()
        return [
            ("save", pygame.Rect(rect.x + 6, rect.y + 6, rect.width - 12, 28)),
            ("load", pygame.Rect(rect.x + 6, rect.y + 38, rect.width - 12, 28)),
            ("disasters", pygame.Rect(rect.x + 6, rect.y + 70, rect.width - 12, 28)),
            ("quit", pygame.Rect(rect.x + 6, rect.y + 102, rect.width - 12, 28)),
        ]

    def draw_game_menu_button(self):
        g = self.game
        rect = self.game_menu_button_rect()
        active = self.game_menu_open
        pygame.draw.rect(g.screen, ACCENT if active else PANEL_2, rect, border_radius=6)
        pygame.draw.rect(g.screen, (75, 86, 99), rect, 1, border_radius=6)
        color = (15, 20, 25) if active else TEXT
        label = g.font.render("Game", True, color)
        g.screen.blit(label, (rect.x + 10, rect.y + 8))
        arrow = g.small.render("v", True, color)
        g.screen.blit(arrow, (rect.right - 16, rect.y + 10))

    def draw_game_menu(self):
        if not self.game_menu_open:
            return
        g = self.game
        rect = self.game_menu_rect()
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (75, 86, 99), rect, 1, border_radius=7)
        labels = {
            "save": "Save",
            "load": "Load",
            "disasters": f"Disasters: {'On' if g.city.disasters_enabled else 'Off'}",
            "quit": "Quit",
        }
        for action, item in self.game_menu_items():
            pygame.draw.rect(g.screen, PANEL_2, item, border_radius=5)
            pygame.draw.rect(g.screen, (75, 86, 99), item, 1, border_radius=5)
            label = g.font.render(labels[action], True, TEXT)
            g.screen.blit(label, (item.x + 10, item.y + 7))

    def draw_sidebar(self):
        g, c = self.game, self.game.city
        x = SCREEN_W - SIDEBAR_W
        pygame.draw.rect(g.screen, PANEL_BG, (x, TOPBAR_H, SIDEBAR_W, SCREEN_H - TOPBAR_H))
        pygame.draw.line(g.screen, (57, 64, 74), (x, TOPBAR_H), (x, SCREEN_H))
        self.section_title("Build", x + 14, TOPBAR_H + 8)
        for b in self.menu_buttons:
            active = g.tool in self.menu_tools(b.menu)
            selected = self.open_menu == b.menu or active
            pygame.draw.rect(g.screen, ACCENT if selected else PANEL_2, b.rect, border_radius=6)
            pygame.draw.rect(g.screen, (75, 86, 99), b.rect, 1, border_radius=6)
            arrow = g.small.render("<", True, (15, 20, 25) if selected else MUTED)
            g.screen.blit(arrow, (b.rect.x + 9, b.rect.y + 10))
            label = g.font.render(b.label, True, (15, 20, 25) if selected else TEXT)
            g.screen.blit(label, (b.rect.x + 24, b.rect.y + 8))
        if self.open_menu is not None:
            self.draw_build_menu_popup(self.open_menu)

        y = TOPBAR_H + 343
        self.section_title("City", x + 14, y)
        y += 24
        self.metric("Demand R", c.stats.demand_r, -80, 100, x + 14, y, GOOD)
        self.metric("Demand C", c.stats.demand_c, -80, 100, x + 14, y + 28, ACCENT)
        self.metric("Demand I", c.stats.demand_i, -80, 100, x + 14, y + 56, WARN)
        self.metric("Power", c.stats.power_used, 0, max(1, c.stats.power_cap), x + 14, y + 86, (255, 218, 88), suffix=f" / {c.stats.power_cap}")
        self.metric("Water", c.stats.water_used, 0, max(1, c.stats.water_cap), x + 14, y + 112, (104, 182, 255), suffix=f" / {c.stats.water_cap}")
        self.metric("Traffic", c.stats.traffic, 0, 100, x + 14, y + 138, WARN)
        self.metric("Pollution", c.stats.pollution, 0, 100, x + 14, y + 164, BAD)

        y += 194
        self.draw_budget_button(x + 14, y)

        map_y = self.minimap_rect().y
        self.draw_minimap(x + 16, map_y)
        self.draw_graphs(x + 154, map_y)
        self.draw_map_menu()

    def budget_button_rect(self):
        return pygame.Rect(SCREEN_W - SIDEBAR_W + 14, TOPBAR_H + 571, 260, 34)

    def map_title_rect(self):
        rect = self.minimap_rect()
        return pygame.Rect(rect.x, rect.y - 24, rect.width, 20)

    def map_menu_items(self):
        rect = self.map_menu_rect()
        return [
            (mode, pygame.Rect(rect.x + 6, rect.y + 6 + i * 32, rect.width - 12, 28))
            for i, mode in enumerate(MapMode)
        ]

    def map_menu_rect(self):
        title = self.map_title_rect()
        width = 174
        height = 4 * 32 + 12
        return pygame.Rect(title.x - width - 8, title.y, width, height)

    def draw_map_menu(self):
        if not self.map_menu_open:
            return
        g = self.game
        rect = self.map_menu_rect()
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (75, 86, 99), rect, 1, border_radius=7)
        for mode, item in self.map_menu_items():
            selected = mode == self.map_mode
            pygame.draw.rect(g.screen, ACCENT if selected else PANEL_2, item, border_radius=5)
            pygame.draw.rect(g.screen, (75, 86, 99), item, 1, border_radius=5)
            color = (15, 20, 25) if selected else TEXT
            label = g.small.render(mode.value, True, color)
            g.screen.blit(label, (item.x + 10, item.y + 8))

    def draw_budget_button(self, x, y):
        g, c = self.game, self.game.city
        rect = self.budget_button_rect()
        active = self.budget_open
        pygame.draw.rect(g.screen, ACCENT if active else PANEL_2, rect, border_radius=6)
        pygame.draw.rect(g.screen, (75, 86, 99), rect, 1, border_radius=6)
        color = (15, 20, 25) if active else TEXT
        label = g.font.render("Budget", True, color)
        g.screen.blit(label, (rect.x + 10, rect.y + 8))
        balance = c.stats.income - c.stats.expenses
        summary = g.small.render(f"{balance:+.0f}/mo", True, color if active else (GOOD if balance >= 0 else BAD))
        g.screen.blit(summary, (rect.right - summary.get_width() - 10, rect.y + 10))

    def budget_popup_rect(self):
        width, height = 272, 178
        return pygame.Rect((SCREEN_W - width) // 2, (SCREEN_H - height) // 2, width, height)

    def budget_close_rect(self):
        rect = self.budget_popup_rect()
        return pygame.Rect(rect.right - 28, rect.y + 8, 20, 20)

    def tax_slider_rect(self):
        rect = self.budget_popup_rect()
        return pygame.Rect(rect.x + 14, rect.y + 132, rect.width - 28, 8)

    def tax_slider_hit_rect(self):
        return self.tax_slider_rect().inflate(0, 18)

    def set_tax_from_slider(self, mx):
        rect = self.tax_slider_rect()
        ratio = clamp((mx - rect.x) / rect.width, 0.0, 1.0)
        self.game.city.tax_rate = round(ratio * 20.0, 1)

    def draw_budget_popup(self):
        if not self.budget_open:
            return
        g, c = self.game, self.game.city
        rect = self.budget_popup_rect()
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=7)
        self.section_title("Budget", rect.x + 12, rect.y + 10)
        close = self.budget_close_rect()
        pygame.draw.rect(g.screen, PANEL_3, close, border_radius=4)
        pygame.draw.rect(g.screen, (88, 100, 116), close, 1, border_radius=4)
        x_label = g.small.render("x", True, MUTED)
        g.screen.blit(x_label, x_label.get_rect(center=close.center))
        y = rect.y + 38
        self.text_line(f"Monthly income ${c.stats.income:,.0f}", rect.x + 14, y, GOOD)
        self.text_line(f"Monthly upkeep ${c.stats.expenses:,.0f}", rect.x + 14, y + 22, WARN)
        balance = c.stats.income - c.stats.expenses
        self.text_line(f"Monthly balance ${balance:,.0f}", rect.x + 14, y + 44, GOOD if balance >= 0 else BAD)
        self.text_line(f"Tax rate {c.tax_rate:.1f}%", rect.x + 14, y + 72, TEXT)
        self.text_line("T/Y adjust tax", rect.x + 144, y + 72, MUTED)
        slider = self.tax_slider_rect()
        pygame.draw.rect(g.screen, PANEL_3, slider, border_radius=4)
        fill = pygame.Rect(slider.x, slider.y, int(slider.width * c.tax_rate / 20.0), slider.height)
        pygame.draw.rect(g.screen, ACCENT, fill, border_radius=4)
        knob_x = slider.x + int(slider.width * c.tax_rate / 20.0)
        pygame.draw.circle(g.screen, TEXT, (knob_x, slider.centery), 8)
        pygame.draw.circle(g.screen, (88, 100, 116), (knob_x, slider.centery), 8, 1)
        self.text_line("0%", slider.x, slider.y + 16, MUTED)
        max_label = g.small.render("20%", True, MUTED)
        g.screen.blit(max_label, (slider.right - max_label.get_width(), slider.y + 16))

    def draw_build_menu_popup(self, menu_index):
        g = self.game
        rect = self.menu_popup_rect(menu_index)
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (75, 86, 99), rect, 1, border_radius=7)
        for b in self.menu_item_buttons(menu_index):
            selected = b.tool == g.tool
            pygame.draw.rect(g.screen, ACCENT if selected else PANEL_2, b.rect, border_radius=5)
            pygame.draw.rect(g.screen, (75, 86, 99), b.rect, 1, border_radius=5)
            label_color = (15, 20, 25) if selected else TEXT
            label = g.font.render(b.label, True, label_color)
            g.screen.blit(label, (b.rect.x + 9, b.rect.y + 8))
            hk = g.small.render(b.hotkey, True, (15, 20, 25) if selected else MUTED)
            g.screen.blit(hk, (b.rect.right - hk.get_width() - 8, b.rect.y + 10))

    def section_title(self, text, x, y):
        surf = self.game.font.render(text.upper(), True, MUTED)
        self.game.screen.blit(surf, (x, y))

    def text_line(self, text, x, y, color=TEXT):
        self.game.screen.blit(self.game.small.render(text, True, color), (x, y))

    def metric(self, label, value, lo, hi, x, y, color, suffix=""):
        g = self.game
        g.screen.blit(g.small.render(label, True, TEXT), (x, y))
        rect = pygame.Rect(x + 82, y + 3, 150, 9)
        pygame.draw.rect(g.screen, PANEL_3, rect, border_radius=4)
        if hi == lo:
            pct = 0
        else:
            pct = clamp((value - lo) / (hi - lo), 0, 1)
        fill = rect.copy()
        fill.width = int(rect.width * pct)
        pygame.draw.rect(g.screen, color, fill, border_radius=4)
        val = f"{value:.0f}{suffix}"
        surf = g.small.render(val, True, MUTED)
        g.screen.blit(surf, (x + 238 - surf.get_width(), y - 1))

    def inspector_lines(self, pos):
        c = self.game.city
        tx, ty = pos
        tile = c.tiles[tx][ty]
        origin = c.building_origin(tx, ty)
        footprint = tile.footprint
        lines = [
            f"{tx}, {ty}  {tile.build.value}  Pipe {'Y' if tile.pipe else 'N'}",
            f"Origin {origin[0]},{origin[1]}  Size {footprint[0]}x{footprint[1]}  Level {tile.level}",
            f"Land {tile.land_value:.0f}  Poll {tile.pollution:.0f}  Crime {tile.crime:.0f}  Fire {tile.fire_risk:.0f}",
            f"Access Road {'Y' if tile.road_access else 'N'}  Water {'Y' if tile.watered else 'N'}  Electricity {'Y' if tile.powered else 'N'}",
        ]
        if tile.build in {BuildKind.RES, BuildKind.COM, BuildKind.IND}:
            lines.append(self.zone_score_line(tile))
        elif tile.build in ROAD_KINDS:
            lines.append(f"Congestion {c.road_congestion(tx, ty):.0f}/100")
        return lines

    def zone_score_line(self, tile):
        score = self.game.city.zone_score(tile)
        if tile.build == BuildKind.RES:
            return f"Score {score:.0f}: land({tile.land_value:.0f}) health({tile.health:.0f}) edu({tile.education:.0f}) - poll({tile.pollution:.0f}) crime({tile.crime:.0f})"
        if tile.build == BuildKind.COM:
            return f"Score {score:.0f}: land({tile.land_value:.0f}) edu({tile.education:.0f}) - poll({tile.pollution:.0f}) crime({tile.crime:.0f})"
        if tile.build == BuildKind.IND:
            return f"Score {score:.0f}: road({'Y' if tile.road_access else 'N'}) power({'Y' if tile.powered else 'N'}) - land({tile.land_value:.0f})"
        return f"Score {score:.0f}"

    def inspector_popup_rect(self):
        g, c = self.game, self.game.city
        if not c.selected:
            return pygame.Rect(0, 0, 0, 0)
        sx, sy = g.tile_screen(*c.selected)
        width, height = 390, 136
        view_right = SCREEN_W - SIDEBAR_W
        x = sx + 24
        if x + width > view_right - 12:
            x = sx - width - 24
        y = sy - height - 18
        if y < TOPBAR_H + 10:
            y = sy + 22
        x = int(clamp(x, 12, view_right - width - 12))
        y = int(clamp(y, TOPBAR_H + 10, SCREEN_H - height - 12))
        return pygame.Rect(x, y, width, height)

    def inspector_close_rect(self):
        rect = self.inspector_popup_rect()
        return pygame.Rect(rect.right - 28, rect.y + 8, 20, 20)

    def draw_inspector_popup(self):
        g, c = self.game, self.game.city
        if not c.selected:
            return
        rect = self.inspector_popup_rect()
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=7)
        self.section_title("Inspector", rect.x + 12, rect.y + 10)
        close = self.inspector_close_rect()
        pygame.draw.rect(g.screen, PANEL_3, close, border_radius=4)
        pygame.draw.rect(g.screen, (88, 100, 116), close, 1, border_radius=4)
        x_label = g.small.render("x", True, MUTED)
        g.screen.blit(x_label, x_label.get_rect(center=close.center))
        x, y = rect.x + 12, rect.y + 36
        lines = self.inspector_lines(c.selected)
        for i, line in enumerate(lines):
            self.text_line(line, x, y + i * 17, TEXT if i == 0 else MUTED)

    def draw_minimap(self, x, y):
        g, c = self.game, self.game.city
        rect = self.minimap_rect()
        x, y = rect.x, rect.y
        title_rect = self.map_title_rect()
        pygame.draw.rect(g.screen, ACCENT if self.map_menu_open else PANEL_2, title_rect, border_radius=5)
        pygame.draw.rect(g.screen, (75, 86, 99), title_rect, 1, border_radius=5)
        title_color = (15, 20, 25) if self.map_menu_open else TEXT
        label = g.small.render("Map", True, title_color)
        g.screen.blit(label, (title_rect.x + 8, title_rect.y + 4))
        arrow = g.small.render("<", True, title_color)
        g.screen.blit(arrow, (title_rect.right - 14, title_rect.y + 4))
        pygame.draw.rect(g.screen, PANEL_2, (x - 2, y - 2, rect.width + 4, rect.height + 4))
        sx = rect.width / c.width
        sy = rect.height / c.height
        for tx in range(c.width):
            for ty in range(c.height):
                color = self.minimap_tile_color(tx, ty)
                pygame.draw.rect(g.screen, color, (x + tx * sx, y + ty * sy, max(1, sx), max(1, sy)))
        self.draw_minimap_viewport(rect)

    def minimap_tile_color(self, tx, ty):
        c = self.game.city
        tile = c.tiles[tx][ty]
        if self.map_mode == MapMode.PIPES:
            if tile.pipe:
                return (65, 156, 218)
            if tile.water:
                return (35, 88, 125)
            if tile.build != BuildKind.EMPTY:
                return (88, 83, 66)
            return (45, 63, 50)
        if self.map_mode == MapMode.TRAFFIC:
            if tile.build in ROAD_KINDS:
                return heat_color(c.road_congestion(tx, ty))
            if tile.build in ZONE_KINDS:
                return (76, 70, 62)
            return (38, 47, 45) if not tile.water else (31, 70, 94)
        if self.map_mode == MapMode.LAND_VALUE:
            if tile.build in ZONE_KINDS:
                return heat_color(tile.land_value)
            if tile.water:
                return (31, 70, 94)
            return (44, 54, 45)
        return self.standard_minimap_color(tile)

    def standard_minimap_color(self, tile):
        color = (35, 88, 125) if tile.water else (58, 104, 61)
        if tile.build == BuildKind.ROAD:
            color = (88, 91, 96)
        elif tile.build == BuildKind.BRIDGE:
            color = (170, 146, 105)
        elif tile.build == BuildKind.RAIL:
            color = (82, 70, 58)
        elif tile.build == BuildKind.RAIL_BRIDGE:
            color = (145, 110, 72)
        elif tile.build == BuildKind.RAIL_CROSSING:
            color = (214, 198, 116)
        elif tile.build == BuildKind.RAIL_STATION:
            color = (170, 154, 122)
        elif tile.build == BuildKind.RES:
            color = GOOD
        elif tile.build == BuildKind.COM:
            color = ACCENT
        elif tile.build == BuildKind.IND:
            color = WARN
        elif tile.build in SERVICE_KINDS:
            color = (220, 220, 220)
        elif tile.build == BuildKind.BURNING:
            color = BAD
        return color

    def draw_minimap_viewport(self, rect):
        g, c = self.game, self.game.city
        view_right = SCREEN_W - SIDEBAR_W
        corners = [
            g.camera.screen_to_world(0, TOPBAR_H),
            g.camera.screen_to_world(view_right, TOPBAR_H),
            g.camera.screen_to_world(0, SCREEN_H),
            g.camera.screen_to_world(view_right, SCREEN_H),
        ]
        min_x = clamp(min(x for x, _ in corners), 0, c.width - 1)
        max_x = clamp(max(x for x, _ in corners), 0, c.width - 1)
        min_y = clamp(min(y for _, y in corners), 0, c.height - 1)
        max_y = clamp(max(y for _, y in corners), 0, c.height - 1)
        sx = rect.width / c.width
        sy = rect.height / c.height
        view_rect = pygame.Rect(
            rect.x + int(min_x * sx),
            rect.y + int(min_y * sy),
            max(4, int((max_x - min_x + 1) * sx)),
            max(4, int((max_y - min_y + 1) * sy)),
        )
        view_rect.clamp_ip(rect)
        pygame.draw.rect(g.screen, (255, 245, 170), view_rect, 2)
        pygame.draw.rect(g.screen, (20, 24, 28), rect, 1)

    def draw_graphs(self, x, y):
        g, c = self.game, self.game.city
        self.section_title("Trend", x, y - 20)
        rect = pygame.Rect(x, y, 112, 112)
        pygame.draw.rect(g.screen, PANEL_2, rect)
        pygame.draw.rect(g.screen, (65, 74, 84), rect, 1)
        series = [
            ("population", GOOD),
            ("money", ACCENT),
            ("mood", WARN),
            ("pollution", BAD),
        ]
        for key, color in series:
            vals = c.graphs[key]
            if len(vals) < 2:
                continue
            lo, hi = min(vals), max(vals)
            if lo == hi:
                hi += 1
            points = []
            for i, val in enumerate(vals):
                px = rect.x + int(i / max(1, len(vals) - 1) * (rect.width - 4)) + 2
                py = rect.bottom - 3 - int((val - lo) / (hi - lo) * (rect.height - 8))
                points.append((px, py))
            pygame.draw.lines(g.screen, color, False, points, 2)

    def draw_messages(self):
        g = self.game
        y = TOPBAR_H + 10
        for m in self.game.city.messages[:4]:
            surf = g.font.render(m.text, True, m.color)
            pad = 8
            rect = pygame.Rect(14, y, surf.get_width() + pad * 2, 28)
            pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=5)
            pygame.draw.rect(g.screen, (65, 72, 82), rect, 1, border_radius=5)
            g.screen.blit(surf, (rect.x + pad, rect.y + 6))
            y += 34

    def draw_tooltip(self):
        g = self.game
        mx, my = pygame.mouse.get_pos()
        if mx >= SCREEN_W - SIDEBAR_W or my < TOPBAR_H:
            return
        if not g.hover and not g.dragging_path and not g.dragging_zone:
            return
        if g.dragging_path:
            tiles = len(g.path_plan)
            text = f"{g.tool.value} path {tiles} tiles ${g.path_cost}"
            if g.path_error:
                text = g.path_error
        elif g.dragging_zone:
            tiles = len(g.zone_plan)
            text = f"{g.tool.value} area {tiles} tiles ${g.zone_cost}"
            if g.zone_error:
                text = g.zone_error
        elif g.tool in TOOL_BUILD:
            price = COST.get(g.tool, 0)
            fw, fh = FOOTPRINTS[TOOL_BUILD[g.tool]]
            size = f" {fw}x{fh}" if (fw, fh) != (1, 1) else ""
            text = f"{g.tool.value}{size} ${price}"
        else:
            text = "Inspect"
        surf = g.small.render(text, True, TEXT)
        rect = pygame.Rect(mx + 14, my + 16, surf.get_width() + 12, 24)
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=5)
        pygame.draw.rect(g.screen, (74, 83, 96), rect, 1, border_radius=5)
        g.screen.blit(surf, (rect.x + 6, rect.y + 5))


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


def main():
    Game().run()


if __name__ == "__main__":
    main()
