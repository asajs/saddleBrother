import arcade
import GlobalInfo
import GameWindow

class PausedScreenView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        pass

    def on_draw(self):
        arcade.start_render()

        self.game_view.on_draw()
        left, right, bottom, top = self.window.get_viewport()
        middle_x = left + GlobalInfo.SCREEN_WIDTH / 2

        arcade.draw_lrtb_rectangle_filled(left=left,
                                          right=right,
                                          top=top,
                                          bottom=bottom,
                                          color=arcade.color.BLACK + (150,))

        arcade.draw_text("Every Saddle Brother needs a rest once in a while",
                         middle_x,
                         top - 50,
                         arcade.color.AMBER,
                         30,
                         anchor_x="center")
        arcade.draw_text("Escape to resume",
                         middle_x,
                         top - 80,
                         arcade.color.AMBER,
                         15,
                         anchor_x="center")
        arcade.draw_text("R to restart",
                         middle_x,
                         top - 110,
                         arcade.color.AMBER,
                         15,
                         anchor_x="center")
        arcade.draw_text("Q to quit",
                         middle_x,
                         top - 140,
                         arcade.color.AMBER,
                         15,
                         anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            return
        elif symbol == arcade.key.R:
            game = GameWindow.GameWindow()
            game.reset()
            game.setup()
            self.window.show_view(game)
        elif symbol == arcade.key.Q:
            arcade.close_window()
