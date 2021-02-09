import sys
import random

from heapq import heappop
from heapq import heappush

import json

import pygame

from settings import *


def terminate():
    sys.exit(pygame.quit())


def show_controls():
    showing_controls = True

    while showing_controls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing_controls = False

        screen.fill('black')

        screen.blit(background, background_rect)
        draw_text(screen, 'Управление', 40, WIDTH / 2, HEIGHT * 0.15, 'red')
        draw_text(screen, 'WASD, стрелки - движение', 20, WIDTH / 2, HEIGHT * 0.45, 'green')
        draw_text(screen, 'Пробел - стрелба', 20, WIDTH / 2, HEIGHT * 0.45 + 50, 'green')

        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    is_selected = {'play_button': False, 'controls_button': False}

    while True:
        screen.fill('black')
        screen.blit(background, background_rect)

        draw_text(screen, 'Space', 48, WIDTH / 2, HEIGHT * 0.15, 'green')
        mouse_pos = pygame.mouse.get_pos()

        play_button = pygame.Rect(
            int(WIDTH / 2) - 100,
            int(HEIGHT * 0.5) - 40, 200, 50)

        controls_button = pygame.Rect(
            int(WIDTH / 2) - 100,
            int(HEIGHT * 0.5) + 40, 200, 50)

        if is_selected['play_button']:
            pygame.draw.rect(screen, 'white', play_button)
            draw_text(screen, 'Играть', 20, int(WIDTH / 2), int(HEIGHT * 0.5 - 25), 'red')
        else:
            pygame.draw.rect(screen, 'red', play_button)
            draw_text(screen, 'Играть', 20, int(WIDTH / 2), int(HEIGHT * 0.5 - 25), 'white')

        if is_selected['controls_button']:
            pygame.draw.rect(screen, 'white', controls_button)
            draw_text(screen, 'Управление', 20, int(WIDTH / 2),
                      int(HEIGHT * 0.5 + 55), 'red')
        else:
            pygame.draw.rect(screen, 'red', controls_button)
            draw_text(
                screen, 'Управление', 20, int(WIDTH / 2), int(HEIGHT * 0.5 + 55), 'white')

        if play_button.collidepoint(mouse_pos):
            is_selected['play_button'] = True
            is_selected['controls_button'] = False
        elif controls_button.collidepoint(mouse_pos):
            is_selected['controls_button'] = True
            is_selected['play_button'] = False
        elif pygame.mouse.get_rel() != (0, 0):
            is_selected['controls_button'] = False
            is_selected['play_button'] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if is_selected['play_button']:
                    start_game()
                elif is_selected['controls_button']:
                    show_controls()

        pygame.display.flip()
        clock.tick(FPS)


def draw_text(surf, text, size, x, y, color='white', font_name=font_dir):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x), int(y))
    surf.blit(text_surface, text_rect)


def spawn_asteroid():
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids_sprites.add(asteroid)


def spawn_bullet(x, y):
    bullet = Bullet(x, y)
    all_sprites.add(bullet)
    bullets_sprites.add(bullet)


def draw_health_bar(surf, x, y, percentage):
    if percentage <= 0:
        percentage = 0

    bar_length = 100
    bar_height = 10

    filled = int(percentage / 100 * bar_length)
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    filled_rect = pygame.Rect(x, y, filled, bar_height)
    pygame.draw.rect(surf, 'green', filled_rect)
    pygame.draw.rect(surf, 'white', outline_rect, 2)


def draw_lives(surf, x, y, lives, image):
    for it in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 30 * it
        img_rect.y = y
        surf.blit(image, img_rect)


def start_game():
    pygame.mixer.music.play(loops=-1)

    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        spawn_asteroid()

    score = 0
    high_score_object = HighScore()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Проверка на попадение (коллизию) пуль и астероидов
        asteroids = pygame.sprite.groupcollide(asteroids_sprites, bullets_sprites, True, True)
        for asteroid in asteroids:
            asteroid: Asteroid

            score += int((70 - asteroid.radius) / 2)

            random.choice(explosion_sounds).play()

            explosion = Explosion(asteroid.rect.center, asteroid.rect.width * 0.9)
            all_sprites.add(explosion)

            if random.random() > 0.9:
                # Генерация power-up а
                power = Power(asteroid.rect.center)
                all_sprites.add(power)
                power_up_sprites.add(power)
            spawn_asteroid()

        # Проверка коллизии игрока и power-up ов
        power_ups = pygame.sprite.spritecollide(player, power_up_sprites, True)
        for power_up in power_ups:
            power_up: Power

            if power_up.type == 'pill':
                pill_power_sound.play()

                player.health = min(100, random.randrange(10, 30) + player.health)
            elif power_up.type == 'gun':
                gun_power_sound.play()
                player.gun_power()

            elif power_up.type == 'shield':
                player.shield_power()

        # проверка коллизии игрока и астероидов
        asteroids = pygame.sprite.spritecollide(player, asteroids_sprites, not player.just_started,
                                                pygame.sprite.collide_circle)

        for asteroid in asteroids:
            asteroid: Asteroid

            if not player.shield_up and not player.just_started:
                player.health -= asteroid.radius * 2

            if player.health <= 0:
                spawn_asteroid()
                player_explosion_sound.play()

                player.gun_pos_y = HEIGHT - 48
                death_explosion = Explosion(player.rect.center, max(asteroid.rect.width * 0.5, player.rect.width * 3))
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
            elif not player.just_started:
                spawn_asteroid()
                random.choice(explosion_sounds).play()

                explosion = Explosion(asteroid.rect.center, asteroid.rect.width * 0.5)
                all_sprites.add(explosion)

        if player.lives == 0 and not death_explosion.alive():
            for sprite in all_sprites:
                sprite.kill()

            running = False

        screen.fill('black')
        screen.blit(background, background_rect)

        all_sprites.draw(screen)

        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_text(screen, f'Рекорд: {high_score_object.high_score}', 12, WIDTH / 2, 30)

        draw_health_bar(screen, 5, 5, player.health)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_img_mini)

        all_sprites.update()

        pygame.display.flip()

        clock.tick(FPS)

    pygame.mixer.music.stop()

    # --- Game-over экран ---
    is_selected = {'exit_button': False}

    if score > high_score_object.high_score:
        # Обновление рекорда в JSON
        high_score_object.update_high_score(score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and is_selected['exit_button']:
                    terminate()

        screen.fill('black')

        draw_text(screen, 'GAME OVER', 48, WIDTH / 2, HEIGHT * 0.4)

        draw_text(screen, f'Очки: {score}', 27, WIDTH / 2, int(HEIGHT * 0.4) + 56, 'yellow')

        if score > high_score_object.high_score:
            draw_text(screen, 'Новый рекорд!', 30, WIDTH / 2, int(HEIGHT * 0.4) + 90, 'green')

        if is_selected['exit_button']:
            exit_button = pygame.draw.rect(
                screen, 'white', (WIDTH // 2 - 70, int(HEIGHT * 0.75), 140, 40))

            draw_text(screen, 'Выход', 30, WIDTH // 2, int(HEIGHT * 0.75), 'red')
        else:
            exit_button = pygame.draw.rect(screen, 'red', (WIDTH // 2 - 70, int(HEIGHT * 0.75), 140, 40))

            draw_text(screen, 'Выход', 30, WIDTH // 2, int(HEIGHT * 0.75), 'white')

        mouse_pos = pygame.mouse.get_pos()
        if exit_button.collidepoint(mouse_pos):
            is_selected['exit_button'] = True
        elif pygame.mouse.get_rel() != (0, 0):
            for button in is_selected:
                is_selected[button] = False

        pygame.display.flip()

        clock.tick(FPS)
    # --- Game-over экран ---


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = player_image
        self.rect = self.image.get_rect()
        self.radius = 20
        self.health = 100

        self.rect.centerx = int(WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.hidden_time = 2000
        self.gun_pos_y = HEIGHT - 48
        self.gun = 1
        self.gun_power_time_heap = []
        self.power_timer = 7000
        self.shield_up = False
        self.shield_up_time = pygame.time.get_ticks()
        self.invulnerability = 2000
        self.start_time = pygame.time.get_ticks()
        self.just_started = True
        self.flicker = 0

    def update(self):
        # Неуязвимость
        if self.just_started:
            if (self.flicker // 4) % 2 == 0:
                self.rect.centery = HEIGHT + 200
            else:
                self.rect.bottom = HEIGHT - 10

            self.flicker += 1

        if self.just_started and pygame.time.get_ticks() - self.start_time > self.invulnerability:
            self.just_started = False
            self.flicker = 0
            self.rect.bottom = HEIGHT - 10

        # Скрытый
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > self.hidden_time:
            self.hidden = False
            self.health = 100
            self.rect.centerx = int(WIDTH / 2)
            self.rect.bottom = HEIGHT - 10
            self.start_time = pygame.time.get_ticks()
            self.just_started = True
            self.flicker = 0

        if len(self.gun_power_time_heap) > 0:
            if pygame.time.get_ticks() - self.gun_power_time_heap[0] > self.power_timer:
                self.gun = max(1, self.gun - 1)
                heappop(self.gun_power_time_heap)

        if pygame.time.get_ticks() - self.shield_up_time > self.power_timer and self.shield_up:
            self.image = player_image  # Возвращение обычной картинки
            old_rect = player_image.get_rect()
            old_rect.center = self.rect.center
            self.rect = old_rect
            self.radius = 20
            self.shield_up = False
            shield_down_sound.play()

        # --- Управление ---
        self.speedx = 0
        self.speedy = 0

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.speedx = -MOVEMENT_DELTA
        elif key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.speedx = MOVEMENT_DELTA
        elif key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.speedy = -MOVEMENT_DELTA
        elif key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            self.speedy = MOVEMENT_DELTA

        self.rect.x += self.speedx

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

        if not self.hidden and not self.just_started:
            self.rect.y += self.speedy

            self.rect.top = max(0, self.rect.top)
            self.rect.bottom = min(HEIGHT - 10, self.rect.bottom)

            self.gun_pos_y = self.rect.top

        elif not self.hidden:
            self.rect.y += self.speedy
        # --- Управление ---

    def shoot(self):
        if not self.hidden:
            if self.gun % 2 != 0:
                spawn_bullet(self.rect.centerx, self.gun_pos_y)
                shoot_sound.play()

                for it in range(1, int((self.gun - 1) / 2) + 1):
                    spawn_bullet(self.rect.centerx + it * 15, self.gun_pos_y)
                    spawn_bullet(self.rect.centerx - it * 15, self.gun_pos_y)
            else:
                for it in range(1, int((self.gun / 2) + 1)):
                    spawn_bullet(self.rect.centerx + it * 15 - 7, self.gun_pos_y)
                    spawn_bullet(self.rect.centerx - it * 15 + 7, self.gun_pos_y)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (int(WIDTH / 2), HEIGHT + 200)

    def gun_power(self):
        self.gun += 1
        heappush(self.gun_power_time_heap, pygame.time.get_ticks())

    def shield_power(self):
        self.shield_up = True
        shield_up_sound.play()

        self.shield_up_time = pygame.time.get_ticks()

        new_rect = shielded_player_img.get_rect()
        new_rect.center = self.rect.center

        self.image = shielded_player_img  # Новая картинка
        self.rect = new_rect
        self.radius = int(new_rect.width / 2.1)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.42)

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -75)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > WIDTH + 3:
            self.speedx = -self.speedx
        if self.rect.left < 0 - 3:
            self.speedx = -self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -16

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(list(power_up_images.keys()))
        self.image = power_up_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()

        self.size = int(size)
        self.anim = []
        for explosion_image in explosion_animation:
            explosion_img_resized = pygame.transform.scale(explosion_image, (self.size, self.size))
            self.anim.append(explosion_img_resized)

        self.frame = 0
        self.image = self.anim[self.frame]

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 40

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.frame += 1
            if self.frame == len(self.anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.anim[self.frame]
                self.rect.center = center


class HighScore:
    # Ключ для JSON файла
    _high_score_key = 'high_score'

    def __init__(self):
        self.high_score = self.get_high_score_from_file()

    def get_high_score_from_file(self):
        """Получение рекорда из JSON файла"""
        try:
            with open(data_file, 'r', encoding='UTF-8') as f:
                data = json.load(f)
                return data[self._high_score_key]
        except FileNotFoundError:
            return 0

    def update_high_score(self, value):
        """Обновление рекорда в JSON файле"""
        try:
            with open(data_file) as f:
                data = json.load(f)

        except FileNotFoundError:
            data = dict()

        data[self._high_score_key] = value

        with open(data_file, 'w', encoding='UTF-8') as f:
            json.dump(data, f)


if __name__ == '__main__':
    # --- Инициализация Pygame  ---
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Space')
    clock = pygame.time.Clock()
    # --- Инициализация Pygame  ---

    # --- Загрузка всей графики ---
    background = pygame.image.load(f'{image_dir}/background.png')
    background_rect = background.get_rect()

    player_image = pygame.image.load(f'{image_dir}/ship.png')
    player_image = pygame.transform.scale(player_image, (50, 38))

    player_img_mini = pygame.transform.scale(player_image, (25, 19))

    bullet_img = pygame.image.load(f'{image_dir}/laser.png')

    meteor_images = []
    meteor_list = [
        'meteor_med1.png',
        'meteor_med3.png',
        'meteor_tiny1.png',
        'meteor_tiny2.png',
        'meteor_big1.png',
        'meteor_big2.png',
        'meteor_big3.png',
        'meteor_big4.png'
    ]

    for meteor in meteor_list:
        meteor_images.append(pygame.image.load(f'{image_dir}/{meteor}'))

    explosion_animation = []
    player_explosion_animation = []
    for i in range(9):
        explosion_animation.append(pygame.image.load(f'{image_dir}/regular_explosion0{i}.png'))

        player_explosion_animation.append(pygame.image.load(f'{image_dir}/sonic_explosion0{i}.png'))

    power_up_images = {
        'shield':
            pygame.image.load(f'{image_dir}/shield_silver.png'),
        'gun':
            pygame.image.load(f'{image_dir}/bolt_gold.png'),
        'pill':
            pygame.image.load(f'{image_dir}/pill.png'),
    }

    shielded_player_img = pygame.image.load(f'{image_dir}/shielded_player.png')
    # --- Загрузка всей графики ---

    # --- Загрузка всех звуков  ---
    if pygame.mixer.get_init():
        shoot_sound = pygame.mixer.Sound(f'{sound_dir}/laser_shoot.wav')

        explosion_sounds = [
            pygame.mixer.Sound(f'{sound_dir}/{explosion}') for explosion in ('explosion1.wav', 'explosion2.wav')
        ]

        for sound in explosion_sounds:
            sound.set_volume(0.2)

        player_explosion_sound = pygame.mixer.Sound(f'{sound_dir}/rumble.ogg')
        player_explosion_sound.set_volume(0.2)

        gun_power_sound = pygame.mixer.Sound(f'{sound_dir}/gun_sound.wav')
        gun_power_sound.set_volume(0.2)

        pill_power_sound = pygame.mixer.Sound(f'{sound_dir}/pill_sound.wav')
        pill_power_sound.set_volume(0.2)

        lose_sound = pygame.mixer.Sound(f'{sound_dir}/lose.ogg')
        lose_sound.set_volume(0.2)

        shield_up_sound = pygame.mixer.Sound(f'{sound_dir}/shield_up.ogg')
        shield_up_sound.set_volume(0.2)

        shield_down_sound = pygame.mixer.Sound(f'{sound_dir}/shield_down.ogg')
        shield_down_sound.set_volume(0.2)

        pygame.mixer.music.load(f'{sound_dir}/theme.ogg')
        pygame.mixer.music.set_volume(0.2)
    # --- Загрузка всех звуков  ---

    # --- Создание sprite-групп ---
    all_sprites = pygame.sprite.Group()
    asteroids_sprites = pygame.sprite.Group()
    bullets_sprites = pygame.sprite.Group()
    power_up_sprites = pygame.sprite.Group()
    # --- Создание sprite-групп ---

    start_screen()
