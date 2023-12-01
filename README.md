# space-invaders
## Intro
Space Invaders is a 1978 arcade game where you play as a spaceship, firing lasers to destroy aliens which are firing back at you. In today’s Hackathon, we will break Space Invaders down to its essential parts, and discover that with Pygame’s built in methods, it’s easier to recreate than you might expect. This has a high ceiling as far as extra features go, but you should at least include the basic mechanics: a player who can move horizontally and fire bullets upwards, and a group of aliens that move horizontally and fire bullets downwards. For more information, play Space Invaders [here](https://freeinvaders.org/). 

## Starter Code
Here’s a review of what's included in the starter file:
~~~python
import math
import random
import pygame
from pygame import mixer

# CONSTANTS
PLAYER_IMG = pygame.image.load('player.png')
ALIEN_IMG = pygame.image.load('enemy.png')
LASER_IMG = pygame.Surface((4,20))
LASER_IMG.fill('white')
MIN_X = 0
MAX_X = 736
NUM_ALIENS = 6
LASER_RESET_Y = 380
NEW_ALIEN_FREQUENCY = 5 # every 5 seconds
~~~
Here we have our imports, and define some of the constants that we’ll use later. The images are how we’ll display our game pieces. MIN_X and MAX_X are the x-coordinate bounds. NUM_ALIENS is how many aliens the player will be fighting. LASER_RESET_Y is the y coordinate that the laser starts at when shot
Below, these are 3 classes that we will later define
~~~python
class Player:
 pass
~~~
The player will move left and right and shoot the aliens with a laser

~~~python
class PlayerLaser:
 pass
~~~
The player’s laser will move upwards from where the player shot it

~~~python
class Alien:
 pass
~~~
An alien will move diagonally downwards, bouncing on the sides of the screen, shooting at the player occasionally

~~~python
# Initialize the pygame
pygame.init()
screen = pygame.display.set_mode((800, 500)) # create the screen
pygame.display.set_caption("Space Invader") # Caption
clock = pygame.time.Clock()
~~~
These lines set up pygame
~~~python
# mixer.music.load("background.wav") # Sound
# mixer.music.play(-1)
~~~
These lines will play music when uncommented
~~~python
score_font = pygame.font.Font('Pixeled.ttf', 32)
game_over_font = pygame.font.Font('Pixeled.ttf', 64)
~~~
These are fonts for text that we will display later
~~~python
def draw_game(screen):
 pass
~~~
This is a function that we will define later. It draws the entire game. 

Below, we have the game loop. This keeps running until we set `running = False`.
~~~python
running = True
# Game Loop
while running:
 clock.tick(30) ```This line controls how fast the game moves (the framerate)```
 screen.fill((0, 0, 0)) ```This fills in the background```
~~~
~~~python
 for event in pygame.event.get(): ```This line gets user input```
   if event.type == pygame.QUIT: ```This quits the game if the user closes the window```
     running = False
   pressedKeys = pygame.key.get_pressed() ```Here we check for keyboard inputs. We’ll fill it in later```
   if pressedKeys[pygame.K_LEFT]:
     pass
   elif pressedKeys[pygame.K_RIGHT]:
     pass
   else:
     pass
~~~
## Running your code
Inside the `starter-code` directory, run `python3 spaceinvaders-starter.py`. This will open and run our pygame window.
## `Player` Class
We want to represent a player using a class.

A player should have an `x` and `y` attribute to keep track of the x and y coordinates, and an `x_velocity` to keep track of its speed (negative speed means it’s going left, and a speed of 0 means it’s still). The `x_velocity` will start off as `0` when we construct a `Player`.
A player should also have a draw method that takes in the screen. Use the `screen.blit(...)` function. 

Now, before the game loop, create an instance of the player class we just made at coordinates `(370, 380)`.

## Drawing function
As we build this game, we want to see all our additions. 

For now, draw the player in `draw_game`, using the player’s draw method.
Now call `draw_game` near the end of our run loop, right before `pygame.display.update()`

## Player Movement
We want to move the player left and right when the user presses the left and right arrow keys. 

First, add an update method to the Player class so each player knows how to move itself based on its velocity. The update method should take nothing in as input, and change the x location of the player using its x velocity. This method should not allow the player to move off the screen (pay attention to when `x < MIN_X`, and `x >= MAX_X)`.

In our game loop, `pressedKeys = pygame.key.get_pressed()` gets a list of all the keys that are pressed down on the keyboard by the user. `pressedKeys[pygame.K_LEFT]` will be true if the user currently is pressing the left arrow key. Similar for `pygame.K_RIGHT`. We want to use the key press to update the player’s `x_velocity`. After we look at game events and have done our updating to the player’s velocity, we want to ask the player to update itself. 

We already draw the player, so the player’s movement should now visually take effect. Try it out!

## Player Laser
Let’s create a class that represents a player’s laser. A player’s laser will shoot vertically upwards from the player’s x location when they shot it. Only one player laser can exist on the screen at once. Later, we’ll add collision functionality, so that when the laser hits an alien, the alien will die and the laser will get reset so it can be shot again. 

The player’s laser should have the following attributes: `x`, `y`, `shooting` (a boolean that is True if currently moving upwards), `y_vel` (speed that the laser is shooting upwards at). Create the `__init__` method that doesn’t take anything in, and initializes these attributes to values. The `y_vel` should be `-5`, `shooting` should be `False`, `x` should be `0`, & `y` should be `LASER_RESET_Y`.

Create an instance of a `PlayerLaser` right after where you created an instance of `Player`. 

Now for methods. Things that a player’s laser should know how to do:
* Draw itself
* Play a sound
* Shoot
* Reset
* Update

First let’s draw the player’s laser. Add a draw method to the laser. Draw it using `screen.blit(...)`. If the laser isn’t shooting, DON’T draw it. 
Now, call this draw method in the `draw_game()` function. 

Now add a method to the player laser that allows it to play a sound. This method shouldn’t take in any input. This is the code inside this method:
~~~python
   LASER_SOUND = mixer.Sound("laser.wav")
   LASER_SOUND.play()
~~~

Now add a method that shoots the laser. It takes in no input, sets shooting to true, and plays the sound.

Add a method that resets the laser. It takes in an x value, sets `y` to `LASER_RESET_Y`, shooting to false, and `x` to the given x value. 

Add a method that updates the laser. It takes in no input. If the laser is currently shooting, add the y velocity to the y value. And also if the laser is off the top of the screen (`y < 0`), reset the laser. 

In our run loop when we check for player keyboard presses, check for if the key pressed is `pygame.K_UP`. If that key is pressed, and the laser isn’t currently being shot, shoot the player laser at the player’s current x value. 

Inside our run loop, now call the player laser’s update method. 

## `Alien` Class
Now we also want to represent an alien using a class.

Aliens should have the following attributes: `x`, `y`, `x_vel`, `y_vel`. When creating an `Alien`, we don’t want to give it a `y_vel` (we can just hardcode it to `0.5`). Make the `__init__` method. After where you made the `Player` instance and `PlayerLaser` instance, create `NUM_ALIENS` number of aliens (using a loop). Store the aliens in a list. The `x` coordinate should be a random number between `0` and `MAX_X`, the `y` coordinate should be a random number between 50 and 150, and the `x_vel` can be `1` for now. 

Aliens should know how to draw themselves. Use this method in `draw_game()` to draw all the aliens.

Aliens should have an update method that adds the x and y velocities to the x and y coordinates. Bounce the alien off the edge of the screen by multiplying the x velocity by `-1` if it’s reached either side.

In our run loop, use a while loop (using a while loop instead of a for loop will become relevant later) to loop through the list of aliens and call the update method for each one. 

## Aliens Being Hit
Aliens can run into the area the player is, or a bullet can run into an alien. Both of those have side effects. Let’s first deal with aliens being hit by player bullets. 

To implement collisions between player bullets and aliens, first add the following function before our run loop:
~~~python
def isCollision(alienX, alienY, laserX, laserY):
 distance = math.sqrt(math.pow(alienX - laserX, 2) + (math.pow(alienY - laserY, 2)))
 return distance < 27
~~~
In our loop through the aliens in our run loop, if there’s a collision between the current alien and the laser, play a sound using the following code:
~~~python
explosionSound = mixer.Sound("explosion.wav")
explosionSound.play()
~~~
and also reset the laser and remove that alien (the fact that we used a while loop to loop through the aliens should be helpful here).

## Aliens Spawning
We want more aliens to spawn for us to keep destroying them. To do this, we’ll trigger a custom event repeatedly (using a timer), and listen to that event in our run loop to create a new alien. 
Add the following lines outside your run loop:
~~~python
NEW_ALIEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_ALIEN_EVENT, NEW_ALIEN_FREQUENCY * 1000)
~~~
Now, as another conditional when you check for different types of events, check if event.type is `NEW_ALIEN_EVENT`. If it is, create another alien in the same way we did before. 

When the game ends, also stop the timer, using the following code:
~~~python
pygame.time.set_timer(NEW_ALIEN_EVENT, 0)
~~~

## Alien Bullets
(From [@JimmieLB](https://github.com/JimmieLB))

We’ve created a class that represents the player’s bullet, now it’s time to make a class that represents the alien’s bullet. An alien bullet should shoot downwards starting from the x and y location of the alien. Later, we’ll add collision functionality, so that when the laser hits a player, the game ends.

The Alien Laser class should have 7 attributes `x`, `y`, `yvel`, `shooting`, `alien`, `min_cooldown`, `cooldown`. `x` and `y` represent the position. `yvel` represents velocity. shooting should be a boolean that represents whether or not the laser is currently moving. `alien` should be an instance of the Alien class. Whenever we shoot the laser we have to know the starting point. We can find this by using the position variables from the alien object. To make a random based cooldown system, we can create a `min_cooldown` variable that can be set to any integer. The larger the number, the more time between laser shots. `cooldown` should represent the current state of the cooldown (how much time is left before the alien can shoot again).

Firstly we have to change the alien class a little. Every alien should have one laser that constantly gets reset. So we should create a new attribute in the Alien class that represents a Laser.

A lot from this laser class will be the same as the player laser. The only differences will be the spawn point, the direction, and instead of detecting a collision with an alien, we have to detect a collision with the player. And if we do detect a player we want to end the game.

Every update step the `cooldown` should go down by 1. When `cooldown` reaches `0`, the laser should shoot. Whenever `cooldown` resets we should `cooldown` to `min_cooldown` + a random amount. 

## Ending the Game
The game ends when the aliens reach the bottom of the screen. There is no way to win mwahaha >:)

First, let’s make it possible for the game to end. Right before the run loop, create a game_over variable that is set to False. Add the following function to your file before the run loop:
~~~python
def game_over_text():
 game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
 screen.blit(game_over_text, (200, 250))
~~~

Now let’s implement what happens when an alien reaches the bottom of the screen. 
Inside your run loop, if the game is over, call the game_over_text function. Otherwise, loop through all the aliens to update them, and inside this loop, also add a section (right before updating each alien) where we check if the current alien’s y position is `> 340`. If yes, set our aliens list to an empty list, set game_over to true, and break the alien while loop.

Run your program to see if the endgame behavior works.

## More Features
Your Space Invaders game is almost done! Add at least one of these extra features to really complete it. Don’t forget that Pygame has excellent documentation (instructions on how to use its code) at https://www.pygame.org/docs/. 
1. Lives
2. Score
3. Obstacles
4. Even more sound effects
5. Different types of aliens
6. Game increases in difficulty as time passes

## Deliverables
* Space Invaders game works as intended:
  * Player can move sideways, cannot go off the screen, fires bullets upwards with spacebar.
  * Aliens randomly spawn in, and fire bullets downwards automatically
  * If an alien gets hit with a player bullet or vice versa, it gets destroyed
* Starter code is intact.
* Game is scalable: will still work if I change the colors, screen size, number of enemies, etc.
* Code has purpose statements and good style practices.
* README file includes:
  * Anything the user needs to know in order to use your program
  * Why you designed your classes, methods, and functions the way you did
  * Anything your future self should know, in case you decide to add to this project later on
  * Written in brief, concise language (Some people do bullet points)

## Attribution
Contributions made from [@JimmieLB](https://github.com/JimmieLB)!

This was created for the curriculum for a Python bootcamp at [Digital Ready](https://www.digitalready.org/).

This was built using some of the materials from the following sources:
* https://codingal.com/coding-for-kids/blog/space-invaders-game-using-python/
* https://github.com/clear-code-projects/Space-invaders/tree/main










