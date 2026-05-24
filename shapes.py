import pygame


def darken(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color)


def clamp(value, low, high):
    return max(low, min(high, value))


def offset_point(point, dx, dy):
    return point[0] + dx, point[1] + dy


def lerp_point(a, b, t):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def draw_sign(self, text, center, text_color, fill_color, outline_color, pad=(10, 5)):
    sign = self.small.render(text, True, text_color)
    rect = pygame.Rect(0, 0, sign.get_width() + pad[0], sign.get_height() + pad[1])
    rect.center = (int(center[0]), int(center[1]))
    radius = max(2, int(3 * self.camera.zoom))
    pygame.draw.rect(self.screen, fill_color, rect, border_radius=radius)
    pygame.draw.rect(self.screen, outline_color, rect, 1, border_radius=radius)
    self.screen.blit(sign, sign.get_rect(center=rect.center))


def draw_outlined_polygon(self, poly, fill_color, outline_color, width=1):
    pygame.draw.polygon(self.screen, fill_color, poly)
    pygame.draw.polygon(self.screen, outline_color, poly, width)
    return poly


def draw_roof_trim(self, roof, roof_color, edge_factor, trim_offset, trim_faces):
    pygame.draw.polygon(self.screen, roof_color, roof)
    pygame.draw.polygon(self.screen, darken(roof_color, edge_factor), roof, max(1, int(self.camera.zoom)))
    trim = [offset_point(p, 0, trim_offset) for p in roof]
    face_points = {
        "right": [trim[1], trim[2], roof[2], roof[1]],
        "front": [trim[2], trim[3], roof[3], roof[2]],
    }
    for face, color in trim_faces:
        pygame.draw.polygon(self.screen, color, face_points[face])


def draw_vertical_rect(self, center, half_width, y0, y1, fill_color, outline_color):
    poly = [
        offset_point(center, -half_width, y0),
        offset_point(center, half_width, y0),
        offset_point(center, half_width, y1),
        offset_point(center, -half_width, y1),
    ]
    return draw_outlined_polygon(self, poly, fill_color, outline_color)


def draw_zone_lot(self, x, y, sx, sy, color):
    poly = self.tile_top_poly(x, y)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    rect = pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)).inflate(2, 2)
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    shifted = [(px - rect.x, py - rect.y) for px, py in poly]
    fill = color
    edge = darken(color, 0.72)
    pygame.draw.polygon(overlay, fill, shifted)
    pygame.draw.polygon(overlay, edge, shifted, max(1, int(2 * self.camera.zoom)))
    self.screen.blit(overlay, rect)

def draw_residential_house(self, x, y, sx, sy, lot_color):
    z = self.camera.zoom
    self.draw_zone_lot(x, y, sx, sy, lot_color)
    base_lift = self.tile_lift(x, y)
    house_base = self.iso_rect_poly(x, y, 1, 1, 0.22, base_lift=base_lift)
    h = 14 * z
    wall_top = [offset_point(p, 0, -h) for p in house_base]
    right = [house_base[1], house_base[2], wall_top[2], wall_top[1]]
    front = [house_base[2], house_base[3], wall_top[3], wall_top[2]]
    left = [house_base[3], house_base[0], wall_top[0], wall_top[3]]
    pygame.draw.polygon(self.screen, (198, 183, 148), left)
    pygame.draw.polygon(self.screen, (225, 211, 174), right)
    pygame.draw.polygon(self.screen, (213, 198, 162), front)

    ridge_a = lerp_point(wall_top[0], wall_top[1], 0.5)
    ridge_b = lerp_point(wall_top[3], wall_top[2], 0.5)
    ridge_a = offset_point(ridge_a, 0, -10 * z)
    ridge_b = offset_point(ridge_b, 0, -10 * z)
    roof_color = (134, 72, 58)
    roof_left = [wall_top[0], wall_top[3], ridge_b, ridge_a]
    roof_right = [wall_top[1], wall_top[2], ridge_b, ridge_a]
    pygame.draw.polygon(self.screen, darken(roof_color, 0.78), roof_left)
    pygame.draw.polygon(self.screen, roof_color, roof_right)
    pygame.draw.polygon(self.screen, (55, 45, 40), roof_left, 1)
    pygame.draw.polygon(self.screen, (55, 45, 40), roof_right, 1)

    door_mid = lerp_point(house_base[2], house_base[3], 0.50)
    door = [
        offset_point(door_mid, -4 * z, 0),
        offset_point(door_mid, 4 * z, 0),
        offset_point(door_mid, 3 * z, -9 * z),
        offset_point(door_mid, -3 * z, -9 * z),
    ]
    draw_outlined_polygon(self, door, (92, 65, 47), (46, 34, 27))

    for edge_a, edge_b, t in ((house_base[1], house_base[2], 0.42), (house_base[3], house_base[0], 0.55)):
        p = lerp_point(edge_a, edge_b, t)
        draw_vertical_rect(self, p, 3.5 * z, -7 * z, -11 * z, (166, 210, 232), (74, 82, 84))

    chimney_base = lerp_point(ridge_a, ridge_b, 0.28)
    chimney = [
        offset_point(chimney_base, -3 * z, 2 * z),
        offset_point(chimney_base, 3 * z, 2 * z),
        offset_point(chimney_base, 3 * z, -7 * z),
        offset_point(chimney_base, -3 * z, -7 * z),
    ]
    draw_outlined_polygon(self, chimney, (112, 69, 54), (50, 38, 32))

def draw_commercial_shop(self, x, y, sx, sy, lot_color):
    z = self.camera.zoom
    self.draw_zone_lot(x, y, sx, sy, lot_color)
    base_lift = self.tile_lift(x, y)
    shop_base = self.iso_rect_poly(x, y, 1, 1, 0.18, base_lift=base_lift)
    h = 16 * z
    roof = [offset_point(p, 0, -h) for p in shop_base]
    right = [shop_base[1], shop_base[2], roof[2], roof[1]]
    front = [shop_base[2], shop_base[3], roof[3], roof[2]]
    left = [shop_base[3], shop_base[0], roof[0], roof[3]]
    pygame.draw.polygon(self.screen, (163, 179, 197), left)
    pygame.draw.polygon(self.screen, (198, 213, 229), right)
    pygame.draw.polygon(self.screen, (184, 199, 216), front)

    roof_cap = [offset_point(p, 0, -4 * z) for p in roof]
    draw_outlined_polygon(self, roof_cap, (57, 83, 142), (34, 43, 70))
    fascia = [offset_point(p, 0, 4 * z) for p in roof_cap]
    pygame.draw.polygon(self.screen, (43, 66, 121), [fascia[2], fascia[3], roof_cap[3], roof_cap[2]])

    front_a, front_b = shop_base[3], shop_base[2]
    glass_a = lerp_point(front_a, front_b, 0.18)
    glass_b = lerp_point(front_a, front_b, 0.82)
    glass = [glass_a, glass_b, offset_point(glass_b, 0, -11 * z), offset_point(glass_a, 0, -11 * z)]
    draw_outlined_polygon(self, glass, (122, 190, 225), (52, 74, 91))
    pygame.draw.line(self.screen, (52, 74, 91), lerp_point(glass[0], glass[1], 0.5), lerp_point(glass[3], glass[2], 0.5), 1)

    awning = [
        offset_point(glass_a, 0, -12 * z),
        offset_point(glass_b, 0, -12 * z),
        offset_point(glass_b, 0, -17 * z),
        offset_point(glass_a, 0, -17 * z),
    ]
    draw_outlined_polygon(self, awning, (238, 205, 86), (101, 79, 37))

    sign_mid = lerp_point(front_a, front_b, 0.5)
    draw_sign(self, "SHOP", (sign_mid[0], sign_mid[1] - 23 * z), (245, 248, 252), (44, 74, 143), (239, 210, 92), pad=(8, 4))

    side_a, side_b = shop_base[1], shop_base[2]
    side_window_mid = lerp_point(side_a, side_b, 0.48)
    draw_vertical_rect(self, side_window_mid, 4 * z, -8 * z, -12 * z, (151, 205, 229), (52, 74, 91))

def draw_industrial_workshop(self, x, y, sx, sy, lot_color):
    z = self.camera.zoom
    self.draw_zone_lot(x, y, sx, sy, lot_color)
    base_lift = self.tile_lift(x, y)
    shop_base = self.iso_rect_poly(x, y, 1, 1, 0.17, base_lift=base_lift)
    h = 15 * z
    roof = [offset_point(p, 0, -h) for p in shop_base]
    right = [shop_base[1], shop_base[2], roof[2], roof[1]]
    front = [shop_base[2], shop_base[3], roof[3], roof[2]]
    left = [shop_base[3], shop_base[0], roof[0], roof[3]]
    pygame.draw.polygon(self.screen, (126, 116, 100), left)
    pygame.draw.polygon(self.screen, (158, 145, 119), right)
    pygame.draw.polygon(self.screen, (145, 132, 108), front)

    roof_left = [roof[0], roof[3], offset_point(lerp_point(roof[3], roof[2], 0.5), 0, -7 * z), offset_point(lerp_point(roof[0], roof[1], 0.5), 0, -7 * z)]
    roof_right = [roof[1], roof[2], roof_left[2], roof_left[3]]
    pygame.draw.polygon(self.screen, (91, 93, 91), roof_left)
    pygame.draw.polygon(self.screen, (112, 115, 112), roof_right)
    pygame.draw.polygon(self.screen, (48, 50, 49), roof_left, 1)
    pygame.draw.polygon(self.screen, (48, 50, 49), roof_right, 1)

    front_a, front_b = shop_base[3], shop_base[2]
    bay_a = lerp_point(front_a, front_b, 0.20)
    bay_b = lerp_point(front_a, front_b, 0.58)
    bay = [bay_a, bay_b, offset_point(bay_b, 0, -11 * z), offset_point(bay_a, 0, -11 * z)]
    draw_outlined_polygon(self, bay, (82, 79, 72), (38, 36, 34))
    for i in range(1, 3):
        pygame.draw.line(self.screen, (122, 116, 98), lerp_point(bay[0], bay[3], i / 3), lerp_point(bay[1], bay[2], i / 3), 1)

    office_mid = lerp_point(front_a, front_b, 0.78)
    draw_vertical_rect(self, office_mid, 4 * z, -8 * z, -12 * z, (178, 203, 214), (58, 62, 61))

    stack_base = lerp_point(roof_left[3], roof_left[2], 0.65)
    sw = 4 * z
    stack_h = 20 * z
    stack = [
        offset_point(stack_base, -sw, 2 * z),
        offset_point(stack_base, sw, 2 * z),
        offset_point(stack_base, sw, -stack_h),
        offset_point(stack_base, -sw, -stack_h),
    ]
    draw_outlined_polygon(self, stack, (86, 78, 68), (38, 35, 32))
    pygame.draw.circle(self.screen, (105, 103, 97), (int(stack_base[0]), int(stack_base[1] - stack_h - 5 * z)), max(2, int(4 * z)))

    pipe_a = lerp_point(shop_base[1], shop_base[2], 0.35)
    pipe_b = lerp_point(shop_base[1], shop_base[2], 0.72)
    pygame.draw.line(self.screen, (64, 69, 68), offset_point(pipe_a, 0, -5 * z), offset_point(pipe_b, 0, -8 * z), max(2, int(3 * z)))

def draw_garbage_zone(self, x, y, sx, sy, lot_color, fill_ratio=0.0):
    z = self.camera.zoom
    self.draw_zone_lot(x, y, sx, sy, lot_color)
    lift = self.tile_lift(x, y)
    outline = (44, 47, 39)
    fill_ratio = clamp(fill_ratio, 0.0, 1.0)

    def ground(wx, wy, y_offset=0):
        px, py = self.camera.world_to_screen(wx, wy)
        return px, py - lift + y_offset

    for wx in (x - 0.34, x + 0.0, x + 0.34):
        post_base = ground(wx, y - 0.36)
        pygame.draw.line(self.screen, (65, 58, 48), post_base, offset_point(post_base, 0, -10 * z), max(1, int(2 * z)))
    pygame.draw.line(self.screen, (92, 82, 63), ground(x - 0.42, y - 0.34, -7 * z), ground(x + 0.42, y - 0.34, -7 * z), max(1, int(2 * z)))

    basin = self.iso_rect_poly(x, y, 1, 1, 0.20, base_lift=lift)
    pygame.draw.polygon(self.screen, (76, 87, 67), basin, max(1, int(z)))
    if fill_ratio <= 0.05:
        return

    heap_specs = ((-0.16, -0.02, (83, 91, 73)), (0.14, 0.16, (116, 103, 72)), (0.30, -0.12, (97, 101, 89)))
    heap_count = max(1, min(len(heap_specs), int(fill_ratio * len(heap_specs) + 0.999)))
    heap_scale = 0.45 + fill_ratio * 0.75
    for cx, cy, color in heap_specs[:heap_count]:
        p = ground(x + cx, y + cy)
        heap = [
            offset_point(p, -9 * z * heap_scale, 1 * z),
            offset_point(p, 0, -9 * z * heap_scale),
            offset_point(p, 10 * z * heap_scale, 2 * z),
            offset_point(p, 3 * z, 6 * z * heap_scale),
        ]
        draw_outlined_polygon(self, heap, color, outline)

    if fill_ratio < 0.45:
        return

    for wx, wy, color in ((x - 0.27, y + 0.27, (135, 74, 54)), (x + 0.07, y + 0.34, (65, 86, 102))):
        p = ground(wx, wy, -3 * z)
        rect = pygame.Rect(p[0] - 4 * z, p[1] - 8 * z, 8 * z, 9 * z)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, outline, rect, max(1, int(z)))
        pygame.draw.ellipse(self.screen, darken(color, 1.25), rect.inflate(0, -5 * z))

    if fill_ratio < 0.70:
        return

    litter_specs = ((x - 0.34, y + 0.06), (x + 0.36, y + 0.30), (x + 0.04, y - 0.28))
    litter_count = max(1, min(len(litter_specs), int(fill_ratio * len(litter_specs) + 0.999)))
    for wx, wy in litter_specs[:litter_count]:
        p = ground(wx, wy, -2 * z)
        pygame.draw.circle(self.screen, (197, 190, 142), (int(p[0]), int(p[1])), max(1, int(2 * z)))

def draw_large_park(self, x, y, fw, fh):
    z = self.camera.zoom
    lift = self.tile_lift(x, y)
    outline = (38, 91, 51)

    def ground(wx, wy, y_offset=0):
        sx, sy = self.camera.world_to_screen(wx, wy)
        return sx, sy - lift + y_offset

    grass = self.iso_rect_poly(x, y, fw, fh, 0.05, base_lift=lift)
    draw_outlined_polygon(self, grass, (72, 158, 86), outline)

    west = ground(x - 0.42, y + 1.45)
    east = ground(x + fw - 0.58, y + 1.45)
    north = ground(x + 1.45, y - 0.42)
    south = ground(x + 1.45, y + fh - 0.58)
    center = ground(x + 1.45, y + 1.45, -2 * z)
    for a, b in ((west, center), (center, east), (north, center), (center, south)):
        pygame.draw.line(self.screen, (150, 132, 91), a, b, max(5, int(7 * z)))
        pygame.draw.line(self.screen, (224, 209, 149), a, b, max(3, int(4 * z)))

    plaza = pygame.Rect(0, 0, int(24 * z), int(12 * z))
    plaza.center = center
    pygame.draw.ellipse(self.screen, (211, 192, 136), plaza)
    pygame.draw.ellipse(self.screen, (119, 102, 70), plaza, max(1, int(z)))
    pygame.draw.circle(self.screen, (86, 150, 174), (int(center[0]), int(center[1] - 2 * z)), max(4, int(7 * z)))
    pygame.draw.circle(self.screen, (151, 211, 220), (int(center[0]), int(center[1] - 4 * z)), max(2, int(3 * z)))

    pond = pygame.Rect(0, 0, int(42 * z), int(18 * z))
    pond.center = ground(x + 2.10, y + 0.78, -1 * z)
    pygame.draw.ellipse(self.screen, (48, 126, 151), pond)
    pygame.draw.ellipse(self.screen, (132, 199, 207), pond.inflate(-7 * z, -5 * z), max(1, int(z)))

    for wx, wy, color in (
        (x + 0.64, y + 0.55, (232, 91, 106)),
        (x + 0.92, y + 0.78, (242, 210, 82)),
        (x + 0.55, y + 2.18, (207, 111, 214)),
        (x + 2.25, y + 2.20, (239, 145, 83)),
    ):
        p = ground(wx, wy, -2 * z)
        for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
            pygame.draw.circle(self.screen, color, (int(p[0] + ox * z), int(p[1] + oy * z)), max(1, int(2 * z)))

    for wx, wy in ((x + 0.48, y + 0.55), (x + 1.08, y + 0.42), (x + 2.42, y + 0.58), (x + 0.52, y + 1.38), (x + 2.44, y + 1.42), (x + 0.66, y + 2.38), (x + 1.58, y + 2.34), (x + 2.34, y + 2.28)):
        p = ground(wx, wy, -5 * z)
        self.draw_tree(p[0], p[1])

    for wx, wy in ((x + 0.94, y + 1.23), (x + 1.86, y + 1.76)):
        a = ground(wx - 0.16, wy, -2 * z)
        b = ground(wx + 0.16, wy, -2 * z)
        pygame.draw.line(self.screen, (94, 62, 43), a, b, max(2, int(3 * z)))
        pygame.draw.line(self.screen, (58, 45, 38), offset_point(a, 0, 3 * z), offset_point(b, 0, 3 * z), max(1, int(2 * z)))

def draw_police_station(self, x, y, fw, fh):
    z = self.camera.zoom
    wall = (207, 214, 221)
    side = (145, 158, 176)
    roof_blue = (43, 82, 158)
    h = 31 * z
    cx, cy, roof, base = self.draw_iso_prism(x, y, fw, fh, h, wall, side, inset=0.08)

    draw_roof_trim(self, roof, roof_blue, 0.58, 5 * z, (("right", darken(roof_blue, 0.72)), ("front", darken(roof_blue, 0.62))))

    awning = [
        lerp_point(base[2], base[3], 0.34),
        lerp_point(base[2], base[3], 0.66),
        lerp_point(base[2], base[3], 0.66),
        lerp_point(base[2], base[3], 0.34),
    ]
    awning[0] = offset_point(awning[0], 0, -17 * z)
    awning[1] = offset_point(awning[1], 0, -17 * z)
    awning[2] = offset_point(awning[2], 0, -24 * z)
    awning[3] = offset_point(awning[3], 0, -24 * z)
    draw_outlined_polygon(self, awning, (35, 70, 143), (22, 35, 62))

    door_center = lerp_point(base[2], base[3], 0.5)
    door_top = offset_point(door_center, 0, -18 * z)
    door_w = 8 * z
    door = [
        offset_point(door_center, -door_w, 0),
        offset_point(door_center, door_w, 0),
        offset_point(door_top, door_w * 0.55, 0),
        offset_point(door_top, -door_w * 0.55, 0),
    ]
    draw_outlined_polygon(self, door, (42, 58, 76), (18, 24, 32))

    step_a = lerp_point(base[2], base[3], 0.38)
    step_b = lerp_point(base[2], base[3], 0.62)
    step = [step_a, step_b, offset_point(step_b, 0, 5 * z), offset_point(step_a, 0, 5 * z)]
    pygame.draw.polygon(self.screen, (118, 124, 130), step)

    for a, b, count, lo, hi in ((base[1], base[2], 3, 0.20, 0.80), (base[3], base[0], 2, 0.25, 0.75)):
        for i in range(count):
            t = lo + (hi - lo) * (i + 1) / (count + 1)
            p = lerp_point(a, b, t)
            draw_vertical_rect(self, p, 5 * z, -11 * z, -17 * z, (168, 207, 236), (65, 82, 100))

    front_mid = lerp_point(base[2], base[3], 0.5)
    draw_sign(self, "POLICE", (front_mid[0], front_mid[1] - 28 * z), (245, 248, 252), (28, 58, 122), (236, 210, 92))

    mast_x, mast_y = cx + 24 * z, cy - 2 * z
    pygame.draw.line(self.screen, (42, 45, 50), (mast_x, mast_y), (mast_x, mast_y - 18 * z), max(1, int(2 * z)))
    pygame.draw.circle(self.screen, (235, 55, 65), (int(mast_x - 4 * z), int(mast_y - 18 * z)), max(2, int(3 * z)))
    pygame.draw.circle(self.screen, (83, 145, 244), (int(mast_x + 4 * z), int(mast_y - 18 * z)), max(2, int(3 * z)))

def draw_fire_station(self, x, y, fw, fh):
    z = self.camera.zoom
    wall = (190, 55, 48)
    side = (132, 46, 43)
    roof = (96, 39, 37)
    h = 30 * z
    cx, cy, roof_poly, base = self.draw_iso_prism(x, y, fw, fh, h, wall, side, inset=0.08)

    draw_roof_trim(self, roof_poly, roof, 0.58, 5 * z, (("front", (222, 206, 166)), ("right", darken(roof, 0.72))))

    front_a, front_b = base[3], base[2]
    for lo, hi in ((0.18, 0.43), (0.57, 0.82)):
        low_a = lerp_point(front_a, front_b, lo)
        low_b = lerp_point(front_a, front_b, hi)
        high_a = offset_point(low_a, 0, -23 * z)
        high_b = offset_point(low_b, 0, -23 * z)
        door = [low_a, low_b, high_b, high_a]
        draw_outlined_polygon(self, door, (232, 223, 199), (82, 44, 40))
        for i in range(1, 4):
            a = lerp_point(low_a, high_a, i / 4)
            b = lerp_point(low_b, high_b, i / 4)
            pygame.draw.line(self.screen, (170, 65, 55), a, b, max(1, int(z)))

    front_mid = lerp_point(front_a, front_b, 0.5)
    draw_sign(self, "FIRE", (front_mid[0], front_mid[1] - 31 * z), (255, 243, 210), (116, 34, 30), (241, 199, 91))

    side_a, side_b = base[1], base[2]
    for t in (0.30, 0.55, 0.78):
        p = lerp_point(side_a, side_b, t)
        draw_vertical_rect(self, p, 4.5 * z, -13 * z, -19 * z, (246, 203, 122), (85, 45, 42))

    tower_x, tower_y = x + 0.35, y + 0.20
    tx, ty = self.camera.world_to_screen(tower_x, tower_y)
    ty -= self.tile_lift(x, y) + h
    tw = 9 * z
    tower_h = 34 * z
    body = [(tx - tw, ty), (tx, ty + tw * 0.45), (tx, ty + tw * 0.45 - tower_h), (tx - tw, ty - tower_h)]
    side_poly = [(tx, ty + tw * 0.45), (tx + tw, ty), (tx + tw, ty - tower_h), (tx, ty + tw * 0.45 - tower_h)]
    cap = [(tx - tw, ty - tower_h), (tx, ty - tower_h - tw * 0.45), (tx + tw, ty - tower_h), (tx, ty + tw * 0.45 - tower_h)]
    pygame.draw.polygon(self.screen, (157, 45, 40), body)
    pygame.draw.polygon(self.screen, (124, 37, 35), side_poly)
    pygame.draw.polygon(self.screen, (88, 36, 34), cap)
    pygame.draw.polygon(self.screen, (44, 32, 30), body, 1)
    pygame.draw.polygon(self.screen, (44, 32, 30), side_poly, 1)
    bell = (int(tx), int(ty - tower_h - 9 * z))
    pygame.draw.circle(self.screen, (230, 183, 70), bell, max(3, int(5 * z)))

def draw_school(self, x, y, fw, fh):
    z = self.camera.zoom
    brick = (178, 114, 77)
    side = (132, 91, 68)
    roof = (92, 84, 74)
    h = 28 * z
    cx, cy, roof_poly, base = self.draw_iso_prism(x, y, fw, fh, h, brick, side, inset=0.08)

    draw_roof_trim(self, roof_poly, roof, 0.58, 4 * z, (("front", (223, 202, 157)), ("right", darken(roof, 0.72))))

    front_a, front_b = base[3], base[2]
    door_mid = lerp_point(front_a, front_b, 0.5)
    door_top = offset_point(door_mid, 0, -18 * z)
    door_w = 8 * z
    door = [
        offset_point(door_mid, -door_w, 0),
        offset_point(door_mid, door_w, 0),
        offset_point(door_top, door_w * 0.58, 0),
        offset_point(door_top, -door_w * 0.58, 0),
    ]
    draw_outlined_polygon(self, door, (72, 68, 62), (42, 35, 30))

    columns = (0.30, 0.70)
    for t in columns:
        p = lerp_point(front_a, front_b, t)
        w = 4 * z
        column = [
            offset_point(p, -w, 0),
            offset_point(p, w, 0),
            offset_point(p, w * 0.55, -24 * z),
            offset_point(p, -w * 0.55, -24 * z),
        ]
        draw_outlined_polygon(self, column, (216, 196, 148), (112, 86, 64))

    for a, b, count, lo, hi in ((base[1], base[2], 4, 0.16, 0.84), (base[3], base[0], 3, 0.20, 0.80)):
        for i in range(count):
            t = lo + (hi - lo) * (i + 1) / (count + 1)
            p = lerp_point(a, b, t)
            window = draw_vertical_rect(self, p, 4.5 * z, -11 * z, -17 * z, (181, 216, 231), (86, 69, 56))
            pygame.draw.line(self.screen, (86, 69, 56), lerp_point(window[0], window[1], 0.5), lerp_point(window[3], window[2], 0.5), 1)

    draw_sign(self, "SCHOOL", (door_mid[0], door_mid[1] - 28 * z), (52, 42, 34), (232, 211, 152), (94, 72, 52))

    flag_x, flag_y = cx + 23 * z, cy + 2 * z
    pygame.draw.line(self.screen, (62, 58, 52), (flag_x, flag_y), (flag_x, flag_y - 25 * z), max(1, int(2 * z)))
    flag = [
        (flag_x, flag_y - 25 * z),
        (flag_x + 17 * z, flag_y - 21 * z),
        (flag_x, flag_y - 17 * z),
    ]
    pygame.draw.polygon(self.screen, (72, 116, 184), flag)

    bell_x, bell_y = cx - 17 * z, cy - 10 * z
    pygame.draw.circle(self.screen, (218, 176, 72), (int(bell_x), int(bell_y)), max(3, int(5 * z)))
    pygame.draw.line(self.screen, (95, 73, 45), (bell_x - 7 * z, bell_y + 5 * z), (bell_x + 7 * z, bell_y + 5 * z), max(1, int(z)))

def draw_clinic(self, x, y, fw, fh):
    z = self.camera.zoom
    wall = (236, 240, 242)
    side = (168, 181, 190)
    roof = (198, 218, 229)
    red = (205, 45, 58)
    h = 30 * z
    cx, cy, roof_poly, base = self.draw_iso_prism(x, y, fw, fh, h, wall, side, inset=0.08)

    draw_roof_trim(self, roof_poly, roof, 0.62, 5 * z, (("front", (218, 232, 239)), ("right", darken(roof, 0.78))))

    front_a, front_b = base[3], base[2]
    entry_mid = lerp_point(front_a, front_b, 0.5)
    entry_top = offset_point(entry_mid, 0, -20 * z)
    entry_w = 10 * z
    entry = [
        offset_point(entry_mid, -entry_w, 0),
        offset_point(entry_mid, entry_w, 0),
        offset_point(entry_top, entry_w * 0.62, 0),
        offset_point(entry_top, -entry_w * 0.62, 0),
    ]
    draw_outlined_polygon(self, entry, (116, 154, 174), (58, 78, 90))
    pygame.draw.line(self.screen, (224, 240, 246), entry_mid, entry_top, max(1, int(z)))

    canopy = [
        offset_point(lerp_point(front_a, front_b, 0.33), 0, -20 * z),
        offset_point(lerp_point(front_a, front_b, 0.67), 0, -20 * z),
        offset_point(lerp_point(front_a, front_b, 0.62), 0, -27 * z),
        offset_point(lerp_point(front_a, front_b, 0.38), 0, -27 * z),
    ]
    draw_outlined_polygon(self, canopy, red, darken(red, 0.6))

    for a, b, count, lo, hi in ((base[1], base[2], 4, 0.15, 0.85), (base[3], base[0], 3, 0.18, 0.82)):
        for i in range(count):
            t = lo + (hi - lo) * (i + 1) / (count + 1)
            p = lerp_point(a, b, t)
            draw_vertical_rect(self, p, 4.5 * z, -12 * z, -18 * z, (166, 214, 229), (94, 117, 128))

    cross_center = (cx, cy - 1 * z)
    cross_w = 18 * z
    cross_t = 6 * z
    pygame.draw.rect(self.screen, red, (cross_center[0] - cross_t / 2, cross_center[1] - cross_w / 2, cross_t, cross_w))
    pygame.draw.rect(self.screen, red, (cross_center[0] - cross_w / 2, cross_center[1] - cross_t / 2, cross_w, cross_t))
    pygame.draw.rect(self.screen, (92, 36, 42), (cross_center[0] - cross_w / 2, cross_center[1] - cross_t / 2, cross_w, cross_t), 1)

    draw_sign(self, "CLINIC", (entry_mid[0], entry_mid[1] - 32 * z), (250, 250, 250), red, (115, 34, 42))

    bay_a = lerp_point(base[1], base[2], 0.15)
    bay_b = lerp_point(base[1], base[2], 0.40)
    bay = [bay_a, bay_b, offset_point(bay_b, 0, -17 * z), offset_point(bay_a, 0, -17 * z)]
    draw_outlined_polygon(self, bay, (230, 236, 238), (104, 118, 126))
    pygame.draw.line(self.screen, red, lerp_point(bay[0], bay[1], 0.5), lerp_point(bay[3], bay[2], 0.5), max(1, int(2 * z)))

def draw_library(self, x, y, fw, fh):
    z = self.camera.zoom
    stone = (184, 154, 113)
    side = (126, 102, 79)
    roof = (80, 74, 70)
    h = 26 * z
    cx, cy, roof_poly, base = self.draw_iso_prism(x, y, fw, fh, h, stone, side, inset=0.08)

    draw_roof_trim(self, roof_poly, roof, 0.60, 4 * z, (("front", (118, 108, 99)), ("right", (60, 56, 53))))

    front_a, front_b = base[3], base[2]
    entry_mid = lerp_point(front_a, front_b, 0.5)
    entry = [
        offset_point(entry_mid, -11 * z, 0),
        offset_point(entry_mid, 11 * z, 0),
        offset_point(entry_mid, 8 * z, -16 * z),
        offset_point(entry_mid, -8 * z, -16 * z),
    ]
    draw_outlined_polygon(self, entry, (70, 58, 50), (42, 35, 31))

    for t in (0.24, 0.39, 0.61, 0.76):
        p = lerp_point(front_a, front_b, t)
        draw_vertical_rect(self, p, 2.7 * z, 0, -23 * z, (219, 199, 153), (99, 76, 56))

    pediment = [
        offset_point(lerp_point(front_a, front_b, 0.27), 0, -23 * z),
        offset_point(lerp_point(front_a, front_b, 0.73), 0, -23 * z),
        offset_point(entry_mid, 0, -36 * z),
    ]
    draw_outlined_polygon(self, pediment, (205, 182, 134), (96, 74, 54))

    for a, b, count in ((base[1], base[2], 3), (base[3], base[0], 2)):
        for i in range(count):
            p = lerp_point(a, b, (i + 1) / (count + 1))
            draw_vertical_rect(self, p, 4 * z, -10 * z, -16 * z, (147, 190, 210), (74, 67, 59))

    draw_sign(self, "LIBRARY", (entry_mid[0], entry_mid[1] - 29 * z), (58, 46, 35), (226, 204, 148), (95, 72, 51), pad=(8, 4))

    book = [
        offset_point((cx, cy), -15 * z, 1 * z),
        offset_point((cx, cy), 0, -5 * z),
        offset_point((cx, cy), 15 * z, 1 * z),
        offset_point((cx, cy), 0, 7 * z),
    ]
    draw_outlined_polygon(self, book, (128, 53, 62), (60, 42, 38))
    pygame.draw.line(self.screen, (232, 215, 174), book[1], book[3], max(1, int(z)))

def draw_rail_station(self, x, y, fw, fh):
    z = self.camera.zoom
    lift = self.tile_lift(x, y)
    outline = (42, 45, 45)

    def ground(wx, wy, y_offset=0):
        sx, sy = self.camera.world_to_screen(wx, wy)
        return sx, sy - lift + y_offset

    full = self.iso_rect_poly(x, y, fw, fh, 0.02, base_lift=lift)
    draw_outlined_polygon(self, full, (88, 93, 91), outline)

    back_platform = [
        ground(x - 0.42, y - 0.38),
        ground(x + fw - 0.58, y - 0.38),
        ground(x + fw - 0.58, y + 0.48),
        ground(x - 0.42, y + 0.48),
    ]
    front_platform = [
        ground(x - 0.42, y + 1.52),
        ground(x + fw - 0.58, y + 1.52),
        ground(x + fw - 0.58, y + fh - 0.62),
        ground(x - 0.42, y + fh - 0.62),
    ]
    draw_outlined_polygon(self, back_platform, (162, 154, 132), outline)
    draw_outlined_polygon(self, front_platform, (178, 170, 146), outline)

    track_bed = [
        ground(x - 0.55, y + 0.56),
        ground(x + fw - 0.45, y + 0.56),
        ground(x + fw - 0.45, y + 1.44),
        ground(x - 0.55, y + 1.44),
    ]
    draw_outlined_polygon(self, track_bed, (58, 53, 48), (30, 31, 31))
    self.draw_double_rail_segment(ground(x - 0.55, y + 1.0), ground(x + fw - 0.45, y + 1.0), z)

    canopy = self.iso_rect_poly(x + 0.25, y + 0.48, fw - 0.5, 1.05, 0.02, y_offset=-31 * z, base_lift=lift)
    canopy_shadow = [offset_point(p, 0, 6 * z) for p in canopy]
    pygame.draw.polygon(self.screen, (77, 67, 55), [canopy_shadow[2], canopy_shadow[3], canopy[3], canopy[2]])
    pygame.draw.polygon(self.screen, (122, 86, 57), [canopy_shadow[1], canopy_shadow[2], canopy[2], canopy[1]])
    draw_outlined_polygon(self, canopy, (176, 136, 86), outline)
    pygame.draw.line(self.screen, (230, 200, 128), lerp_point(canopy[0], canopy[1], 0.08), lerp_point(canopy[3], canopy[2], 0.08), max(1, int(2 * z)))

    for wx in (x + 0.4, x + 1.4, x + 2.4, x + 3.4, x + 4.4, x + 5.4):
        for wy in (y + 0.55, y + 1.45):
            base = ground(wx, wy)
            top = offset_point(base, 0, -29 * z)
            pygame.draw.line(self.screen, (61, 58, 54), base, top, max(1, int(3 * z)))
            pygame.draw.circle(self.screen, (42, 40, 38), (int(base[0]), int(base[1])), max(1, int(2 * z)))

    hall_h = 24 * z
    cx, cy, roof, base = self.draw_iso_prism(x + 0.55, y - 0.02, 1.95, 0.82, hall_h, (196, 188, 166), (135, 124, 106), inset=0.04, base_lift=lift)
    draw_roof_trim(self, roof, (88, 82, 72), 0.62, 4 * z, (("front", (142, 130, 108)), ("right", (78, 72, 64))))

    front_a, front_b = base[3], base[2]
    door_mid = lerp_point(front_a, front_b, 0.50)
    door = [
        offset_point(door_mid, -7 * z, 0),
        offset_point(door_mid, 7 * z, 0),
        offset_point(door_mid, 6 * z, -15 * z),
        offset_point(door_mid, -6 * z, -15 * z),
    ]
    draw_outlined_polygon(self, door, (62, 74, 82), (34, 38, 42))
    for t in (0.22, 0.78):
        p = lerp_point(front_a, front_b, t)
        draw_vertical_rect(self, p, 4 * z, -10 * z, -15 * z, (151, 199, 220), (74, 82, 86))
    draw_sign(self, "STATION", (door_mid[0], door_mid[1] - 27 * z), (245, 240, 210), (94, 62, 38), (226, 188, 96), pad=(9, 4))

    for wx in (x + 3.0, x + 3.65, x + 4.3):
        bench = [
            ground(wx - 0.18, y + 1.76, -2 * z),
            ground(wx + 0.18, y + 1.76, -2 * z),
            ground(wx + 0.18, y + 1.92, -2 * z),
            ground(wx - 0.18, y + 1.92, -2 * z),
        ]
        draw_outlined_polygon(self, bench, (117, 74, 44), (52, 38, 30))

    clock_base = ground(x + fw - 0.75, y + 0.20)
    clock_top = offset_point(clock_base, 0, -31 * z)
    pygame.draw.line(self.screen, (45, 47, 48), clock_base, clock_top, max(1, int(3 * z)))
    pygame.draw.circle(self.screen, (232, 231, 218), (int(clock_top[0]), int(clock_top[1] - 7 * z)), max(4, int(7 * z)))
    pygame.draw.circle(self.screen, (45, 47, 48), (int(clock_top[0]), int(clock_top[1] - 7 * z)), max(4, int(7 * z)), max(1, int(z)))

def draw_stadium(self, x, y, fw, fh):
    z = self.camera.zoom
    lift = self.tile_lift(x, y)
    outline = (36, 41, 42)

    base = self.iso_rect_poly(x, y, fw, fh, 0.04, base_lift=lift)
    draw_outlined_polygon(self, base, (84, 101, 96), outline)

    outer = self.iso_rect_poly(x + 0.18, y + 0.18, fw - 0.36, fh - 0.36, 0.0, y_offset=-17 * z, base_lift=lift)
    lower = [offset_point(p, 0, 13 * z) for p in outer]
    pygame.draw.polygon(self.screen, (91, 96, 101), [lower[0], lower[1], outer[1], outer[0]])
    pygame.draw.polygon(self.screen, (70, 77, 82), [lower[3], lower[0], outer[0], outer[3]])
    pygame.draw.polygon(self.screen, (110, 116, 120), [lower[1], lower[2], outer[2], outer[1]])
    pygame.draw.polygon(self.screen, (82, 89, 93), [lower[2], lower[3], outer[3], outer[2]])
    pygame.draw.polygon(self.screen, outline, outer, 1)

    stand = self.iso_rect_poly(x + 0.45, y + 0.45, fw - 0.9, fh - 0.9, 0.0, y_offset=-22 * z, base_lift=lift)
    field = self.iso_rect_poly(x + 0.95, y + 0.95, fw - 1.9, fh - 1.9, 0.0, y_offset=-23 * z, base_lift=lift)
    draw_outlined_polygon(self, stand, (177, 187, 184), outline)
    draw_outlined_polygon(self, field, (60, 151, 78), (31, 92, 50))

    for t in (0.28, 0.50, 0.72):
        a = lerp_point(field[0], field[3], t)
        b = lerp_point(field[1], field[2], t)
        pygame.draw.line(self.screen, (92, 181, 101), a, b, max(1, int(z)))
    pygame.draw.line(self.screen, (238, 238, 218), lerp_point(field[0], field[3], 0.5), lerp_point(field[1], field[2], 0.5), max(1, int(2 * z)))

    track_rect = pygame.Rect(0, 0, int(88 * z), int(38 * z))
    track_rect.center = (sum(p[0] for p in field) / 4, sum(p[1] for p in field) / 4)
    pygame.draw.ellipse(self.screen, (174, 92, 65), track_rect, max(2, int(4 * z)))
    pygame.draw.ellipse(self.screen, (232, 215, 184), track_rect.inflate(-9 * z, -5 * z), max(1, int(z)))

    seat_colors = ((54, 113, 174), (215, 191, 78), (185, 70, 65))
    for edge_a, edge_b, seats in ((stand[0], stand[1], 5), (stand[1], stand[2], 4), (stand[3], stand[0], 4)):
        for i in range(seats):
            p = lerp_point(edge_a, edge_b, (i + 1) / (seats + 1))
            pygame.draw.circle(self.screen, seat_colors[i % len(seat_colors)], (int(p[0]), int(p[1] + 3 * z)), max(2, int(3 * z)))

    front_mid = lerp_point(base[3], base[2], 0.5)
    gate = [
        offset_point(front_mid, -18 * z, 0),
        offset_point(front_mid, 18 * z, 0),
        offset_point(front_mid, 13 * z, -17 * z),
        offset_point(front_mid, -13 * z, -17 * z),
    ]
    draw_outlined_polygon(self, gate, (135, 143, 144), outline)
    draw_sign(self, "STADIUM", (front_mid[0], front_mid[1] - 26 * z), (245, 248, 250), (43, 72, 115), (230, 199, 82), pad=(9, 4))

    for wx, wy in ((x + 0.35, y + 0.35), (x + fw - 0.35, y + 0.35), (x + 0.35, y + fh - 0.35), (x + fw - 0.35, y + fh - 0.35)):
        sx, sy = self.camera.world_to_screen(wx, wy)
        sy -= lift
        top = (sx, sy - 45 * z)
        pygame.draw.line(self.screen, (54, 59, 60), (sx, sy - 6 * z), top, max(1, int(3 * z)))
        pygame.draw.circle(self.screen, (248, 239, 164), (int(top[0]), int(top[1])), max(3, int(5 * z)))

def draw_seaport(self, x, y, fw, fh):
    z = self.camera.zoom
    lift = self.tile_lift(x, y)
    outline = (38, 43, 45)

    def ground(wx, wy, y_offset=0):
        sx, sy = self.camera.world_to_screen(wx, wy)
        return sx, sy - lift + y_offset

    apron = self.iso_rect_poly(x, y, fw, fh, 0.04, base_lift=lift)
    draw_outlined_polygon(self, apron, (106, 112, 110), outline)

    quay = self.iso_rect_poly(x + 0.08, y + 1.35, fw - 0.16, 1.45, 0.0, y_offset=-2 * z, base_lift=lift)
    draw_outlined_polygon(self, quay, (127, 118, 96), outline)
    for t in (0.18, 0.36, 0.54, 0.72, 0.90):
        p = lerp_point(quay[3], quay[2], t)
        pygame.draw.circle(self.screen, (54, 48, 40), (int(p[0]), int(p[1] - 2 * z)), max(2, int(3 * z)))

    water = [
        ground(x - 0.10, y + 2.50, 5 * z),
        ground(x + fw + 0.10, y + 2.50, 5 * z),
        ground(x + fw - 0.20, y + fh + 0.45, 5 * z),
        ground(x + 0.20, y + fh + 0.45, 5 * z),
    ]
    draw_outlined_polygon(self, water, (43, 107, 140), (28, 70, 92))
    for t in (0.22, 0.50, 0.78):
        pygame.draw.line(self.screen, (91, 154, 177), lerp_point(water[0], water[3], t), lerp_point(water[1], water[2], t), max(1, int(z)))

    ship = [
        ground(x + 0.65, y + 2.75, -3 * z),
        ground(x + 2.65, y + 2.75, -3 * z),
        ground(x + 2.38, y + 3.22, -3 * z),
        ground(x + 0.90, y + 3.25, -3 * z),
    ]
    draw_outlined_polygon(self, ship, (178, 54, 48), outline)
    deck = [offset_point(p, 0, -8 * z) for p in ship]
    pygame.draw.polygon(self.screen, (231, 232, 220), [deck[0], deck[1], ship[1], ship[0]])
    cabin = [
        ground(x + 1.35, y + 2.65, -12 * z),
        ground(x + 2.05, y + 2.65, -12 * z),
        ground(x + 1.95, y + 2.88, -22 * z),
        ground(x + 1.42, y + 2.88, -22 * z),
    ]
    draw_outlined_polygon(self, cabin, (218, 224, 221), outline)

    wx, wy = x + 0.35, y + 0.20
    _, _, roof, base = self.draw_iso_prism(wx, wy, 1.45, 0.78, 18 * z, (148, 127, 91), (107, 92, 70), inset=0.03, base_lift=lift)
    draw_roof_trim(self, roof, (83, 88, 86), 0.65, 4 * z, (("front", (116, 112, 100)), ("right", (65, 70, 70))))
    door_mid = lerp_point(base[3], base[2], 0.50)
    draw_vertical_rect(self, door_mid, 6 * z, 0, -12 * z, (62, 72, 76), outline)

    for wx, wy, color in ((x + 2.25, y + 0.35, (190, 74, 54)), (x + 2.78, y + 0.58, (61, 104, 165)), (x + 3.18, y + 0.32, (218, 177, 70))):
        box = self.iso_rect_poly(wx, wy, 0.42, 0.38, 0.0, y_offset=-7 * z, base_lift=lift)
        low = [offset_point(p, 0, 7 * z) for p in box]
        pygame.draw.polygon(self.screen, darken(color, 0.72), [low[2], low[3], box[3], box[2]])
        pygame.draw.polygon(self.screen, darken(color, 0.84), [low[1], low[2], box[2], box[1]])
        draw_outlined_polygon(self, box, color, outline)

    crane_base = ground(x + 3.35, y + 1.05)
    crane_top = offset_point(crane_base, 0, -48 * z)
    pygame.draw.line(self.screen, (196, 151, 50), crane_base, crane_top, max(2, int(4 * z)))
    boom_end = offset_point(crane_top, -45 * z, 12 * z)
    pygame.draw.line(self.screen, (219, 173, 56), crane_top, boom_end, max(2, int(4 * z)))
    pygame.draw.line(self.screen, (83, 71, 52), boom_end, offset_point(boom_end, 0, 19 * z), max(1, int(z)))
    pygame.draw.rect(self.screen, (92, 82, 70), (boom_end[0] - 4 * z, boom_end[1] + 17 * z, 8 * z, 5 * z))

    draw_sign(self, "PORT", ground(x + 0.95, y + 0.10, -28 * z), (245, 248, 250), (42, 76, 100), (225, 190, 82), pad=(8, 4))

def draw_airport(self, x, y, fw, fh):
    z = self.camera.zoom
    lift = self.tile_lift(x, y)
    outline = (35, 39, 42)

    def ground(wx, wy, y_offset=0):
        sx, sy = self.camera.world_to_screen(wx, wy)
        return sx, sy - lift + y_offset

    base = self.iso_rect_poly(x, y, fw, fh, 0.03, base_lift=lift)
    draw_outlined_polygon(self, base, (91, 98, 101), outline)

    runway = [
        ground(x + 0.25, y + 2.55, -1 * z),
        ground(x + 5.75, y + 2.55, -1 * z),
        ground(x + 5.55, y + 3.45, -1 * z),
        ground(x + 0.45, y + 3.45, -1 * z),
    ]
    draw_outlined_polygon(self, runway, (48, 52, 55), (24, 27, 30))
    center_a = lerp_point(runway[0], runway[3], 0.5)
    center_b = lerp_point(runway[1], runway[2], 0.5)
    for i in range(8):
        a = i / 8
        b = min(1.0, a + 0.06)
        pygame.draw.line(self.screen, (235, 232, 207), lerp_point(center_a, center_b, a), lerp_point(center_a, center_b, b), max(1, int(2 * z)))
    for t in (0.15, 0.30, 0.70, 0.85):
        p = lerp_point(runway[0], runway[1], t)
        q = lerp_point(runway[3], runway[2], t)
        pygame.draw.line(self.screen, (235, 232, 207), p, q, max(1, int(z)))

    taxi = [
        ground(x + 1.35, y + 1.72),
        ground(x + 4.85, y + 1.72),
        ground(x + 5.15, y + 2.27),
        ground(x + 1.65, y + 2.27),
    ]
    draw_outlined_polygon(self, taxi, (69, 74, 77), outline)
    pygame.draw.line(self.screen, (219, 183, 55), lerp_point(taxi[0], taxi[3], 0.5), lerp_point(taxi[1], taxi[2], 0.5), max(1, int(2 * z)))

    apron = self.iso_rect_poly(x + 0.20, y + 0.20, 2.55, 1.55, 0.0, y_offset=-1 * z, base_lift=lift)
    draw_outlined_polygon(self, apron, (119, 126, 126), outline)

    _, _, roof, terminal_base = self.draw_iso_prism(x + 0.35, y + 0.35, 1.95, 0.72, 20 * z, (191, 204, 207), (132, 146, 151), inset=0.04, base_lift=lift)
    draw_roof_trim(self, roof, (63, 91, 124), 0.62, 4 * z, (("front", (78, 105, 139)), ("right", (45, 67, 92))))
    front_a, front_b = terminal_base[3], terminal_base[2]
    for t in (0.22, 0.44, 0.66, 0.84):
        p = lerp_point(front_a, front_b, t)
        draw_vertical_rect(self, p, 3.8 * z, -9 * z, -14 * z, (143, 199, 225), (65, 80, 88))
    draw_sign(self, "AIR", ground(x + 1.20, y + 0.14, -29 * z), (245, 248, 250), (48, 79, 122), (226, 194, 82), pad=(8, 4))

    tower_base = ground(x + 2.70, y + 0.45)
    tower_top = offset_point(tower_base, 0, -42 * z)
    pygame.draw.line(self.screen, (95, 105, 110), tower_base, tower_top, max(2, int(5 * z)))
    cabin = [
        offset_point(tower_top, -13 * z, -2 * z),
        offset_point(tower_top, 13 * z, -2 * z),
        offset_point(tower_top, 9 * z, -13 * z),
        offset_point(tower_top, -9 * z, -13 * z),
    ]
    draw_outlined_polygon(self, cabin, (154, 194, 211), outline)

    plane_center = ground(x + 3.70, y + 1.72, -8 * z)
    nose = offset_point(plane_center, 34 * z, -7 * z)
    tail = offset_point(plane_center, -28 * z, 6 * z)
    pygame.draw.line(self.screen, (235, 238, 236), tail, nose, max(3, int(6 * z)))
    wing_l = [offset_point(plane_center, -5 * z, 0), offset_point(plane_center, -30 * z, -14 * z), offset_point(plane_center, 8 * z, -5 * z)]
    wing_r = [offset_point(plane_center, -3 * z, 4 * z), offset_point(plane_center, -18 * z, 18 * z), offset_point(plane_center, 10 * z, 7 * z)]
    pygame.draw.polygon(self.screen, (215, 219, 219), wing_l)
    pygame.draw.polygon(self.screen, (184, 190, 193), wing_r)
    pygame.draw.polygon(self.screen, outline, wing_l, 1)
    pygame.draw.polygon(self.screen, outline, wing_r, 1)
    pygame.draw.circle(self.screen, (202, 57, 54), (int(nose[0]), int(nose[1])), max(2, int(3 * z)))

    for wx in (x + 0.6, x + 1.4, x + 2.2, x + 3.0, x + 3.8, x + 4.6, x + 5.4):
        light = ground(wx, y + 3.55, -3 * z)
        pygame.draw.circle(self.screen, (245, 231, 135), (int(light[0]), int(light[1])), max(1, int(2 * z)))

def draw_water_pump(self, x, y, fw, fh):
    z = self.camera.zoom
    lift = self.tile_lift(x, y)
    outline = (34, 48, 55)

    pad = self.iso_rect_poly(x, y, fw, fh, 0.10, base_lift=lift)
    draw_outlined_polygon(self, pad, (84, 121, 126), outline)

    _, _, roof, base = self.draw_iso_prism(x + 0.13, y + 0.16, 0.55, 0.54, 13 * z, (116, 160, 176), (72, 112, 128), inset=0.02, base_lift=lift)
    draw_roof_trim(self, roof, (55, 92, 118), 0.65, 3 * z, (("front", (68, 103, 126)), ("right", (42, 70, 91))))

    front_mid = lerp_point(base[3], base[2], 0.52)
    draw_vertical_rect(self, front_mid, 3.5 * z, 0, -8 * z, (45, 67, 78), outline)

    tank_center = self.camera.world_to_screen(x + 0.68, y + 0.58)
    tank_center = tank_center[0], tank_center[1] - lift - 12 * z
    tank_w = 16 * z
    tank_h = 17 * z
    tank_rect = pygame.Rect(tank_center[0] - tank_w / 2, tank_center[1] - tank_h / 2, tank_w, tank_h)
    pygame.draw.ellipse(self.screen, (136, 190, 205), tank_rect)
    pygame.draw.rect(self.screen, (98, 154, 174), (tank_rect.x, tank_rect.centery, tank_rect.width, tank_rect.height / 2))
    pygame.draw.ellipse(self.screen, (183, 224, 232), tank_rect.inflate(-3 * z, -7 * z), max(1, int(z)))
    pygame.draw.ellipse(self.screen, outline, tank_rect, max(1, int(z)))

    pipe_a = self.camera.world_to_screen(x + 0.22, y + 0.72)
    pipe_b = self.camera.world_to_screen(x + 0.82, y + 0.72)
    pipe_a = pipe_a[0], pipe_a[1] - lift - 2 * z
    pipe_b = pipe_b[0], pipe_b[1] - lift - 2 * z
    pygame.draw.line(self.screen, (61, 118, 146), pipe_a, pipe_b, max(2, int(4 * z)))
    pygame.draw.line(self.screen, (150, 212, 226), offset_point(pipe_a, 0, -1 * z), offset_point(pipe_b, 0, -1 * z), max(1, int(z)))

    spout = self.camera.world_to_screen(x + 0.53, y + 0.83)
    spout = spout[0], spout[1] - lift - 5 * z
    pygame.draw.circle(self.screen, (65, 126, 154), (int(spout[0]), int(spout[1])), max(3, int(5 * z)))
    pygame.draw.circle(self.screen, (173, 221, 231), (int(spout[0]), int(spout[1])), max(1, int(2 * z)))

def draw_smokestack(self, wx, wy, roof_height, stack_height):
    z = self.camera.zoom
    sx, sy = self.camera.world_to_screen(wx, wy)
    ox = int(clamp(round(wx), 0, self.city.width - 1))
    oy = int(clamp(round(wy), 0, self.city.height - 1))
    sy -= self.tile_lift(ox, oy)
    sy -= roof_height
    w = 7 * z
    body = [(sx - w, sy), (sx, sy + w * 0.45), (sx, sy + w * 0.45 - stack_height), (sx - w, sy - stack_height)]
    side = [(sx, sy + w * 0.45), (sx + w, sy), (sx + w, sy - stack_height), (sx, sy + w * 0.45 - stack_height)]
    cap = [(sx - w, sy - stack_height), (sx, sy - stack_height - w * 0.45), (sx + w, sy - stack_height), (sx, sy + w * 0.45 - stack_height)]
    pygame.draw.polygon(self.screen, (44, 42, 40), body)
    pygame.draw.polygon(self.screen, (58, 55, 52), side)
    pygame.draw.polygon(self.screen, (75, 72, 68), cap)
    pygame.draw.circle(self.screen, (95, 94, 91), (int(sx), int(sy - stack_height - 8 * z)), max(3, int(5 * z)))
