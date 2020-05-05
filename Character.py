from MovingEntity import MovingEntityBase


class Character(MovingEntityBase.MovingEntityBase):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.lasso_count = 0

