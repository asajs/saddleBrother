import math
import ImageHandler
import EnumTypes
import GameMap
from Items import MovingItemBase
from MovingEntity import MovementComponent, MovingEntityHandler


class AttackLasso(MovingItemBase.MovingItemBase):
    def __init__(self, start_point, end_point):
        sprite = ImageHandler.get_specifc_image(EnumTypes.ZoneType.DESERT,
                                                EnumTypes.ImageType.ITEM,
                                                EnumTypes.AttackItemType.ATTACK_LASSO)
        self.acceleration = 2
        self.friction = 0
        self.max_speed = 10
        super().__init__(sprite, self.acceleration, self.friction, self.max_speed)
        self.damage = 5
        self.distance_traveled = 0
        self.distance_per_frame = 0
        self.max_distance = 0
        self.set_angle_of_movement(start_point, end_point)

    def set_angle_of_movement(self, start_point, end_point):
        self.center_x = start_point[0]
        self.center_y = start_point[1]

        # x_diff = (end_point[0] + self.view_left) - self.center_x
        # y_diff = (end_point[1] + self.view_bottom) - self.center_y

        x_diff = (end_point[0]) - self.center_x
        y_diff = (end_point[1]) - self.center_y
        self.max_distance = math.hypot(x_diff, y_diff)

        angle = math.atan2(y_diff, x_diff)
        self.angle = math.degrees(angle) - 90
        self.change_x = math.cos(angle) * self.max_speed
        self.change_y = math.sin(angle) * self.max_speed

    def update(self):
        super().update()
        self.distance_traveled += self.max_speed
        entity = EnumTypes.MovingType.SCORPION
        collisions = MovementComponent.detect_collision_with_sprite_list(self, GameMap.GameMap.WALL_LIST)
        entity_collisions = MovementComponent.detect_collision_with_sprite_list(self, MovingEntityHandler.MovingEntityHandler.movingTypes[entity])
        if collisions or self.distance_traveled >= self.max_distance:
            self.remove_from_sprite_lists()
        if entity_collisions:
            self.remove_from_sprite_lists()
            for entity in entity_collisions:
                entity.health -= self.damage
