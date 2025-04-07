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
CIRCLE_RADIUS = 60
DOT_RADIUS = 6
DOT_OFFSET = CIRCLE_RADIUS // 2  # Halfway between center and edge

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ringette Game")
clock = pygame.time.Clock()

# Create fonts
score_font = pygame.font.Font(None, 36)
instructions_font = pygame.font.Font(None, 24)  # Smaller font for instructions

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
    circle_radius = CIRCLE_RADIUS
    dot_radius = DOT_RADIUS
    
    # Center face-off circle
    pygame.draw.circle(surface, BLUE_LINE, (WIDTH // 2, HEIGHT // 2), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2), dot_radius)  # Left dot
    pygame.draw.circle(surface, BLUE_LINE, (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2), dot_radius)  # Right dot
    

    # Face off circles
    right_face_off = WIDTH // 2 - 280
    left_face_off = WIDTH // 2 + 280  
    higher_face_off = HEIGHT // 4  
    lower_face_off = HEIGHT*3 // 4  

    # Higher face-off circles
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off, higher_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off - DOT_OFFSET, higher_face_off), dot_radius)  # Left dot
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off + DOT_OFFSET, higher_face_off), dot_radius)  # Right dot
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off, higher_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off - DOT_OFFSET, higher_face_off), dot_radius)  # Left dot
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off + DOT_OFFSET, higher_face_off), dot_radius)  # Right dot
    
    # Add vertical lines through higher face-off circles
    pygame.draw.line(surface, BLUE_LINE, 
                    (right_face_off, higher_face_off - circle_radius),
                    (right_face_off, higher_face_off + circle_radius), 2)
    pygame.draw.line(surface, BLUE_LINE,
                    (left_face_off, higher_face_off - circle_radius),
                    (left_face_off, higher_face_off + circle_radius), 2)
    
    # Lower face-off circles
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off, lower_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off - DOT_OFFSET, lower_face_off), dot_radius)  # Left dot
    pygame.draw.circle(surface, BLUE_LINE, (right_face_off + DOT_OFFSET, lower_face_off), dot_radius)  # Right dot
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off, lower_face_off), circle_radius, 2)
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off - DOT_OFFSET, lower_face_off), dot_radius)  # Left dot
    pygame.draw.circle(surface, BLUE_LINE, (left_face_off + DOT_OFFSET, lower_face_off), dot_radius)  # Right dot
    
    # Add vertical lines through lower face-off circles
    pygame.draw.line(surface, BLUE_LINE,
                    (right_face_off, lower_face_off - circle_radius),
                    (right_face_off, lower_face_off + circle_radius), 2)
    pygame.draw.line(surface, BLUE_LINE,
                    (left_face_off, lower_face_off - circle_radius),
                    (left_face_off, lower_face_off + circle_radius), 2)


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
        self.direction = [1, 0]  # Default direction to right

    def update(self, keys=None):
        if keys:
            # Arrow keys and WASD movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= PLAYER_SPEED
                self.direction = [-1, 0]
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += PLAYER_SPEED
                self.direction = [1, 0]
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect.y -= PLAYER_SPEED
                self.direction = [0, -1]
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += PLAYER_SPEED
                self.direction = [0, 1]

        # Keep player on screen
        self.rect.clamp_ip(screen.get_rect())

    def get_shoot_direction(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate direction vector from player to mouse
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        # Normalize the vector
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            return [dx / length, dy / length]
        return [1, 0]  # Default to right if mouse is on player

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
        self.shoot_cooldown = 0  # Add cooldown timer

    def update(self):
        if self.active:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            
            # Update cooldown
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

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
# Add ring first so it's drawn underneath
all_sprites.add(ring)
# Then add player so it's drawn on top
all_sprites.add(player)
# Add goals last
all_sprites.add(goal1)
all_sprites.add(goal2)

# Game variables
score = 0

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
                # Position ring at bottom right of player with offset
                ring.rect.bottomright = (player.rect.right + 10, player.rect.bottom)
                # Get direction from player to mouse
                direction = player.get_shoot_direction()
                ring.velocity = [direction[0] * RING_SPEED, 
                               direction[1] * RING_SPEED]
                ring.shoot_cooldown = 30  # Set cooldown to 30 frames (0.5 seconds at 60 FPS)

    # Get keys
    keys = pygame.key.get_pressed()

    # Update
    player.update(keys)
    ring.update()

    # Check for ring pickup
    if not ring.active and pygame.sprite.collide_rect(player, ring):
        player.has_ring = True
        # Position ring at bottom right of player with offset
        ring.rect.bottomright = (player.rect.right + 10, player.rect.bottom)
    elif ring.active and pygame.sprite.collide_rect(player, ring) and ring.shoot_cooldown == 0:
        player.has_ring = True
        ring.active = False
        # Position ring at bottom right of player with offset
        ring.rect.bottomright = (player.rect.right + 10, player.rect.bottom)
        ring.velocity = [0, 0]

    # Check for goals
    if ring.active:
        if pygame.sprite.collide_rect(ring, goal1):
            score += 1
            ring.active = False
            # Place ring on left team's center dot (they got scored on)
            ring.rect.center = (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2)
            ring.velocity = [0, 0]
        elif pygame.sprite.collide_rect(ring, goal2):
            score += 1
            ring.active = False
            # Place ring on right team's center dot (they got scored on)
            ring.rect.center = (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2)
            ring.velocity = [0, 0]
        # Then check for pickup if no goal was scored and cooldown is over
        elif pygame.sprite.collide_rect(player, ring) and ring.shoot_cooldown == 0:
            player.has_ring = True
            ring.active = False
            # Position ring at bottom right of player with offset
            ring.rect.bottomright = (player.rect.right + 10, player.rect.bottom)
            ring.velocity = [0, 0]
    # Check for initial pickup when ring is not active
    elif not ring.active and pygame.sprite.collide_rect(player, ring):
        player.has_ring = True
        # Position ring at bottom right of player with offset
        ring.rect.bottomright = (player.rect.right + 10, player.rect.bottom)

    # Draw
    draw_rink(screen)
    all_sprites.draw(screen)
    
    # Draw score (moved down and to the right)
    score_text = score_font.render(f"Score: {score}", True, RINK_BLUE)
    screen.blit(score_text, (WIDTH - 160, 20))  # Moved to top-right corner

    # Draw instructions (moved to left side)
    instructions = instructions_font.render("ARROW KEYS: Move", True, RINK_BLUE)
    screen.blit(instructions, (20, HEIGHT - 50))
    instructions2 = instructions_font.render("SPACE: Shoot", True, RINK_BLUE)
    screen.blit(instructions2, (20, HEIGHT - 35))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 