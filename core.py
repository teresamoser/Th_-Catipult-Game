#%%
import arcade
import csv

from arcade import physics_engines

GAME_STATE = "Testing"


class Game(arcade.Window):

    def __init__(self):
        self.catapult = Catapult()
        super().__init__(game_settings.get("SCREEN_WIDTH"),game_settings.get("SCREEN_HEIGHT"),game_settings.get("SCREEN_TITLE"))

        arcade.set_background_color(arcade.color.RED)

    def setup(self):
        self.catapult.setup()

    def on_draw(self):
        self.catapult.draw()

    def update(self, delta_time):
        physics_engine.step()
        self.catapult.update()


class Catapult(arcade.Sprite):

    def __init__(self):
        self.catapults = 0
        self.cycle_counter = 0
        self.game_state = "Primed"

        # -- GAME STATE DEFINITIONS --
        #
        # -IDLE GAME STATES-
        # Primed: Catapult is in its Primed position, without a rock loaded
        # Fired: Catapult arm is in its furthest deployed state.  
        # Loaded: As Primed, but a rock is on the launch arm
        #
        # -ACTIVE GAME STATES
        # Fireing: While in this state, the catapult's arm swings out, launching a rock
        # Arming: While in this state, the catapult arm will slowly wind back until it reaches its "Primed" Position
     
    def setup(self):
        self.catapult_scale = .25

        # Define sprites
        self.catapult_body_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/chassis.png",self.catapult_scale)
        self.catapult_arm_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/arm.png",self.catapult_scale)
        self.rear_wheel_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/wheel-front.png",self.catapult_scale)
        self.front_wheel_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/wheel-front.png",self.catapult_scale)
        self.rock_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/stone.png",self.catapult_scale*.65)


        # Create Lists
        self.rock_list = arcade.SpriteList()

        # Enable Physics
        physics_engine.add_sprite(self.catapult_arm_sprite)
        physics_engine.add_sprite_list(self.rock_list)
    
    def update(self):

        # -- START FOR TESTING ONLY --
        # Creates a catapult in the center of the screen on game launch
        if self.catapults == 0:
            self.create_catapult(game_settings.get("SCREEN_WIDTH")/2,game_settings.get("SCREEN_HEIGHT")/2)
            self.catapults += 1

        print(self.game_state)
        # -- END FOR TESTING ONLY -- 
        
        if self.game_state == 'Primed':
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.game_state = 'Loaded'
            self.cycle_counter = 0
            return
        if self.game_state == 'Fired':
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.game_state = 'Arming'
            self.cycle_counter = 0
            return
        if self.game_state == 'Loaded':
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.game_state = 'Fireing'
            self.cycle_counter = 0
            return
        if self.game_state == 'Fireing':
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.game_state = 'Fired'
            self.cycle_counter = 0
            return
        if self.game_state == 'Arming':
            while self.cycle_counter != 50:
                self.cycle_counter += 1
                return
            self.game_state = 'Primed'
            self.cycle_counter = 0
            return

    def draw(self):
        self.catapult_arm_sprite.draw()
        self.catapult_body_sprite.draw()
        self.rear_wheel_sprite.draw()
        self.front_wheel_sprite.draw()
        if self.game_state != "Loaded" or self.game_state != "Fireing":
            #self.stuck_rock.draw()
            pass

    def create_catapult(self,x,y):
        #Place Body of Catapult
        self.catapult_body_sprite.center_x = x
        self.catapult_body_sprite.center_y = y
        
        #Define Catapult body areas
        self.main_axel_x = x - (185*self.catapult_scale)
        self.main_axel_y = y + (160*self.catapult_scale)
        self.front_wheel_axel_x = x - (375*self.catapult_scale)
        self.front_wheel_axel_y = y - (200*self.catapult_scale)
        self.rear_wheel_axel_x = x + (375*self.catapult_scale)
        self.rear_wheel_axel_y = y - (200*self.catapult_scale)

        #Place wheels
        self.front_wheel_sprite.center_x = self.front_wheel_axel_x
        self.front_wheel_sprite.center_y = self.front_wheel_axel_y
        self.rear_wheel_sprite.center_x = self.rear_wheel_axel_x
        self.rear_wheel_sprite.center_y = self.rear_wheel_axel_y

        #Place Arm of Catapult
        self.catapult_arm_sprite.center_x = x - (120*self.catapult_scale)
        self.catapult_arm_sprite.center_y = y +(150*self.catapult_scale)
        self.catapult_arm_sprite.angle = 20

        #Define Catapult arm variables
        self.arm_angle = 0
        self.rock_spawn_point_x = x
        self.rock_spawn_point_y = y
        self.rock_spawn_angle = 0


        
    def fire(self):
        self.game_state = "Fireing"


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
    global physics_engine
    gravity = (0,float(game_settings.get("GRAVITY")))
    physics_engine = arcade.PymunkPhysicsEngine(damping=float(game_settings.get("DEFAULT_DAMPING")),gravity=gravity)
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
# %%
