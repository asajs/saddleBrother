import GlobalInfo
from MovingEntity import MovingEntityBase

CLOSE_ENOUGH = 200


class MonsterBase(MovingEntityBase.MovingEntityBase):
    def __init__(self, sprite, acceleration=1.0, friction=0.2, max_speed=5.0, awareness=6):
        super().__init__(sprite, acceleration, friction, max_speed)
        self.awareness = awareness * GlobalInfo.IMAGE_SIZE

        # if self.distance_to_target() <= CLOSE_ENOUGH:
        #     self.set_state(State.ATTACKING)
        # elif self.distance_to_target() > CLOSE_ENOUGH:
        #     self.set_state(State.IDLE)


    # def distance_to_target(self):
    #     x = self.center_x - self.target.center_x
    #     y = self.center_y - self.target.center_y
    #     return math.hypot(x, y)
