# core/level.py

import json
from entities.platform import Platform
from entities.enemy import Enemy

class Level:
    def __init__(self, filename,image):
        with open(filename, "r") as f:
            data = json.load(f)

        self.player_start = tuple(data["player_start"])
        self.end_x = data["end_x"]

        self.platforms = [
            Platform(*p,image) for p in data["platforms"]
        ]

        self.enemies = [
            Enemy(tuple(e),image.get_height()) for e in data["enemies"]
        ]
