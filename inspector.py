import avatars
from pycity2000 import BUILDING_OUTPUT_CAPACITY, BuildKind, RAIL_KINDS, ROAD_KINDS, TILE_SCORE_EFFECTS


AVATAR_DRAWERS = {
    BuildKind.SCHOOL: avatars.draw_school_avatar,
    BuildKind.CLINIC: avatars.draw_clinic_avatar,
    BuildKind.POLICE: avatars.draw_police_avatar,
    BuildKind.FIRE: avatars.draw_fire_avatar,
    BuildKind.LIBRARY: avatars.draw_library_avatar,
    BuildKind.STADIUM: avatars.draw_stadium_avatar,
    BuildKind.RAIL_STATION: avatars.draw_rail_station_avatar,
    BuildKind.SEAPORT: avatars.draw_seaport_avatar,
    BuildKind.AIRPORT: avatars.draw_airport_avatar,
    BuildKind.PARK: avatars.draw_park_avatar,
    BuildKind.LARGE_PARK: avatars.draw_large_park_avatar,
    BuildKind.WATER_PUMP: avatars.draw_water_pump_avatar,
    BuildKind.COAL: avatars.draw_coal_avatar,
    BuildKind.SOLAR: avatars.draw_solar_avatar,
}


def draw_inspector_avatar(ui, kind, rect):
    drawer = AVATAR_DRAWERS.get(kind, avatars.draw_generic_avatar)
    if drawer is avatars.draw_generic_avatar:
        drawer(ui, rect, kind)
    else:
        drawer(ui, rect)


def park_lines(ui, origin):
    return park_effect_lines(ui, origin, BuildKind.PARK)


def large_park_lines(ui, origin):
    return park_effect_lines(ui, origin, BuildKind.LARGE_PARK)


def park_effect_lines(ui, origin, kind):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Status Missing building record"]
    tile = c.tiles[origin[0]][origin[1]]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    effects = TILE_SCORE_EFFECTS[kind]
    return [
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Land score {tile.land_value:.0f}/100  Health score {tile.health:.0f}/100",
        f"Local effects Land +{effects['land_value']:.0f}  Health +{effects['health']:.0f}",
        f"Resources P{power} W{water} G{garbage}",
    ]


def solar_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Status Missing building record"]
    tile = c.tiles[origin[0]][origin[1]]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    capacity = c.power_source_capacity(BuildKind.SOLAR)
    return [
        f"Power capacity {capacity}",
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Land score {tile.land_value:.0f}/100  Pollution {tile.pollution:.0f}/100",
        f"Resources P{power} W{water} G{garbage}",
    ]


def coal_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Status Missing building record"]
    tile = c.tiles[origin[0]][origin[1]]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    capacity = c.power_source_capacity(BuildKind.COAL)
    pollution_effect = TILE_SCORE_EFFECTS[BuildKind.COAL]["pollution"]
    return [
        f"Power capacity {capacity}",
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Pollution {tile.pollution:.0f}/100  Local effect +{pollution_effect:.0f}",
        f"Resources P{power} W{water} G{garbage}",
    ]


def water_pump_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Status Missing building record"]
    x, y = origin
    active_capacity = c.water_pump_capacity(x, y)
    nominal_capacity = BUILDING_OUTPUT_CAPACITY[BuildKind.WATER_PUMP]["water"]
    pipe_connections = sum(1 for nx, ny in c.neighbors4(x, y) if c.tiles[nx][ny].pipe)
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    return [
        f"Status {'Active' if active_capacity else 'No water source'}",
        f"Water capacity {active_capacity}/{nominal_capacity}",
        f"Pipe connections {pipe_connections}",
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Resources P{power} W{water} G{garbage}",
    ]


def transport_effect_line(kind):
    effects = TILE_SCORE_EFFECTS[kind]
    return f"Local effects Land {effects.get('land_value', 0):+.0f}  Poll {effects.get('pollution', 0):+.0f}"


def rail_station_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Status Missing building record"]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    track_tiles = sum(1 for tx, ty in c.building_tiles(*origin) if c.is_rail_station_track(tx, ty))
    rail_connections = sum(1 for nx, ny in c.building_boundary(*origin) if c.tiles[nx][ny].build in RAIL_KINDS)
    traffic = sum(c.traffic_loads.get((nx, ny), 0.0) for nx, ny in c.building_boundary(*origin) if c.tiles[nx][ny].build in ROAD_KINDS)
    return [
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Track tiles {track_tiles}  Rail links {rail_connections}",
        f"Road traffic nearby {traffic:.0f} trips",
        transport_effect_line(BuildKind.RAIL_STATION),
        f"Resources P{power} W{water} G{garbage}",
    ]


def seaport_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Status Missing building record"]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    shoreline_edges = sum(1 for nx, ny in c.building_boundary(*origin) if c.tiles[nx][ny].water)
    traffic = sum(c.traffic_loads.get((nx, ny), 0.0) for nx, ny in c.building_boundary(*origin) if c.tiles[nx][ny].build in ROAD_KINDS)
    return [
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Shoreline contact {shoreline_edges} tiles",
        f"Road traffic nearby {traffic:.0f} trips",
        transport_effect_line(BuildKind.SEAPORT),
        f"Resources P{power} W{water} G{garbage}",
    ]


def airport_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Status Missing building record"]
    tile = c.tiles[origin[0]][origin[1]]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    terrain_levels = {c.tiles[tx][ty].terrain for tx, ty in c.building_tiles(*origin)}
    traffic = sum(c.traffic_loads.get((nx, ny), 0.0) for nx, ny in c.building_boundary(*origin) if c.tiles[nx][ny].build in ROAD_KINDS)
    return [
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Flat terrain {'Y' if len(terrain_levels) == 1 else 'N'}  Elevation {tile.terrain}",
        f"Road traffic nearby {traffic:.0f} trips",
        transport_effect_line(BuildKind.AIRPORT),
        f"Resources P{power} W{water} G{garbage}",
    ]


def covered_residential_stats(c, coverage_fn_name):
    coverage_fn = getattr(c, coverage_fn_name)
    covered_homes = [
        other
        for other in c.buildings.values()
        if other.kind == BuildKind.RES and coverage_fn(other.origin) > 0
    ]
    covered_residents = sum(
        len([cid for cid in home.resident_ids if cid in c.citizens])
        for home in covered_homes
    )
    return covered_homes, covered_residents


def service_building_lines(ui, origin, metric_line, coverage_fn_name):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Staff 0/0"]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    covered_homes, covered_residents = covered_residential_stats(c, coverage_fn_name)
    return [
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        metric_line(c.tiles[origin[0]][origin[1]], len(covered_homes)),
        f"Covered residents {covered_residents}",
        f"Resources P{power} W{water} G{garbage}",
    ]


def clinic_lines(ui, origin):
    return service_building_lines(
        ui,
        origin,
        lambda tile, homes: f"Health score {tile.health:.0f}/100  Coverage homes {homes}",
        "clinic_coverage",
    )


def police_lines(ui, origin):
    return service_building_lines(
        ui,
        origin,
        lambda tile, homes: f"Crime score {tile.crime:.0f}/100  Coverage homes {homes}",
        "police_coverage",
    )


def fire_lines(ui, origin):
    return service_building_lines(
        ui,
        origin,
        lambda tile, homes: f"Fire risk {tile.fire_risk:.0f}/100  Coverage homes {homes}",
        "fire_coverage",
    )


def library_lines(ui, origin):
    return service_building_lines(
        ui,
        origin,
        lambda tile, homes: f"Education score {tile.education:.0f}/100  Coverage homes {homes}",
        "library_coverage",
    )


def stadium_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Staff 0/0"]
    tile = c.tiles[origin[0]][origin[1]]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    power, water, garbage = c.building_resource_use(building)
    covered_homes, covered_residents = covered_residential_stats(c, "stadium_coverage")
    return [
        f"Staff {len(worker_ids)}/{building.job_capacity}",
        f"Land score {tile.land_value:.0f}/100  Crime {tile.crime:.0f}/100",
        f"Coverage homes {len(covered_homes)}  Residents {covered_residents}",
        f"Resources P{power} W{water} G{garbage}",
    ]


def school_lines(ui, origin):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Students 0/0", "Staff 0/0"]
    student_ids = [cid for cid in building.student_ids if cid in c.citizens]
    worker_ids = [cid for cid in building.worker_ids if cid in c.citizens]
    school_trips = [
        trip.distance
        for trip in c.trips
        if trip.purpose == "school" and trip.to_building_id == building.id
    ]
    education_gains = [
        c.education_gain(c.citizens[cid])
        for cid in student_ids
    ]
    lines = [
        f"Students {len(student_ids)}/{building.student_capacity}  City school-age {len(c.school_age_citizens())}",
        f"Staff {len(worker_ids)}/{building.job_capacity}",
    ]
    if school_trips:
        lines.append(f"Avg school trip {sum(school_trips) / len(school_trips):.1f} tiles")
    else:
        lines.append("Avg school trip n/a")
    if education_gains:
        lines.append(f"Avg monthly education gain {sum(education_gains) / len(education_gains):.2f}")
    else:
        lines.append("Avg monthly education gain n/a")
    return lines


def resident_lines(ui, origin, limit=10):
    c = ui.game.city
    building = c.building_at_origin(origin)
    if not building:
        return ["Residents 0/0"]
    resident_ids = [cid for cid in building.resident_ids if cid in c.citizens]
    lines = [f"Residents {len(resident_ids)}/{building.resident_capacity}"]
    for citizen_id in resident_ids[:limit]:
        citizen = c.citizens[citizen_id]
        lines.append(f"{citizen.name}  Born {c.format_date(citizen.born)}")
    if len(resident_ids) > limit:
        lines.append(f"... {len(resident_ids) - limit} more residents")
    return lines


def zone_score_line(ui, tile):
    score = ui.game.city.zone_score(tile)
    if tile.build == BuildKind.RES:
        return f"Score {score:.0f}: land({tile.land_value:.0f}) health({tile.health:.0f}) edu({tile.education:.0f}) - poll({tile.pollution:.0f}) crime({tile.crime:.0f})"
    if tile.build == BuildKind.COM:
        return f"Score {score:.0f}: land({tile.land_value:.0f}) edu({tile.education:.0f}) - poll({tile.pollution:.0f}) crime({tile.crime:.0f})"
    if tile.build == BuildKind.IND:
        return f"Score {score:.0f}: road({'Y' if tile.road_access else 'N'}) power({'Y' if tile.powered else 'N'}) - land({tile.land_value:.0f})"
    return f"Score {score:.0f}"


def building_label(ui, building_id):
    building = ui.game.city.buildings.get(building_id)
    if not building:
        return "None"
    return f"{building.kind.value} {building.origin[0]},{building.origin[1]}"


def citizen_lines(ui, citizen_id):
    c = ui.game.city
    citizen = c.citizens.get(citizen_id)
    if not citizen:
        return ["Citizen not found"]
    home_id = c.citizen_home_building_id(citizen)
    return [
        citizen.name,
        f"Born {c.format_date(citizen.born)}  Age {c.citizen_age(citizen)}  Gender {citizen.gender.upper()}",
        f"Home {building_label(ui, home_id)}",
        f"Job {building_label(ui, citizen.job_id)}",
        f"School {building_label(ui, citizen.school_id)}",
        f"Health {citizen.health:.0f}  Education {citizen.education:.0f}  Ability {citizen.education_ability:.2f}",
        f"Mood {citizen.happiness:.0f}",
    ]


def road_lines(ui, pos):
    c = ui.game.city
    tx, ty = pos
    return [
        f"Congestion {c.road_congestion(tx, ty):.0f}/100",
        f"Traffic {c.traffic_loads.get((tx, ty), 0.0):.0f} trips",
    ]


LINE_BUILDERS = {
    BuildKind.RES: resident_lines,
    BuildKind.SCHOOL: school_lines,
    BuildKind.PARK: park_lines,
    BuildKind.LARGE_PARK: large_park_lines,
    BuildKind.WATER_PUMP: water_pump_lines,
    BuildKind.COAL: coal_lines,
    BuildKind.SOLAR: solar_lines,
    BuildKind.RAIL_STATION: rail_station_lines,
    BuildKind.SEAPORT: seaport_lines,
    BuildKind.AIRPORT: airport_lines,
    BuildKind.CLINIC: clinic_lines,
    BuildKind.POLICE: police_lines,
    BuildKind.FIRE: fire_lines,
    BuildKind.LIBRARY: library_lines,
    BuildKind.STADIUM: stadium_lines,
}


def extra_lines(ui, kind, origin):
    builder = LINE_BUILDERS.get(kind)
    if not builder:
        return None
    return builder(ui, origin)
