import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta Ukuran & Kecepatan
WIDTH, HEIGHT = 400, 460       # Tambahan 60px di atas untuk Header UI
HEADER_HEIGHT = 60
GRID_SIZE = 20
FPS = 10

# Palet Warna Modern
BG_COLOR_1 = (30, 39, 46)      # Abu-abu gelap (kotak grid 1)
BG_COLOR_2 = (38, 50, 56)      # Abu-abu agak terang (kotak grid 2)
HEADER_COLOR = (19, 25, 30)    # Warna panel atas
SNAKE_HEAD = (46, 213, 115)    # Hijau terang
SNAKE_BODY = (39, 174, 96)     # Hijau medium
APPLE_RED = (255, 71, 87)      # Merah cerah
APPLE_LEAF = (46, 213, 115)    # Hijau daun
TEXT_WHITE = (241, 242, 246)
GOLD_COLOR = (255, 165, 2)

# Setup Layar & Font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Snake Modern")
clock = pygame.time.Clock()

font_score = pygame.font.SysFont("segoeui", 24, bold=True)
font_title = pygame.font.SysFont("segoeui", 42, bold=True)
font_sub = pygame.font.SysFont("segoeui", 18)

# Variabel State Game
snake = [(200, 200 + HEADER_HEIGHT)]
snake_dir = (0, 0)
next_dir = (0, 0)
score = 0
high_score = 0
game_over = False
running = True

def spawn_food():
    while True:
        x = random.randrange(0, WIDTH, GRID_SIZE)
        y = random.randrange(HEADER_HEIGHT, HEIGHT, GRID_SIZE)
        if (x, y) not in snake:
            return pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

food = spawn_food()

def reset_game():
    global snake, snake_dir, next_dir, score, food, game_over
    snake = [(200, 200 + HEADER_HEIGHT)]
    snake_dir = (0, 0)
    next_dir = (0, 0)
    score = 0
    food = spawn_food()
    game_over = False

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(HEADER_HEIGHT, HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            if (x // GRID_SIZE + y // GRID_SIZE) % 2 == 0:
                pygame.draw.rect(screen, BG_COLOR_1, rect)
            else:
                pygame.draw.rect(screen, BG_COLOR_2, rect)

def draw_snake():
    for i, pos in enumerate(snake):
        rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
        if i == 0:
            # Gambar Kepala Ular
            pygame.draw.rect(screen, SNAKE_HEAD, rect, border_radius=6)
            
            # Tentukan posisi mata berdasarkan arah jalan
            dx, dy = snake_dir
            if dx == 0 and dy == 0:
                dx, dy = 20, 0  # Default menghadap kanan saat diam
            
            # Hitung offset mata
            if dx > 0:    # Kanan
                eyes = [(pos[0] + 14, pos[1] + 5), (pos[0] + 14, pos[1] + 15)]
            elif dx < 0:  # Kiri
                eyes = [(pos[0] + 6, pos[1] + 5), (pos[0] + 6, pos[1] + 15)]
            elif dy < 0:  # Atas
                eyes = [(pos[0] + 5, pos[1] + 6), (pos[0] + 15, pos[1] + 6)]
            else:         # Bawah
                eyes = [(pos[0] + 5, pos[1] + 14), (pos[0] + 15, pos[1] + 14)]
                
            for eye in eyes:
                pygame.draw.circle(screen, TEXT_WHITE, eye, 3)
                pygame.draw.circle(screen, (0, 0, 0), eye, 1.5)
        else:
            # Gambar Tubuh Ular (sedikit lebih kecil agar ada efek beruas)
            body_rect = rect.inflate(-2, -2)
            pygame.draw.rect(screen, SNAKE_BODY, body_rect, border_radius=4)

def draw_apple():
    center = (food.x + GRID_SIZE // 2, food.y + GRID_SIZE // 2 + 1)
    # Buah apel
    pygame.draw.circle(screen, APPLE_RED, center, GRID_SIZE // 2 - 2)
    # Highlight mengkilap
    pygame.draw.circle(screen, (255, 160, 160), (center[0] - 3, center[1] - 3), 2)
    # Daun apel
    leaf_rect = pygame.Rect(center[0] - 1, food.y + 1, 6, 4)
    pygame.draw.ellipse(screen, APPLE_LEAF, leaf_rect)

def draw_ui():
    # Background Header
    pygame.draw.rect(screen, HEADER_COLOR, (0, 0, WIDTH, HEADER_HEIGHT))
    pygame.draw.line(screen, (50, 65, 75), (0, HEADER_HEIGHT), (WIDTH, HEADER_HEIGHT), 2)
    
    # Render Skor & High Score
    score_surf = font_score.render(f"APEL: {score}", True, TEXT_WHITE)
    high_surf = font_score.render(f"BEST: {high_score}", True, GOLD_COLOR)
    
    screen.blit(score_surf, (20, 16))
    screen.blit(high_surf, (WIDTH - high_surf.get_width() - 20, 16))

def draw_game_over():
    # Overlay hitam transparan
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Teks Game Over
    title_surf = font_title.render("GAME OVER", True, APPLE_RED)
    sub_surf = font_sub.render("Tekan SPASI untuk main lagi", True, TEXT_WHITE)
    
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, HEIGHT // 2 + 15))

# Game Loop Utama
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()
            else:
                # Menggunakan next_dir untuk mencegah bug balik arah instan
                if event.key == pygame.K_UP and snake_dir != (0, GRID_SIZE):
                    next_dir = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -GRID_SIZE):
                    next_dir = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (GRID_SIZE, 0):
                    next_dir = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-GRID_SIZE, 0):
                    next_dir = (GRID_SIZE, 0)

    # Update Logika Game
    if not game_over:
        snake_dir = next_dir
        if snake_dir != (0, 0):
            head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
            snake.insert(0, head)

            # Cek makan apel
            if pygame.Rect(head, (GRID_SIZE, GRID_SIZE)).colliderect(food):
                score += 1
                if score > high_score:
                    high_score = score
                food = spawn_food()
            else:
                snake.pop()

            # Cek tabrakan dengan dinding atau badan sendiri
            if (head in snake[1:] or 
                head[0] < 0 or head[0] >= WIDTH or 
                head[1] < HEADER_HEIGHT or head[1] >= HEIGHT):
                game_over = True

    # Render Visual
    draw_grid()
    draw_apple()
    draw_snake()
    draw_ui()
    
    if game_over:
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()