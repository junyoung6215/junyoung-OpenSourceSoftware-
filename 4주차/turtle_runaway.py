# -*- coding: utf-8 -*-
#21101718_권준영
# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.

import turtle, random

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50, init_dist=400):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius ** 2
        self.timer = 0  # Timer for tracking time
        self.score = 0  # Game score
        self.game_over = False  # Flag for game over status

        # Drawer for showing game status
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        """Check if the chaser catches the runner."""
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    def is_out_of_bounds_runner(self):
        """Check if the runner goes out of the visible window area."""
        x, y = self.runner.pos()
        screen_width = self.canvas.window_width() / 2
        screen_height = self.canvas.window_height() / 2
        return abs(x) > screen_width or abs(y) > screen_height

    def is_out_of_bounds_chaser(self):
        """Check if the runner goes out of the visible window area."""
        x, y = self.chaser.pos()
        screen_width = self.canvas.window_width() / 2
        screen_height = self.canvas.window_height() / 2
        return abs(x) > screen_width or abs(y) > screen_height

    def reset_runner(self):
        """Reset the runner to a new random position within the visible area."""
        new_x = random.randint(-self.canvas.window_width() // 2 + 50, self.canvas.window_width() // 2 - 50)
        new_y = random.randint(-self.canvas.window_height() // 2 + 50, self.canvas.window_height() // 2 - 50)
        self.runner.setpos(new_x, new_y)

    def game_over_screen(self):
        """Display 'Game Over' and stop the game."""
        self.drawer.undo()  # Clear previous message
        self.drawer.penup()
        self.drawer.setpos(0, 0)  # Center the message
        self.drawer.write("Game Over", align="center", font=("Arial", 30, "bold"))

    def start(self, init_dist=400, ai_timer_msec=100):
        """Start the game and initialize the turtles' positions."""
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        """The main game loop, called repeatedly."""
        if self.game_over:
            return  # Stop the game loop if the game is over

        # AI for movement
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.chaser.heading())

        # Timer updates
        self.timer += 1

        # Check if the runner is caught and update the score
        is_catched = self.is_catched()
        
        if is_catched:
            self.score += 1  # Increment score when the chaser catches the runner
            self.reset_runner()  # Reset runner's position after being caught

        # Check if the runner is out of bounds (outside the window)
        if self.is_out_of_bounds_runner():
            self.game_over = True
            self.game_over_screen()  # Display "Game Over" and stop the game
            return  # End the game loop
        
        #Check if the runner is out of bounds (outside the window)
        if self.is_out_of_bounds_chaser():
            self.game_over = True
            self.game_over_screen()  # Display "Game Over" and stop the game
            return  # End the game loop

        # Display game status (timer, score, and catch status)
        self.drawer.undo()  # Clears the previous message
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Time: {self.timer} | Score: {self.score} | Is caught? {is_catched}')

        # Continue the game loop
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.shape('turtle')  # Set the shape to a turtle
        self.color('blue')
        self.step_move = step_move
        self.step_turn = step_turn
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.shape('turtle')  # Set the shape to a turtle
        self.color('red')
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        """Basic random movement AI."""
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

# Main game setup
if __name__ == '__main__':
    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.title("Turtle Runaway")

    runner = RandomMover(screen)  # Runner is controlled by AI
    chaser = ManualMover(screen)  # Chaser is controlled by the user

    game = RunawayGame(screen, runner, chaser)
    game.start()  # Start the game
    screen.mainloop()  # Keeps the window open and the game running
