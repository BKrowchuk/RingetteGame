import pygame
import sys
import random
import math
import os
from assets import *

# Initialize Pygame
pygame.init()

# Get the base path for assets
def get_asset_path(filename):
    # If we're running as a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'assets', filename)

# Load Lynx logo
try:
    lynx_logo = pygame.image.load(get_asset_path('lynxlogo.svg'))
    lynx_logo = pygame.transform.scale(lynx_logo, (PLAYER_WIDTH, PLAYER_HEIGHT))
except Exception as e:
    print(f"Warning: Could not load lynxlogo.svg: {str(e)}. Using default player shape.")
    lynx_logo = None

# Constants
WIDTH, HEIGHT = RINK_WIDTH, RINK_HEIGHT
FPS = 60
PLAYER_SPEED = 5
RING_SPEED = 8

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ringette Game")
clock = pygame.time.Clock()

def draw_rink(surface):
    # Draw ice surface
    surface.fill(ICE_WHITE)
    
    # Draw rink outline (thicker border)
    pygame.draw.rect(surface, RINK_BLUE, (0, 0, WIDTH, HEIGHT), 15)
    
    # Draw center line (vertical red line)
    pygame.draw.line(surface, RED_LINE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 8)
    
    # Draw blue lines (ringette has two blue lines with specific width)
    blue_line_width = 10  # Thinner blue lines
    # Move blue lines closer to center (about 1/4 of the way from center)
    blue_line_1_x = WIDTH // 2 - 100  # 100 pixels left of center
    blue_line_2_x = WIDTH // 2 + 100  # 100 pixels right of center
    pygame.draw.rect(surface, BLUE_LINE, (blue_line_1_x - blue_line_width//2, 0, blue_line_width, HEIGHT))
    pygame.draw.rect(surface, BLUE_LINE, (blue_line_2_x - blue_line_width//2, 0, blue_line_width, HEIGHT))
    
    # Draw goal lines (vertical red lines - thinner)
    pygame.draw.line(surface, RED_LINE, (GOAL_LINE_1_X, 0), (GOAL_LINE_1_X, HEIGHT), 3)
    pygame.draw.line(surface, RED_LINE, (GOAL_LINE_2_X, 0), (GOAL_LINE_2_X, HEIGHT), 3)
    
    # Draw face-off circles (larger circles with dots)
    circle_radius = 60 # Increased from 15
    dot_radius = 6     # Increased from 3
    
    # Center face-off circle
    pygame.draw.circle(surface, BLUE_LINE, (WIDTH // 2, HEIGHT // 2), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (WIDTH // 2, HEIGHT // 2), dot_radius)
    

    # Face off circles
    right_face_off = WIDTH // 2 - 280
    left_face_off = WIDTH // 2 + 280  
    higher_face_off = HEIGHT // 4  
    lower_face_off = HEIGHT*3 // 4  

    # Higher face-off circles
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off, higher_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off, higher_face_off), dot_radius)
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off, higher_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off, higher_face_off), dot_radius)
    # Lower face-off circles
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off, lower_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off, lower_face_off), dot_radius)
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off, lower_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off, lower_face_off), dot_radius)


    # Draw goal creases (proper semi-circles with specific radius)
    crease_radius = 60  # Decreased from 80
    # Left goal crease (facing towards goal)
    pygame.draw.arc(surface, BLUE_LINE, 
                   (GOAL_LINE_1_X - crease_radius, HEIGHT//2 - crease_radius, 
                    crease_radius*2, crease_radius*2), 
                   -math.pi/2, math.pi/2, 3)
    # Right goal crease (facing towards goal)
    pygame.draw.arc(surface, BLUE_LINE, 
                   (GOAL_LINE_2_X - crease_radius, HEIGHT//2 - crease_radius, 
                    crease_radius*2, crease_radius*2), 
                   math.pi/2, 3*math.pi/2, 3)
    
    # Draw free play lines (ringette specific, closer to goal)
    free_play_distance = 150  # Standard ringette free play line distance
    pygame.draw.line(surface, RED_LINE, 
                    (GOAL_LINE_1_X + free_play_distance, 0), 
                    (GOAL_LINE_1_X + free_play_distance, HEIGHT), 3)
    pygame.draw.line(surface, RED_LINE, 
                    (GOAL_LINE_2_X - free_play_distance, 0), 
                    (GOAL_LINE_2_X - free_play_distance, HEIGHT), 3)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if lynx_logo:
            self.image = lynx_logo
        else:
            # Create a simple player shape for now
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
            # Draw a simple player shape
            pygame.draw.ellipse(self.image, PLAYER_COLOR, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT))
            # Add a stick
            pygame.draw.line(self.image, (139, 69, 19), 
                            (PLAYER_WIDTH//2, PLAYER_HEIGHT//2),
                            (PLAYER_WIDTH, PLAYER_HEIGHT//2), 3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.has_ring = False
        self.direction = [0, 0]

    def update(self, keys=None):
        if keys:
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
                self.direction = [-1, 0]
            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
                self.direction = [1, 0]
            if keys[pygame.K_UP]:
                self.rect.y -= PLAYER_SPEED
                self.direction = [0, -1]
            if keys[pygame.K_DOWN]:
                self.rect.y += PLAYER_SPEED
                self.direction = [0, 1]

        # Keep player on screen
        self.rect.clamp_ip(screen.get_rect())

class Ring(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Draw a blue ring
        pygame.draw.circle(self.image, RING_COLOR, (10, 10), 10)
        pygame.draw.circle(self.image, ICE_WHITE, (10, 10), 5)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.active = False
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        if self.active:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            # Bounce off walls
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.velocity[0] *= -1
            if self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.velocity[1] *= -1

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RINK_BLUE, (0, 0, 20, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create game objects
player = Player(WIDTH // 2, HEIGHT // 2)
ring = Ring()
# Create two goals
goal1 = Goal(GOAL_LINE_1_X - 20, HEIGHT // 2 - 50)  # Move goal1 to the left side of its goal line
goal2 = Goal(GOAL_LINE_2_X, HEIGHT // 2 - 50)  # Move goal2 to the right side of its goal line

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ring)
all_sprites.add(goal1)
all_sprites.add(goal2)

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.has_ring:
                player.has_ring = False
                ring.active = True
                ring.rect.center = player.rect.center
                ring.velocity = [player.direction[0] * RING_SPEED, 
                               player.direction[1] * RING_SPEED]

    # Get keys
    keys = pygame.key.get_pressed()

    # Update
    player.update(keys)
    ring.update()

    # Check for ring pickup
    if not ring.active and pygame.sprite.collide_rect(player, ring):
        player.has_ring = True
        ring.rect.center = player.rect.center

    # Check for goals
    if ring.active:
        if pygame.sprite.collide_rect(ring, goal1) or pygame.sprite.collide_rect(ring, goal2):
            score += 1
            ring.active = False
            ring.rect.center = (WIDTH // 2, HEIGHT // 2)
            ring.velocity = [0, 0]

    # Draw
    draw_rink(screen)
    all_sprites.draw(screen)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, RINK_BLUE)
    screen.blit(score_text, (10, 10))

    # Draw instructions
    instructions = font.render("Use arrow keys to move, SPACE to shoot", True, RINK_BLUE)
    screen.blit(instructions, (WIDTH // 2 - 200, HEIGHT - 30))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 