import pygame
import keyboard
import time
pygame.init()
info = pygame.display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h
GRAV = 0.08
JUMP = -5
BALLSCALE = 80
MOVESPEED = 4
BGC = 'yellow'
TEXTC = 'black'

font = pygame.font.Font(None, 36)
arr_text = font.render('LEFT UP RIGHT --> MOVEMENT', True, TEXTC)
dtext = font.render('DOWN --> REACH GROUND WHILE IN AIR', True, TEXTC)
icetext = font.render('A --> Iceball', True, TEXTC)
firetext = font.render('D --> Fireball', True, TEXTC)
c1text = font.render('A/D --> COW', True, TEXTC)
c2text = font.render('UP/DOWN --> IRONMAN', True, TEXTC)

class Player:
    def __init__(self, x, y) -> None:
        self.x = x - WIDTH//30
        self.y = y
        self.width = WIDTH//15
        self.height = HEIGHT//4
        self.vely = 0
        self.side = True
        self.down = False
        self.ground = True
        self.im = False
        self.dj = True
        self.djump = False
        self.sonic = pygame.image.load('Images//Sonic.png')
        self.ironman = pygame.image.load('Images//IronMan.png')
    
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.sonic if not self.im else self.ironman, (self.width, self.height)), (self.x, self.y))
    
    def jump(self):
        self.vely=JUMP
    
    def gravity(self, ground):
        self.y+=self.vely
        self.vely+=GRAV + (2 if self.down else 0)
        if self.y>=ground.y-self.height:
            self.y = ground.y-self.height
            self.vely=0
            self.ground = True
            self.dj = True

    def move(self, side:bool):
        if self.side!=side:
            self.sonic = pygame.transform.flip(self.sonic, True, False)
            self.ironman = pygame.transform.flip(self.ironman, True, False)
        self.side = side
        if side:
            self.x+=MOVESPEED
        else:
            self.x-=MOVESPEED


class Ground:
    def __init__(self) -> None:
        self.x = 0
        self.y = HEIGHT*3//5+HEIGHT//4
        self.height = HEIGHT - self.y
        self.width = WIDTH
        self.image = pygame.image.load('Images//Background.jpeg')
    
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (WIDTH, HEIGHT)),(0,0))
    
class Ball:
    def __init__(self, player, type, a, b) -> None:
        self.x = player.x + player.width//2
        self.y = player.y
        self.vely = (b[1] - a[1])/BALLSCALE
        self.velx = (b[0] - a[0])/BALLSCALE
        self.image = pygame.image.load('Images//'+type+".png")

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (WIDTH//7, HEIGHT//7)), (self.x, self.y))


    def move(self):
        self.y+=self.vely
        self.x+=self.velx

class Dot:
    def __init__(self, c:tuple, type) -> None:
        self.x1 = c[0]
        self.y1 = c[1]
        self.type = type
    
    def draw(self, screen, player):
        pygame.draw.line(screen, self.type, (self.x1, self.y1), (player.x, player.y), WIDTH//100)
        pygame.draw.circle(screen, self.type, (self.x1, self.y1), (WIDTH//90))

def draw(screen, player, ground, dot, ball, hisls):
    ground.draw(screen)
    for i in dot:
        i.draw(screen, player)
    for i in ball:
        i.draw(screen)
        i.move()
    player.draw(screen)
    if len(hisls)>0:
        htext = font.render("History: "+hisls[-1], True, 'magenta')
        screen.blit(htext, (20, 20))
    screen.blit(arr_text, (WIDTH*2//3, 30))
    screen.blit(dtext, (WIDTH*2//3, 70))
    screen.blit(icetext, (WIDTH*2//3, 110))
    screen.blit(firetext, (WIDTH*2//3, 150))
    screen.blit(c1text, (WIDTH*2//3, 190))
    screen.blit(c2text, (WIDTH*2//3, 230))
    pygame.display.flip()

def bitstring():
    s = []
    s.append(1 if keyboard.is_pressed('down') else 0)
    s.append(1 if keyboard.is_pressed('up') else 0)
    s.append(1 if keyboard.is_pressed('left') else 0)
    s.append(1 if keyboard.is_pressed('right') else 0)
    s.append(1 if keyboard.is_pressed('a') else 0)
    s.append(1 if keyboard.is_pressed('d') else 0)
    s.append(1 if keyboard.is_pressed('a') and keyboard.is_pressed('d') else 0)
    s.append(1 if keyboard.is_pressed('up') and keyboard.is_pressed('down') else 0)
    return ''.join([str(i) for i in s])

def action(s, screen, player):
    bs = [int(i) for i in s]
    for i, j in enumerate(bs[::-1]):
        if j==0:continue
        if i==4:
            player.move(True)
        if i==5:
            player.move(False)
        if i==0: break
        if i==6:
            if player.ground:
                player.jump()
                player.ground = False
            elif player.djump:
                player.jump()
                player.djump = False
            continue
        if i==7:
            player.down = True
        else:
            player.down = False

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CSP PROJECT")
    player = Player(WIDTH//2, HEIGHT*3//5)
    ground = Ground()
    dotls = []
    ballls = []
    history = []
    run = True

    a = False
    b = False
    c1 = False

    while run:
        draw(screen, player, ground, dotls, ballls, history)
        for event in pygame.event.get():
            if event == pygame.QUIT or keyboard.is_pressed('q'):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if keyboard.is_pressed('a') and keyboard.is_pressed('d') and (a or b):
                    a = False
                    b = False
                    dotls.pop()
                    c1 = True
                    dotls.append(Dot((player.x, player.y), 'white'))
                
                if keyboard.is_pressed('up') and keyboard.is_pressed('down'):
                    player.im = True
                
                if not a and keyboard.is_pressed('a') and not keyboard.is_pressed('d') and not c1:
                    a = True
                    dotls.append(Dot((player.x, player.y), 'blue'))
                if not b and keyboard.is_pressed('d') and not keyboard.is_pressed('a') and not c1:
                    b = True
                    dotls.append(Dot((player.x, player.y), 'orange'))
            if event.type == pygame.KEYUP:
                if not keyboard.is_pressed('up') and not player.ground and not player.djump and player.dj:
                    player.djump=True
                    player.dj = False
                if a and not keyboard.is_pressed('a'):
                    ballls.append(Ball(player, 'Iceball', (dotls[0].x1, dotls[0].y1), (player.x, player.y)))
                    dotls.pop()
                    a = False
                if b and not keyboard.is_pressed('d'):
                    ballls.append(Ball(player, 'Fireball', (dotls[0].x1, dotls[0].y1), (player.x, player.y)))
                    dotls.pop()
                    b = False
                
                if c1 and (not keyboard.is_pressed('a') or not keyboard.is_pressed('d')):
                    ballls.append(Ball(player, 'Cow', (dotls[0].x1, dotls[0].y1), (player.x, player.y)))
                    dotls.pop()
                    c1 = False
                
                if not keyboard.is_pressed('up') or not keyboard.is_pressed('down'):
                    player.im =False
                    
        bs = bitstring()
        if bs!='00000000':
            history.append(bs)
            print(history[-1])
            action(bs, screen, player)
        
        while len(ballls)>5:
            del ballls[0]
        
        if not player.ground:
            player.gravity(ground)
                

if __name__ == "__main__":
    main()