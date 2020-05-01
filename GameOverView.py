from GameWindow import GameWindow
import arcade
import GlobalInfo


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        left, right, bottom, top = self.window.get_viewport()
        middle_x = left + GlobalInfo.SCREEN_WIDTH / 2

        arcade.draw_text("Ride into the sunset Saddle Brother", middle_x - 200, top - 25, arcade.color.WHITE, 50, anchor_x="center")
        arcade.draw_text("(Esc) to quit, any key to play again", middle_x - 200, top - 30, arcade.color.WHITE, 20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
            return
        else:
            game_window = GameWindow()
            game_window.setup()
            self.window.show_view(game_window)
