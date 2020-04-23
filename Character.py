import arcade
import GlobalInfo


class Character(arcade.Sprite):
    def __init__(self, sprite):
        super().__init__(sprite, GlobalInfo.CHARACTER_SCALING)
        self.acceleration = 1.0
        self.friction = 0.2
        self.max_speed = 8.0
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

    def account_for_collision_list(self, collisions):
        if collisions:
            top_collision = [collide for collide in collisions if self.top - collide.bottom < self.max_speed]
            bottom_collision = [collide for collide in collisions if collide.top - self.bottom < self.max_speed]
            left_collisions = [collide for collide in collisions if collide.right - self.left < self.max_speed]
            right_collisions = [collide for collide in collisions if self.right - collide.left < self.max_speed]

            if top_collision:
                self.change_y = 0
                self.top = top_collision.pop().bottom - 1
            elif bottom_collision:
                self.change_y = 0
                self.bottom = bottom_collision.pop().top + 1
            if left_collisions:
                self.change_x = 0
                self.left = left_collisions.pop().right + 1
            elif right_collisions:
                self.change_x = 0
                self.right = right_collisions.pop().left - 1

    def move(self):
        if self.change_x > self.friction:
            self.change_x -=  self.friction
        elif self.change_x < -self.friction:
            self.change_x += self.friction
        else:
            self.change_x = 0

        if self.change_y > self.friction:
            self.change_y -=  self.friction
        elif self.change_y < -self.friction:
            self.change_y += self.friction
        else:
            self.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.change_y += self.acceleration
        elif self.down_pressed and not self.up_pressed:
            self.change_y -= self.acceleration
        elif self.left_pressed and not self.right_pressed:
            self.change_x -= self.acceleration
        elif self.right_pressed and not self.left_pressed:
            self.change_x += self.acceleration

        if self.change_x > self.max_speed:
            self.change_x = self.max_speed
        elif self.change_x < -self.max_speed:
            self.change_x = -self.max_speed
        elif self.change_y > self.max_speed:
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
