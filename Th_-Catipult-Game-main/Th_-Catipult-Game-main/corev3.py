#%%
from PIL.Image import Image
import arcade
import csv
import math
from arcade import physics_engines
import pymunk

GAME_STATE = "Testing"


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        #-- Physics settup
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, -900.0)

        # -- Catapult initialization
        self.catapults = 0
        self.cycle_counter = 0
        self.arm_game_state = "Primed"
        self.catapult_game_state = "Loaded"
        
        self.tile_map = None
        
        self.background = None

    def setup(self):
        #--- Start Catapult Setup

        # Create Defaults for variables
        self.auto_launch_angle = 90
        self.catapult_scale = .25
        self.loaded = False

        # Define sprites
        self.catapult_body_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/chassis.png",self.catapult_scale)
        self.catapult_arm_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/arm_flat.png",self.catapult_scale)
        self.catapult_arm_loaded_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/arm_flat_w_rock.png",self.catapult_scale)
        self.rear_wheel_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/wheel-front.png",self.catapult_scale)
        self.front_wheel_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/wheel-front.png",self.catapult_scale)

        # Create Lists
        self.rock_list = arcade.SpriteList()

        self.create_catapult(game_settings.get("SCREEN_WIDTH")-150,game_settings.get("SCREEN_HEIGHT")/5)

        #--- End catapult setup
        
        #self.background = arcade.load_texture("Assets/Tilesets/field.png")
        #########################################################################
        
        map_name = "Assets/Tilesets/level2.json"

        layer_options = {
            "floor": {"use_spatial_hash": True}, 
            "castle": {"use_spatial_hash": True},
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, layer_options=layer_options, scaling=1
        )
        self.end_of_map = self.tile_map.width * 32
        #"""
       #################################################################################################

    def on_draw(self):
        #self.clear()
        arcade.start_render()
        self.scene.draw()
        #arcade.draw_lrwh_rectangle_textured(0, 0,
         #                                   game_settings.get("SCREEN_WIDTH"),game_settings.get("SCREEN_HEIGHT"),
          #                                  self.background)
        # --- Start catapult Draw ---

        arcade.draw_circle_outline(self.catapult_arm_sprite.center_x,self.catapult_arm_sprite.center_y,450*self.catapult_scale,arcade.color.RED)
        self.catapult_arm_sprite.draw()
        self.catapult_arm_loaded_sprite.draw()
        self.catapult_body_sprite.draw()
        self.rear_wheel_sprite.draw()
        self.front_wheel_sprite.draw()
        self.rock_list.draw()

        # --- End Catapult Draw ---
        #if self.tile_map.background_color:
         #   arcade.set_background_color(self.tile_map.background_color)
         

        
        

    def update(self, delta_time):
        #--- Start Catapult Update ---

        print(self.catapult_game_state)
        #Actions that always take place
        self.catapult_arm_loaded_sprite.center_x = self.catapult_arm_sprite.center_x
        self.catapult_arm_loaded_sprite.center_y = self.catapult_arm_sprite.center_y
        self.catapult_arm_loaded_sprite.angle = self.catapult_arm_sprite.angle
        if self.loaded:
            self.catapult_arm_loaded_sprite.alpha = 255
            self.catapult_arm_sprite.alpha = 0
        else:
            self.catapult_arm_loaded_sprite.alpha = 0
            self.catapult_arm_sprite.alpha = 255

        if self.catapult_game_state == 'Primed':
            #Actions that take place while the catapult is in the "Primed" state.
            # -- FOR TESTING ONLY --
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.catapult_game_state = 'Loaded'
            self.cycle_counter = 0
            # -- END FOR TESTING ONLY --
            return

        if self.catapult_game_state == 'Fired':
            #Actions that take place while the catapult is in the "Fired" state.
            # -- FOR TESTING ONLY --
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.catapult_game_state = 'Arming'
            self.cycle_counter = 0
            # -- END FOR TESTING ONLY --
            return

        if self.catapult_game_state == 'Loaded':
            #Actions that take place while the catapult is in the "Loaded" state.
            # -- FOR TESTING ONLY --
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.catapult_game_state = 'Fireing'
            self.cycle_counter = 0
            # -- END FOR TESTING ONLY --
            # Update held rock
            return

        if self.catapult_game_state == 'Fireing':
            #Actions that take place while the catapult is in the "Fireing" state.
            if self.arm_angle < self.auto_launch_angle:
                # Increment the arm
                self.arm_angle += 10
                self.catapult_arm_sprite.angle = self.arm_angle
                # Update held rock
                return
            self.loaded = False
            self.create_rock(1,100)
            self.catapult_game_state = 'Fired'
            self.cycle_counter = 0
            return

        if self.catapult_game_state == 'Arming':
            #Actions that take place while the catapult is in the "Arming" state.
            while self.arm_angle > -20:
                self.arm_angle -= .25
                self.catapult_arm_sprite.angle = self.arm_angle
                return
            self.loaded = True
            self.catapult_game_state = 'Primed'
            self.cycle_counter = 0
            return

        # --- End Catapult Update

    def create_catapult(self,x,y,scale=.25):
        self.catapult_scale = scale

        #Place Body of Catapult
        self.catapult_body_sprite.center_x = x
        self.catapult_body_sprite.center_y = y
        
        #Define Catapult body areas
        self.main_axel_x = x - (185*self.catapult_scale)
        self.main_axel_y = y + (160*self.catapult_scale)
        self.front_wheel_axel_x = x - (375*self.catapult_scale)
        self.front_wheel_axel_y = y - (250*self.catapult_scale)
        self.rear_wheel_axel_x = x + (375*self.catapult_scale)
        self.rear_wheel_axel_y = y - (250*self.catapult_scale)

        #Place wheels
        self.front_wheel_sprite.center_x = self.front_wheel_axel_x
        self.front_wheel_sprite.center_y = self.front_wheel_axel_y
        self.rear_wheel_sprite.center_x = self.rear_wheel_axel_x
        self.rear_wheel_sprite.center_y = self.rear_wheel_axel_y

        #Place Arm of Catapult
        self.catapult_arm_sprite.center_x = self.main_axel_x
        self.catapult_arm_sprite.center_y = self.main_axel_y

        #Define Catapult arm variables
        self.arm_angle = -20
        self.rock_start_point_x = x + (250*self.catapult_scale)
        self.rock_start_point_y = y + (50*self.catapult_scale)
        self.rock_holder_point_x = self.rock_start_point_x
        self.rock_holder_point_y = self.rock_start_point_y
        self.rock_spawn_angle = 0
 
    def fire(self):
        #Toggles the state to "Fireing" on a command.  used for a player manually controlling launch/release.
        self.catapult_game_state = "Fireing"

    def release(self):
        #Toggles the state to "Fired" on a command.  used for manual player launch/release.
        self.catapult_game_state = "Fired"

    def program_fire(self,angle,force,rock_mass):
        #Used for a programed fireing sequence.  catapult will automatically change through states using the given peramiters.
        pass

    def create_rock_physics(self,mass,inertia):
        #creates then releces the rock
        rock_start_x =  self.main_axel_x + (math.cos((math.pi * self.arm_angle)/180) * 450*self.catapult_scale)
        rock_start_y = self.main_axel_y + (math.sin((math.pi * self.arm_angle)/180) * 450*self.catapult_scale)

        body = pymunk.Body(mass,inertia,body_type=pymunk.Body.DYNAMIC)
        body.position = (rock_start_x,rock_start_y)

        shape = pymunk.Poly.create_box(body,(120,120))
        
        self.space.add(body,shape)
 
        sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/stone_rotated.png",self.catapult_scale)
        sprite.center_x = rock_start_x
        sprite.center_y = rock_start_y
        sprite.angle = self.arm_angle
        self.rock_list.append(sprite)

        #rock = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/stone_rotated.png",self.catapult_scale)
        #rock.angle = self.arm_angle
        #rock.center_x = math.cos((math.pi * self.arm_angle)/180) * 450*self.catapult_scale
        #rock.center_y = math.sin((math.pi * self.arm_angle)/180) * 450*self.catapult_scale

        # radius sin(angle) = y
        # radius cos(angle) = x

    def create_rock(self,force,rock_mass):
        pass
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        
        new_view = VictoryView()
        #new_view.setup()
        self.window.show_view(new_view)
    
class GameOverView(arcade.View):

    def __init__(self):
        
        super().__init__()
        self.texture = arcade.load_texture("game_over.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, game_settings.get("SCREEN_WIDTH") - 1, 0, game_settings.get("SCREEN_HEIGHT") - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(game_settings.get("SCREEN_WIDTH") / 2, game_settings.get("SCREEN_HEIGHT") / 2,
                                game_settings.get("SCREEN_WIDTH"), game_settings.get("SCREEN_HEIGHT"))

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class VictoryView(arcade.View):

    def __init__(self):
        
        super().__init__()
        self.texture = arcade.load_texture("Assets/Tilesets/victory.png")

        arcade.set_viewport(0, game_settings.get("SCREEN_WIDTH") - 1, 0, game_settings.get("SCREEN_HEIGHT") - 1)
        #elf.background = None

    def on_draw(self):
        arcade.start_render()
        #self.background = arcade.load_texture("Assets/Tilesets/victory.png")
        self.texture.draw_sized(game_settings.get("SCREEN_WIDTH") / 2, game_settings.get("SCREEN_HEIGHT") / 2,
                                game_settings.get("SCREEN_WIDTH"), game_settings.get("SCREEN_HEIGHT"))
        arcade.draw_text("VICTORY!", game_settings.get("SCREEN_WIDTH") - 400, game_settings.get("SCREEN_HEIGHT") - 100,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class StartView(arcade.View):
    
    def __init__(self):
        
        super().__init__()
        self.texture = arcade.load_texture("Assets/Tilesets/starting.png")

        arcade.set_viewport(0, game_settings.get("SCREEN_WIDTH") - 1, 0, game_settings.get("SCREEN_HEIGHT") - 1)


    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(game_settings.get("SCREEN_WIDTH") /2, game_settings.get("SCREEN_HEIGHT") /2,
                                game_settings.get("SCREEN_WIDTH"), game_settings.get("SCREEN_HEIGHT"))
        arcade.draw_text("Welcome to Castle Crusher!", game_settings.get("SCREEN_WIDTH") / 2, game_settings.get("SCREEN_HEIGHT") / 2 + 225,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to continue to our game", game_settings.get("SCREEN_WIDTH") / 2, game_settings.get("SCREEN_HEIGHT") / 2 - 300,
                         arcade.color.BLACK, font_size=40, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

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

    window = arcade.Window(game_settings.get("SCREEN_WIDTH"),game_settings.get("SCREEN_HEIGHT"),game_settings.get("SCREEN_TITLE"))
    start_view = StartView()
    window.show_view(start_view)
    #start_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()
# %%