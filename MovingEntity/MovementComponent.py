import math
import arcade
import GlobalInfo


def move(sprite):
    if sprite.change_x > sprite.friction:
        sprite.change_x -= sprite.friction
    elif sprite.change_x < -sprite.friction:
        sprite.change_x += sprite.friction
    else:
        sprite.change_x = 0

    if sprite.change_y > sprite.friction:
        sprite.change_y -= sprite.friction
    elif sprite.change_y < -sprite.friction:
        sprite.change_y += sprite.friction
    else:
        sprite.change_y = 0

    if sprite.up_pressed and not sprite.down_pressed:
        sprite.change_y += sprite.acceleration
    elif sprite.down_pressed and not sprite.up_pressed:
        sprite.change_y -= sprite.acceleration
    if sprite.left_pressed and not sprite.right_pressed:
        sprite.change_x -= sprite.acceleration
    elif sprite.right_pressed and not sprite.left_pressed:
        sprite.change_x += sprite.acceleration

    if sprite.change_x > sprite.max_speed:
        sprite.change_x = sprite.max_speed
    elif sprite.change_x < -sprite.max_speed:
        sprite.change_x = -sprite.max_speed
    if sprite.change_y > sprite.max_speed:
        sprite.change_y = sprite.max_speed
    elif sprite.change_y < -sprite.max_speed:
        sprite.change_y = -sprite.max_speed


def account_for_collision_list(sprite, sprite_list):
    collisions = detect_collision_with_sprite_list(sprite, sprite_list)
    if collisions:
        collide = collisions.pop()

        x = collide.center_x - sprite.center_x
        y = collide.center_y - sprite.center_y
        angle = math.degrees(math.atan2(x, y))  # angles are from 0-180 and -180-0

        top_collision = -45 < angle <= 45
        right_collisions = 45 < angle <= 135
        bottom_collision = 135 < angle <= 180 or -180 <= angle <= -135
        left_collisions = -135 < angle <= -45

        if top_collision:
            sprite.change_y = 0
            sprite.top = collide.bottom - 1
        elif bottom_collision:
            sprite.change_y = 0
            sprite.bottom = collide.top + 1
        elif left_collisions:
            sprite.change_x = 0
            sprite.left = collide.right + 1
        elif right_collisions:
            sprite.change_x = 0
            sprite.right = collide.left - 1

    return collisions


def detect_collision_with_sprite_list(sprite, sprite_list):
    return arcade.check_for_collision_with_list(sprite, sprite_list)


def update(sprite):
    sprite.center_x += sprite.change_x
    sprite.center_y += sprite.change_y

    if sprite.left < 0:
        sprite.left = 0
        sprite.change_x = 0
    elif sprite.right > GlobalInfo.GAME_WIDTH - 1:
        sprite.right = GlobalInfo.GAME_WIDTH - 1
        sprite.change_x = 0

    if sprite.bottom < 0:
        sprite.bottom = 0
        sprite.change_y = 0
    elif sprite.top > GlobalInfo.GAME_HEIGHT - 1:
        sprite.top = GlobalInfo.GAME_HEIGHT - 1
        sprite.change_y = 0
