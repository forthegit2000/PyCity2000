import math

from pycity2000 import BASE_TILE_H, BASE_TILE_W, MAP_H, MAP_W, SCREEN_W


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
