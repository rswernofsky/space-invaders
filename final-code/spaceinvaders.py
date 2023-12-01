import math
import random
import pygame
from pygame import mixer

# CONSTANTS
PLAYER_IMG = pygame.image.load('player.png')
ALIEN_IMG = pygame.image.load('enemy.png')
LASER_IMG = pygame.Surface((4,20))
LASER_IMG.fill('white')
MAX_X = 736
NUM_ALIENS = 6
LASER_RESET_Y = 380
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
NEW_ALIEN_FREQUENCY = 5 # every 5 seconds


class Player:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.x_velocity = 0
  def update(self):
    self.x += self.x_velocity
    if self.x <= 0:
      self.x = 0
    elif self.x >= MAX_X:
      self.x = MAX_X
  def draw(self, screen):
    screen.blit(PLAYER_IMG, (self.x, self.y))

class PlayerLaser:
  def __init__(self):
    self.x = 0
    self.y = LASER_RESET_Y
    self.shooting = False
    self.y_vel = -5
  def draw(self, screen):
    if (self.shooting):
      screen.blit(LASER_IMG, (self.x + 16, self.y + 10)) #TODO: why the offset?
  def reset(self):
    self.y = LASER_RESET_Y
    self.shooting = False
  def shoot(self, x):
    self.shooting = True
    self.play_sound()
    self.x = x
  def play_sound(self):
    LASER_SOUND = mixer.Sound("laser.wav")
    LASER_SOUND.play()
  def update(self):
    if self.shooting:
      self.y += self.y_vel
    if self.y <= 0:
      self.reset()

class Alien:
  def __init__(self, x, y, x_vel):
    self.x = x
    self.y = y
    self.x_vel = x_vel
    self.y_vel = 0.5
    self.laser = AlienLaser(self)
  def draw(self, screen):
    screen.blit(ALIEN_IMG, (self.x, self.y))
  def update(self):
    if self.x <= 0 or self.x >= MAX_X:
      self.x_vel = self.x_vel * -1
    self.x += self.x_vel
    self.y += self.y_vel
class AlienLaser:
  def __init__(self, alien: Alien):
    self.x = alien.x
    self.y = alien.y
    self.shooting = False
    self.y_vel = 5
    self.alien = alien
    self.base_cooldown = 50
    self.cooldown = self.base_cooldown + random.randint(0,100)
  def draw(self, screen):
    if (self.shooting):
      screen.blit(LASER_IMG, (self.x + 16, self.y + 10)) #TODO: why the offset?
  def reset(self):
    self.y = self.alien.y
    self.x = self.alien.x
    self.shooting = False
  def shoot(self):
    self.shooting = True
    self.play_sound()
    self.x = self.alien.x
    self.y = self.alien.y
  def play_sound(self):
    LASER_SOUND = mixer.Sound("laser.wav")
    LASER_SOUND.play()
  def update(self):
    if (not self.shooting):
      self.cooldown-=1
      if (self.cooldown <= 0 ):
        self.shoot()
        self.cooldown = self.base_cooldown + random.randint(0,100)
    if self.shooting:
      self.y += self.y_vel
    if self.y > SCREEN_HEIGHT:
      self.reset()

# Intialize the pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create the screen
pygame.display.set_caption("Space Invader") # Caption
clock = pygame.time.Clock()
mixer.music.load("background.wav") # Sound
mixer.music.play(-1)
score_font = pygame.font.Font('Pixeled.ttf', 32)
game_over_font = pygame.font.Font('Pixeled.ttf', 64)

# Create the player
player = Player(370, 380)

# Create the score
score_value = 0

# Create the aliens
def create_new_alien():
  alien = Alien(random.randint(0, MAX_X), random.randint(50, 150), 1)
  laser = AlienLaser(alien)
  alien.laser = laser
  aliens.append(alien)

aliens = []
for i in range(NUM_ALIENS):
  create_new_alien()

NEW_ALIEN = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_ALIEN, NEW_ALIEN_FREQUENCY * 1000)

# Create the player's laser
player_laser = PlayerLaser()

def show_score():
  score_text = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
  screen.blit(score_text, (10, 10))

def game_over_text():
  game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
  screen.blit(game_over_text, (200, 250))

def isCollision(alienX, alienY, laserX, laserY):
  distance = math.sqrt(math.pow(alienX - laserX, 2) + (math.pow(alienY - laserY, 2)))
  return distance < 27

def draw_game(screen):
  for alien in aliens:
    alien.draw(screen)
    alien.laser.draw(screen)
  player.draw(screen)
  player_laser.draw(screen)
  show_score()


running = True
game_over = False

# Game Loop
while running:
  clock.tick(30)
  screen.fill((0, 0, 0))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == NEW_ALIEN:
      create_new_alien()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        if not player_laser.shooting:
          player_laser.shoot(player.x)

  pressedKeys = pygame.key.get_pressed()
  if pressedKeys[pygame.K_LEFT]:
    player.x_velocity = -5
  elif pressedKeys[pygame.K_RIGHT]:
    player.x_velocity = 5
  else:
    player.x_velocity = 0

  player.update()

  if game_over:
    game_over_text()
  else:
    # Enemy Movement
    alien_num = 0
    while alien_num < len(aliens):
      # Game Over
      current_alien = aliens[alien_num]
      if current_alien.y > 340:
        aliens = [] # remove all the surviving aliens
        game_over = True
        pygame.time.set_timer(NEW_ALIEN, 0) # stop generating more aliens
        break

      current_alien.update()
      current_alien.laser.update()
      # Collision
      if isCollision(current_alien.x, current_alien.y, player_laser.x, player_laser.y):
        explosionSound = mixer.Sound("explosion.wav")
        explosionSound.play()
        player_laser.reset()
        score_value += 1
        aliens.remove(current_alien)
      else:
        alien_num += 1
      if isCollision(player.x, player.y, current_alien.laser.x, current_alien.laser.y):
        aliens = [] # remove all the surviving aliens
        game_over = True
        pygame.time.set_timer(NEW_ALIEN, 0) # stop generating more aliens

    # Laser Movement
    player_laser.update()


  draw_game(screen)
  pygame.display.update()