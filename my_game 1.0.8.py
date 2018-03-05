import pygame, os, random, sys

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

def terminate():
    pygame.quit()
    sys.exit()

def startScreen():
    image_fon = pygame.transform.scale(load_image("background.jpg"), (800,600))
    nameText = "Обед for cat"
    ruleText = ["Правила игры:",
                "С помощью мыши передвигай миску",
                "и лови рыбок! Не дай рыбкам упасть,",
                "а то cat останется без обеда...",
                "Берегись бомбочек!!!"]

    screen.blit(image_fon,(0,0))
    font = pygame.font.Font(None, 45)
    textCoord = 150
    for line in ruleText:
        stringRendered = font.render(line, 1, pygame.Color('black'))
        introRect = stringRendered.get_rect()
        textCoord += 20
        introRect.top = textCoord
        introRect.x = 40
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)

    font = pygame.font.Font(None,150)
    stringRendered = font.render(nameText, 1, pygame.Color('black'))
    introRect = stringRendered.get_rect()
    introRect.x = 80
    introRect.y = 45
    screen.blit(stringRendered, introRect)
    screen.blit(pygame.transform.scale(load_image("cat_cry.png"),(232,300)),(510,300))

def winScreen():
    image_fon = pygame.transform.scale(load_image("background.jpg"), (800, 600))
    text = "Ты молодец!"
    text_win = "Спасибо, я наелся!"
    screen.blit(image_fon, (0, 0))

    font = pygame.font.Font(None, 150)
    stringRendered = font.render(text, 1, pygame.Color('black'))
    introRect = stringRendered.get_rect()
    introRect.x = (width - stringRendered.get_rect()[2]) / 2
    introRect.y = 60

    font_text = pygame.font.Font(None, 80)
    stringRendered_text = font_text.render(text_win, 1, pygame.Color('black'))
    introRect_text = stringRendered_text.get_rect()
    introRect_text.x = (width - stringRendered_text.get_rect()[2]) / 2
    introRect_text.y = 150

    screen.blit(stringRendered, introRect)
    screen.blit(stringRendered_text, introRect_text)
    score_print((295, 280), "black", 80)
    screen.blit(pygame.transform.scale(load_image("cat_happy.png"), (250, 380)), (20, 200))


def gameover():
    gameOverText = "GAME OVER"
    screen.fill((0,0,0))
    font = pygame.font.Font(None, 150)
    stringRendered = font.render(gameOverText, 1, pygame.Color('white'))
    introRect = stringRendered.get_rect()
    introRect.x = (width - stringRendered.get_rect()[2])/2
    introRect.y = 60
    screen.blit(stringRendered, introRect)
    score_print((295,280),"white", 80)
    screen.blit(pygame.transform.scale(load_image("cat_cry.png"),(232,300)),(20,200))

def score_print(coordinate, score_color, font_text):
    font = pygame.font.Font(None, font_text)
    stringRendered = font.render("счёт: "+str(score), 1, pygame.Color(score_color))
    introRect = stringRendered.get_rect()
    introRect.x = coordinate[0]
    introRect.y = coordinate[1]
    screen.blit(stringRendered, introRect)

def life_print(life_num):
    i = 0
    image_life = pygame.transform.scale(load_image("life.png", -1),(40,40))
    for life in range(life_num):
        screen.blit(image_life,(image_life.get_rect()[2]*i + 5,10))
        i += 1


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        image = image.convert_alpha()
        return image

    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

class Food(pygame.sprite.Sprite):
    image = load_image("fish.png")
    def __init__(self):
        super().__init__(all_sprites)
        self.add(food_sprite)
        self.image = Food.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(172, width-self.image.get_rect()[2])
        self.rect.y = -self.image.get_rect()[3]

    def update(self):
        self.rect.y += (v/fps) * acceleration

class BadFood(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    def __init__(self):
        super().__init__()
        self.add(bad_food_sprite)
        self.image = BadFood.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(172, width - self.image.get_rect()[2])
        self.rect.y = -self.image.get_rect()[3]

    def update(self):
        self.rect.y += (v / fps) * acceleration


class Basket(pygame.sprite.Sprite):
    image = load_image("bowl.png")
    def __init__(self):
        super().__init__(basket_sprite)
        self.image = Basket.image
        self.rect = self.image.get_rect()
        self.rect.x = (width - self.image.get_rect()[2])/2
        self.rect.y = height - self.image.get_rect()[3]

    def get_event(self, event):
        if event.pos[0]-(self.image.get_rect()[2]/2) >= 170 and event.pos[0]+(self.image.get_rect()[2]/2-2) < width:
            self.rect.x = event.pos[0]-(self.image.get_rect()[2]/2)

class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(bord_sprite)
        self.image = load_image("bord.jpg")
        self.rect = pygame.Rect(0, height-80, width, height-80)

class ButtonStart:
    def __init__(self, rect=(290,450,220,100), text="START"):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("gray")
        self.font_color = pygame.Color("black")
        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False
        return self.pressed


all_sprites = pygame.sprite.Group()
food_sprite = pygame.sprite.Group()
bad_food_sprite = pygame.sprite.Group()
bord_sprite = pygame.sprite.Group()
basket_sprite = pygame.sprite.Group()


acceleration = 1
fps = 60
game = -1
life = 4
score = 0
v = 140

clock = pygame.time.Clock()
game_image = pygame.transform.scale(load_image("paws.jpg"), (800, 600))

Border()
basket = Basket()

MYEVENT = pygame.USEREVENT + 1
myevent_timer = 1700
pygame.time.set_timer(MYEVENT, myevent_timer)

button_start = ButtonStart()

while True:

    stroke = random.randrange(-1,2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        if pygame.mouse.get_focused() and game == 1:
            pygame.mouse.set_visible(False)
        elif pygame.mouse.get_focused() and game == 0:
            pygame.mouse.set_visible(True)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_start.get_event(event) and game == -1:
                game = 1

        if event.type == pygame.MOUSEMOTION:
            basket.get_event(event)

        if event.type == MYEVENT and game == 1:
            if stroke < 0:
                bad_food = BadFood()
                bad_food_sprite.add(bad_food)
                all_sprites.add(bad_food)

            else:
                food = Food()
                food_sprite.add(food)
                all_sprites.add(food)

            myevent_timer -= 20
            pygame.time.set_timer(MYEVENT, max(100, myevent_timer))


    for food in food_sprite:
        if pygame.sprite.spritecollideany(food, bord_sprite):
            life -= 1
            food.kill()

        if pygame.sprite.spritecollideany(food, basket_sprite):
            score += 1
            if score%5 == 0:
                acceleration += 0.5
            food.kill()

    for bad_food in bad_food_sprite:
        if pygame.sprite.spritecollideany(bad_food, basket_sprite):
            life -= 1
            bad_food.kill()

        if pygame.sprite.spritecollideany(bad_food, bord_sprite):
            bad_food.kill()

    if life == 0:
        pygame.time.set_timer(MYEVENT, 0)
        for spr in all_sprites:
            spr.kill()
        game = 0

    if game == 1:
        screen.blit(game_image,(0,0))
        pygame.draw.rect(screen,pygame.Color("gray"),(0,0,170,600),0)
        score_print((10,55),"black", 50)
        life_print(life)
        all_sprites.update()
        all_sprites.draw(screen)
        basket_sprite.draw(screen)
    elif game == 0:
        if score < 25:
            gameover()
        elif score >= 25:
            winScreen()
    else:
        startScreen()
        button_start.render(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()