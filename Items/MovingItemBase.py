import arcade
from MovingEntity import MovementComponent
import GlobalInfo
import GameMap


class MovingItemBase(arcade.Sprite):
    def __init__(self, sprite, acceleration=1.0, friction=0.2, max_speed=8.0):
        super().__init__(sprite, GlobalInfo.CHARACTER_SCALING)
        self.acceleration = acceleration
        self.friction = friction
        self.max_speed = max_speed

    def update(self):
        MovementComponent.account_for_collision_list(self, GameMap.GameMap.WALL_LIST)
        MovementComponent.update(self)
