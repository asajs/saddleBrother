from MovingEntity.Scorpion import ScorpionIdle, ScorpionChasing
from MovingEntity import MovementComponent, MovingEntityHandler, MovingEntityBase
from enum import Enum
import ImageHandler
import EnumTypes
import GlobalInfo


class ValidStates(Enum):
    IDLE = 1
    CHASE = 2
    ATTACK = 3


class ScorpionBase(MovingEntityBase.MovingEntityBase):
    def __init__(self):
        sprite = ImageHandler.get_specifc_image(EnumTypes.ZoneType.DESERT,
                                                EnumTypes.ImageType.MONSTER,
                                                EnumTypes.MovingType.SCORPION)
        super().__init__(sprite)
        self.awareness = 3 * GlobalInfo.IMAGE_SIZE
        self.attack_range = 0 * GlobalInfo.IMAGE_SIZE + 10  # Melee distance
        self.health = 10
        self.__target_types = [EnumTypes.MovingType.SCORPION, EnumTypes.MovingType.CHARACTER]
        self.__target = None
        self.__state = ScorpionIdle.ScorpionIdle()
        self.current_state = ValidStates.IDLE
        self.__state.enter_state(self)

    def next_move(self):
        self.__state.next_move(self)
        self.next_state()

    def next_state(self):
        target, distance = MovingEntityHandler.MovingEntityHandler.get_nearest_target(self, self.__target_types)

        if distance > self.awareness and self.current_state != ValidStates.IDLE:
            self.__state = ScorpionIdle.ScorpionIdle()
            self.current_state = ValidStates.IDLE
            self.__state.enter_state(self)
        elif self.attack_range < distance <= self.awareness and (self.current_state != ValidStates.CHASE or self.__target != target):
            self.__state = ScorpionChasing.ScorpionChasing(target)
            self.current_state = ValidStates.CHASE
            self.__state.enter_state(self)

    def update(self):
        if self.health <= 0:
            self.remove_from_sprite_lists()
        self.next_move()
        for sprite_list in MovingEntityHandler.MovingEntityHandler.movingTypes.values():
            MovementComponent.account_for_collision_list(self, sprite_list)
        super().update()

