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
RING_SPEED = 5  # Reduced from 8 to make the ring move slower
CIRCLE_RADIUS = 60
DOT_RADIUS = 6
DOT_OFFSET = CIRCLE_RADIUS // 2  # Halfway between center and edge
PICKUP_RANGE = 70  # Range within which the player can pick up the ring
SHOT_CLOCK_DURATION = 30  # 30 seconds shot clock

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ringette Game")
clock = pygame.time.Clock()

# Create fonts
score_font = pygame.font.Font(None, 36)
instructions_font = pygame.font.Font(None, 16)  # Smaller font for instructions

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

# Load sprites
def create_ring_sprite():
    surface = pygame.Surface((20, 20), pygame.SRCALPHA)
    # Draw a blue ring
    pygame.draw.circle(surface, RING_COLOR, (10, 10), 10)
    pygame.draw.circle(surface, ICE_WHITE, (10, 10), 5)
    return surface

def create_goalie_sprite():
    surface = pygame.Surface((20, 40), pygame.SRCALPHA)
    
    # Body (red jersey)
    pygame.draw.rect(surface, (220, 20, 20), (5, 10, 10, 20))  # Torso
    
    # Head
    pygame.draw.circle(surface, (255, 218, 185), (10, 7), 5)  # Flesh color
    
    # Arms (holding stick)
    pygame.draw.line(surface, (220, 20, 20), (5, 15), (3, 25), 3)   # Left arm
    pygame.draw.line(surface, (220, 20, 20), (15, 15), (17, 25), 3) # Right arm
    
    # Hands (holding stick)
    pygame.draw.circle(surface, (255, 218, 185), (3, 25), 2)  # Left hand
    pygame.draw.circle(surface, (255, 218, 185), (17, 25), 2)  # Right hand
    
    # Legs (slightly spread)
    pygame.draw.line(surface, (0, 0, 0), (7, 30), (7, 38), 3)  # Left leg
    pygame.draw.line(surface, (0, 0, 0), (13, 30), (13, 38), 3)  # Right leg
    
    # Goalie stick (held horizontally)
    pygame.draw.line(surface, (139, 69, 19), (3, 25), (17, 25), 3)  # Brown stick
    
    return surface

# Load all sprites
ring_sprite = create_ring_sprite()
goalie_sprite = create_goalie_sprite()

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
        # Calculate direction vector from ring to mouse (using ring's position)
        ring_x = self.rect.right + 10  # Ring's x position (offset from player)
        ring_y = self.rect.bottom      # Ring's y position
        dx = mouse_x - ring_x
        dy = mouse_y - ring_y
        # Normalize the vector
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            return [dx / length, dy / length]
        return [1, 0]  # Default to right if mouse is on ring

class Ring(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ring_sprite
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.active = False
        self.thrown_by_goalie = False  # Track if ring was thrown by goalie
        self.decay_factor = 0.98  # Decay factor for velocity
        # Start on the left center dot
        self.rect.center = (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2)

    def update(self):
        if self.active:
            # Apply velocity decay if thrown by goalie
            if self.thrown_by_goalie:
                self.velocity[0] *= self.decay_factor
                self.velocity[1] *= self.decay_factor
                # Stop very slow movement to prevent endless sliding
                if abs(self.velocity[0]) < 0.1 and abs(self.velocity[1]) < 0.1:
                    self.velocity = [0, 0]
                    self.thrown_by_goalie = False

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

class Goalie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = goalie_sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1  # Reduced from 4 to make goalie movement slower
        self.direction = 1  # 1 for down, -1 for up
        self.goal_top = HEIGHT // 2 - 50  # Top of the goal
        self.goal_bottom = HEIGHT // 2 + 50  # Bottom of the goal
        self.has_ring = False  # Track if goalie is holding the ring
        self.hold_time = 0  # Track how long goalie has held the ring
        self.throw_direction = [0, 0]  # Direction to throw the ring
        self.throw_cooldown = 0  # Cooldown after throwing before can catch again

    def update(self):
        # Only move if not holding the ring
        if not self.has_ring:
            # Move up and down within goal area
            self.rect.y += self.speed * self.direction
            
            # Change direction at goal boundaries
            if self.rect.top <= self.goal_top:
                self.direction = 1
            elif self.rect.bottom >= self.goal_bottom:
                self.direction = -1

            # Update throw cooldown
            if self.throw_cooldown > 0:
                self.throw_cooldown -= 1

        # Update ring position if goalie has it
        if self.has_ring:
            self.hold_time += 1
            if self.hold_time >= 180:  # 3 seconds at 60 FPS
                self.has_ring = False
                self.throw_cooldown = 120  # 2 second cooldown (60 FPS * 2)
                return self.throw_direction  # Return direction to throw the ring
        return None

    def can_catch(self):
        return not self.has_ring and self.throw_cooldown == 0

# Create game objects
player = Player(WIDTH // 2 - 100, HEIGHT // 2)  # Start on left blue line
ring = Ring()
# Create two goals
goal1 = Goal(GOAL_LINE_1_X - 20, HEIGHT // 2 - 50)  # Move goal1 to the left side of its goal line
goal2 = Goal(GOAL_LINE_2_X, HEIGHT // 2 - 50)  # Move goal2 to the right side of its goal line
# Create goalies
goalie1 = Goalie(GOAL_LINE_1_X - 10, HEIGHT // 2 - 30)  # Left goalie
goalie2 = Goalie(GOAL_LINE_2_X - 10, HEIGHT // 2 - 30)  # Right goalie

# Create sprite groups
all_sprites = pygame.sprite.Group()
# Add ring first so it's drawn underneath
all_sprites.add(ring)
# Then add player so it's drawn on top
all_sprites.add(player)
# Add goals and goalies
all_sprites.add(goal1)
all_sprites.add(goal2)
all_sprites.add(goalie1)
all_sprites.add(goalie2)

# Game variables
score = 0
show_instructions = True  # New variable to track if instructions should be shown
shot_clock = SHOT_CLOCK_DURATION  # Initialize shot clock
last_time = pygame.time.get_ticks()  # Track time for shot clock
ring_picked_up_since_goal = False  # Track if ring has been picked up since last goal

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
                ring.thrown_by_goalie = False  # Ensure decay is not applied to player shots
                shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock when shooting
            elif event.key == pygame.K_ESCAPE:  # Toggle instructions with Escape key
                show_instructions = not show_instructions
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if show_instructions:
                show_instructions = False  # Clear instructions on first click
            else:
                # Calculate distance between player and ring
                dx = ring.rect.centerx - player.rect.centerx
                dy = ring.rect.centery - player.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Toggle pickup if within range
                if distance <= PICKUP_RANGE:
                    player.has_ring = not player.has_ring  # Toggle pickup state
                    if player.has_ring:
                        # Position ring at bottom right of player with offset
                        ring.rect.bottomright = (player.rect.right + 10, player.rect.bottom)
                        ring.active = False  # Stop the ring from moving
                        ring.velocity = [0, 0]  # Reset velocity
                        ring_picked_up_since_goal = True  # Mark that ring has been picked up

    # Update shot clock
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= 1000:  # Every second
        if not show_instructions and ring_picked_up_since_goal:  # Only count down after first pickup
            shot_clock -= 1
            if shot_clock <= 0:
                # Time's up! Reset ring to center
                player.has_ring = False
                ring.active = False
                ring.velocity = [0, 0]
                ring.rect.center = (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2)  # Reset to left center dot
                shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock
                ring_picked_up_since_goal = False  # Reset pickup flag
        last_time = current_time

    # Get keys
    keys = pygame.key.get_pressed()

    # Update
    player.update(keys)
    
    # Update goalies and check for throws
    throw_direction = goalie1.update()
    if throw_direction:
        ring.active = True
        # Position ring slightly in front of goalie (to the right)
        ring.rect.center = (goalie1.rect.centerx + 20, goalie1.rect.centery)
        ring.velocity = [throw_direction[0] * RING_SPEED * 0.5, throw_direction[1] * RING_SPEED * 0.5]  # Half speed for goalie throws
        ring.thrown_by_goalie = True  # Mark that ring was thrown by goalie
        goalie1.hold_time = 0
        shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock on throw
    
    throw_direction = goalie2.update()
    if throw_direction:
        ring.active = True
        # Position ring slightly in front of goalie (to the left)
        ring.rect.center = (goalie2.rect.centerx - 20, goalie2.rect.centery)
        ring.velocity = [throw_direction[0] * RING_SPEED * 0.5, throw_direction[1] * RING_SPEED * 0.5]  # Half speed for goalie throws
        ring.thrown_by_goalie = True  # Mark that ring was thrown by goalie
        goalie2.hold_time = 0
        shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock on throw
    
    # Update ring position if player has it
    if player.has_ring and not ring.active:
        ring.rect.bottomright = (player.rect.right + 10, player.rect.bottom)
    
    ring.update()

    # Check for goals and goalie blocks
    if ring.active:
        # Check for goalie blocks first
        if pygame.sprite.collide_rect(ring, goalie1) and goalie1.can_catch():
            if random.random() < 0.9:  # 90% chance to catch
                # Goalie catches the ring
                ring.active = False
                goalie1.has_ring = True
                goalie1.hold_time = 0  # Reset hold time
                # Calculate throw direction (away from net)
                goalie1.throw_direction = [1, random.uniform(-1, 1)]  # Left goalie throws right (away from net)
                ring.rect.center = goalie1.rect.center  # Position ring on goalie
            else:
                # Normal bounce
                ring.velocity[0] *= -1  # Reverse x velocity
                ring.velocity[1] *= -1  # Reverse y velocity
                # Add some randomness to the bounce
                ring.velocity[0] += random.uniform(-1, 1)
                ring.velocity[1] += random.uniform(-1, 1)
            shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock when ring hits goalie
        elif pygame.sprite.collide_rect(ring, goalie2) and goalie2.can_catch():
            if random.random() < 0.9:  # 90% chance to catch
                # Goalie catches the ring
                ring.active = False
                goalie2.has_ring = True
                goalie2.hold_time = 0  # Reset hold time
                # Calculate throw direction (away from net)
                goalie2.throw_direction = [-1, random.uniform(-1, 1)]  # Right goalie throws left (away from net)
                ring.rect.center = goalie2.rect.center  # Position ring on goalie
            else:
                # Normal bounce
                ring.velocity[0] *= -1  # Reverse x velocity
                ring.velocity[1] *= -1  # Reverse y velocity
                # Add some randomness to the bounce
                ring.velocity[0] += random.uniform(-1, 1)
                ring.velocity[1] += random.uniform(-1, 1)
            shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock when ring hits goalie
        elif pygame.sprite.collide_rect(ring, goal1):
            score += 1
            ring.active = False
            # Place ring on left team's center dot (they got scored on)
            ring.rect.center = (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2)
            ring.velocity = [0, 0]
            shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock on goal
            ring_picked_up_since_goal = False  # Reset pickup flag after goal
        elif pygame.sprite.collide_rect(ring, goal2):
            score += 1
            ring.active = False
            # Place ring on right team's center dot (they got scored on)
            ring.rect.center = (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2)
            ring.velocity = [0, 0]
            shot_clock = SHOT_CLOCK_DURATION  # Reset shot clock on goal
            ring_picked_up_since_goal = False  # Reset pickup flag after goal

    # Draw
    draw_rink(screen)
    all_sprites.draw(screen)
    
    # Draw score
    score_text = score_font.render(f"Score: {score}", True, RINK_BLUE)
    screen.blit(score_text, (WIDTH - 160, 20))

    # Draw shot clock (always visible when not in instructions)
    if not show_instructions:
        # Create a background for the shot clock
        clock_bg = pygame.Surface((100, 40), pygame.SRCALPHA)
        clock_bg.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(clock_bg, (20, 20))
        
        # Draw the shot clock text
        clock_text = score_font.render(f"{shot_clock}s", True, (255, 255, 255))
        screen.blit(clock_text, (30, 25))

    # Draw instructions popup if needed
    if show_instructions:
        # Create a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(overlay, (0, 0))
        
        # Instructions text
        instructions = [
            "HOW TO PLAY:",
            "ARROW KEYS or WASD: Move",
            "LEFT CLICK near ring: Pick up",
            "LEFT CLICK while holding: Drop",
            "SPACE: Shoot ring",
            "AIM: Mouse position determines",
            "     shooting direction",
            "Get close to ring to pick it up",
            "Score by shooting into goals",
            "30 second shot clock!",
            "",
            "Click anywhere to start!",
            "Press ESC to show/hide instructions"
        ]
        
        # Calculate total height and width of instructions
        total_height = len(instructions) * 16
        max_width = max(instructions_font.size(text)[0] for text in instructions)
        start_y = (HEIGHT - total_height) // 2
        start_x = (WIDTH - max_width) // 2
        
        # Draw background rectangle for text
        padding = 20
        bg_rect = pygame.Rect(
            start_x - padding,
            start_y - padding,
            max_width + padding * 2,
            total_height + padding * 2
        )
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)  # Black background
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)  # White border
        
        for i, text in enumerate(instructions):
            instruction_text = instructions_font.render(text, True, (255, 255, 255))  # White text
            text_rect = instruction_text.get_rect(centerx=WIDTH//2, y=start_y + i * 16)
            screen.blit(instruction_text, text_rect)

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 