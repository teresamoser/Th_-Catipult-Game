# Th_-Catipult-Game

## Code Formating
To keep things orginized, here are the formating conventions for the code:
- Variables:  all lowercase using underscores to seperate words.  (my_varible)
- Classes: Prefrebly one word, capitilized.  (Engine)

## Filestructure
The game is composed primarily of three main files, with all other assets contained within the appropriate "Assets" sub folder.  The Core.py file conains the main game, while the game_settings.csv file works as long term storage for the game.  The game_save.csv file keeps track to run sespific elements of the game, tracking user informaion for future use.

## core.py Structure
The core.py file is structured into two main components, the Engine and the Interface.
- Interface:  The interface is responsible for managing all graphical elements, allowing the user to see into the game world.  This includes the game window (the section of screen that is the game), The room (the 'location' that the game is taking place in), and the camera (the secion of the room that is displayed at any given time)
- Engine: the Engine is responsible for handling all the elements that the user does not directly see.  Game objects, the Physics engine, and save/load systems all fall into this catagory.  



