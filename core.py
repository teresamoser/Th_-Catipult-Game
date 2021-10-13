import arcade
import math


class engine:
    # What runs the game.  This is for everything not visible to the player (mechanicly speeking)

    class physics:
        #the physics that runs the world and applys to all objects 

        gravity = 9.8

    class object():
        #each item in the world that is not static is an object.  
        pass


class GUI:
    #The User interface.  This class contains all elements visible to the user.

    class window:
        # the device that is used to view the game.  It is the box that appears on screen
        pass

    class room:
        #the space in wich the game takes place.  This class defines its area, properties, and other details.  Each room is a single level.
        pass

    class camera:
        #controlls what section of room is visible at any given time
        pass

