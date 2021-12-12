# Th_-Catapult-Game

## Code Formating
To keep things orginized, here are the formating conventions for the code:
- Variables:  all lowercase using underscores to seperate words.  (my_variable)
- Classes: Preferably one word, capitalized.  (Engine)

## Filestructure
The game is composed primarily of three main files, with all other assets contained within the appropriate "Assets" sub folder.  The Core.py file conains the main game, while the game_settings.csv file works as long term storage for the game.  The game_save.csv file keeps track to run specific elements of the game, tracking user information for future use.

## core.py Structure
The core.py file is structured into two main components, the Engine and the Interface.
- Interface:  The interface is responsible for managing all graphical elements, allowing the user to see into the game world.  This includes the game window (the section of screen that is the game), The room (the 'location' that the game is taking place in), and the camera (the section of the room that is displayed at any given time)
- Engine: the Engine is responsible for handling all the elements that the user does not directly see.  Game objects, the Physics engine, and save/load systems all fall into this catagory.  


## Catapult Game states
### IDLE GAME STATES

Primed: Catapult is in its Primed position, without a rock loaded.
Fired: Catapult arm is in its furthest deployed state.  
Loaded: As Primed, but a rock is on the launch arm.

### ACTIVE GAME STATES

Firing: While in this state, the catapult's arm swings out, launching a rock.
Arming: While in this state, the catapult arm will slowly wind back until it reaches its "Primed" Position.

### Other notes
There is a variable called "arm_game_state" and this refers to either "Primed" (a rock is loaded) or 
