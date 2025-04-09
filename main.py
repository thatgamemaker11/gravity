import pygame
import random
# Initialize Pygame and setup the screen
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
Rsize = random.randint(50,100)
# Rocket and game settings
rocket_size = (20, 40)
Rock_size = (Rsize,Rsize)
rotation_speed = 5
acceleration = 0.2
friction = 0.99
max_speed = 5
bullet_speed = 10
shoot_cooldown = 250  # milliseconds
bg_color = (10, 10, 30)

# Colors
rocket_color_1 = (255, 100, 100)
rocket_color_2 = (100, 200, 255)
bullet_color = (255, 255, 255)

# Create rocket dictionary with all necessary properties
def create_rocket(x, y):
    return {
        "pos": pygame.math.Vector2(x, y),     # Position of the rocket
        "vel": pygame.math.Vector2(0, 0),     # Velocity vector
        "angle": 0,                           # Rotation angle
        "bullets": [],                        # List of bullets fired
        "hits": 0                             # Number of times hit
    }

# Initialize both players
player1 = create_rocket(300, 500)
player2 = create_rocket(1600, 500)

# Game loop
running = True
while running:
    dt = clock.tick(60) / 1000  # Frame rate control (in seconds)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ---- Player 1 Controls (WASD + SPACE to shoot) ----
    if keys[pygame.K_a]:
        player1["angle"] += rotation_speed
    if keys[pygame.K_d]:
        player1["angle"] -= rotation_speed
    if keys[pygame.K_w]:
        direction = pygame.math.Vector2(0, -1).rotate(-player1["angle"])
        player1["vel"] += direction * acceleration
    if keys[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        if len(player1["bullets"]) == 0 or now - player1["bullets"][-1]["spawn_time"] > shoot_cooldown:
            direction = pygame.math.Vector2(0, -1).rotate(-player1["angle"])
            bullet_pos = player1["pos"] + direction * 25
            bullet_vel = direction * bullet_speed
            player1["bullets"].append({
                "pos": bullet_pos,
                "vel": bullet_vel,
                "spawn_time": now
            })

    # ---- Player 2 Controls (Arrow keys + Enter to shoot) ----
    if keys[pygame.K_LEFT]:
        player2["angle"] += rotation_speed
    if keys[pygame.K_RIGHT]:
        player2["angle"] -= rotation_speed
    if keys[pygame.K_UP]:
        direction = pygame.math.Vector2(0, -1).rotate(-player2["angle"])
        player2["vel"] += direction * acceleration
    if keys[pygame.K_RCTRL] or keys[pygame.K_RETURN]:
        now = pygame.time.get_ticks()
        if len(player2["bullets"]) == 0 or now - player2["bullets"][-1]["spawn_time"] > shoot_cooldown:
            direction = pygame.math.Vector2(0, -1).rotate(-player2["angle"])
            bullet_pos = player2["pos"] + direction * 25
            bullet_vel = direction * bullet_speed
            player2["bullets"].append({
                "pos": bullet_pos,
                "vel": bullet_vel,
                "spawn_time": now
            })

    # ---- Update Players ----
    for player in (player1, player2):
        # Apply friction and limit speed
        player["vel"] *= friction
        if player["vel"].length() > max_speed:
            player["vel"].scale_to_length(max_speed)
        # Update position
        player["pos"] += player["vel"]
        # Screen wrapping
        if player["pos"].x < 0:
            player["pos"].x = 1920
        elif player["pos"].x > 1920:
            player["pos"].x = 0
        if player["pos"].y < 0:
            player["pos"].y = 1080
        elif player["pos"].y > 1080:
            player["pos"].y = 0

    # ---- Bullet Updates and Collision Detection ----
    for player, opponent in [(player1, player2), (player2, player1)]:
        new_bullets = []
        opponent_rect = pygame.Rect(0, 0, *rocket_size)
        opponent_rect.center = opponent["pos"]

        for bullet in player["bullets"]:
            bullet["pos"] += bullet["vel"]
            # Check screen bounds
            if 0 <= bullet["pos"].x <= 1920 and 0 <= bullet["pos"].y <= 1080:
                # Check collision with opponent
                if opponent_rect.collidepoint(bullet["pos"]):
                    opponent["hits"] += 1
                else:
                    new_bullets.append(bullet)
        player["bullets"] = new_bullets

    # ---- Drawing ----
    screen.fill(bg_color)  # Clear screen

    # Draw function for each rocket
    def draw_rocket(player, color):
        # Create triangle shape on surface
        surface = pygame.Surface(rocket_size, pygame.SRCALPHA)
        pygame.draw.polygon(surface, color, [(10, 0), (0, 40), (20, 40)])
        # Rotate and position
        rotated = pygame.transform.rotate(surface, player["angle"])
        rect = rotated.get_rect(center=player["pos"])
        screen.blit(rotated, rect.topleft)

        # Draw bullets
        for bullet in player["bullets"]:
            pygame.draw.circle(screen, bullet_color, bullet["pos"], 3)

    def draw_rock( ):
        # Create triangle shape on surface
        surface = pygame.Surface(Rock_size, pygame.SRCALPHA)
        pygame.draw.polygon(surface, "gray", [(0,Rsize/3) ,(Rsize/3, 0),((Rsize/3)*2, 0),(Rsize, Rsize/3),(Rsize,(Rsize/3)*2),((Rsize/3)*2,Rsize),(Rsize/3,Rsize),(0,(Rsize/3)*2)])
        # Rotate and position
        rotated = pygame.transform.rotate(surface, 0)
        rect = rotated.get_rect(center=(1000,1000))
        screen.blit(rotated, rect.topleft)

    draw_rocket(player1, rocket_color_1)
    draw_rocket(player2, rocket_color_2)
    draw_rock()

    # Draw hit counters
    font = pygame.font.SysFont(None, 48)
    hit_text1 = font.render(f"Player 1 Hits: {player1['hits']}", True, rocket_color_1)
    hit_text2 = font.render(f"Player 2 Hits: {player2['hits']}", True, rocket_color_2)
    screen.blit(hit_text1, (20, 20))
    screen.blit(hit_text2, (20, 80))

    # Flip display
    pygame.display.flip()

# Quit Pygame when the game loop ends
pygame.quit()
