import math

import pygame


def draw_school_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    yard = pygame.Rect(rect.x + 8, rect.y + 60, rect.width - 16, 21)
    pygame.draw.ellipse(g.screen, (65, 119, 74), yard)
    pygame.draw.line(g.screen, (184, 167, 113), (rect.x + 16, rect.y + 82), (rect.right - 16, rect.y + 82), 3)

    body = pygame.Rect(rect.x + 18, rect.y + 36, rect.width - 36, 34)
    roof = [
        (rect.x + 12, rect.y + 38),
        (cx, rect.y + 13),
        (rect.right - 12, rect.y + 38),
    ]
    pygame.draw.polygon(g.screen, (178, 151, 74), roof)
    pygame.draw.polygon(g.screen, (80, 67, 39), roof, 2)
    pygame.draw.rect(g.screen, (216, 201, 135), body, border_radius=2)
    pygame.draw.rect(g.screen, (86, 75, 46), body, 1)

    tower = pygame.Rect(cx - 11, rect.y + 24, 22, 46)
    pygame.draw.rect(g.screen, (226, 211, 145), tower, border_radius=2)
    pygame.draw.rect(g.screen, (86, 75, 46), tower, 1)
    tower_roof = [(cx - 15, rect.y + 25), (cx, rect.y + 8), (cx + 15, rect.y + 25)]
    pygame.draw.polygon(g.screen, (151, 74, 62), tower_roof)
    pygame.draw.polygon(g.screen, (73, 47, 43), tower_roof, 1)

    clock_center = (cx, rect.y + 34)
    pygame.draw.circle(g.screen, (236, 232, 199), clock_center, 7)
    pygame.draw.circle(g.screen, (74, 64, 44), clock_center, 7, 1)
    pygame.draw.line(g.screen, (74, 64, 44), clock_center, (cx, rect.y + 30), 1)
    pygame.draw.line(g.screen, (74, 64, 44), clock_center, (cx + 4, rect.y + 34), 1)

    door = pygame.Rect(cx - 7, rect.y + 52, 14, 18)
    pygame.draw.rect(g.screen, (94, 68, 47), door)
    pygame.draw.rect(g.screen, (48, 37, 29), door, 1)

    for wx in (body.x + 9, body.x + 24, body.right - 30, body.right - 15):
        window = pygame.Rect(wx, rect.y + 47, 9, 10)
        pygame.draw.rect(g.screen, (111, 159, 192), window)
        pygame.draw.rect(g.screen, (56, 69, 78), window, 1)
        pygame.draw.line(g.screen, (56, 69, 78), window.midtop, window.midbottom, 1)

    steps = pygame.Rect(cx - 15, rect.y + 70, 30, 6)
    pygame.draw.rect(g.screen, (113, 103, 78), steps)
    sign = pygame.Rect(cx - 20, rect.y + 75, 40, 12)
    pygame.draw.rect(g.screen, (52, 76, 94), sign, border_radius=2)
    pygame.draw.rect(g.screen, (25, 35, 43), sign, 1, border_radius=2)
    label = g.small.render("SCHOOL", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))

    for tree_x in (rect.x + 14, rect.right - 14):
        pygame.draw.rect(g.screen, (91, 64, 41), (tree_x - 2, rect.y + 63, 4, 10))
        pygame.draw.circle(g.screen, (66, 136, 82), (tree_x, rect.y + 60), 8)


def draw_clinic_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 10, rect.y + 70, rect.width - 20, 13)
    pygame.draw.ellipse(g.screen, (93, 120, 103), ground)

    body = pygame.Rect(rect.x + 18, rect.y + 31, rect.width - 36, 40)
    pygame.draw.rect(g.screen, (236, 239, 240), body, border_radius=3)
    pygame.draw.rect(g.screen, (89, 98, 105), body, 1, border_radius=3)

    roof = pygame.Rect(rect.x + 14, rect.y + 25, rect.width - 28, 10)
    pygame.draw.rect(g.screen, (190, 63, 73), roof, border_radius=3)
    pygame.draw.rect(g.screen, (105, 37, 45), roof, 1, border_radius=3)

    wing_left = pygame.Rect(rect.x + 11, rect.y + 43, 18, 27)
    wing_right = pygame.Rect(rect.right - 29, rect.y + 43, 18, 27)
    for wing in (wing_left, wing_right):
        pygame.draw.rect(g.screen, (215, 224, 226), wing, border_radius=2)
        pygame.draw.rect(g.screen, (89, 98, 105), wing, 1, border_radius=2)

    door = pygame.Rect(cx - 8, rect.y + 51, 16, 20)
    pygame.draw.rect(g.screen, (104, 165, 190), door)
    pygame.draw.rect(g.screen, (52, 76, 88), door, 1)
    pygame.draw.line(g.screen, (52, 76, 88), door.midtop, door.midbottom, 1)

    for wx in (body.x + 11, body.right - 20):
        window = pygame.Rect(wx, rect.y + 45, 10, 10)
        pygame.draw.rect(g.screen, (126, 181, 206), window)
        pygame.draw.rect(g.screen, (58, 82, 94), window, 1)

    cross_v = pygame.Rect(cx - 4, rect.y + 33, 8, 24)
    cross_h = pygame.Rect(cx - 13, rect.y + 41, 26, 8)
    pygame.draw.rect(g.screen, (208, 52, 65), cross_v, border_radius=2)
    pygame.draw.rect(g.screen, (208, 52, 65), cross_h, border_radius=2)

    sign = pygame.Rect(cx - 23, rect.y + 75, 46, 12)
    pygame.draw.rect(g.screen, (72, 83, 91), sign, border_radius=2)
    pygame.draw.rect(g.screen, (34, 40, 45), sign, 1, border_radius=2)
    label = g.small.render("CLINIC", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_police_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 10, rect.y + 72, rect.width - 20, 12)
    pygame.draw.ellipse(g.screen, (70, 91, 111), ground)

    body = pygame.Rect(rect.x + 17, rect.y + 35, rect.width - 34, 36)
    pygame.draw.rect(g.screen, (69, 101, 174), body, border_radius=3)
    pygame.draw.rect(g.screen, (31, 47, 86), body, 1, border_radius=3)

    roof = [
        (rect.x + 12, rect.y + 36),
        (cx, rect.y + 18),
        (rect.right - 12, rect.y + 36),
    ]
    pygame.draw.polygon(g.screen, (45, 63, 121), roof)
    pygame.draw.polygon(g.screen, (21, 31, 66), roof, 2)

    entry = pygame.Rect(cx - 12, rect.y + 48, 24, 23)
    pygame.draw.rect(g.screen, (47, 65, 118), entry)
    pygame.draw.rect(g.screen, (20, 28, 58), entry, 1)
    door = pygame.Rect(cx - 6, rect.y + 56, 12, 15)
    pygame.draw.rect(g.screen, (35, 42, 63), door)
    pygame.draw.rect(g.screen, (15, 18, 28), door, 1)

    for wx in (body.x + 9, body.right - 20):
        window = pygame.Rect(wx, rect.y + 47, 11, 10)
        pygame.draw.rect(g.screen, (151, 194, 225), window)
        pygame.draw.rect(g.screen, (27, 42, 72), window, 1)
        pygame.draw.line(g.screen, (27, 42, 72), window.midtop, window.midbottom, 1)

    badge = [
        (cx, rect.y + 25),
        (cx + 12, rect.y + 31),
        (cx + 9, rect.y + 44),
        (cx, rect.y + 51),
        (cx - 9, rect.y + 44),
        (cx - 12, rect.y + 31),
    ]
    pygame.draw.polygon(g.screen, (236, 199, 88), badge)
    pygame.draw.polygon(g.screen, (100, 74, 31), badge, 1)
    star = g.small.render("*", True, (62, 47, 24))
    g.screen.blit(star, star.get_rect(center=(cx, rect.y + 38)))

    mast_x = rect.right - 21
    pygame.draw.line(g.screen, (31, 35, 48), (mast_x, rect.y + 34), (mast_x, rect.y + 18), 2)
    pygame.draw.polygon(g.screen, (210, 70, 70), [(mast_x, rect.y + 18), (mast_x + 12, rect.y + 22), (mast_x, rect.y + 26)])

    sign = pygame.Rect(cx - 22, rect.y + 76, 44, 12)
    pygame.draw.rect(g.screen, (28, 39, 83), sign, border_radius=2)
    pygame.draw.rect(g.screen, (12, 18, 40), sign, 1, border_radius=2)
    label = g.small.render("POLICE", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_fire_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 10, rect.y + 72, rect.width - 20, 12)
    pygame.draw.ellipse(g.screen, (104, 86, 75), ground)

    body = pygame.Rect(rect.x + 16, rect.y + 36, rect.width - 32, 35)
    pygame.draw.rect(g.screen, (197, 58, 52), body, border_radius=3)
    pygame.draw.rect(g.screen, (91, 34, 31), body, 1, border_radius=3)

    roof = [
        (rect.x + 11, rect.y + 37),
        (cx, rect.y + 17),
        (rect.right - 11, rect.y + 37),
    ]
    pygame.draw.polygon(g.screen, (124, 39, 37), roof)
    pygame.draw.polygon(g.screen, (67, 27, 27), roof, 2)

    bay = pygame.Rect(cx - 18, rect.y + 48, 36, 23)
    pygame.draw.rect(g.screen, (85, 44, 39), bay)
    pygame.draw.rect(g.screen, (45, 24, 22), bay, 1)
    for offset in (6, 12, 18):
        pygame.draw.line(g.screen, (139, 76, 67), (bay.x, bay.y + offset), (bay.right, bay.y + offset), 1)

    for wx in (body.x + 8, body.right - 18):
        window = pygame.Rect(wx, rect.y + 46, 10, 9)
        pygame.draw.rect(g.screen, (236, 194, 91), window)
        pygame.draw.rect(g.screen, (83, 45, 34), window, 1)

    tower = pygame.Rect(rect.x + 21, rect.y + 27, 18, 43)
    pygame.draw.rect(g.screen, (211, 67, 57), tower, border_radius=2)
    pygame.draw.rect(g.screen, (91, 34, 31), tower, 1, border_radius=2)
    tower_roof = [(tower.x - 3, tower.y), (tower.centerx, rect.y + 12), (tower.right + 3, tower.y)]
    pygame.draw.polygon(g.screen, (115, 35, 34), tower_roof)
    pygame.draw.polygon(g.screen, (64, 24, 24), tower_roof, 1)
    pygame.draw.rect(g.screen, (236, 194, 91), (tower.x + 5, tower.y + 13, 8, 8))
    pygame.draw.rect(g.screen, (83, 45, 34), (tower.x + 5, tower.y + 13, 8, 8), 1)

    hose = pygame.Rect(rect.right - 35, rect.y + 56, 20, 10)
    pygame.draw.ellipse(g.screen, (221, 194, 103), hose)
    pygame.draw.ellipse(g.screen, (105, 84, 39), hose, 2)
    flame = [
        (rect.right - 20, rect.y + 30),
        (rect.right - 27, rect.y + 45),
        (rect.right - 14, rect.y + 45),
    ]
    pygame.draw.polygon(g.screen, (239, 112, 53), flame)
    pygame.draw.polygon(g.screen, (251, 205, 80), [(rect.right - 20, rect.y + 35), (rect.right - 23, rect.y + 43), (rect.right - 16, rect.y + 43)])

    sign = pygame.Rect(cx - 18, rect.y + 76, 36, 12)
    pygame.draw.rect(g.screen, (91, 35, 34), sign, border_radius=2)
    pygame.draw.rect(g.screen, (47, 21, 21), sign, 1, border_radius=2)
    label = g.small.render("FIRE", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_library_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 10, rect.y + 72, rect.width - 20, 12)
    pygame.draw.ellipse(g.screen, (116, 96, 78), ground)

    body = pygame.Rect(rect.x + 17, rect.y + 35, rect.width - 34, 36)
    pygame.draw.rect(g.screen, (157, 113, 75), body, border_radius=2)
    pygame.draw.rect(g.screen, (79, 55, 38), body, 1, border_radius=2)

    pediment = [
        (rect.x + 12, rect.y + 36),
        (cx, rect.y + 17),
        (rect.right - 12, rect.y + 36),
    ]
    pygame.draw.polygon(g.screen, (126, 86, 57), pediment)
    pygame.draw.polygon(g.screen, (67, 46, 32), pediment, 2)

    shelf = pygame.Rect(rect.x + 22, rect.y + 47, rect.width - 44, 16)
    pygame.draw.rect(g.screen, (94, 63, 42), shelf)
    pygame.draw.rect(g.screen, (49, 35, 26), shelf, 1)
    book_colors = ((202, 72, 68), (79, 119, 176), (221, 181, 82), (92, 151, 94), (173, 88, 153))
    bx = shelf.x + 4
    for color in book_colors:
        book = pygame.Rect(bx, shelf.y + 3, 6, 10)
        pygame.draw.rect(g.screen, color, book)
        pygame.draw.rect(g.screen, (42, 32, 25), book, 1)
        bx += 8

    column_y = rect.y + 38
    for col_x in (rect.x + 22, rect.x + 37, rect.right - 43, rect.right - 28):
        pygame.draw.rect(g.screen, (203, 175, 128), (col_x, column_y, 8, 33), border_radius=2)
        pygame.draw.rect(g.screen, (82, 60, 43), (col_x, column_y, 8, 33), 1, border_radius=2)

    door = pygame.Rect(cx - 8, rect.y + 56, 16, 15)
    pygame.draw.rect(g.screen, (76, 48, 34), door)
    pygame.draw.rect(g.screen, (39, 27, 21), door, 1)
    pygame.draw.line(g.screen, (121, 88, 60), door.midtop, door.midbottom, 1)

    open_book = [
        (cx - 20, rect.y + 26),
        (cx - 2, rect.y + 31),
        (cx - 2, rect.y + 45),
        (cx - 20, rect.y + 39),
    ]
    open_book_r = [
        (cx + 2, rect.y + 31),
        (cx + 20, rect.y + 26),
        (cx + 20, rect.y + 39),
        (cx + 2, rect.y + 45),
    ]
    pygame.draw.polygon(g.screen, (229, 214, 170), open_book)
    pygame.draw.polygon(g.screen, (244, 230, 183), open_book_r)
    pygame.draw.line(g.screen, (84, 61, 42), (cx, rect.y + 31), (cx, rect.y + 45), 1)
    pygame.draw.polygon(g.screen, (84, 61, 42), open_book, 1)
    pygame.draw.polygon(g.screen, (84, 61, 42), open_book_r, 1)

    sign = pygame.Rect(cx - 23, rect.y + 76, 46, 12)
    pygame.draw.rect(g.screen, (83, 55, 38), sign, border_radius=2)
    pygame.draw.rect(g.screen, (42, 30, 23), sign, 1, border_radius=2)
    label = g.small.render("LIBRARY", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_stadium_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    cy = rect.y + 49
    shadow = pygame.Rect(rect.x + 12, rect.y + 28, rect.width - 24, 48)
    pygame.draw.ellipse(g.screen, (54, 65, 55), shadow)

    outer = pygame.Rect(rect.x + 15, rect.y + 22, rect.width - 30, 48)
    inner = outer.inflate(-20, -15)
    pygame.draw.ellipse(g.screen, (124, 137, 126), outer)
    pygame.draw.ellipse(g.screen, (72, 147, 84), inner)
    pygame.draw.ellipse(g.screen, (45, 84, 54), inner, 2)
    pygame.draw.ellipse(g.screen, (73, 78, 82), outer, 2)

    field = pygame.Rect(cx - 18, cy - 10, 36, 20)
    pygame.draw.rect(g.screen, (70, 158, 82), field, border_radius=3)
    pygame.draw.rect(g.screen, (231, 237, 219), field, 1, border_radius=3)
    pygame.draw.line(g.screen, (231, 237, 219), (cx, field.y), (cx, field.bottom), 1)
    pygame.draw.circle(g.screen, (231, 237, 219), (cx, cy), 5, 1)

    seat_colors = ((205, 83, 74), (226, 191, 84), (83, 125, 190))
    for i, color in enumerate(seat_colors):
        band = outer.inflate(-6 - i * 7, -5 - i * 5)
        pygame.draw.arc(g.screen, color, band, 3.35, 6.05, 3)

    for light_x in (rect.x + 20, rect.right - 20):
        pygame.draw.line(g.screen, (79, 84, 86), (light_x, rect.y + 63), (light_x, rect.y + 22), 2)
        lamp = [(light_x - 5, rect.y + 22), (light_x + 5, rect.y + 22), (light_x + 3, rect.y + 28), (light_x - 3, rect.y + 28)]
        pygame.draw.polygon(g.screen, (234, 221, 137), lamp)
        pygame.draw.polygon(g.screen, (91, 83, 48), lamp, 1)

    sign = pygame.Rect(cx - 25, rect.y + 76, 50, 12)
    pygame.draw.rect(g.screen, (48, 89, 57), sign, border_radius=2)
    pygame.draw.rect(g.screen, (24, 45, 31), sign, 1, border_radius=2)
    label = g.small.render("STADIUM", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_water_pump_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    basin = pygame.Rect(rect.x + 12, rect.y + 61, rect.width - 24, 22)
    pygame.draw.ellipse(g.screen, (35, 90, 125), basin)
    pygame.draw.ellipse(g.screen, (76, 154, 190), basin.inflate(-8, -7))

    base = pygame.Rect(cx - 26, rect.y + 48, 52, 18)
    pygame.draw.rect(g.screen, (76, 98, 105), base, border_radius=3)
    pygame.draw.rect(g.screen, (38, 50, 56), base, 1, border_radius=3)

    tower = pygame.Rect(cx - 15, rect.y + 24, 30, 37)
    pygame.draw.rect(g.screen, (91, 145, 164), tower, border_radius=4)
    pygame.draw.rect(g.screen, (39, 70, 82), tower, 1, border_radius=4)

    cap = pygame.Rect(cx - 20, rect.y + 18, 40, 10)
    pygame.draw.rect(g.screen, (53, 83, 96), cap, border_radius=3)
    pygame.draw.rect(g.screen, (26, 42, 51), cap, 1, border_radius=3)

    pipe = pygame.Rect(cx + 11, rect.y + 36, 30, 10)
    pygame.draw.rect(g.screen, (59, 105, 126), pipe, border_radius=5)
    pygame.draw.rect(g.screen, (28, 59, 74), pipe, 1, border_radius=5)
    pygame.draw.line(g.screen, (145, 211, 235), (pipe.right - 2, pipe.centery), (rect.right - 9, rect.y + 55), 3)
    pygame.draw.circle(g.screen, (145, 211, 235), (rect.right - 9, rect.y + 57), 3)

    gauge_center = (cx, rect.y + 42)
    pygame.draw.circle(g.screen, (226, 232, 223), gauge_center, 8)
    pygame.draw.circle(g.screen, (37, 61, 69), gauge_center, 8, 1)
    pygame.draw.line(g.screen, (37, 61, 69), gauge_center, (cx + 5, rect.y + 38), 1)

    sign = pygame.Rect(cx - 23, rect.y + 76, 46, 12)
    pygame.draw.rect(g.screen, (41, 86, 111), sign, border_radius=2)
    pygame.draw.rect(g.screen, (20, 43, 57), sign, 1, border_radius=2)
    label = g.small.render("PUMP", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_coal_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 9, rect.y + 70, rect.width - 18, 13)
    pygame.draw.ellipse(g.screen, (76, 72, 64), ground)

    body = pygame.Rect(rect.x + 15, rect.y + 43, rect.width - 30, 28)
    pygame.draw.rect(g.screen, (87, 84, 78), body, border_radius=3)
    pygame.draw.rect(g.screen, (39, 38, 36), body, 1, border_radius=3)

    roof = [(body.x, body.y), (cx, rect.y + 28), (body.right, body.y)]
    pygame.draw.polygon(g.screen, (62, 59, 55), roof)
    pygame.draw.polygon(g.screen, (31, 30, 29), roof, 1)

    for wx in (body.x + 10, body.x + 27, body.right - 37, body.right - 20):
        window = pygame.Rect(wx, body.y + 10, 10, 9)
        pygame.draw.rect(g.screen, (236, 193, 83), window)
        pygame.draw.rect(g.screen, (54, 45, 31), window, 1)

    for stack_x, height in ((rect.x + 25, 43), (rect.right - 31, 52)):
        stack = pygame.Rect(stack_x, rect.y + 67 - height, 14, height)
        pygame.draw.rect(g.screen, (70, 66, 61), stack)
        pygame.draw.rect(g.screen, (33, 32, 31), stack, 1)
        pygame.draw.rect(g.screen, (49, 47, 44), (stack.x - 2, stack.y - 4, stack.width + 4, 6), border_radius=2)
        for i in range(3):
            smoke_center = (stack.centerx + i * 5 - 5, stack.y - 9 - i * 8)
            pygame.draw.circle(g.screen, (98, 102, 100), smoke_center, 7 - i)

    bolt = [(cx - 5, rect.y + 34), (cx + 7, rect.y + 34), (cx + 1, rect.y + 48), (cx + 10, rect.y + 48), (cx - 4, rect.y + 64), (cx, rect.y + 51), (cx - 9, rect.y + 51)]
    pygame.draw.polygon(g.screen, (244, 205, 79), bolt)
    pygame.draw.polygon(g.screen, (97, 75, 30), bolt, 1)

    coal = pygame.Rect(rect.x + 16, rect.y + 66, 28, 10)
    pygame.draw.ellipse(g.screen, (31, 30, 29), coal)
    for dot_x in (coal.x + 7, coal.x + 14, coal.x + 21):
        pygame.draw.circle(g.screen, (18, 18, 18), (dot_x, coal.centery), 5)

    sign = pygame.Rect(cx - 21, rect.y + 76, 42, 12)
    pygame.draw.rect(g.screen, (55, 53, 50), sign, border_radius=2)
    pygame.draw.rect(g.screen, (25, 24, 23), sign, 1, border_radius=2)
    label = g.small.render("COAL", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_solar_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 10, rect.y + 72, rect.width - 20, 12)
    pygame.draw.ellipse(g.screen, (79, 105, 96), ground)

    sun_center = (rect.x + 24, rect.y + 22)
    pygame.draw.circle(g.screen, (246, 202, 77), sun_center, 9)
    for angle in range(0, 360, 45):
        dx = int(math.cos(math.radians(angle)) * 15)
        dy = int(math.sin(math.radians(angle)) * 15)
        pygame.draw.line(g.screen, (246, 202, 77), sun_center, (sun_center[0] + dx, sun_center[1] + dy), 2)

    base_y = rect.y + 66
    for i, px in enumerate((rect.x + 18, rect.x + 44, rect.x + 70)):
        panel = pygame.Rect(px, rect.y + 38 + (i % 2) * 3, 24, 18)
        pygame.draw.polygon(
            g.screen,
            (54, 129, 172),
            [(panel.x, panel.bottom), (panel.x + 6, panel.y), (panel.right, panel.y), (panel.right - 6, panel.bottom)],
        )
        pygame.draw.polygon(
            g.screen,
            (23, 62, 89),
            [(panel.x, panel.bottom), (panel.x + 6, panel.y), (panel.right, panel.y), (panel.right - 6, panel.bottom)],
            1,
        )
        pygame.draw.line(g.screen, (125, 188, 212), (panel.x + 8, panel.y + 1), (panel.x + 2, panel.bottom - 1), 1)
        pygame.draw.line(g.screen, (125, 188, 212), (panel.x + 16, panel.y + 1), (panel.x + 10, panel.bottom - 1), 1)
        pygame.draw.line(g.screen, (125, 188, 212), (panel.x + 4, panel.y + 9), (panel.right - 4, panel.y + 9), 1)
        pygame.draw.line(g.screen, (70, 74, 77), panel.midbottom, (panel.centerx, base_y), 2)

    inverter = pygame.Rect(cx - 10, rect.y + 58, 20, 14)
    pygame.draw.rect(g.screen, (224, 228, 218), inverter, border_radius=2)
    pygame.draw.rect(g.screen, (91, 99, 96), inverter, 1, border_radius=2)
    pygame.draw.circle(g.screen, (74, 154, 86), (inverter.x + 6, inverter.y + 7), 3)
    pygame.draw.line(g.screen, (91, 99, 96), (inverter.right - 7, inverter.y + 5), (inverter.right - 3, inverter.y + 5), 1)
    pygame.draw.line(g.screen, (91, 99, 96), (inverter.right - 7, inverter.y + 9), (inverter.right - 3, inverter.y + 9), 1)

    sign = pygame.Rect(cx - 22, rect.y + 76, 44, 12)
    pygame.draw.rect(g.screen, (36, 99, 134), sign, border_radius=2)
    pygame.draw.rect(g.screen, (17, 49, 69), sign, 1, border_radius=2)
    label = g.small.render("SOLAR", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_large_park_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 8, rect.y + 62, rect.width - 16, 22)
    pygame.draw.ellipse(g.screen, (58, 126, 73), ground)
    pygame.draw.ellipse(g.screen, (81, 155, 90), ground.inflate(-16, -8))

    path = [(rect.x + 16, rect.y + 82), (cx - 9, rect.y + 68), (cx + 6, rect.y + 55), (rect.right - 14, rect.y + 42)]
    pygame.draw.lines(g.screen, (197, 179, 125), False, path, 5)
    pygame.draw.lines(g.screen, (129, 112, 76), False, path, 1)

    pond = pygame.Rect(rect.x + 18, rect.y + 43, 30, 16)
    pygame.draw.ellipse(g.screen, (55, 124, 164), pond)
    pygame.draw.ellipse(g.screen, (137, 200, 219), pond.inflate(-8, -6))

    for tree_x, tree_y, size in (
        (rect.x + 26, rect.y + 35, 11),
        (rect.x + 48, rect.y + 30, 13),
        (rect.right - 32, rect.y + 34, 12),
        (rect.right - 20, rect.y + 56, 10),
    ):
        pygame.draw.rect(g.screen, (91, 65, 40), (tree_x - 2, tree_y + size - 3, 4, 12))
        pygame.draw.circle(g.screen, (49, 118, 64), (tree_x, tree_y + size), size)
        pygame.draw.circle(g.screen, (70, 150, 79), (tree_x - 4, tree_y + size - 3), max(4, size - 5))

    bench = pygame.Rect(cx - 10, rect.y + 61, 24, 6)
    pygame.draw.rect(g.screen, (128, 83, 55), bench, border_radius=2)
    pygame.draw.line(g.screen, (67, 46, 34), (bench.x + 4, bench.bottom), (bench.x + 4, bench.bottom + 7), 2)
    pygame.draw.line(g.screen, (67, 46, 34), (bench.right - 4, bench.bottom), (bench.right - 4, bench.bottom + 7), 2)

    sign = pygame.Rect(cx - 25, rect.y + 76, 50, 12)
    pygame.draw.rect(g.screen, (44, 98, 58), sign, border_radius=2)
    pygame.draw.rect(g.screen, (21, 49, 31), sign, 1, border_radius=2)
    label = g.small.render("PARK", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_park_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 13, rect.y + 64, rect.width - 26, 19)
    pygame.draw.ellipse(g.screen, (59, 130, 72), ground)
    pygame.draw.ellipse(g.screen, (86, 160, 89), ground.inflate(-13, -7))

    path = [(rect.x + 18, rect.y + 81), (cx - 3, rect.y + 68), (rect.right - 17, rect.y + 59)]
    pygame.draw.lines(g.screen, (198, 181, 128), False, path, 5)
    pygame.draw.lines(g.screen, (128, 112, 77), False, path, 1)

    for tree_x, tree_y, size in (
        (rect.x + 33, rect.y + 36, 12),
        (rect.right - 34, rect.y + 40, 11),
        (cx, rect.y + 31, 14),
    ):
        pygame.draw.rect(g.screen, (88, 63, 39), (tree_x - 2, tree_y + size - 2, 4, 13))
        pygame.draw.circle(g.screen, (48, 117, 61), (tree_x, tree_y + size), size)
        pygame.draw.circle(g.screen, (74, 153, 77), (tree_x - 4, tree_y + size - 3), max(4, size - 5))

    bench = pygame.Rect(cx - 15, rect.y + 60, 30, 6)
    pygame.draw.rect(g.screen, (130, 84, 55), bench, border_radius=2)
    pygame.draw.line(g.screen, (67, 46, 34), (bench.x + 5, bench.bottom), (bench.x + 5, bench.bottom + 7), 2)
    pygame.draw.line(g.screen, (67, 46, 34), (bench.right - 5, bench.bottom), (bench.right - 5, bench.bottom + 7), 2)

    flower_colors = ((223, 87, 92), (235, 202, 82), (116, 151, 223))
    for i, color in enumerate(flower_colors):
        pygame.draw.circle(g.screen, color, (rect.x + 24 + i * 8, rect.y + 68), 3)

    sign = pygame.Rect(cx - 20, rect.y + 76, 40, 12)
    pygame.draw.rect(g.screen, (42, 96, 55), sign, border_radius=2)
    pygame.draw.rect(g.screen, (20, 47, 29), sign, 1, border_radius=2)
    label = g.small.render("PARK", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_rail_station_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    cx = rect.centerx
    ground = pygame.Rect(rect.x + 9, rect.y + 70, rect.width - 18, 13)
    pygame.draw.ellipse(g.screen, (83, 76, 68), ground)

    body = pygame.Rect(rect.x + 19, rect.y + 36, rect.width - 38, 32)
    pygame.draw.rect(g.screen, (132, 105, 78), body, border_radius=3)
    pygame.draw.rect(g.screen, (64, 50, 39), body, 1, border_radius=3)
    roof = [(body.x - 4, body.y), (cx, rect.y + 20), (body.right + 4, body.y)]
    pygame.draw.polygon(g.screen, (91, 66, 49), roof)
    pygame.draw.polygon(g.screen, (47, 35, 28), roof, 1)

    clock = (cx, rect.y + 41)
    pygame.draw.circle(g.screen, (231, 224, 187), clock, 7)
    pygame.draw.circle(g.screen, (56, 46, 36), clock, 7, 1)
    pygame.draw.line(g.screen, (56, 46, 36), clock, (cx, rect.y + 37), 1)
    pygame.draw.line(g.screen, (56, 46, 36), clock, (cx + 4, rect.y + 42), 1)

    platform = pygame.Rect(rect.x + 13, rect.y + 66, rect.width - 26, 8)
    pygame.draw.rect(g.screen, (104, 93, 80), platform, border_radius=2)
    for yoff in (75, 81):
        pygame.draw.line(g.screen, (164, 166, 158), (rect.x + 13, rect.y + yoff - 7), (rect.right - 13, rect.y + yoff - 7), 2)
    for i in range(6):
        sx = rect.x + 18 + i * 13
        pygame.draw.line(g.screen, (79, 63, 47), (sx, rect.y + 70), (sx + 8, rect.y + 78), 2)

    sign = pygame.Rect(cx - 23, rect.y + 76, 46, 12)
    pygame.draw.rect(g.screen, (75, 58, 45), sign, border_radius=2)
    pygame.draw.rect(g.screen, (36, 28, 23), sign, 1, border_radius=2)
    label = g.small.render("RAIL", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_seaport_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    water = pygame.Rect(rect.x + 8, rect.y + 56, rect.width - 16, 28)
    pygame.draw.ellipse(g.screen, (37, 101, 135), water)
    for i in range(3):
        y = rect.y + 61 + i * 7
        pygame.draw.arc(g.screen, (107, 177, 207), (rect.x + 14 + i * 5, y - 5, rect.width - 28, 10), 0.1, 3.0, 1)

    dock = pygame.Rect(rect.x + 18, rect.y + 48, 72, 11)
    pygame.draw.rect(g.screen, (126, 91, 59), dock, border_radius=2)
    pygame.draw.rect(g.screen, (63, 44, 31), dock, 1, border_radius=2)
    for px in (dock.x + 8, dock.x + 28, dock.x + 50, dock.right - 8):
        pygame.draw.line(g.screen, (70, 50, 35), (px, dock.y), (px, dock.bottom + 12), 3)

    hull = [(rect.x + 30, rect.y + 60), (rect.x + 76, rect.y + 60), (rect.x + 67, rect.y + 72), (rect.x + 38, rect.y + 72)]
    pygame.draw.polygon(g.screen, (78, 112, 126), hull)
    pygame.draw.polygon(g.screen, (32, 52, 63), hull, 1)
    pygame.draw.rect(g.screen, (224, 226, 214), (rect.x + 43, rect.y + 47, 24, 13), border_radius=2)
    pygame.draw.rect(g.screen, (73, 91, 96), (rect.x + 43, rect.y + 47, 24, 13), 1, border_radius=2)
    pygame.draw.line(g.screen, (58, 60, 63), (rect.x + 55, rect.y + 47), (rect.x + 55, rect.y + 30), 2)
    pygame.draw.polygon(g.screen, (222, 197, 108), [(rect.x + 56, rect.y + 31), (rect.x + 75, rect.y + 44), (rect.x + 56, rect.y + 44)])

    sign = pygame.Rect(rect.centerx - 22, rect.y + 76, 44, 12)
    pygame.draw.rect(g.screen, (43, 88, 111), sign, border_radius=2)
    pygame.draw.rect(g.screen, (20, 42, 55), sign, 1, border_radius=2)
    label = g.small.render("PORT", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_airport_avatar(ui, rect):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)

    runway = pygame.Rect(rect.x + 12, rect.y + 59, rect.width - 24, 16)
    pygame.draw.rect(g.screen, (66, 72, 76), runway, border_radius=2)
    pygame.draw.rect(g.screen, (34, 38, 42), runway, 1, border_radius=2)
    for i in range(5):
        pygame.draw.rect(g.screen, (224, 224, 210), (runway.x + 10 + i * 15, runway.y + 7, 7, 2))

    terminal = pygame.Rect(rect.x + 17, rect.y + 33, 34, 24)
    pygame.draw.rect(g.screen, (155, 169, 174), terminal, border_radius=3)
    pygame.draw.rect(g.screen, (70, 81, 87), terminal, 1, border_radius=3)
    pygame.draw.rect(g.screen, (92, 148, 180), (terminal.x + 6, terminal.y + 7, 22, 8))

    tower = pygame.Rect(rect.right - 31, rect.y + 28, 16, 32)
    pygame.draw.rect(g.screen, (132, 145, 151), tower, border_radius=2)
    pygame.draw.rect(g.screen, (66, 75, 82), tower, 1, border_radius=2)
    pygame.draw.polygon(g.screen, (85, 138, 169), [(tower.x - 4, tower.y), (tower.right + 4, tower.y), (tower.right, tower.y - 9), (tower.x, tower.y - 9)])
    pygame.draw.polygon(g.screen, (48, 78, 96), [(tower.x - 4, tower.y), (tower.right + 4, tower.y), (tower.right, tower.y - 9), (tower.x, tower.y - 9)], 1)

    plane = [(rect.centerx - 5, rect.y + 48), (rect.centerx + 28, rect.y + 39), (rect.centerx + 4, rect.y + 57), (rect.centerx + 6, rect.y + 72)]
    pygame.draw.polygon(g.screen, (230, 234, 232), plane)
    pygame.draw.polygon(g.screen, (80, 91, 101), plane, 1)
    pygame.draw.polygon(g.screen, (91, 151, 188), [(rect.centerx + 2, rect.y + 54), (rect.centerx - 18, rect.y + 43), (rect.centerx - 2, rect.y + 61)])
    pygame.draw.polygon(g.screen, (91, 151, 188), [(rect.centerx + 3, rect.y + 60), (rect.centerx - 12, rect.y + 75), (rect.centerx + 8, rect.y + 65)])

    sign = pygame.Rect(rect.centerx - 24, rect.y + 76, 48, 12)
    pygame.draw.rect(g.screen, (58, 78, 91), sign, border_radius=2)
    pygame.draw.rect(g.screen, (26, 38, 47), sign, 1, border_radius=2)
    label = g.small.render("AIRPORT", True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=sign.center))


def draw_generic_avatar(ui, rect, kind):
    g = ui.game
    pygame.draw.rect(g.screen, ui.PANEL_3, rect, border_radius=5)
    pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=5)
    pygame.draw.rect(g.screen, (62, 74, 88), rect.inflate(-18, -24), border_radius=4)
    pygame.draw.rect(g.screen, (111, 179, 255), rect.inflate(-18, -24), 2, border_radius=4)
    label = g.font.render(kind.value[:1], True, ui.TEXT)
    g.screen.blit(label, label.get_rect(center=(rect.centerx, rect.centery - 8)))
    name = g.small.render(kind.value.split()[0], True, ui.MUTED)
    g.screen.blit(name, name.get_rect(center=(rect.centerx, rect.bottom - 16)))
