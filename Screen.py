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

        self.env = Environment()

    def handleEvent(self, event):
        if event.type == QUIT:
            self.gameOver = True

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
        if elapsed < self.dt:
            sleep(self.dt-elapsed)

    def loop(self):
        while not self.gameOver:
            self.begin()
            for event in pg.event.get():
                self.handleEvent(event)
            self.update()
            self.display()
            self.end()
        pg.display.quit()
