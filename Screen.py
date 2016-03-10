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

        self.env = Environment()

    def handleEvent(self, event):
        if event.type == QUIT:
            self.gameOver = True
        elif event.type == MOUSEBUTTONDOWN:
            mousePos = pg.mouse.get_pos()
            self.env.checkClick(mousePos)
        elif event.type == KEYDOWN:
            if event.key == K_s:
                self.env.saveSelected()
            elif event.key == K_p:
                self.paused = not self.paused

    def display(self):
        self.screen.blit(self.background, (0,0))
        self.env.draw(self.screen)
        pg.display.flip()

    def update(self):
        self.env.update(self.dt)

    def begin(self):
        self.time = clock()

    def end(self):
        elapsed = clock()-self.time
        if elapsed < 1./self.fps:
            sleep(1./self.fps-elapsed)

    def loop(self):
        while not self.gameOver:
            self.begin()
            for event in pg.event.get():
                self.handleEvent(event)
            if not self.paused:
                self.update()
            self.display()
            self.end()
        pg.display.quit()
