import pygame

import citizen_avatars
import inspector
from pycity2000 import (
    ACCENT,
    BAD,
    Button,
    BuildKind,
    Citizen,
    COST,
    FASTER_SPEED,
    FAST_SPEED,
    FOOTPRINTS,
    GARBAGE_ZONE_CAPACITY,
    GOOD,
    INSPECTOR_AVATAR_KINDS,
    MapMode,
    MUTED,
    PANEL_2,
    PANEL_3,
    PANEL_BG,
    PLAY_SPEED,
    ROAD_KINDS,
    SCREEN_H,
    SCREEN_W,
    SERVICE_KINDS,
    SIDEBAR_W,
    TEXT,
    TOOL_BUILD,
    TOPBAR_H,
    Tool,
    WARN,
    WORKING_AGE_MIN,
    ZONE_KINDS,
    clamp,
    heat_color,
    meter_color,
    risk_color,
)


AVATAR_ROLE_OPTIONS = (
    "child",
    "student",
    "unemployed",
    "worker",
    "commercial",
    "industrial",
    "civic",
    "utility",
    "transport",
    "elder",
)

AVATAR_EDITOR_SLIDERS = (
    ("gender", "Gender", 0, 1),
    ("age", "Age", 0, 95),
    ("role", "Role", 0, len(AVATAR_ROLE_OPTIONS) - 1),
    ("skin", "Skin", 0, len(citizen_avatars.SKIN_TONES) - 1),
    ("hair", "Hair", 0, len(citizen_avatars.HAIR_COLORS) - 1),
    ("hair-style", "Hair style", 0, 6),
    ("health", "Health", 0, 100),
    ("education", "Education", 0, 100),
    ("happiness", "Happiness", 0, 100),
)


class UI:
    def __init__(self, game):
        self.game = game
        self.PANEL_3 = PANEL_3
        self.TEXT = TEXT
        self.MUTED = MUTED
        self.buttons = []
        self.menu_buttons = []
        self.time_buttons = []
        self.build_menus = []
        self.open_menu = None
        self.game_menu_open = False
        self.map_menu_open = False
        self.map_mode = MapMode.STANDARD
        self.budget_open = False
        self.population_open = False
        self.population_scroll = 0
        self.selected_citizen_id = None
        self.avatar_editor_open = False
        self.avatar_slider_dragging = None
        self.avatar_editor_values = {
            "gender": 1,
            "age": 32,
            "role": AVATAR_ROLE_OPTIONS.index("commercial"),
            "skin": 1,
            "hair": 1,
            "hair-style": 1,
            "health": 80,
            "education": 35,
            "happiness": 70,
        }
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

    def handle_wheel(self, mx, my, dy):
        if not self.population_open or not self.population_popup_rect().collidepoint(mx, my):
            return False
        max_scroll = max(0, len(self.population_citizen_ids()) - self.population_visible_count())
        self.population_scroll = int(clamp(self.population_scroll - dy, 0, max_scroll))
        return True

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
                    elif action == "avatar_editor":
                        self.avatar_editor_open = True
                    elif action == "quit":
                        self.game.running = False
                    return True
            if self.game_menu_rect().collidepoint(mx, my):
                return True
            self.game_menu_open = False
            return True
        if self.avatar_editor_open and self.avatar_editor_popup_rect().collidepoint(mx, my):
            if self.avatar_editor_close_rect().collidepoint(mx, my):
                self.avatar_editor_open = False
                self.avatar_slider_dragging = None
            else:
                slider_key = self.avatar_editor_slider_at(mx, my)
                if slider_key:
                    self.avatar_slider_dragging = slider_key
                    self.set_avatar_editor_slider_from_mouse(slider_key, mx)
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

        if self.selected_citizen_id and self.citizen_popup_rect().collidepoint(mx, my):
            if self.citizen_close_rect().collidepoint(mx, my):
                self.selected_citizen_id = None
            else:
                for building_id, rect in self.citizen_building_click_items():
                    if rect.collidepoint(mx, my):
                        self.select_building(building_id)
                        break
            return True
        if self.population_open and self.population_popup_rect().collidepoint(mx, my):
            if self.population_close_rect().collidepoint(mx, my):
                self.population_open = False
            else:
                for citizen_id, citizen_rect, home_rect in self.population_click_items():
                    if citizen_rect.collidepoint(mx, my):
                        self.selected_citizen_id = citizen_id
                        break
                    if home_rect.collidepoint(mx, my):
                        home_id = self.game.city.citizen_home_building_id(self.game.city.citizens[citizen_id])
                        self.select_building(home_id)
                        break
            return True
        if self.game.city.selected and self.inspector_popup_rect().collidepoint(mx, my):
            if self.inspector_close_rect().collidepoint(mx, my):
                self.game.city.selected = None
                self.selected_citizen_id = None
            else:
                for citizen_id, rect in self.resident_click_items():
                    if rect.collidepoint(mx, my):
                        self.selected_citizen_id = citizen_id
                        break
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
        if self.population_button_rect().collidepoint(mx, my):
            self.game_menu_open = False
            self.map_menu_open = False
            self.open_menu = None
            self.population_open = not self.population_open
            max_scroll = max(0, len(self.population_citizen_ids()) - self.population_visible_count())
            self.population_scroll = int(clamp(self.population_scroll, 0, max_scroll))
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
        self.draw_population_popup()
        self.draw_inspector_popup()
        self.draw_citizen_popup()
        self.draw_avatar_editor_popup()
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
        return pygame.Rect(button.right - width, TOPBAR_H - 2, width, 168)

    def game_menu_items(self):
        rect = self.game_menu_rect()
        return [
            ("save", pygame.Rect(rect.x + 6, rect.y + 6, rect.width - 12, 28)),
            ("load", pygame.Rect(rect.x + 6, rect.y + 38, rect.width - 12, 28)),
            ("disasters", pygame.Rect(rect.x + 6, rect.y + 70, rect.width - 12, 28)),
            ("avatar_editor", pygame.Rect(rect.x + 6, rect.y + 102, rect.width - 12, 28)),
            ("quit", pygame.Rect(rect.x + 6, rect.y + 134, rect.width - 12, 28)),
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
            "avatar_editor": "Avatar editor",
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

        self.draw_population_button(x + 14, TOPBAR_H + 286)

        y = TOPBAR_H + 343
        self.section_title("City", x + 14, y)
        y += 24
        self.metric("Demand R", c.stats.demand_r, -80, 100, x + 14, y, GOOD)
        self.metric("Demand C", c.stats.demand_c, -80, 100, x + 14, y + 28, ACCENT)
        self.metric("Demand I", c.stats.demand_i, -80, 100, x + 14, y + 56, WARN)
        self.metric("Power", c.stats.power_used, 0, max(1, c.stats.power_cap), x + 14, y + 86, (255, 218, 88), suffix=f" / {c.stats.power_cap}")
        self.metric("Water", c.stats.water_used, 0, max(1, c.stats.water_cap), x + 14, y + 112, (104, 182, 255), suffix=f" / {c.stats.water_cap}")
        self.metric("Garbage", c.stats.garbage_used, 0, max(1, c.stats.garbage_cap), x + 14, y + 138, (151, 189, 118), suffix=f" / {c.stats.garbage_cap}")
        self.metric("Traffic", c.stats.traffic, 0, 100, x + 14, y + 164, WARN)
        self.metric("Pollution", c.stats.pollution, 0, 100, x + 14, y + 190, BAD)

        y += 220
        self.draw_budget_button(x + 14, y)

        map_y = self.minimap_rect().y
        self.draw_minimap(x + 16, map_y)
        self.draw_graphs(x + 154, map_y)
        self.draw_map_menu()

    def budget_button_rect(self):
        return pygame.Rect(SCREEN_W - SIDEBAR_W + 14, TOPBAR_H + 571, 260, 34)

    def population_button_rect(self):
        return pygame.Rect(SCREEN_W - SIDEBAR_W + 14, TOPBAR_H + 286, 260, 34)

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
        height = len(MapMode) * 32 + 12
        y = int(clamp(title.y, TOPBAR_H + 8, SCREEN_H - height - 8))
        return pygame.Rect(title.x - width - 8, y, width, height)

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

    def draw_population_button(self, x, y):
        g, c = self.game, self.game.city
        rect = self.population_button_rect()
        active = self.population_open
        pygame.draw.rect(g.screen, ACCENT if active else PANEL_2, rect, border_radius=6)
        pygame.draw.rect(g.screen, (75, 86, 99), rect, 1, border_radius=6)
        color = (15, 20, 25) if active else TEXT
        label = g.font.render("Population", True, color)
        g.screen.blit(label, (rect.x + 10, rect.y + 8))
        count = g.small.render(f"{len(c.citizens):,}", True, color if active else MUTED)
        g.screen.blit(count, (rect.right - count.get_width() - 10, rect.y + 10))

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

    def avatar_editor_popup_rect(self):
        width, height = 650, 396
        return pygame.Rect((SCREEN_W - SIDEBAR_W - width) // 2, TOPBAR_H + 72, width, height)

    def avatar_editor_close_rect(self):
        rect = self.avatar_editor_popup_rect()
        return pygame.Rect(rect.right - 28, rect.y + 8, 20, 20)

    def avatar_editor_preview_rect(self):
        rect = self.avatar_editor_popup_rect()
        return pygame.Rect(rect.x + 26, rect.y + 74, 174, 174)

    def avatar_editor_slider_rect(self, key):
        rect = self.avatar_editor_popup_rect()
        keys = [slider[0] for slider in AVATAR_EDITOR_SLIDERS]
        i = keys.index(key)
        return pygame.Rect(rect.x + 282, rect.y + 58 + i * 34, 270, 8)

    def avatar_editor_slider_hit_rect(self, key):
        return self.avatar_editor_slider_rect(key).inflate(0, 18)

    def avatar_editor_slider_at(self, mx, my):
        for key, _, _, _ in AVATAR_EDITOR_SLIDERS:
            if self.avatar_editor_slider_hit_rect(key).collidepoint(mx, my):
                return key
        return None

    def set_avatar_editor_slider_from_mouse(self, key, mx):
        slider = self.avatar_editor_slider_rect(key)
        spec = next(item for item in AVATAR_EDITOR_SLIDERS if item[0] == key)
        _, _, min_value, max_value = spec
        ratio = clamp((mx - slider.x) / slider.width, 0.0, 1.0)
        self.avatar_editor_values[key] = int(round(min_value + ratio * (max_value - min_value)))

    def avatar_editor_value_label(self, key):
        value = self.avatar_editor_values[key]
        if key == "gender":
            return "Female" if value else "Male"
        if key == "role":
            return AVATAR_ROLE_OPTIONS[value].replace("_", " ").title()
        return str(value)

    def avatar_editor_citizen(self):
        c = self.game.city
        age = self.avatar_editor_values["age"]
        born = (c.month, c.day, c.year - age)
        gender = "f" if self.avatar_editor_values["gender"] else "m"
        citizen = Citizen(
            id=900001,
            name="Avatar Preview",
            gender=gender,
            born=born,
            health=float(self.avatar_editor_values["health"]),
            education=float(self.avatar_editor_values["education"]),
            happiness=float(self.avatar_editor_values["happiness"]),
        )
        citizen.avatar_overrides = {
            "role": AVATAR_ROLE_OPTIONS[self.avatar_editor_values["role"]],
            "skin": self.avatar_editor_values["skin"],
            "hair": self.avatar_editor_values["hair"],
            "hair-style": self.avatar_editor_values["hair-style"],
        }
        return citizen

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

    def draw_avatar_editor_popup(self):
        if not self.avatar_editor_open:
            return
        g = self.game
        rect = self.avatar_editor_popup_rect()
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=7)
        self.section_title("Avatar editor", rect.x + 14, rect.y + 12)
        close = self.avatar_editor_close_rect()
        pygame.draw.rect(g.screen, PANEL_3, close, border_radius=4)
        pygame.draw.rect(g.screen, (88, 100, 116), close, 1, border_radius=4)
        x_label = g.small.render("x", True, MUTED)
        g.screen.blit(x_label, x_label.get_rect(center=close.center))

        preview_rect = self.avatar_editor_preview_rect()
        citizen_avatars.draw_citizen_avatar(self, preview_rect, self.avatar_editor_citizen())
        self.text_line("Preview", preview_rect.x + 50, preview_rect.bottom + 16, MUTED)

        for key, label, min_value, max_value in AVATAR_EDITOR_SLIDERS:
            slider = self.avatar_editor_slider_rect(key)
            value = self.avatar_editor_values[key]
            ratio = (value - min_value) / max(1, max_value - min_value)
            self.text_line(label, rect.x + 226, slider.y - 7, TEXT)
            value_label = g.small.render(self.avatar_editor_value_label(key), True, MUTED)
            g.screen.blit(value_label, (slider.right + 12, slider.y - 7))
            pygame.draw.rect(g.screen, PANEL_3, slider, border_radius=4)
            fill = pygame.Rect(slider.x, slider.y, int(slider.width * ratio), slider.height)
            pygame.draw.rect(g.screen, ACCENT, fill, border_radius=4)
            knob_x = slider.x + int(slider.width * ratio)
            pygame.draw.circle(g.screen, TEXT, (knob_x, slider.centery), 7)
            pygame.draw.circle(g.screen, (88, 100, 116), (knob_x, slider.centery), 7, 1)

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
        if tile.build == BuildKind.GARBAGE:
            lines.append(f"Landfill {tile.garbage_fill:.0f}/{GARBAGE_ZONE_CAPACITY}")
        if tile.build in {BuildKind.RES, BuildKind.COM, BuildKind.IND}:
            if tile.build == BuildKind.RES:
                lines.extend(inspector.extra_lines(self, tile.build, origin) or [])
            lines.append(inspector.zone_score_line(self, tile))
        elif tile.build in ROAD_KINDS:
            lines.extend(inspector.road_lines(self, pos))
        else:
            extra = inspector.extra_lines(self, tile.build, origin)
            if extra:
                lines.extend(extra)
        return lines

    def resident_click_items(self, limit=10):
        c = self.game.city
        if not c.selected:
            return []
        tx, ty = c.selected
        tile = c.tiles[tx][ty]
        if tile.build != BuildKind.RES:
            return []
        building = c.building_at_origin(c.building_origin(tx, ty))
        if not building:
            return []
        rect = self.inspector_popup_rect()
        resident_ids = [cid for cid in building.resident_ids if cid in c.citizens][:limit]
        items = []
        first_line_index = 5
        for i, citizen_id in enumerate(resident_ids):
            row = pygame.Rect(rect.x + 12, rect.y + 36 + (first_line_index + i) * 17, rect.width - 24, 17)
            items.append((citizen_id, row))
        return items

    def citizen_building_click_items(self):
        c = self.game.city
        citizen = c.citizens.get(self.selected_citizen_id)
        if not citizen:
            return []
        home_id = c.citizen_home_building_id(citizen)
        building_ids = [home_id, citizen.job_id, citizen.school_id]
        rect = self.citizen_popup_rect()
        text_x, text_y = self.citizen_text_origin()
        items = []
        for i, building_id in enumerate(building_ids):
            if building_id in c.buildings:
                row_index = i + 2
                row = pygame.Rect(text_x, text_y + row_index * 16, rect.right - text_x - 12, 16)
                items.append((building_id, row))
        return items

    def population_citizen_ids(self):
        c = self.game.city

        def citizen_home(citizen_id, citizen):
            home_id = c.citizen_home_building_id(citizen)
            if home_id in c.buildings:
                return c.buildings[home_id]
            for building in c.buildings.values():
                if building.kind == BuildKind.RES and citizen_id in building.resident_ids:
                    return building
            return None

        def sort_key(citizen_id):
            citizen = c.citizens[citizen_id]
            home = citizen_home(citizen_id, citizen)
            home_origin = home.origin if home else (c.width, c.height)
            household_id = citizen.household_id if citizen.household_id is not None else citizen_id
            age = c.citizen_age(citizen)
            age_order = 1 if age < WORKING_AGE_MIN else 0
            return home_origin[1], home_origin[0], household_id, age_order, citizen.name, citizen_id

        return sorted(c.citizens, key=sort_key)

    def population_popup_rect(self):
        width = 470
        height = min(SCREEN_H - TOPBAR_H - 90, 520)
        x = SCREEN_W - SIDEBAR_W - width - 10
        y = TOPBAR_H + 58
        return pygame.Rect(x, y, width, height)

    def population_close_rect(self):
        rect = self.population_popup_rect()
        return pygame.Rect(rect.right - 28, rect.y + 8, 20, 20)

    def population_visible_count(self):
        rect = self.population_popup_rect()
        return max(1, (rect.height - 76) // 86)

    def population_click_items(self):
        c = self.game.city
        rect = self.population_popup_rect()
        ids = self.population_citizen_ids()
        visible_count = self.population_visible_count()
        max_scroll = max(0, len(ids) - visible_count)
        self.population_scroll = int(clamp(self.population_scroll, 0, max_scroll))
        visible_ids = ids[self.population_scroll:self.population_scroll + visible_count]
        items = []
        y = rect.y + 58
        for i, citizen_id in enumerate(visible_ids):
            row_y = y + i * 86
            citizen_rect = pygame.Rect(rect.x + 94, row_y + 12, 250, 28)
            home_rect = pygame.Rect(rect.x + 94, row_y + 44, 126, 24)
            items.append((citizen_id, citizen_rect, home_rect))
        return items

    def select_building(self, building_id):
        building = self.game.city.buildings.get(building_id)
        if not building:
            return
        self.game.city.selected = building.origin
        self.center_camera_on_tile(*building.origin)

    def inspector_popup_rect(self):
        g, c = self.game, self.game.city
        if not c.selected:
            return pygame.Rect(0, 0, 0, 0)
        sx, sy = g.tile_screen(*c.selected)
        width = 480 if self.inspector_avatar_kind(c.selected) else 390
        height = min(360, max(136, 54 + len(self.inspector_lines(c.selected)) * 17))
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

    def inspector_avatar_kind(self, pos=None):
        c = self.game.city
        if pos is None:
            pos = c.selected
        if not pos:
            return None
        tile = c.tiles[pos[0]][pos[1]]
        if tile.build in INSPECTOR_AVATAR_KINDS:
            return tile.build
        return None

    def inspector_avatar_rect(self):
        if not self.inspector_avatar_kind():
            return pygame.Rect(0, 0, 0, 0)
        rect = self.inspector_popup_rect()
        return pygame.Rect(rect.x + 12, rect.y + 36, 108, 92)

    def inspector_text_origin(self):
        rect = self.inspector_popup_rect()
        if self.inspector_avatar_kind():
            return rect.x + 132, rect.y + 36
        return rect.x + 12, rect.y + 36

    def citizen_popup_rect(self):
        if not self.selected_citizen_id or self.selected_citizen_id not in self.game.city.citizens:
            return pygame.Rect(0, 0, 0, 0)
        anchor = self.inspector_popup_rect()
        width = 430
        height = 176
        view_right = SCREEN_W - SIDEBAR_W
        x = anchor.right + 12
        if x + width > view_right - 12:
            x = anchor.left - width - 12
        y = anchor.top
        x = int(clamp(x, 12, view_right - width - 12))
        y = int(clamp(y, TOPBAR_H + 10, SCREEN_H - height - 12))
        return pygame.Rect(x, y, width, height)

    def citizen_close_rect(self):
        rect = self.citizen_popup_rect()
        return pygame.Rect(rect.right - 28, rect.y + 8, 20, 20)

    def citizen_avatar_rect(self):
        rect = self.citizen_popup_rect()
        return pygame.Rect(rect.x + 12, rect.y + 40, 104, 104)

    def citizen_text_origin(self):
        rect = self.citizen_popup_rect()
        return rect.x + 132, rect.y + 40

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
        self.draw_inspector_avatar()
        x, y = self.inspector_text_origin()
        lines = self.inspector_lines(c.selected)
        resident_rows = {citizen_id: row for citizen_id, row in self.resident_click_items()}
        for i, line in enumerate(lines):
            row_color = TEXT if i == 0 else MUTED
            for citizen_id, row in resident_rows.items():
                if row.y == y + i * 17:
                    row_color = ACCENT if citizen_id == self.selected_citizen_id else TEXT
                    break
            self.text_line(line, x, y + i * 17, row_color)

    def draw_inspector_avatar(self):
        kind = self.inspector_avatar_kind()
        if not kind:
            return
        inspector.draw_inspector_avatar(self, kind, self.inspector_avatar_rect())

    def draw_citizen_popup(self):
        g = self.game
        if not self.selected_citizen_id or self.selected_citizen_id not in self.game.city.citizens:
            return
        rect = self.citizen_popup_rect()
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=7)
        self.section_title("Citizen", rect.x + 12, rect.y + 10)
        close = self.citizen_close_rect()
        pygame.draw.rect(g.screen, PANEL_3, close, border_radius=4)
        pygame.draw.rect(g.screen, (88, 100, 116), close, 1, border_radius=4)
        x_label = g.small.render("x", True, MUTED)
        g.screen.blit(x_label, x_label.get_rect(center=close.center))
        citizen = self.game.city.citizens[self.selected_citizen_id]
        citizen_avatars.draw_citizen_avatar(self, self.citizen_avatar_rect(), citizen)
        x, y = self.citizen_text_origin()
        building_rows = {building_id: row for building_id, row in self.citizen_building_click_items()}
        for i, line in enumerate(inspector.citizen_lines(self, self.selected_citizen_id)):
            color = TEXT if i == 0 else MUTED
            for _, row in building_rows.items():
                if row.y == y + i * 16:
                    color = ACCENT
                    break
            self.text_line(line, x, y + i * 16, color)

    def draw_population_popup(self):
        if not self.population_open:
            return
        g, c = self.game, self.game.city
        rect = self.population_popup_rect()
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=7)
        pygame.draw.rect(g.screen, (88, 100, 116), rect, 1, border_radius=7)
        self.section_title("Population", rect.x + 12, rect.y + 10)
        close = self.population_close_rect()
        pygame.draw.rect(g.screen, PANEL_3, close, border_radius=4)
        pygame.draw.rect(g.screen, (88, 100, 116), close, 1, border_radius=4)
        x_label = g.small.render("x", True, MUTED)
        g.screen.blit(x_label, x_label.get_rect(center=close.center))

        total = len(c.citizens)
        visible = self.population_visible_count()
        end = min(total, self.population_scroll + visible)
        summary = g.small.render(f"{self.population_scroll + 1 if total else 0}-{end} of {total}", True, MUTED)
        g.screen.blit(summary, (rect.right - summary.get_width() - 42, rect.y + 13))

        if not total:
            self.text_line("No citizens yet", rect.x + 12, rect.y + 62, MUTED)
            return

        for citizen_id, citizen_rect, home_rect in self.population_click_items():
            citizen = c.citizens[citizen_id]
            selected = citizen_id == self.selected_citizen_id
            card = pygame.Rect(rect.x + 12, citizen_rect.y - 10, rect.width - 34, 76)
            pygame.draw.rect(g.screen, PANEL_3 if selected else PANEL_2, card, border_radius=6)
            pygame.draw.rect(g.screen, ACCENT if selected else (75, 86, 99), card, 1, border_radius=6)
            avatar_rect = pygame.Rect(card.x + 8, card.y + 6, 64, 64)
            citizen_avatars.draw_citizen_avatar(self, avatar_rect, citizen)
            pygame.draw.rect(g.screen, ACCENT if selected else PANEL_3, citizen_rect, border_radius=5)
            pygame.draw.rect(g.screen, (88, 100, 116), citizen_rect, 1, border_radius=5)
            name = g.small.render(f"{citizen.name}  Age {c.citizen_age(citizen)}", True, (15, 20, 25) if selected else TEXT)
            g.screen.blit(name, (citizen_rect.x + 8, citizen_rect.y + 7))
            home_id = c.citizen_home_building_id(citizen)
            home = c.buildings.get(home_id)
            home_label = f"{home.origin[0]},{home.origin[1]}" if home else "None"
            pygame.draw.rect(g.screen, PANEL_3, home_rect, border_radius=5)
            pygame.draw.rect(g.screen, (88, 100, 116), home_rect, 1, border_radius=5)
            home_text = g.small.render(f"Home {home_label}", True, ACCENT if home else MUTED)
            g.screen.blit(home_text, (home_rect.x + 8, home_rect.y + 5))

        if total > visible:
            track = pygame.Rect(rect.right - 10, rect.y + 58, 4, rect.height - 78)
            pygame.draw.rect(g.screen, PANEL_3, track, border_radius=2)
            max_scroll = max(1, total - visible)
            thumb_h = max(24, int(track.height * visible / total))
            thumb_y = track.y + int((track.height - thumb_h) * self.population_scroll / max_scroll)
            pygame.draw.rect(g.screen, MUTED, (track.x, thumb_y, track.width, thumb_h), border_radius=2)

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
                return risk_color(c.road_congestion(tx, ty))
            if tile.build in ZONE_KINDS:
                return (76, 70, 62)
            return (38, 47, 45) if not tile.water else (31, 70, 94)
        if self.map_mode == MapMode.LAND_VALUE:
            if tile.build in ZONE_KINDS:
                return heat_color(tile.land_value)
            if tile.water:
                return (31, 70, 94)
            return (44, 54, 45)
        if self.map_mode == MapMode.POLLUTION:
            return risk_color(tile.pollution)
        if self.map_mode == MapMode.CRIME:
            return risk_color(tile.crime)
        if self.map_mode == MapMode.FIRE_RISK:
            return risk_color(tile.fire_risk)
        if self.map_mode == MapMode.HEALTH:
            return heat_color(tile.health)
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

    def tool_tooltip_text(self):
        g = self.game
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
        elif g.tool == Tool.BULLDOZE:
            text = f"{g.tool.value} ${COST.get(g.tool, 0)}"
        elif g.tool in TOOL_BUILD:
            price = COST.get(g.tool, 0)
            fw, fh = FOOTPRINTS[TOOL_BUILD[g.tool]]
            size = f" {fw}x{fh}" if (fw, fh) != (1, 1) else ""
            text = f"{g.tool.value}{size} ${price}"
        else:
            text = "Inspect"
        return text

    def draw_tooltip(self):
        g = self.game
        mx, my = pygame.mouse.get_pos()
        if mx >= SCREEN_W - SIDEBAR_W or my < TOPBAR_H:
            return
        if not g.hover and not g.dragging_path and not g.dragging_zone:
            return
        text = self.tool_tooltip_text()
        surf = g.small.render(text, True, TEXT)
        rect = pygame.Rect(mx + 14, my + 16, surf.get_width() + 12, 24)
        pygame.draw.rect(g.screen, (18, 22, 27), rect, border_radius=5)
        pygame.draw.rect(g.screen, (74, 83, 96), rect, 1, border_radius=5)
        g.screen.blit(surf, (rect.x + 6, rect.y + 5))
