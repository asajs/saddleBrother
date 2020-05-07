from MovingEntity import MovingEntityBase, MovementComponent, MovingEntityHandler
from Items import ItemHandler
import EnumTypes
import ImageHandler
import arcade


class Character(MovingEntityBase.MovingEntityBase):
    def __init__(self):
        sprite = ImageHandler.get_path("Images/saddlebrother.png")
        super().__init__(sprite)
        self.lasso_count = 0
        self.score = 0

    def update(self):
        for entity_type, sprite_list in MovingEntityHandler.MovingEntityHandler.movingTypes.items():
            if entity_type is not EnumTypes.MovingType.CHARACTER:
                MovementComponent.account_for_collision_list(self, sprite_list)
        for entity_type, sprite_list in ItemHandler.ItemHandler.itemTypes.items():
            collisions = MovementComponent.account_for_collision_list(self, sprite_list)
            if collisions:
                self.lasso_count += 1
        super().update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.lasso_count > 0:
            self.lasso_count -= 1
            # TODO: create lasso
