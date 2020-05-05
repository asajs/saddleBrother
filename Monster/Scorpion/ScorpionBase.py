from Monster import MonsterBase
from Monster.Scorpion import ScorpionIdle
from Monster.Scorpion import ScorpionAttacking


class ScorpionBase(MonsterBase.MonsterBase):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.__state = ScorpionIdle.ScorpionIdle()
        self.__state.enter_state(self)


    def next_move(self):
        state = self.__state.next_move(self)
        if state is not None:
            self.__state = state
            self.__state.enter_state(self)


