# core/level.py

import json
from entities.platform import Platform
from entities.enemy import create_enemy

class Level:
    def __init__(self, filename, image):
        with open(filename, "r") as f:
            data = json.load(f)

        self.player_start = tuple(data["player_start"])
        self.end_x = data["end_x"]

        self.platforms = [
            Platform(*p, image) for p in data["platforms"]
        ]

        # Load enemies with type specification
        self.enemies = []
        for enemy_data in data.get("enemies", []):
            if isinstance(enemy_data, list):
                # Old format: [x, y]
                self.enemies.append(create_enemy("ground", tuple(enemy_data)))
            elif isinstance(enemy_data, dict):
                # New format: {"x": 100, "y": 200, "type": "ground"}
                enemy_type = enemy_data.get("type", "ground")
                pos = (enemy_data["x"], enemy_data["y"])
                self.enemies.append(create_enemy(enemy_type, pos))
