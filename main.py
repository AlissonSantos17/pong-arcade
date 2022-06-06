import random
from arcade import Window, Section, SpriteList, SpriteSolidColor, \
    SpriteCircle, draw_text, draw_line, View, PyMunk
from arcade.color import BLACK, BLUE, RED, BEAU_BLUE, GRAY, WHITE
from arcade.key import W, S, UP, DOWN
import arcade
import os
import math

PLAYER_SECTION_WIDTH = 100
PLAYER_PADDLE_SPEED = 15

velocity = 7

def degree():
    return random.randrange(15, 45)

# Finds the y value to determine how the ball will choose an angle
def find_y(degree, velo_x):
    return round(math.tan(math.radians(degree)) * velo_x * flip_coin(), 1)

# Random chance generator to create a positive or negative number
def flip_coin():
    if random.choice([1, 2, 3, 4, 5, 6]) > 3:
        return -1
    else:
        return 1


class Player(Section):
    def __init__(self, left: int, bottom: int, width: int, height: int,
                 key_up: int, key_down: int, **kwargs):
        super().__init__(left, bottom, width, height,
                         accept_keyboard_events={key_up, key_down}, **kwargs)

        self.key_up: int = key_up
        self.key_down: int = key_down

        self.paddle: SpriteSolidColor = SpriteSolidColor(30, 100, WHITE)

        self.score: int = 0

    def setup(self):
        self.paddle.position = self.left + 50, self.height / 2

    def on_update(self, delta_time: float):
        self.paddle.update()

    def on_draw(self):
        if self.name == 'Left':
            keys = 'W e S'
            start_x = self.left + 5
        else:
            keys = 'UP e DOWN'
            start_x = self.left - 290

        draw_text(f'Jogador {self.name} (mova a base com: {keys})',
                  start_x, self.top - 20, WHITE, 9)

        draw_text(f'{self.score}', self.left + 20,
                  self.bottom + 20, WHITE, 15)

        self.paddle.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == self.key_up:
            self.paddle.change_y = PLAYER_PADDLE_SPEED
        else:
            self.paddle.change_y = -PLAYER_PADDLE_SPEED

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.paddle.stop()


class Pong(View):
    def __init__(self):
        super().__init__()
        self.paddles: SpriteList = SpriteList()

        self.left_player: Player = Player(
            0, 0, PLAYER_SECTION_WIDTH, self.window.height, key_up=W,
            key_down=S, name='Left')
        self.right_player: Player = Player(
            self.window.width - PLAYER_SECTION_WIDTH, 0, PLAYER_SECTION_WIDTH,
            self.window.height, key_up=UP, key_down=DOWN, name='Right')

        self.add_section(self.left_player)
        self.add_section(self.right_player)

        self.paddles.append(self.left_player.paddle)
        self.paddles.append(self.right_player.paddle)

        self.ball: SpriteCircle = SpriteCircle(10, WHITE)

        self.vel_x = None
        self.vel_y = None


    def setup(self):
        ball_angle = degree()
        self.vel_x = velocity * flip_coin()
        #
        self.vel_y = find_y(ball_angle, self.vel_x) * flip_coin()

        self.ball.position = self.window.width / 2, self.window.height / 2

        self.ball.change_x = self.vel_x
        self.ball.change_y = self.vel_y

        self.left_player.setup()
        self.right_player.setup()

    def on_update(self, delta_time: float):
        self.ball.update()

        if self.ball.bottom <= 0:
            self.ball.change_y *= -1
        elif self.ball.top >= self.window.height:
            self.ball.change_y *= -1

        collided_paddle = self.ball.collides_with_list(self.paddles)
        if collided_paddle:
            if collided_paddle[0] is self.left_player.paddle:
                self.ball.left = self.left_player.paddle.right
            else:
                self.ball.right = self.right_player.paddle.left

            self.ball.change_x *= -1

        if self.ball.right <= 0:
            self.end_game(self.right_player)
        elif self.ball.left >= self.window.width:
            self.end_game(self.left_player)


    def end_game(self, winner: Player):
        winner.score += 1
        self.setup()

    def on_draw(self):
        self.clear(BLACK)
        self.ball.draw()
        half_window_x = self.window.width / 2
        draw_line(half_window_x, 0, half_window_x, self.window.height, GRAY, 2)

class InstructionView(View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Arcade Game MultPlayer", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Clique para iniciar", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Pong()
        game_view.setup()
        self.window.show_view(game_view)

def main():
    window = Window(title='Arcade Game MultiPlayer')
    game = InstructionView()
    window.show_view(game)
    window.run()


if __name__ == '__main__':
    main()