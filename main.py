# Resources:
# https://realpython.com/pygame-a-primer/#pygame-concepts
# https://www.pygame.org/docs/ref/key.html


# Challenges encountered:
# - Using a circular character rather than a rectangular one
# - Collision detection between bullets and player
# - Bullets going far too fast


import random
import math
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_LSHIFT,
    K_ESCAPE,
    K_x,
    KEYDOWN,
    KEYUP,
    QUIT,
)


# Initialize pygame
pygame.init()


# Set up the window
screenwidth, screenheight = 400, 600
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("The Game")


class Player:

    def __init__(self):
        # Player features
        self.player_surface = screen
        self.player_color = (255, 0, 0)
        self.player_radius = 5
        self.player_pos = [200, 550]
        self.player_width = 0

    def update(self, p_keys, p_speed):

        # Checks which direction to move the player in
        if p_keys[K_UP]:
            self.player_pos[1] = self.player_pos[1] - p_speed

        if p_keys[K_DOWN]:
            self.player_pos[1] = self.player_pos[1] + p_speed

        if p_keys[K_LEFT]:
            self.player_pos[0] = self.player_pos[0] - p_speed

        if p_keys[K_RIGHT]:
            self.player_pos[0] = self.player_pos[0] + p_speed

        # Checks if any bit of the player is offscreen
        if self.player_pos[0] < 0 + self.player_radius:
            self.player_pos[0] = 0 + self.player_radius

        if self.player_pos[0] > screenwidth - self.player_radius:
            self.player_pos[0] = screenwidth - self.player_radius

        if self.player_pos[1] < 0 + self.player_radius:
            self.player_pos[1] = 0 + self.player_radius

        if self.player_pos[1] > screenheight - self.player_radius:
            self.player_pos[1] = screenheight - self.player_radius

    def character(self):
        # Draws the circle
        pygame.draw.circle(self.player_surface, self.player_color, self.player_pos, self.player_radius, self.player_width)


player = Player()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.size = 15
        self.surf = pygame.Surface((self.size, self.size))  # Size
        self.surf.fill((random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, screenwidth),  # Spawning position on X axis
                0,  # Spawning position on Y axis
            )
        )
        self.speed = random.randint(2, 5)

    def getsize(self):
        return self.size

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > screenheight:
            self.kill()


enemies = pygame.sprite.Group()


ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 100)


def collision(rec_left, rec_top, width, height,  # Rectangle definition
              center_x, center_y, radius):       # Circle definition

    # Complete the boundbox of the rectangle
    rec_right, rec_bottom = rec_left + width, rec_top + height

    # Bounding box of the circle
    cir_left, cir_top, cir_right, cir_bottom = center_x - radius, center_y - radius, center_x + radius, center_y + radius

    # Checks if bounding boxes do not intersect
    if rec_right < cir_left or rec_left > cir_right or rec_bottom < cir_top or rec_top > cir_bottom:
        return  # No collision possible, breaks early

    # Check if center of circle is inside rectangle, increases likelihood of detection
    if rec_left <= center_x <= rec_right and rec_top <= center_y <= rec_bottom:
        return True  # Collision detected

    # Check whether any point of rectangle is inside circle's radius
    for x in (rec_left, rec_left + width):
        for y in (rec_top, rec_top + height):
            # Compares the distance between circle's center point and each point of the rectangle with the circle's radius
            if math.hypot(x - center_x, y - center_y) <= radius:
                return True  # Collision detected

    return


running = True
bombs_used = 0
speed = 6

while running:
    # Fills the screen with a colour
    screen.fill((200, 200, 255))

    # Look at every event in the queue
    for event in pygame.event.get():
        # Checks for key presses
        if event.type == KEYUP:
            if event.key == K_LSHIFT:
                speed = 6

        if event.type == KEYDOWN:
            if event.key == K_LSHIFT:  # Slows down the player for more precise movement
                speed = 3

            # Stops the loop when escape is pressed
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_x:
                for entity in enemies:
                    entity.kill()
                bombs_used += 1

        # Add a new bullet
        if event.type == ADD_ENEMY:
            # Create the new bullet and add it to the enemy group
            for i in range(4):
                new_enemy = Enemy()
                enemies.add(new_enemy)

        # Stops the loop when the close windows button is pressed
        elif event.type == QUIT:
            running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    player.character()
    player.update(pressed_keys, speed)

    # Update enemy position
    enemies.update()

    # Draw all sprites
    for entity in enemies:
        screen.blit(entity.surf, entity.rect)

    for entity in enemies:
        if collision(entity.rect.left, entity.rect.top, 15, 15, player.player_pos[0], player.player_pos[1],
                     player.player_radius):
            running = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
print(f"\n ==== You used {bombs_used} screen clears ====")
