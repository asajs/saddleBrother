import random

IDLE_PAUSE = 25
CHANCE_OF_ACTION_MAX = 20


class ScorpionIdle:
    def __init__(self):
        self.__wait_to_move_again = 0
        self.__idle_pause = 25
        self.__chance_of_action_max = 20

    def next_move(self, scorpion_sprite):
        if self.__wait_to_move_again < self.__idle_pause:
            self.__wait_to_move_again += 1
            return

        self.__wait_to_move_again = 0

        random_int = random.randint(0, self.__chance_of_action_max)
        if random_int == 0:
            scorpion_sprite.down_pressed = False
            scorpion_sprite.up_pressed = True
        elif random_int == 1:
            scorpion_sprite.left_pressed = False
            scorpion_sprite.right_pressed = True
        elif random_int == 2:
            scorpion_sprite.up_pressed = False
            scorpion_sprite.down_pressed = True
        elif random_int == 3:
            scorpion_sprite.right_pressed = False
            scorpion_sprite.left_pressed = True
        else:
            scorpion_sprite.down_pressed = False
            scorpion_sprite.left_pressed = False
            scorpion_sprite.up_pressed = False
            scorpion_sprite.right_pressed = False

        return None

    def enter_state(self, scorpion_sprite):
        scorpion_sprite.acceleration = 0.3
        scorpion_sprite.max_speed = 2.5
