import hashlib
import math

import pygame


SKIN_TONES = [
    (238, 198, 160),
    (219, 170, 126),
    (191, 132, 91),
    (139, 88, 62),
    (93, 59, 45),
]

HAIR_COLORS = [
    (41, 31, 26),
    (82, 58, 39),
    (134, 91, 47),
    (181, 139, 72),
    (170, 170, 162),
]

SHIRT_COLORS = {
    "child": (67, 132, 196),
    "student": (58, 111, 184),
    "worker": (77, 148, 133),
    "commercial": (60, 155, 170),
    "industrial": (174, 111, 48),
    "civic": (204, 211, 218),
    "utility": (94, 141, 91),
    "transport": (121, 111, 170),
    "unemployed": (115, 124, 132),
    "elder": (136, 116, 156),
}

FEMININE_ACCENTS = [
    (188, 72, 106),
    (204, 92, 132),
    (168, 79, 151),
    (211, 104, 91),
]

JOB_ROLE_BY_KIND_VALUE = {
    "Commercial Zone": "commercial",
    "Industrial Zone": "industrial",
    "Police": "civic",
    "Fire Station": "civic",
    "Clinic": "civic",
    "School": "civic",
    "Library": "civic",
    "Sports Stadium": "civic",
    "Park": "civic",
    "Large Park": "civic",
    "Water Pump": "utility",
    "Coal Plant": "utility",
    "Solar Plant": "utility",
    "Railway Station": "transport",
    "Seaport": "transport",
    "Airport": "transport",
}


def avatar_override(citizen, key, default=None):
    overrides = getattr(citizen, "avatar_overrides", None)
    if overrides and key in overrides:
        return overrides[key]
    return default


def avatar_index(citizen, key, options, salt):
    override = avatar_override(citizen, key)
    if override is not None:
        return int(override) % len(options)
    return stable_int(citizen, salt) % len(options)


def stable_int(citizen, salt):
    key = f"{getattr(citizen, 'id', '')}:{getattr(citizen, 'name', '')}:{salt}"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def stable_choice(citizen, options, salt):
    if not options:
        raise ValueError("stable_choice requires at least one option")
    return options[avatar_index(citizen, salt, options, salt)]


def citizen_age(citizen, city=None):
    if city and hasattr(city, "citizen_age"):
        return city.citizen_age(citizen)
    birth_month, birth_day, birth_year = citizen.born
    current_month = getattr(city, "month", 1)
    current_day = getattr(city, "day", 1)
    current_year = getattr(city, "year", 1900)
    age = current_year - birth_year
    if (current_month, current_day) < (birth_month, birth_day):
        age -= 1
    return max(0, age)


def age_group(citizen, city=None):
    age = citizen_age(citizen, city)
    if age < 18:
        return "child"
    if age >= 65:
        return "elder"
    return "adult"


def child_age_band(citizen, city=None):
    age = citizen_age(citizen, city)
    if age < 5:
        return "toddler"
    if age < 13:
        return "school"
    if age < 18:
        return "teen"
    return None


def building_kind_value(building):
    kind = getattr(building, "kind", None)
    return getattr(kind, "value", str(kind))


def citizen_role(citizen, city=None):
    role = avatar_override(citizen, "role")
    if role in SHIRT_COLORS:
        return role
    group = age_group(citizen, city)
    if group == "child":
        return "student" if citizen.school_id is not None else "child"
    if group == "elder":
        return "elder"
    if citizen.job_id is None:
        return "unemployed"
    if city:
        building = city.buildings.get(citizen.job_id)
        if building:
            return JOB_ROLE_BY_KIND_VALUE.get(building_kind_value(building), "worker")
    return "worker"


def clamp_color(value):
    return max(0, min(255, int(value)))


def adjust_color(color, delta):
    return tuple(clamp_color(channel + delta) for channel in color)


def shirt_color(citizen, role):
    variation = stable_int(citizen, "shirt-shade") % 25 - 12
    return adjust_color(SHIRT_COLORS[role], variation)


def hair_style(citizen, style_count):
    override = avatar_override(citizen, "hair-style")
    if override is not None:
        return int(override) % style_count
    return stable_int(citizen, "hair-style") % style_count


def draw_citizen_avatar(ui, rect, citizen):
    screen = ui.game.screen
    pygame.draw.rect(screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(screen, (88, 100, 116), rect, 1, border_radius=5)

    gender = getattr(citizen, "gender", "m")
    group = age_group(citizen, ui.game.city)
    child_band = child_age_band(citizen, ui.game.city) if group == "child" else None
    role = citizen_role(citizen, ui.game.city)
    skin = SKIN_TONES[avatar_index(citizen, "skin", SKIN_TONES, "skin")]
    hair = HAIR_COLORS[avatar_index(citizen, "hair", HAIR_COLORS, "hair")]
    shirt = shirt_color(citizen, role)

    cx = rect.centerx
    base = min(rect.width, rect.height)
    if child_band == "toddler":
        head_w, head_h, head_y = int(base * 0.44), int(base * 0.49), rect.y + int(base * 0.13)
    elif child_band == "school":
        head_w, head_h, head_y = int(base * 0.40), int(base * 0.45), rect.y + int(base * 0.14)
    elif child_band == "teen":
        head_w = int(base * (0.38 if gender == "f" else 0.41))
        head_h = int(base * (0.47 if gender == "f" else 0.44))
        head_y = rect.y + int(base * 0.11)
    else:
        head_w = int(base * (0.38 if gender == "f" else 0.42))
        head_h = int(base * (0.48 if gender == "f" else 0.45))
        head_y = rect.y + int(base * 0.10)
    head = pygame.Rect(cx - head_w // 2, head_y, head_w, head_h)

    if child_band == "toddler":
        shoulder_inset, shoulder_y, shoulder_h = 0.30, 0.74, 0.16
    elif child_band == "school":
        shoulder_inset, shoulder_y, shoulder_h = 0.25, 0.71, 0.19
    else:
        shoulder_inset = 0.22 if gender == "f" and group != "child" else 0.18
        shoulder_y, shoulder_h = 0.69, 0.22
    shoulders = pygame.Rect(rect.x + int(rect.width * shoulder_inset), rect.y + int(rect.height * shoulder_y), int(rect.width * (1 - shoulder_inset * 2)), int(rect.height * shoulder_h))
    pygame.draw.ellipse(screen, shirt, shoulders)
    pygame.draw.ellipse(screen, adjust_color(shirt, -40), shoulders, 1)
    draw_role_detail(screen, shoulders, role)

    neck = pygame.Rect(cx - max(3, head_w // 8), head.bottom - 2, max(6, head_w // 4), int(base * 0.11))
    pygame.draw.rect(screen, skin, neck, border_radius=2)

    draw_hair_back(screen, head, hair, citizen, group, child_band)
    pygame.draw.ellipse(screen, skin, head)
    pygame.draw.ellipse(screen, adjust_color(skin, -45), head, 1)

    draw_hair(screen, head, hair, citizen, group, child_band)
    draw_face(screen, head, citizen, group, child_band)
    draw_accessories(screen, head, citizen, group, child_band)


def draw_hair_back(screen, head, color, citizen, group, child_band=None):
    if group == "child":
        draw_child_hair_back(screen, head, color, citizen, child_band)
        return
    if getattr(citizen, "gender", "m") != "f":
        return
    style = hair_style(citizen, 7)
    if style in {0, 1, 3, 5}:
        shade = adjust_color(color, -18)
        crown = pygame.Rect(head.x - head.width // 10, head.y + head.height // 8, head.width + head.width // 5, head.height // 2)
        pygame.draw.ellipse(screen, shade, crown)
        left = pygame.Rect(head.x - head.width // 5, head.y + head.height // 4, head.width // 4, int(head.height * 0.76))
        right = pygame.Rect(head.right - head.width // 18, head.y + head.height // 4, head.width // 4, int(head.height * 0.76))
        pygame.draw.rect(screen, shade, left, border_radius=max(3, head.width // 8))
        pygame.draw.rect(screen, shade, right, border_radius=max(3, head.width // 8))
    if style in {2, 6}:
        left = pygame.Rect(head.x - head.width // 5, head.y + head.height // 4, head.width // 3, head.height // 2)
        right = pygame.Rect(head.right - head.width // 8, head.y + head.height // 4, head.width // 3, head.height // 2)
        pygame.draw.ellipse(screen, adjust_color(color, -14), left)
        pygame.draw.ellipse(screen, adjust_color(color, -14), right)


def draw_hair(screen, head, color, citizen, group, child_band=None):
    gender = getattr(citizen, "gender", "m")
    if group == "child":
        draw_child_hair(screen, head, color, citizen, child_band)
    elif gender == "f":
        draw_feminine_hair(screen, head, color, citizen)
    else:
        draw_masculine_hair(screen, head, color, citizen, group)


def draw_child_hair_back(screen, head, color, citizen, child_band):
    gender = getattr(citizen, "gender", "m")
    if gender != "f":
        return
    style = hair_style(citizen, 7)
    shade = adjust_color(color, -14)
    if child_band == "toddler" and style in {0, 3, 5}:
        left = pygame.Rect(head.x - head.width // 5, head.y + head.height // 3, head.width // 4, head.height // 3)
        right = pygame.Rect(head.right - head.width // 12, head.y + head.height // 3, head.width // 4, head.height // 3)
        pygame.draw.ellipse(screen, shade, left)
        pygame.draw.ellipse(screen, shade, right)
    elif child_band == "school" and style in {0, 1, 3, 5}:
        left = pygame.Rect(head.x - head.width // 5, head.y + head.height // 4, head.width // 4, int(head.height * 0.62))
        right = pygame.Rect(head.right - head.width // 18, head.y + head.height // 4, head.width // 4, int(head.height * 0.62))
        pygame.draw.rect(screen, shade, left, border_radius=max(3, head.width // 8))
        pygame.draw.rect(screen, shade, right, border_radius=max(3, head.width // 8))
    elif child_band == "teen" and style in {0, 1, 3, 5}:
        back = pygame.Rect(head.x - head.width // 9, head.y + head.height // 6, head.width + head.width // 5, int(head.height * 0.76))
        pygame.draw.ellipse(screen, shade, back)


def draw_child_hair(screen, head, color, citizen, child_band):
    gender = getattr(citizen, "gender", "m")
    if gender == "f":
        draw_girl_hair(screen, head, color, citizen, child_band)
    else:
        draw_boy_hair(screen, head, color, citizen, child_band)


def draw_girl_hair(screen, head, color, citizen, child_band):
    accent = stable_choice(citizen, FEMININE_ACCENTS, "clip")
    style = hair_style(citizen, 7)
    is_toddler = child_band == "toddler"
    is_school = child_band == "school"
    height_scale = 0.34 if is_toddler else 0.42 if is_school else 0.50
    top_y = head.y - (1 if is_toddler else 2)
    pygame.draw.ellipse(screen, color, pygame.Rect(head.x - 1, top_y, head.width + 2, int(head.height * height_scale)))

    if style == 0:
        pygame.draw.line(screen, adjust_color(color, 34), (head.centerx - 3, head.y), (head.centerx - head.width // 4, head.y + head.height // 3), 2)
        if not is_toddler:
            side = pygame.Rect(head.x - head.width // 8, head.y + head.height // 3, head.width // 5, head.height // 3)
            pygame.draw.ellipse(screen, adjust_color(color, -8), side)
    elif style == 1:
        left_bang = [
            (head.x + 2, head.y + head.height // 4),
            (head.x + head.width // 3, head.y),
            (head.centerx - head.width // 12, head.y + head.height // 5),
        ]
        right_bang = [
            (head.right - 2, head.y + head.height // 4),
            (head.centerx + head.width // 10, head.y),
            (head.centerx - head.width // 14, head.y + head.height // 5),
        ]
        pygame.draw.polygon(screen, color, left_bang)
        pygame.draw.polygon(screen, color, right_bang)
    elif style == 2:
        bun_h = head.height // (4 if is_toddler else 3)
        bun = pygame.Rect(head.centerx - head.width // 5, head.y - bun_h // 2, head.width * 2 // 5, bun_h)
        pygame.draw.ellipse(screen, adjust_color(color, -8), bun)
        pygame.draw.rect(screen, accent, pygame.Rect(head.centerx - head.width // 8, head.y + head.height // 5, max(3, head.width // 4), max(2, head.height // 14)), border_radius=2)
    elif style == 3:
        bang = [
            (head.x + 1, head.y + head.height // 4),
            (head.x + head.width // 3, head.y),
            (head.centerx, head.y + head.height // 5),
            (head.right - 2, head.y + head.height // 5),
        ]
        pygame.draw.polygon(screen, color, bang)
    elif style == 4:
        pony_h = head.height // (3 if is_toddler else 2)
        pony = pygame.Rect(head.right - head.width // 10, head.y + head.height // 3, head.width // 4, pony_h)
        pygame.draw.ellipse(screen, adjust_color(color, -10), pony)
        pygame.draw.rect(screen, accent, pygame.Rect(pony.x, pony.y + pony.height // 3, pony.width, max(2, head.height // 14)), border_radius=2)
    elif style == 5:
        curl_count = 2 if is_toddler else 3 if is_school else 4
        for i in range(curl_count):
            x = head.x + 4 + i * max(2, head.width // max(2, curl_count))
            pygame.draw.circle(screen, adjust_color(color, -8), (x, head.y + head.height // 3), max(2, head.width // 12))
    else:
        pygame.draw.line(screen, adjust_color(color, 36), (head.centerx + 3, head.y), (head.centerx + head.width // 5, head.y + head.height // 3), 2)

    if child_band == "toddler":
        pygame.draw.circle(screen, accent, (head.x + head.width // 5, head.y + head.height // 3), max(2, head.width // 18))
    elif child_band == "school":
        pygame.draw.rect(screen, accent, pygame.Rect(head.right - head.width // 5, head.y + head.height // 4, max(3, head.width // 6), max(2, head.height // 14)), border_radius=2)
    else:
        pygame.draw.circle(screen, accent, (head.x + head.width // 5, head.y + head.height // 3), max(2, head.width // 18))


def draw_boy_hair(screen, head, color, citizen, child_band):
    style = hair_style(citizen, 7)
    if child_band == "teen":
        draw_masculine_hair(screen, head, color, citizen, "adult")
    elif style == 0:
        cap = pygame.Rect(head.x + 1, head.y - 1, head.width - 2, head.height // (3 if child_band == "toddler" else 2))
        pygame.draw.arc(screen, color, cap, math.pi, math.tau, max(2, head.width // 9))
        pygame.draw.line(screen, color, (head.x + 4, head.y + head.height // 5), (head.right - 4, head.y + head.height // 6), max(2, head.width // 12))
    elif style == 1:
        fringe = [
            (head.x + 2, head.y + head.height // 4),
            (head.x + head.width // 4, head.y),
            (head.centerx, head.y + head.height // 5),
            (head.x + head.width * 3 // 4, head.y),
            (head.right - 2, head.y + head.height // 4),
        ]
        pygame.draw.polygon(screen, color, fringe)
    elif style == 2:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x + 1, head.y - 2, head.width - 2, head.height // (4 if child_band == "toddler" else 3)))
    elif style == 3:
        part_y = head.y + head.height // 5
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x + 1, head.y - 2, head.width - 2, head.height // 2))
        pygame.draw.line(screen, adjust_color(color, 35), (head.centerx - 2, head.y + 1), (head.centerx - 7, part_y), 2)
    elif style == 4:
        pygame.draw.rect(screen, color, pygame.Rect(head.x + 2, head.y + 1, head.width - 4, head.height // 5), border_radius=max(2, head.width // 10))
    elif style == 5:
        pygame.draw.arc(screen, color, pygame.Rect(head.x + 2, head.y, head.width - 4, head.height // 3), math.pi, math.tau, max(2, head.width // 12))
    else:
        tuft = [
            (head.centerx - head.width // 6, head.y + head.height // 6),
            (head.centerx, head.y - head.height // 12),
            (head.centerx + head.width // 6, head.y + head.height // 6),
        ]
        pygame.draw.polygon(screen, color, tuft)


def draw_feminine_hair(screen, head, color, citizen):
    style = hair_style(citizen, 7)
    if style == 0:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x - 1, head.y - 4, head.width + 2, head.height // 2))
        pygame.draw.line(screen, adjust_color(color, 34), (head.centerx - 4, head.y), (head.centerx - 10, head.y + head.height // 3), 2)
    elif style == 1:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x, head.y - 3, head.width, head.height // 2))
        left_bang = [
            (head.x + 2, head.y + head.height // 4),
            (head.x + head.width // 3, head.y),
            (head.centerx - head.width // 12, head.y + head.height // 5),
        ]
        right_bang = [
            (head.right - 2, head.y + head.height // 4),
            (head.centerx + head.width // 10, head.y),
            (head.centerx - head.width // 14, head.y + head.height // 5),
        ]
        pygame.draw.polygon(screen, color, left_bang)
        pygame.draw.polygon(screen, color, right_bang)
    elif style == 2:
        bun = pygame.Rect(head.centerx - head.width // 5, head.y - head.height // 5, head.width * 2 // 5, head.height // 3)
        pygame.draw.ellipse(screen, adjust_color(color, -8), bun)
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x, head.y - 2, head.width, head.height // 3))
    elif style == 3:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x - 2, head.y - 2, head.width + 4, head.height // 2))
        bang = [
            (head.x + 1, head.y + head.height // 4),
            (head.x + head.width // 3, head.y),
            (head.centerx, head.y + head.height // 5),
            (head.right - 2, head.y + head.height // 5),
        ]
        pygame.draw.polygon(screen, color, bang)
    elif style == 4:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x, head.y - 2, head.width, head.height // 3))
        pony = pygame.Rect(head.right - head.width // 12, head.y + head.height // 4, head.width // 4, head.height // 2)
        pygame.draw.ellipse(screen, adjust_color(color, -10), pony)
    elif style == 5:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x - 1, head.y - 2, head.width + 2, head.height // 2))
        for i in range(4):
            x = head.x + 4 + i * max(2, head.width // 4)
            pygame.draw.circle(screen, adjust_color(color, -8), (x, head.y + head.height // 3), max(2, head.width // 12))
    else:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x + 1, head.y - 3, head.width - 2, head.height // 2))
        pygame.draw.line(screen, adjust_color(color, 36), (head.centerx + 3, head.y), (head.centerx + 9, head.y + head.height // 3), 2)


def draw_masculine_hair(screen, head, color, citizen, group):
    style = hair_style(citizen, 6)
    if group == "elder" and style in {2, 5}:
        pygame.draw.arc(screen, color, pygame.Rect(head.x + 2, head.y, head.width - 4, head.height // 3), math.pi, math.tau, max(2, head.width // 12))
    elif style == 0:
        cap = pygame.Rect(head.x + 1, head.y - 2, head.width - 2, head.height // 2)
        pygame.draw.arc(screen, color, cap, math.pi, math.tau, max(3, head.width // 7))
        pygame.draw.line(screen, color, (head.x + 4, head.y + head.height // 4), (head.right - 4, head.y + head.height // 5), max(2, head.width // 10))
    elif style == 1:
        fringe = [
            (head.x + 2, head.y + head.height // 4),
            (head.x + head.width // 4, head.y),
            (head.centerx, head.y + head.height // 5),
            (head.x + head.width * 3 // 4, head.y),
            (head.right - 2, head.y + head.height // 4),
        ]
        pygame.draw.polygon(screen, color, fringe)
    elif style == 2:
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x, head.y - 3, head.width, head.height // 3))
    elif style == 3:
        part_y = head.y + head.height // 5
        pygame.draw.ellipse(screen, color, pygame.Rect(head.x + 1, head.y - 2, head.width - 2, head.height // 2))
        pygame.draw.line(screen, adjust_color(color, 35), (head.centerx - 2, head.y + 1), (head.centerx - 7, part_y), 2)
    elif style == 4:
        pygame.draw.rect(screen, color, pygame.Rect(head.x + 2, head.y + 1, head.width - 4, head.height // 5), border_radius=max(2, head.width // 10))
    else:
        pygame.draw.arc(screen, color, pygame.Rect(head.x + 2, head.y, head.width - 4, head.height // 3), math.pi, math.tau, max(2, head.width // 12))


def draw_face(screen, head, citizen, group, child_band=None):
    gender = getattr(citizen, "gender", "m")
    eye_y = head.y + int(head.height * 0.48)
    eye_dx = max(4, head.width // 5)
    eye_radius = max(1, head.width // 18)
    for eye_x in (head.centerx - eye_dx, head.centerx + eye_dx):
        pygame.draw.circle(screen, (30, 35, 39), (eye_x, eye_y), eye_radius)
        if gender == "f" and group != "child":
            pygame.draw.line(screen, (30, 35, 39), (eye_x - eye_radius - 1, eye_y - 2), (eye_x - eye_radius - 4, eye_y - 4), 1)
            pygame.draw.line(screen, (30, 35, 39), (eye_x + eye_radius + 1, eye_y - 2), (eye_x + eye_radius + 4, eye_y - 4), 1)

    if citizen.health < 60:
        shadow = (92, 76, 82)
        pygame.draw.line(screen, shadow, (head.centerx - eye_dx - 3, eye_y + 4), (head.centerx - eye_dx + 3, eye_y + 5), 1)
        pygame.draw.line(screen, shadow, (head.centerx + eye_dx - 3, eye_y + 4), (head.centerx + eye_dx + 3, eye_y + 5), 1)
        brow_y = max(head.y + 2, eye_y - head.height // 5)
        pygame.draw.line(screen, shadow, (head.centerx - eye_dx - 4, brow_y), (head.centerx - eye_dx + 4, brow_y + 2), 1)
        pygame.draw.line(screen, shadow, (head.centerx + eye_dx - 4, brow_y + 2), (head.centerx + eye_dx + 4, brow_y), 1)
    if citizen.health < 35:
        sweat = (82, 163, 209)
        drop_x = head.right - max(3, head.width // 8)
        drop_y = eye_y - max(2, head.height // 8)
        pygame.draw.circle(screen, sweat, (drop_x, drop_y), max(2, head.width // 18))
        pygame.draw.polygon(screen, sweat, [
            (drop_x, drop_y - max(4, head.height // 8)),
            (drop_x - max(2, head.width // 20), drop_y),
            (drop_x + max(2, head.width // 20), drop_y),
        ])

    if gender == "f" and group != "child":
        blush = adjust_color(stable_choice(citizen, SKIN_TONES, "skin"), 18)
        pygame.draw.circle(screen, blush, (head.centerx - eye_dx - max(2, head.width // 9), eye_y + head.height // 7), max(1, head.width // 18))
        pygame.draw.circle(screen, blush, (head.centerx + eye_dx + max(2, head.width // 9), eye_y + head.height // 7), max(1, head.width // 18))
    elif gender == "m" and group == "adult" and stable_int(citizen, "facial-hair") % 3 == 0:
        beard = adjust_color(stable_choice(citizen, HAIR_COLORS, "hair"), 8)
        beard_rect = pygame.Rect(head.centerx - head.width // 4, head.y + head.height * 2 // 3, head.width // 2, head.height // 5)
        pygame.draw.arc(screen, beard, beard_rect, 0, math.pi, max(1, head.width // 14))

    mouth_y = head.y + int(head.height * 0.72)
    mouth_w = max(6, head.width // 3)
    happiness = max(0.0, min(100.0, citizen.happiness))
    mouth_color = stable_choice(citizen, FEMININE_ACCENTS, "lip") if gender == "f" and group != "child" else (104, 52, 55)
    if happiness >= 60:
        rect = pygame.Rect(head.centerx - mouth_w // 2, mouth_y - 5, mouth_w, 10)
        pygame.draw.arc(screen, mouth_color, rect, math.pi, math.tau, 2)
    elif happiness <= 35:
        rect = pygame.Rect(head.centerx - mouth_w // 2, mouth_y, mouth_w, 10)
        pygame.draw.arc(screen, mouth_color, rect, 0, math.pi, 2)
    else:
        pygame.draw.line(screen, mouth_color, (head.centerx - mouth_w // 2, mouth_y), (head.centerx + mouth_w // 2, mouth_y), 2)

    if group == "elder":
        pygame.draw.line(screen, (125, 103, 92), (head.x + head.width // 5, eye_y + 5), (head.x + head.width // 3, eye_y + 7), 1)
        pygame.draw.line(screen, (125, 103, 92), (head.right - head.width // 5, eye_y + 5), (head.right - head.width // 3, eye_y + 7), 1)
    elif group == "child":
        if child_band == "toddler":
            pygame.draw.circle(screen, (232, 126, 129), (head.centerx - eye_dx - max(2, head.width // 8), eye_y + head.height // 7), max(1, head.width // 18))
            pygame.draw.circle(screen, (232, 126, 129), (head.centerx + eye_dx + max(2, head.width // 8), eye_y + head.height // 7), max(1, head.width // 18))
        elif child_band == "teen" and gender == "f":
            pygame.draw.line(screen, (30, 35, 39), (head.centerx - eye_dx - eye_radius - 1, eye_y - 2), (head.centerx - eye_dx - eye_radius - 4, eye_y - 4), 1)
            pygame.draw.line(screen, (30, 35, 39), (head.centerx + eye_dx + eye_radius + 1, eye_y - 2), (head.centerx + eye_dx + eye_radius + 4, eye_y - 4), 1)


def draw_accessories(screen, head, citizen, group, child_band=None):
    if getattr(citizen, "gender", "m") == "f" and group != "child":
        accent = stable_choice(citizen, FEMININE_ACCENTS, "earrings")
        y = head.y + int(head.height * 0.56)
        pygame.draw.circle(screen, accent, (head.x + 1, y), max(1, head.width // 22))
        pygame.draw.circle(screen, accent, (head.right - 1, y), max(1, head.width // 22))
    elif getattr(citizen, "gender", "m") == "m" and group == "child" and child_band == "school":
        cap = pygame.Rect(head.x + head.width // 3, head.y - head.height // 10, head.width // 2, head.height // 6)
        pygame.draw.rect(screen, (45, 79, 135), cap, border_radius=max(2, head.width // 12))
    elif getattr(citizen, "gender", "m") == "f" and group == "child" and child_band == "teen":
        accent = stable_choice(citizen, FEMININE_ACCENTS, "teen-earring")
        y = head.y + int(head.height * 0.58)
        pygame.draw.circle(screen, accent, (head.x + 1, y), max(1, head.width // 25))
        pygame.draw.circle(screen, accent, (head.right - 1, y), max(1, head.width // 25))
    if citizen.education >= 70:
        y = head.y + int(head.height * 0.48)
        left = pygame.Rect(head.centerx - head.width // 3, y - 4, head.width // 4, 8)
        right = pygame.Rect(head.centerx + head.width // 12, y - 4, head.width // 4, 8)
        pygame.draw.rect(screen, (42, 49, 55), left, 1, border_radius=3)
        pygame.draw.rect(screen, (42, 49, 55), right, 1, border_radius=3)
        pygame.draw.line(screen, (42, 49, 55), left.midright, right.midleft, 1)


def draw_role_detail(screen, shoulders, role):
    pygame.draw.line(screen, (225, 229, 224), (shoulders.centerx, shoulders.y + 2), (shoulders.centerx, shoulders.bottom - 4), 1)
    if role == "student":
        pygame.draw.line(screen, (236, 232, 199), shoulders.midtop, (shoulders.centerx, shoulders.y + shoulders.height - 4), 2)
    elif role == "commercial":
        badge = pygame.Rect(shoulders.centerx + shoulders.width // 10, shoulders.y + 5, shoulders.width // 5, shoulders.height // 4)
        pygame.draw.rect(screen, (232, 238, 218), badge, border_radius=2)
    elif role == "industrial":
        pygame.draw.line(screen, (242, 203, 73), (shoulders.x + shoulders.width // 5, shoulders.y + 5), (shoulders.right - shoulders.width // 6, shoulders.bottom - 4), 3)
    elif role == "civic":
        pygame.draw.circle(screen, (69, 91, 113), (shoulders.centerx, shoulders.y + shoulders.height // 3), max(2, shoulders.width // 18))
    elif role == "utility":
        bolt = [
            (shoulders.centerx - 3, shoulders.y + 4),
            (shoulders.centerx + 4, shoulders.y + 4),
            (shoulders.centerx, shoulders.y + shoulders.height // 2),
            (shoulders.centerx + 6, shoulders.y + shoulders.height // 2),
            (shoulders.centerx - 3, shoulders.bottom - 4),
        ]
        pygame.draw.lines(screen, (240, 215, 87), False, bolt, 2)
    elif role == "transport":
        pygame.draw.line(screen, (222, 218, 194), (shoulders.x + shoulders.width // 4, shoulders.y + 4), (shoulders.right - shoulders.width // 5, shoulders.bottom - 4), 2)
