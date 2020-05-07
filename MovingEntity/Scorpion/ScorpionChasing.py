
class ScorpionChasing:
    def __init__(self, target_sprite):
        self.__target_sprite = target_sprite

    def next_move(self, scorpion_sprite):
        if self.__target_sprite.center_x > scorpion_sprite.center_x:
            scorpion_sprite.right_pressed = True
            scorpion_sprite.left_pressed = False
        elif self.__target_sprite.center_x < scorpion_sprite.center_x:
            scorpion_sprite.left_pressed = True
            scorpion_sprite.right_pressed = False
        if self.__target_sprite.center_y > scorpion_sprite.center_y:
            scorpion_sprite.up_pressed = True
            scorpion_sprite.down_pressed = False
        elif self.__target_sprite.center_y < scorpion_sprite.center_y:
            scorpion_sprite.down_pressed = True
            scorpion_sprite.up_pressed = False

    def enter_state(self, scorpion_sprite):
        scorpion_sprite.acceleration = 0.5
        scorpion_sprite.max_speed = 5.0
