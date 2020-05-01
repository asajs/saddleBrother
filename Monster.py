import arcade
import GameMap
import math
import random
import GlobalInfo
from enum import Enum


class State(Enum):
    IDLE = 1
    ATTACKING = 2


class Monster(arcade.Sprite):
    def __init__(self, sprite, acceleration=1.0, friction=0.2, max_speed=5.0, awareness=6):
        super().__init__(sprite, GlobalInfo.CHARACTER_SCALING)
        self.acceleration = acceleration
        self.friction = friction
        self.max_speed = max_speed
        self.awareness = awareness * GlobalInfo.IMAGE_SIZE
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.state = State.IDLE
        self.frame_counter = 0

        self.set_state(State.IDLE)

    def account_for_collision_list(self, item, list):
        collisions = arcade.check_for_collision_with_list(item, list)
        if collisions:
            collide = collisions.pop()

            x = collide.center_x - self.center_x
            y = collide.center_y - self.center_y
            angle = math.degrees(math.atan2(x, y)) # angles are from 0-180 and -180-0

            top_collision = -45 < angle <= 45
            right_collisions = 45 < angle <= 135
            bottom_collision = 135 < angle <= 180 or -180 <= angle <= -135
            left_collisions = -135 < angle <= -45

            if top_collision:
                self.change_y = 0
                self.top = collide.bottom - 1
            elif bottom_collision:
                self.change_y = 0
                self.bottom = collide.top + 1
            elif left_collisions:
                self.change_x = 0
                self.left = collide.right + 1
            elif right_collisions:
                self.change_x = 0
                self.right = collide.left - 1

    def move(self):
        if self.change_x > self.friction:
            self.change_x -= self.friction
        elif self.change_x < -self.friction:
            self.change_x += self.friction
        else:
            self.change_x = 0

        if self.change_y > self.friction:
            self.change_y -= self.friction
        elif self.change_y < -self.friction:
            self.change_y += self.friction
        else:
            self.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.change_y += self.acceleration
        elif self.down_pressed and not self.up_pressed:
            self.change_y -= self.acceleration
        if self.left_pressed and not self.right_pressed:
            self.change_x -= self.acceleration
        elif self.right_pressed and not self.left_pressed:
            self.change_x += self.acceleration

        if self.change_x > self.max_speed:
            self.change_x = self.max_speed
        elif self.change_x < -self.max_speed:
            self.change_x = -self.max_speed
        if self.change_y > self.max_speed:
            self.change_y = self.max_speed
        elif self.change_y < -self.max_speed:
            self.change_y = -self.max_speed

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
            self.change_x = 0
        elif self.right > GlobalInfo.GAME_WIDTH - 1:
            self.right = GlobalInfo.GAME_WIDTH - 1
            self.change_x = 0

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > GlobalInfo.GAME_HEIGHT - 1:
            self.top = GlobalInfo.GAME_HEIGHT - 1
            self.change_y = 0

    def computer_next_move(self):
        # only check state every 5 frames
        if self.frame_counter < 25:
            self.frame_counter += 1
            return

        self.frame_counter = 0

        if self.state == State.IDLE:
            random_int = random.randint(0, 20)
            if random_int == 0:
                self.down_pressed = False
                self.up_pressed = True
            elif random_int == 1:
                self.left_pressed = False
                self.right_pressed = True
            elif random_int == 2:
                self.up_pressed = False
                self.down_pressed = True
            elif random_int == 3:
                self.right_pressed = False
                self.left_pressed = True
            else:
                self.down_pressed = False
                self.left_pressed = False
                self.up_pressed = False
                self.right_pressed = False

    def set_state(self, next_state):
        if next_state == State.IDLE:
            self.state = next_state
            self.acceleration = 0.3
            self.max_speed = 2.5
