import pygame
#import pygame_menu
import random

WIDTH = 500
HEIGHT = 500
FPS = 60
fallen = 0
max_level = 1
win = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Алхимик")
clock = pygame.time.Clock()
bg = pygame.image.load('bg.jpg')

images_path = 'images/'
walkRight, walkLeft = [], []
for i in range(1, 7):
    walkRight.append(pygame.image.load(images_path + 'pygame_right_' + str(i) + '.png'))
    walkLeft.append(pygame.image.load(images_path + 'pygame_left_' + str(i) + '.png'))
playerStand = pygame.image.load((images_path + 'pygame_idle.png'))
heartImg = pygame.image.load((images_path + 'heart.png'))

img_true_1 = {}
img_true_2 = {}
img_false_1 = {}
img_false_2 = {}
for number in range(7):
    img_true_1[number] = pygame.image.load(images_path + '1_level/1' + str(number+1) + '.png')
    img_true_2[number] = pygame.image.load(images_path + '2_level/1' + str(number+1) + '.png')
    img_false_1[number] = pygame.image.load(images_path + '1_level/2' + str(number+1) + '.png')
    img_false_2[number] = pygame.image.load(images_path + '2_level/2' + str(number+1) + '.png')


def drawHearts(n):
    for i in range(n):
        screen.blit(heartImg, (HEIGHT - 20 * (i + 1), 4))

font_name = pygame.font.match_font('arial')

def draw_text(surf, score, size=20, x=5, y=5):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render('Счет: ' + str(score), True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerStand, (60, 71))
        self.rect = self.image.get_rect()
        self.rect.topleft = 50, 420
        #self.image.blit(playerStand, self.rect.topleft)
        self.isJump = False
        self.jumpCount = 10
        self.animCount = 0
        self.left = False
        self.right = False
        self.speedx = 0
        self.life = 3
        self.memory = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if self.animCount + 1 >= 30:
            self.animCount = 0

        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            self.left = True
            self.right = False
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 8
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False
        if not self.isJump:
            if keystate[pygame.K_UP]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) / 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) / 2
                self.jumpCount -= 1
            else:
                self.rect.y += 5
                self.isJump = False
                self.jumpCount = 10

        self.rect.x += self.speedx
        if self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH - 5
        if self.rect.left < 5:
            self.rect.left = 5

        if self.left:
            self.image = pygame.transform.scale(walkLeft[self.animCount // 5], (60, 71))
            self.animCount += 1
        elif self.right:
            self.image = pygame.transform.scale(walkRight[self.animCount // 5], (60, 71))
            self.animCount += 1
        else:
            self.image = pygame.transform.scale(playerStand, (60, 71))

class Word(pygame.sprite.Sprite):
    def __init__(self, lev, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.memory = random.randint(0,6)
        if lev == 1:
            if type == 1:
                self.image = img_true_1[self.memory]
            elif type == 0:
                self.image = img_false_1[self.memory]
        elif lev == 2:
            if type == 1:
                self.image = img_true_2[self.memory]
            elif type == 0:
                self.image = img_false_2[self.memory]

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 3)
        #self.speedx = random.randrange(-3, 3)

    def update(self):
        global fallen
        #self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)
            if self.type == 1:
                fallen += 1


def show_menu():    #показать меню
    menu_fon = pygame.image.load('bg.jpg')
    global max_level

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
        screen.blit(menu_fon, (0,0))
        pygame.draw.rect(screen, (13, 162, 58), (190, 200, 130, 40))  # отрисовка кнопки
        if max_level == 1:
            pygame.draw.rect(screen, (128, 128, 128), (190, 250, 130, 40))  # отрисовка кнопки
            font = pygame.font.Font(None, 20)
            text = font.render('не доступен', True, (0, 0, 0))
            screen.blit(text, (214, 278))
        else:
            pygame.draw.rect(screen, (13, 162, 58), (190, 250, 130, 40))  # отрисовка кнопки
        pygame.draw.rect(screen, (13, 162, 58), (190, 300, 130, 40))  # отрисовка кнопки
        font = pygame.font.Font(None, 30)
        text = font.render('Уровень 1', True, (0, 0, 0))
        screen.blit(text, (200, 210))
        text = font.render('Уровень 2', True, (0, 0, 0))
        screen.blit(text, (200, 260))
        text = font.render('Выход', True, (0, 0, 0))
        screen.blit(text, (215, 310))
        pygame.display.update()
        clock.tick(60)

        mouse = pygame.mouse.get_pos()  # координаты мыши
        click = pygame.mouse.get_pressed()  # было ли нажатие мышью
        if (190 < mouse[0] < 190+130) and (200 < mouse[1] < 200+40) and (click[0]==1):  # при нажатии мыши на кнопку
            start_game_1()
        elif (190 < mouse[0] < 190+130) and (250 < mouse[1] < 250+40) and (click[0]==1):  # при нажатии мыши на кнопку
            if max_level == 2:
                start_game_2()
        elif (190 < mouse[0] < 190+130) and (300 < mouse[1] < 300+40) and (click[0]==1):  # при нажатии мыши на кнопку
            exit()


def game_over():
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:   #если нажмем крестик
                exit()
        font = pygame.font.Font(None, 20)
        global win, max_level
        if win == True:
            text = font.render('Вы выиграли!', True, (0, 0, 0))
            screen.blit(text, (210, 200))
            if max_level == 1:
                max_level = 2
        else:
            text = font.render('Вы проиграли...', True, (0, 0, 0))
            screen.blit(text, (210, 200))
        text = font.render('Нажмите ENTER чтобы начать заново или ESC чтобы выйти', True, (0, 0, 0))
        screen.blit(text, (60, 250))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]: # ENTER
            return True
        if keys[pygame.K_ESCAPE]:   # ESC
            return False
        pygame.display.update()
        clock.tick(60)

def start_game_1():
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:   #если нажмем крестик
                exit()
        menu_fon = pygame.image.load('bg.jpg')
        screen.blit(menu_fon, (0, 0))
        font = pygame.font.Font(None, 20)
        text = font.render('Металлы. Часть 1.', True, (0, 0, 0))
        screen.blit(text, (190, 200))
        text = font.render('Необходимо собрать 15 металлов за 40 секунд.', True, (0, 0, 0))
        screen.blit(text, (100, 240))
        pygame.draw.rect(screen, (13, 162, 58), (190, 300, 130, 40))  # отрисовка кнопки
        text = font.render('Далее', True, (0, 0, 0))
        screen.blit(text, (235, 310))
        pygame.display.update()
        clock.tick(60)
        mouse = pygame.mouse.get_pos()  # координаты мыши
        click = pygame.mouse.get_pressed()  # было ли нажатие мышью
        if (190 < mouse[0] < 190 + 130) and (300 < mouse[1] < 300 + 40) and (click[0] == 1):  # при нажатии мыши на кнопку
            while game_1() == True:
                pass
            else:
                break

def game_1():
    global fallen
    global win
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    words = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(2):
        w = Word(1, 1)
        all_sprites.add(w)
        words.add(w)
    for i in range(2):
        m = Word(1, 0)
        all_sprites.add(m)
        mobs.add(m)

    running = True
    time = 0
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        time += 1
        font = pygame.font.Font(None, 20)
        text = font.render('Время: '+str(40 - round(time/60)), True, (0, 0, 0))
        screen.blit(text, (5, 50))
        if time == 40*60:
            running = False

        all_sprites.update()
        if fallen > 0:
            player.life -= fallen
            fallen = 0
            if player.life <= 0:
                running = False
        hits = pygame.sprite.spritecollide(player, mobs, True)
        for hit in hits:
            player.life -= 1
            print(player.life)
            if player.life <= 0:
                running = False
            m = Word(1,0)
            all_sprites.add(m)
            mobs.add(m)

        hits = pygame.sprite.spritecollide(player, words, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.memory += 1  #hit.memory
            if player.memory >= 15:
                win = True
            else:
                win = False
            if player.life <= 0:
                running = False
            w = Word(1,1)
            all_sprites.add(w)
            words.add(w)

        all_sprites.draw(screen)
        pygame.display.flip()
        screen.blit(bg, (0, 0))
        drawHearts(player.life)
        draw_text(screen, player.memory)

    return game_over()  # выбор: выйти или перезапустить


def start_game_2():
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:   #если нажмем крестик
                exit()
        menu_fon = pygame.image.load('bg.jpg')
        screen.blit(menu_fon, (0, 0))
        font = pygame.font.Font(None, 20)
        text = font.render('Металлы. Часть 2.', True, (0, 0, 0))
        screen.blit(text, (190, 200))
        text = font.render('Необходимо собрать 15 металлов за 40 секунд.', True, (0, 0, 0))
        screen.blit(text, (100, 240))
        pygame.draw.rect(screen, (13, 162, 58), (190, 300, 130, 40))  # отрисовка кнопки
        text = font.render('Далее', True, (0, 0, 0))
        screen.blit(text, (235, 310))
        pygame.display.update()
        clock.tick(60)
        mouse = pygame.mouse.get_pos()  # координаты мыши
        click = pygame.mouse.get_pressed()  # было ли нажатие мышью
        if (190 < mouse[0] < 190 + 130) and (300 < mouse[1] < 300 + 40) and (click[0] == 1):  # при нажатии мыши на кнопку
            while game_2() == True:
                pass
            else:
                break

def game_2():
    global fallen
    global win
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    words = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(2):
        w = Word(2, 1)
        all_sprites.add(w)
        words.add(w)
    for i in range(2):
        m = Word(2, 0)
        all_sprites.add(m)
        mobs.add(m)

    running = True
    time = 0
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        time += 1
        font = pygame.font.Font(None, 20)
        text = font.render('Время: '+str(40 - round(time/60)), True, (0, 0, 0))
        screen.blit(text, (5, 50))
        if time == 40*60:
            running = False

        all_sprites.update()
        if fallen > 0:
            player.life -= fallen
            fallen = 0
            if player.life <= 0:
                running = False
        hits = pygame.sprite.spritecollide(player, mobs, True)
        for hit in hits:
            player.life -= 1
            if player.life <= 0:
                running = False
            m = Word(2,0)
            all_sprites.add(m)
            mobs.add(m)

        hits = pygame.sprite.spritecollide(player, words, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.memory += 1  #hit.memory
            if player.memory >= 15:
                win = True
            else:
                win = False
            if player.life <= 0:
                running = False
            w = Word(2,1)
            all_sprites.add(w)
            words.add(w)

        all_sprites.draw(screen)
        pygame.display.flip()
        screen.blit(bg, (0, 0))
        drawHearts(player.life)
        draw_text(screen, player.memory)

    return game_over()  # выбор: выйти или перезапустить


show_menu()
exit()