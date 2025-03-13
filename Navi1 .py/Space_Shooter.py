import pygame
import random
import webbrowser

pygame.init()

# Definición de la pantalla
width, height = 1366, 768
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Space Shooter")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)

# Inicialización de variables de puntuación y vidas
score = 0
lives = 5
paused = False

# Cargar imágenes
background_image = pygame.image.load('images/bckg.jpg').convert()
background_image = pygame.transform.scale(background_image, (width, height))
player_images = [
    pygame.image.load('images/plyerN.png').convert_alpha(),
    pygame.image.load('images/newN.png').convert_alpha(),
    pygame.image.load('images/Nave1.png').convert_alpha(),
    pygame.image.load('images/NaveR.png').convert_alpha()
]
enemy_images = [
    pygame.image.load('images/Navee.png').convert_alpha(),
    pygame.image.load('images/NaveP3.png').convert_alpha(),
]
bullet_image = pygame.image.load('images/Proyectil.png').convert_alpha()
enemy_bullet_image = pygame.image.load('images/DisparoE.png').convert_alpha()
explosion_image = pygame.image.load('images/explosion.png').convert_alpha()
game_over_image = pygame.image.load('images/gameover.png').convert()
game_over_image = pygame.transform.scale(game_over_image, (width, height))
cover_image = pygame.image.load('images/NaveeP.jpg').convert()
cover_image = pygame.transform.scale(cover_image, (width, height))

# Cargar imagen negra con baja opacidad
black_overlay = pygame.image.load('images/negro.jpg').convert_alpha()
black_overlay = pygame.transform.scale(black_overlay, (width, height))
black_overlay.set_alpha(150)  # Ajusta la opacidad (0-255)

# Cargar música y efectos de sonido
pygame.mixer.music.load('sounds/backgroundmusic2.mp3')
pygame.mixer.music.set_volume(0.5)
shoot_sound = pygame.mixer.Sound('sounds/disparo.mp3')
enemy_shoot_sound = pygame.mixer.Sound('sounds/D.mp3')
explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')

# Función para configurar la fuente del título
def set_title_font(font_path, size):
    return pygame.font.Font(font_path, size)

# Función para configurar la fuente del juego
def set_game_font(font_path, size):
    return pygame.font.Font(font_path, size)

# Función para configurar la fuente del Game Over
def set_game_over_font(font_path, size):
    return pygame.font.Font(font_path, size)

# Definición de la fuente y tamaño para la puntuación y vidas
font_path = 'todooo/Xirod.otf'  
title_font_path = 'titulo/Bruce.ttf'  
game_over_font_path = 'todooo/Xirod.otf' 
font = set_game_font(font_path, 16)
title_font = set_title_font(title_font_path, 66)
game_over_font = set_game_over_font(game_over_font_path, 22)

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.y += 5

# Clase de los disparos
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        shoot_sound.play()

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

# Clase de los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-150, -50)

    def update(self):
        self.rect.y += 5
        if self.rect.top > height:
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(-150, -50)

# Clase de los disparos enemigos
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        enemy_shoot_sound.play()

    def update(self):
        self.rect.y += 10
        if self.rect.top > height:
            self.kill()

# Clase de la explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = explosion_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 30 
        explosion_sound.play()

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

# Función para mostrar la pantalla de Game Over
def game_over():
    global score, lives
    message = game_over_font.render(f"Game Over! Score: {score}", True, RED)
    restart_button = game_over_font.render("Presiona (R) para Reiniciar o (M) para Menú", True, WHITE)
   
    screen.fill(BLACK)
    screen.blit(game_over_image, (0, 0))
    screen.blit(message, (width // 2 - message.get_rect().width // 2, height // 3))
    screen.blit(restart_button, (width // 2 - restart_button.get_rect().width // 2, height // 2))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    score = 0
                    lives = 5
                    run_game()  
                    return
                elif event.key == pygame.K_m: 
                    show_start_screen()
                    return

# Función para pausar el juego y mostrar el menú de pausa
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pygame.time.set_timer(pygame.USEREVENT, 0) 
        show_pause_menu()
    else:
        pygame.time.set_timer(pygame.USEREVENT, 1000)  

# Función para mostrar la pantalla de inicio
def show_start_screen():
    global score, lives, paused, selected_player_image
    score = 0
    lives = 5
    paused = False
    pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    title = title_font.render("SPACE SHOOTER", True, RED)
    start_button = font.render("Iniciar (1)", True, WHITE)
    score_button = font.render("Puntuacion (2)", True, WHITE)
    change_ship_button = font.render("Cambiar Nave (C)", True, WHITE)
    quit_button = font.render("Salir (Q)", True, WHITE)

    screen.blit(cover_image, (0, 0))
    screen.blit(black_overlay, (0, 0))

    # Centrando el título
    title_rect = title.get_rect(center=(width // 2, height // 6))
    screen.blit(title, title_rect)

    screen.blit(start_button, (width // 2.5, height // 2.5))
    screen.blit(score_button, (width // 2.5, height // 2.5 + 50))
    screen.blit(change_ship_button, (width // 2.5, height // 2.5 + 100))
    screen.blit(quit_button, (width // 2.5, height // 2.5 + 150))

    # Botón para ir al repositorio de GitHub
    github_button = font.render("D3LV®", True, RED)
    github_rect = github_button.get_rect(topleft=(10, 10))
    screen.blit(github_button, github_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  
                    pygame.mixer.music.stop()
                    run_game()
                    return
                elif event.key == pygame.K_2:  
                    show_score_screen()
                elif event.key == pygame.K_c:  
                    show_change_ship_screen()
                elif event.key == pygame.K_q:  
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if github_rect.collidepoint(event.pos):
                    webbrowser.open("https://github.com/D3lV/D3LV.py")

# Función para mostrar la pantalla de puntuación
def show_score_screen():
    screen.fill(BLACK)
    title = title_font.render("Puntuaciones", True, RED)
    back_button = font.render("Volver (B)", True, WHITE)

    screen.blit(background_image, (0, 0))
    screen.blit(title, (width // 4, height // 6))
    screen.blit(back_button, (width // 2.5, height // 2.5 + 200))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: 
                    waiting_for_input = False
                    show_start_screen()
                    return

# Función para mostrar la pantalla de selección de nave
def show_change_ship_screen():
    global selected_player_image
    screen.fill(BLACK)
    title_font = pygame.font.Font(title_font_path, 70)
    title = title_font.render("Selecciona tu Nave", True, RED)
    confirm_button = font.render("Confirmar (Enter)", True, WHITE)
    back_button = font.render("Volver (B)", True, WHITE)

    new_background_image = pygame.image.load('images/bckg.jpg').convert()
    new_background_image = pygame.transform.scale(new_background_image, (width, height))
    screen.blit(new_background_image, (0, 0))
    screen.blit(black_overlay, (0, 0))  

    # Centrando el título
    title_rect = title.get_rect(center=(width // 2, height // 6))
    screen.blit(title, title_rect)

    # Ajustando los botones de confirmación y volver
    screen.blit(confirm_button, (width // 2.5, height // 1.5))
    screen.blit(back_button, (width // 2.5, height // 1.5 + 50))

    # Mostrar la nave seleccionada
    screen.blit(player_images[selected_player_image], (width // 2 - player_images[selected_player_image].get_width() // 2, height // 3))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    waiting_for_input = False
                    show_start_screen()
                    return
                elif event.key == pygame.K_b:  
                    waiting_for_input = False
                    show_start_screen()
                    return
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  
                    selected_player_image = (selected_player_image + 1) % len(player_images)
                    screen.fill(BLACK)
                    screen.blit(new_background_image, (0, 0))
                    screen.blit(black_overlay, (0, 0)) 
                    screen.blit(title, title_rect)
                    screen.blit(confirm_button, (width // 2.5, height // 1.5))
                    screen.blit(back_button, (width // 2.5, height // 1.5 + 50))
                    screen.blit(player_images[selected_player_image], (width // 2 - player_images[selected_player_image].get_width() // 2, height // 3))
                    pygame.display.flip()

# Función para mostrar el menú de pausa
def show_pause_menu():
    screen.fill(BLACK)
    pause_text = title_font.render("Pausa", True, RED)
    resume_button = font.render("Reanudar (ESC)", True, WHITE)
    restart_button = font.render("Reiniciar (R)", True, WHITE)
    quit_button = font.render("Salir (M)", True, WHITE)

    screen.blit(background_image, (0, 0))
    screen.blit(pause_text, (width // 3, height // 6))
    screen.blit(resume_button, (width // 2.5, height // 2.5))
    screen.blit(restart_button, (width // 2.5, height // 2.5 + 50))
    screen.blit(quit_button, (width // 2.5, height // 2.5 + 100))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    toggle_pause()
                    waiting_for_input = False
                elif event.key == pygame.K_r:  
                    score = 0
                    lives = 5
                    run_game()
                    return
                elif event.key == pygame.K_m:  
                    show_start_screen()
                    return

# Función principal
def run_game():
    global score, lives, paused
    clock = pygame.time.Clock()

    # Reiniciar variables
    score = 0
    lives = 5
    paused = False

    # Crear jugador
    player = Player(player_images[selected_player_image])
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Crear grupos de enemigos, disparos y disparos enemigos
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    # Spawnear enemigos
    enemy_spawn_time = 1000  
    pygame.time.set_timer(pygame.USEREVENT, enemy_spawn_time)

    # Loop principal
    running = True
    while running:
        clock.tick(60)  # FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if event.key == pygame.K_p:
                    toggle_pause()
                if event.key == pygame.K_ESCAPE:
                    toggle_pause()

            if event.type == pygame.USEREVENT and not paused:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        if not paused:
            # Actualizar todos los sprites
            all_sprites.update()

            # Detectar colisiones entre balas y enemigos
            hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
            for hit in hits:
                explosion = Explosion(hit.rect.centerx, hit.rect.centery)
                all_sprites.add(explosion)
                explosions.add(explosion)
                score += 10  

            # Detectar disparos enemigos
            for enemy in enemies:
                if random.random() < 0.01:  
                    enemy_bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
                    all_sprites.add(enemy_bullet)
                    enemy_bullets.add(enemy_bullet)

            # Detectar colisiones entre disparos enemigos y jugador
            enemy_hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_mask)
            for hit in enemy_hits:
                lives -= 1
                hit.kill()  
                if lives <= 0:
                    if not game_over():
                        running = False

            # Detectar colisiones entre jugador y enemigos
            player_hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
            for hit in player_hits:
                lives -= 1
                if lives <= 0:
                    if not game_over():
                        running = False

        # Dibujar todo
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # Mostrar puntuación y vidas
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (width - 100, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    selected_player_image = 0
    show_start_screen()
    run_game()