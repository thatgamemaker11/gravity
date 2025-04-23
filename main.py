import pygame
import random



# Initialize Pygame and setup the screen
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
Rsize = random.choice(
[
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
    30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
    40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
    50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
    60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
    70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
    80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
    90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
    100
]
)
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

# Rock position and velocity
pos = pygame.Vector2(random.randint(0, 1920), random.randint(0, 1080))
vel = pygame.Vector2(random.choice([-1, 1])*10000/Rsize, random.choice([-1, 1])*6000/Rsize)

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
        "health": 20                                  # Number of times hit
    }

# Initialize both players
player1 = create_rocket(300, 500)
player2 = create_rocket(1600, 500)
rock = {
    "pos": pygame.Vector2(random.randint(0, 1920), random.randint(0, 1080)),
    "vel": pygame.Vector2(random.choice([-1, 1])*10000/Rsize, random.choice([-1, 1])*6000/Rsize),
    "size": Rsize}
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

    # ---- Update Rock ----
    pos += vel * dt
    if pos.x < 0 :
        pos.x = 2100
    elif pos.x > 2100:
        pos.x = 0
    if pos.y < 0:
        pos.y = 1200
    elif pos.y > 1200:
        pos.y = 0

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
                    opponent["health"] -= 1
                else:
                    new_bullets.append(bullet)
        player["bullets"] = new_bullets
    rock_rect = pygame.Rect(0, 0, rock["size"], rock["size"])
    rock_rect.center = rock["pos"]
    rock["pos"] += rock["vel"] * dt
    if rock["pos"].x < 0:
        rock["pos"].x = 2100
    elif rock["pos"].x > 2100:
        rock["pos"].x = 0
    if rock["pos"].y < 0:
        rock["pos"].y = 1200
    elif rock["pos"].y > 1200:
        rock["pos"].y = 0
    for opponent in [player1, player2]:
        opponent_rect = pygame.Rect(0, 0, *rocket_size)
        opponent_rect.center = opponent["pos"]
        if rock_rect.colliderect(opponent_rect):
            opponent["health"] -= 5
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

    def draw_rock():
        surface = pygame.Surface((rock["size"], rock["size"]), pygame.SRCALPHA)
        Rsize = rock["size"]
        pygame.draw.polygon(surface, "gray", [
            (0, Rsize / 3), (Rsize / 3, 0), ((Rsize / 3) * 2, 0), (Rsize, Rsize / 3),
            (Rsize, (Rsize / 3) * 2), ((Rsize / 3) * 2, Rsize), (Rsize / 3, Rsize), (0, (Rsize / 3) * 2)
        ])
        rotated = pygame.transform.rotate(surface, 0)
        rect = rotated.get_rect(center=rock["pos"])
        screen.blit(rotated, rect.topleft)





    draw_rocket(player1, rocket_color_1)
    draw_rocket(player2, rocket_color_2)
    draw_rock()

    # Draw hit counters
    font = pygame.font.SysFont(None, 48)
    hit_text1 = font.render(f"Player 1 Health: {player1['health']}", True, rocket_color_1)
    if player1['health'] == 0:
        print("P2 WINS")
        exit()
    if player2['health'] == 0:
        print("P1 WINS")
        exit()
    hit_text2 = font.render(f"Player 2 Health: {player2['health']}", True, rocket_color_2)
    screen.blit(hit_text1, (20, 20))
    screen.blit(hit_text2, (20, 80))

    # Flip display
    pygame.display.flip()

# Quit Pygame when the game loop ends
pygame.quit()
