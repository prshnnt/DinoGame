# player_states.py

from enum import Enum


class PlayerState(Enum):
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    DUCK = "duck"
    KICK = "kick"
    HURT = "hurt"