# PyCity 2000

A compact SimCity 2000-inspired city builder written in Python and Pygame.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 pycity2000.py
```

## Goal

Grow a balanced city while keeping money, power, water, safety, health, and citizen mood under control. Zone land, connect it with roads, add infrastructure, tune taxes, and react to fires.

Some civic and utility buildings reserve larger footprints: police, fire, clinic, school, and solar plants are 2x2; coal plants are 3x3. Hovering a tool previews the full footprint before placement.

## Controls

- `WASD` / arrow keys: pan camera
- Mouse wheel: zoom
- Click minimap: center camera on that map location
- Left click: use selected tool
- Drag roads, bridges, power lines, or water pipes to preview a path; release to build it
- Drag residential, commercial, or industrial zoning to preview an area; release to zone it
- Right click: inspect a tile
- `1`: road
- `B`: bridge
- `2`: residential zone
- `3`: commercial zone
- `4`: industrial zone
- `5`: power line
- `6`: water pipe
- `7`: park
- `8`: police
- `9`: fire station
- `0`: clinic
- `-`: school
- `=`: coal plant
- `P`: solar plant
- `X`: bulldoze
- `F`: trigger fire disaster
- `Q` / `E`: rotate map left / right
- `Space`: pause or resume
- `[` / `]`: adjust simulation speed
- Top bar buttons: Pause, Play (`0.5x`), Fast (`1.5x`), Faster (`2.5x`)
- Camera movement and rotation temporarily pause simulation, then restore the previous time state
- `T` / `Y`: lower / raise tax
- `N`: new map
- `Esc`: quit
