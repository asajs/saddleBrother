import arcade
import GlobalInfo
import GameWindow


def main():
    window = arcade.Window(GlobalInfo.SCREEN_WIDTH, GlobalInfo.SCREEN_HEIGHT, GlobalInfo.SCREEN_TITLE)
    game = GameWindow.GameWindow()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
