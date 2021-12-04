#%%

import arcade
import math
import csv

CHARACTER_SCALING = 1
TILE_SCALING = 0.5

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

                arcade.set_background_color(arcade.color.WHITE_SMOKE)

                # If you have sprite lists, you should create them here,
                # and set them to None
                self.scene = None

                self.player_sprite = None

           
            #An issue is occuring when i have the following code in a seperate function, I think its having an issue passing
            #Information between it but I'm not sure
            #def setup(self):

                self.scene = arcade.Scene()
                self.scene.add_sprite_list("Player")
                self.scene.add_sprite_list("Walls", use_spatial_hash=True)
                #self.player_list = arcade.SpriteList()
                #self.wall_list = arcade.SpriteList(use_spatial_hash=True)

                image_source = ":resources:images/topdown_tanks/tank_red.png"
                self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
                self.player_sprite.center_x = 20
                self.player_sprite.center_y = 70
                self.scene.add_sprite("Player", self.player_sprite)
                #self.player_list.append(self.player_sprite)

                for x in range(0,800, 25):
                    wall = arcade.Sprite(":resources:images/topdown_tanks/tileGrass1.png", TILE_SCALING)
                    wall.center_x = x
                    wall.center_y = 32
                    self.scene.add_sprite("Walls", wall)

            def on_draw(self):
                """
                Render the screen.
                """

                # This command should happen before we start drawing. It will clear
                # the screen to the background color, and erase what we drew last frame.
                arcade.start_render()

                # Call draw() on all your sprite lists below
                self.scene.draw()




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

