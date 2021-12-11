import arcade
import csv

GAME_STATE = "Testing"


class Game(arcade.Window):

    def __init__(self):
        self.catapult = Catapult_body()

        super().__init__(game_settings.get("SCREEN_WIDTH"),game_settings.get("SCREEN_HEIGHT"),game_settings.get("SCREEN_TITLE"))

        arcade.set_background_color()

        self.physics_list = None
        self.static_list = None

    def setup(self):
        pass

    def on_draw(self):
        pass

    def update(self, delta_time):
        pass

class Catapult_body(arcade.Sprite):

    def __init__(self):
        self.catapult_sprite = arcade.Sprite("Assets\Sprites\Trebuchette\pieces\chassis.png")

    def setup(self):
        pass
    
    def update(self):
        pass

    def draw(self):
        pass
    sg.theme('DarkAmber')   # Add a touch of color
    #  All the stuff inside your window.
    layout = [  [sg.Text('Determine Trajectory of Trebuchet')],
                [sg.Text('Enter trajectory height: '), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('Trajectory Entry', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
             # if user closes window or clicks cancel
            break
        print('You entered ', values[0])


def main():

    global game_settings
    reader = csv.reader(open('game_settings.csv','r'))
    game_settings = {}
    for row in reader:
        k, v = row
        try:
            v = int(v)
        except:
            pass
            game_settings[k] = v

    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()