from MovingEntity import MovingEntityBase, MovementComponent, MovingEntityHandler
from Items import ItemHandler
import EnumTypes
import ImageHandler
import arcade
import GameMap


class Character(MovingEntityBase.MovingEntityBase):
    def __init__(self):
        sprite = ImageHandler.get_path("Images/saddlebrother.png")
        super().__init__(sprite)
        self.lasso_count = 20
        self.score = 0

    def update(self):
        for entity_type, sprite_list in MovingEntityHandler.MovingEntityHandler.movingTypes.items():
            if entity_type is not EnumTypes.MovingType.CHARACTER:
                MovementComponent.account_for_collision_list(self, sprite_list)
        for entity_type, sprite_list in ItemHandler.ItemHandler.itemTypes.items():
            if entity_type == EnumTypes.PickupItemType.PICKUP_LASSO:
                collisions = MovementComponent.detect_collision_with_sprite_list(self, sprite_list)
                if collisions:
                    self.lasso_count += 1
                    for lasso in collisions:
                        GameMap.GameMap.place_object_random_empty_spot(lasso)
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

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int, view_left, view_bottom):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.lasso_count > 0:
                # self.lasso_count -= 1
                item_type = EnumTypes.AttackItemType.ATTACK_LASSO
                start_point = (self.center_x, self.center_y)
                end_point = (x + view_left, y + view_bottom)
                ItemHandler.ItemHandler.add_type_with_start_end_points(item_type, start_point, end_point)
