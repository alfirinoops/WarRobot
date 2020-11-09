import pygame
import random
import math
import time

pygame.init()

display_width = 800
display_height = 800

mainDisplay = pygame.display.set_mode((display_width + 75, display_height))
gameDisplay = pygame.Surface((display_height, display_width))
pygame.display.set_caption('WarRobot')

health = pygame.image.load("health.png")
nuke = pygame.image.load("nuke.png")
dead = pygame.image.load("dead.png")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255,255,0)
blue = (0, 0, 255)
shit_color = (100, 0, 0)

clock = pygame.time.Clock()
running = True
fire = False

f = pygame.font.Font(None, 36)


class Player():
    def __init__(self, x, y, radius, color, health):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.health = health
        self.nuke = 740
    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), self.radius)
        mainDisplay.blit(health, (815, 770))
        pygame.draw.rect(mainDisplay, (255, 0, 0), (811, 750 - self.health, 26, self.health))
        mainDisplay.blit(nuke, (840, 770))
        pygame.draw.rect(mainDisplay, (0, 0, 255), (840, 750 - self.nuke, 26, self.nuke))

class Enemy():
    def __init__(self, x, y, radius, color, health):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.health = health
        self.lifetime = 900
    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), self.radius)

class Shits():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.health = 25
    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), self.radius)

class Bullet():
    def __init__(self, start_x, start_y, vel_x, vel_y):
        self.x = start_x
        self.y = start_y
        self.vel_x = vel_x
        self.vel_y = vel_y
    def draw(self):
        pygame.draw.circle(gameDisplay, yellow, (self.x, self.y), 3)
    def move(self):
        self.x += 5 * self.vel_x
        self.y += 5 * self.vel_y

class Effects():
    def __init__(self, start_x, start_y, color):
        self.color = color
        self.x = start_x
        self.y = start_y
        self.vel_x = random.randint(-12,12)
        self.vel_y = random.randint(-12,12)
    def move(self):
        if self.vel_x == 0:
            self.vel_x += 1
        if self.vel_y == 0:
            self.vel_y += 1
        self.x += self.vel_x
        self.y += self.vel_y
    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), 3)

def spawn_enemy():
    list = []
    for i in range(100):
        list.append(i - 100)
    for i in range(100):
        list.append(i + 800)
    x = list[random.randint(0,199)]
    y = list[random.randint(0,199)]
    can_spawn = True
    for enemy in enemy_list:
        s = math.sqrt((enemy.x - x) ** 2 + (enemy.y - y) ** 2)
        if s < 25:
            can_spawn = False
    if can_spawn:
        enemy_list.append(Enemy(x, y, 20, red, 100))


def shit_move():
    for shit in shits:
        cos = (shit.x - player.x) / math.sqrt((shit.x - player.x) ** 2 + (shit.y - player.y) ** 2)

        move_x = 1 * cos

        move_y = math.sqrt(1 - (move_x) ** 2)

        if player.x > shit.x:
            move_x = abs(move_x)
        else:
            move_x = 0 - abs(move_x)

        if player.y > shit.y:
            move_y = abs(move_y)
        else:
            move_y = 0 - abs(move_y)

        shit.x += move_x * 2
        shit.y += move_y * 2

        s = math.sqrt((player.x - shit.x) ** 2 + (player.y - shit.y) ** 2)
        if s != 0:
            if s < 40:
                shits.remove(shit)
                player.health -= 5


def enemy_move():
    for enemy in enemy_list:
        old_x = enemy.x
        old_y = enemy.y
        cos = (enemy.x - player.x) / math.sqrt((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2)

        move_x = 1 * cos

        move_y = math.sqrt(1 - (move_x) ** 2)

        if player.x > enemy.x:
            move_x = abs(move_x)
        else:
            move_x = 0 - abs(move_x)

        if player.y > enemy.y:
            move_y = abs(move_y)
        else:
            move_y = 0 - abs(move_y)

        enemy.x += move_x
        enemy.y += move_y

        for other_enemy in enemy_list:
            s = math.sqrt((other_enemy.x - enemy.x) ** 2 + (other_enemy.y - enemy.y) ** 2)
            if s != 0:
                if s < 20:
                    enemy.x = old_x
                    enemy.y = old_y

        s = math.sqrt((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2)
        if s != 0:
            if s < 50:
                enemy.x = old_x
                enemy.y = old_y
                player.health -= 1
        enemy.lifetime -= 1
        if enemy.lifetime < 0:
            shits.append(Shits(enemy.x, enemy.y, 10, shit_color))
            enemy_list.remove(enemy)



x_change = 0
y_change = 0
player = Player(display_width/2, display_height/2, 30, white, 740)
timer = 0
enemy_list = []
bullets = []
effects = []
shits = []
killed = 0
enemy_list.append(Enemy(-1000, -1000, 20, red, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                fire = True
            if event.button == 3:
                if player.nuke >= 740:
                    player.nuke = 0
                    for enemy in enemy_list:
                        s = math.sqrt((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2)
                        if s < 200:
                            enemy.health -= 80

                        if enemy.health < 0:
                            for i in range(60):
                                effects.append(Effects(bullet.x, bullet.y, red))
                            try:
                                enemy_list.remove(enemy)
                                killed += 1
                            except:
                                pass
                    for shit in shits:
                        s = math.sqrt((shit.x - player.x) ** 2 + (shit.y - player.y) ** 2)
                        if s < 200:
                            shit.health -= 80

                        if shit.health < 0:
                            for i in range(60):
                                effects.append(Effects(bullet.x, bullet.y, shit_color))
                            try:
                                shits.remove(shit)
                                killed += 1
                            except:
                                pass
                    for i in range(200):
                        effects.append(Effects(player.x, player.y, blue))

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                fire = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_change += -5
            if event.key == pygame.K_d:
                x_change += 5
            if event.key == pygame.K_w:
                y_change += -5
            if event.key == pygame.K_s:
                y_change += 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change += 5
            if event.key == pygame.K_d:
                x_change += -5
            if event.key == pygame.K_w:
                y_change += 5
            if event.key == pygame.K_s:
                y_change += -5

    player.x += x_change
    if player.x > 800:
        player.x = 799
    if player.x < 0:
        player.x = 1
    if player.y > 800:
        player.y = 799
    if player.y < 0:
        player.y = 1
    player.y += y_change



    timer += 1
    if timer == 10:
        spawn_enemy()
        timer = 0
        if player.health < 740:
            player.health += 1
        if player.nuke < 740:
            player.nuke += 6
    if timer == 5 and fire:
        pos = pygame.mouse.get_pos()
        cos = (player.x - pos[0]) / math.sqrt((player.x - pos[0]) ** 2 + (player.y - pos[1]) ** 2)

        move_x = 1 * cos
        move_y = math.sqrt(1 - (move_x) ** 2)

        if pos[0] > player.x:
            move_x = abs(move_x)
        else:
            move_x = 0 - abs(move_x)

        if pos[1] > player.y:
            move_y = abs(move_y)
        else:
            move_y = 0 - abs(move_y)

        bullets.append(Bullet(player.x, player.y, move_x, move_y))



    enemy_move()
    shit_move()
    for bullet in bullets:
        bullet.move()
        if bullet.x > 1000 or bullet.x < -1000 or bullet.y > 1000 or bullet.y < -1000:
            bullets.remove(bullet)
        for enemy in enemy_list:
            s = math.sqrt((enemy.x - bullet.x) ** 2 + (enemy.y - bullet.y) ** 2)
            if s != 0:
                if s < 20:
                    enemy.health -= 21
                    for i in range(5):
                        effects.append(Effects(bullet.x, bullet.y, yellow))
                    try:
                        bullets.remove(bullet)
                    except:
                        pass

                    if enemy.health < 0:
                        for i in range(60):
                            effects.append(Effects(bullet.x, bullet.y, red))
                        try:
                            enemy_list.remove(enemy)
                            killed += 1
                        except:
                            pass
        for shit in shits:
            s = math.sqrt((shit.x - bullet.x) ** 2 + (shit.y - bullet.y) ** 2)
            if s != 0:
                if s < 12:
                    shit.health -= 21
                    for i in range(5):
                        effects.append(Effects(bullet.x, bullet.y, yellow))
                    try:
                        bullets.remove(bullet)
                    except:
                        pass

                    if shit.health < 0:
                        for i in range(60):
                            effects.append(Effects(bullet.x, bullet.y, shit_color))
                        try:
                            shits.remove(shit)
                            killed += 1
                        except:
                            pass

            
    for effect in effects:
        effect.move()
        if effect.x > 1000 or effect.x < -1000 or effect.y > 1000 or effect.y < -1000:
            effects.remove(effect)

    if player.health <= 0:
        mainDisplay.fill((150,150,150))
        mainDisplay.blit(dead, (0, 0))

        string = 'Всего лишь ' + str(killed) + ' врагов. Ты можешь лучше!!!'
        last_text = f.render(string, 1, (250, 250, 250))
        mainDisplay.blit(last_text, (173, 465))
        credits = f.render('By Portunov Andrew', 1, (250, 250, 250))
        mainDisplay.blit(credits, (10, 770))
        pygame.display.update()
        time.sleep(5)
        running = False



    mainDisplay.fill((150,150,150))
    gameDisplay.fill(black)

    for enemy in enemy_list:
        enemy.draw()
    for shit in shits:
        shit.draw()
    for bullet in bullets:
        bullet.draw()
    for effect in effects:
        effect.draw()
    player.draw()



    mainDisplay.blit(gameDisplay, (0,0))
    score = f.render(str(killed), 1, (250, 250, 250))
    mainDisplay.blit(score, (20, 20))

    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()