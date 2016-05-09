from Environment import *
from time import sleep,clock

class Screen(object):
    def __init__(self):
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption('Evolving Organisms')
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill((150,170,150))
        self.gameOver = False
        self.time = 0
        self.dt = 1./30
        self.fps = 60
        self.paused = False

        self.width = 2000
        self.height = 2000
        self.center = map(int,(self.width/2,self.height/2))

        self.env = Environment(self)

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.gameOver = True
            elif event.type == MOUSEBUTTONDOWN:
                mousePos = pg.mouse.get_pos()
                self.env.checkClick(mousePos, self.center)
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    self.env.saveSelected()
                elif event.key == K_p:
                    self.paused = not self.paused
        keysPressed = pg.key.get_pressed()
        if keysPressed[K_UP]:
            self.center[1] -= 2
        elif keysPressed[K_DOWN]:
            self.center[1] += 2
        if keysPressed[K_LEFT]:
            self.center[0] -= 2
        elif keysPressed[K_RIGHT]:
            self.center[0] += 2

    def display(self):
        self.screen.blit(self.background, (0,0))
        self.env.draw(self.screen, self.center)
        pg.display.flip()

    def update(self):
        if self.env.update(self.dt):
            self.center = map(int,(self.width/2,self.height/2))

    def begin(self):
        self.time = clock()

    def end(self):
        elapsed = clock()-self.time
        if elapsed < 1./self.fps:
            sleep(1./self.fps-elapsed)

    def loop(self):
        while not self.gameOver:
            self.begin()
            self.handleEvents()
            if not self.paused:
                self.update()
            self.display()
            self.end()
        pg.display.quit()
