#%%

import arcade
import math
import csv


class Engine:
    # What runs the game.  This is for everything not visible to the player (mechanicly speeking)

    def start(self):
        #performs the startup actions of the game, such as showing a logo and importing all save data
        self.load_settings()
        self.Interface.Window(game_settings.get("SCREEN_WIDTH"),game_settings.get("SCREEN_HEIGHT"),game_settings.get("SCREEN_TITLE"))
        arcade.run()

    def load_settings(self):
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

    class Physics:
        #the physics that runs the world and applys to all objects 
        # - Josh will be working on this primarily
        gravity = 9.8

    class Object():
        #each item in the world that is not static is an object.  
        pass

        #Needed objects:
        # - block for castle - Teresa 
        # - angle block for castle - Teresa
        # - rock for catapult - Joshua
        # - catapult - Joshua
        # - enemey in the castle (stretch) - Teresa


    class Interface:
        #The User interface.  This class contains all elements visible to the user.

        class Window(arcade.Window):
            # the device that is used to view the game.  It is the box that appears on screen
            
            def __init__(self, width, height, title):
                super().__init__(width, height, title)

                arcade.set_background_color(arcade.color.AMAZON)

                # If you have sprite lists, you should create them here,
                # and set them to None

            def on_draw(self):
                """
                Render the screen.
                """

                # This command should happen before we start drawing. It will clear
                # the screen to the background color, and erase what we drew last frame.
                arcade.start_render()

                # Call draw() on all your sprite lists below

            def on_update(self, delta_time):

                pass

        class Room:
            #the space in wich the game takes place.  This class defines its area, properties, and other details.  Each room is a single level.
            pass

            # Rooms needed
            # - level 1+ - Devan
            # - Victory screen - Devan
            # - opening screen - Manoell
            # - save/load menu - Richard

        class Camera:
            #controlls what section of room is visible at any given time
            pass

def main():
    game = Engine()
    game.start()

main()
# %%
