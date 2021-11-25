#%%
import arcade
import csv
import math
from arcade import physics_engines
import pymunk
import timeit

GAME_STATE = "Testing"

class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape

class CircleSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2

class BoxSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename, scale):
        super().__init__(pymunk_shape, filename)
        self.scale = scale

class Game(arcade.Window):

    def __init__(self):
        super().__init__(game_settings.get("SCREEN_WIDTH"),game_settings.get("SCREEN_HEIGHT"),game_settings.get("SCREEN_TITLE"))
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # -- Physics settup
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, -900.0)

        # -- Sprite Settup
        self.sprite_list: arcade.SpriteList[PhysicsSprite] = arcade.SpriteList()
        self.static_lines = []

        # Create the floor
        floor_height = (game_settings.get("SCREEN_HEIGHT")*.25)-100
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, floor_height], [game_settings.get("SCREEN_WIDTH"), floor_height], 0.0)
        shape.friction = 1
        shape.elasticity = .5
        self.space.add(shape, body)
        self.static_lines.append(shape)

        # Create Walls
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, 0], [0, game_settings.get("SCREEN_HEIGHT")], 0.0)
        shape.friction = 1
        shape.elasticity = .1
        self.space.add(shape, body)
        self.static_lines.append(shape)

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [game_settings.get("SCREEN_WIDTH"), 0], [game_settings.get("SCREEN_WIDTH"), game_settings.get("SCREEN_HEIGHT")], 0.0)
        shape.friction = 1
        shape.elasticity = .1
        self.space.add(shape, body)
        self.static_lines.append(shape)

        # -- Catapult initialization
        self.catapults = 0
        self.cycle_counter = 0
        self.arm_game_state = "Primed"
        self.catapult_game_state = "Loaded"

    def setup(self):
        #--- Start Catapult Setup

        # Create Defaults for variables
        self.auto_launch_angle = 85
        self.catapult_scale = .25
        self.loaded = False


        # Create Lists
        self.rock_list = arcade.SpriteList()

        self.create_catapult(game_settings.get("SCREEN_WIDTH")*.88,game_settings.get("SCREEN_HEIGHT")*.17,scale=.15)
        #--- End catapult setup

        self.create_board(game_settings.get("SCREEN_WIDTH")*.5,game_settings.get("SCREEN_HEIGHT")*.5,500,200)

    def on_draw(self):
        arcade.start_render()

        self.sprite_list.draw()

        # --- start line draw ---
        for line in self.static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 2)

        # --- end line draw ---

        # --- start static item draw ---
        self.catapult_arm_sprite.draw()
        self.catapult_arm_loaded_sprite.draw()
        self.catapult_body_sprite.draw()
        self.rear_wheel_sprite.draw()
        self.front_wheel_sprite.draw()


        # --- end static item draw ---

    def update(self, delta_time):
        #--- step physics ---
        self.space.step(1/60)

        self.catapult_state_machine()

        # --- update sprite locations ---
        for sprite in self.sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

    def catapult_state_machine(self):
        #print(self.catapult_game_state)
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
            self.create_rock()
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

    def create_catapult(self,x,y,scale=.25):
        self.catapult_scale = scale

        self.catapult_body_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/chassis.png",self.catapult_scale)
        self.catapult_arm_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/arm_flat.png",self.catapult_scale)
        self.catapult_arm_loaded_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/arm_flat_w_rock.png",self.catapult_scale)
        self.rear_wheel_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/wheel-front.png",self.catapult_scale)
        self.front_wheel_sprite = arcade.Sprite("Assets/Sprites/Trebuchette/pieces/wheel-front.png",self.catapult_scale)

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

        self.catapult_game_state = 'Arming'

    def fire(self):
        #Toggles the state to "Fireing" on a command.  used for a player manually controlling launch/release.
        self.catapult_game_state = "Fireing"

    def release(self):
        #Toggles the state to "Fired" on a command.  used for manual player launch/release.
        self.catapult_game_state = "Fired"

    def program_fire(self,angle,force,rock_mass):
        #Used for a programed fireing sequence.  catapult will automatically change through states using the given peramiters.
        pass

    def create_rock(self,mass = 4.0,elasticity = .5,friction = 0.4,force = 150000):
        x = self.main_axel_x + (math.cos((self.arm_angle * math.pi)/180) * 500 * self.catapult_scale)
        y = self.main_axel_y + (math.sin((self.arm_angle * math.pi)/180) * 500 * self.catapult_scale)
        width = 135*self.catapult_scale
        height = 135*self.catapult_scale
        moment = pymunk.moment_for_box(mass, (width, height))
        body = pymunk.Body(mass, moment)
        body.angle = self.arm_angle
        body.position = pymunk.Vec2d(x, y)
        shape = pymunk.Poly.create_box(body, (width, height))
        shape.elasticity = elasticity
        shape.friction = friction
        self.space.add(body, shape)
        # body.sleep()
        y_force = (math.sin((self.arm_angle * math.pi)/180) * force)
        x_force = -(math.cos((self.arm_angle * math.pi)/180) * force)
        shape.body.apply_force_at_local_point((x_force,y_force),(0,1))

        sprite = BoxSprite(shape, "Assets/Sprites/Trebuchette/pieces/stone_rotated.png", self.catapult_scale)
        
        self.sprite_list.append(sprite)

    def create_box(self, x, y, scale = 1, elasticity = .2, friction = .5):
            length = 125 * scale
            height = 125 * scale
            mass = 2
            moment = pymunk.moment_for_box(mass, (length, height))
            body = pymunk.Body(mass, moment)
            body.position = pymunk.Vec2d(x,y)
            shape = pymunk.Poly.create_box(body,(length, height))
            shape.elasticity = elasticity
            shape.friction = friction
            self.space.add(body, shape)
            sprite = BoxSprite(shape,":resources:images/tiles/brickGrey.png",scale)
            self.sprite_list.append(sprite)

    def create_board(self, x, y, h,w,scale = 1, elasticity = .2, friction = .5):
            length = w * scale
            height = h * scale
            mass = 2
            moment = pymunk.moment_for_box(mass, (length, height))
            body = pymunk.Body(mass, moment)
            body.position = pymunk.Vec2d(x,y)
            shape = pymunk.Poly.create_box(body,(length, height))
            shape.elasticity = elasticity
            shape.friction = friction
            self.space.add(body, shape)
            sprite = BoxSprite(shape,":resources:images/tiles/brickGrey.png",scale)
            sprite.width = w
            sprite.height = h
            self.sprite_list.append(sprite)



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
# %%
