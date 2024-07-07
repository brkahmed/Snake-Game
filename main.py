import pygame, random
from pygame.locals import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen_size = pygame.math.Vector2(1080, 600)
        self.screen = pygame.display.set_mode(self.screen_size, SCALED)
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.event_map = set()

    def update_event_map(self):
        self.event_map.clear()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.event_map.add(QUIT)
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.event_map.add(K_UP)
                elif event.key == K_DOWN:
                    self.event_map.add(K_DOWN)
                elif event.key == K_LEFT:
                    self.event_map.add(K_LEFT)
                elif event.key == K_RIGHT:
                    self.event_map.add(K_RIGHT)
                    
    def run(self):
        cell_width = 60
        apple = Apple(self, '#ff9922', cell_width)
        snake = Snake(self, apple, cell_width)
        while True:
            self.update_event_map()
            if QUIT in self.event_map:
                break
            self.clock.tick(10)

            self.screen.fill("#111111")

            self.draw_cells(cell_width)

            apple.draw()

            snake.update()
            snake.draw()

            pygame.display.flip()

        pygame.quit()

    def draw_cells(self, width = 60) -> None:
        for i in range(0,int(self.screen_size.x), width):
            pygame.draw.line(self.screen, 'white', (i, 0), (i, self.screen_size.y))
        for i in range(0,int(self.screen_size.y), width):
            pygame.draw.line(self.screen, 'white', (0, i), (self.screen_size.x, i))


class Segment(pygame.Rect):
    def __init__(self, x, y, color, width) -> None:
        super().__init__(x, y, width, width)
        self.color = color

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self)

class Snake:
    def __init__(self, game: Game, apple: 'Apple', cell_width) -> None:
        self.game = game
        self.apple = apple
        self.cell_width = cell_width
        self.head = Segment(self.game.screen_size.x // 2,
                            self.game.screen_size.y // 2,
                            '#00ff66',
                            self.cell_width)
        self.segments: list[Segment] = list()
        self.segments.append(self.head)

        self.dx = 1
        self.dy = 0
        for _ in range(2): self.increase()

    def increase(self) -> None:
        self.segments.append(Segment(self.segments[-1].x - self.cell_width * self.dx,
                                     self.segments[-1].y - self.cell_width * self.dy,
                                     'red',
                                     self.cell_width))

    def draw(self) -> None:
        for i in range(len(self.segments) - 1, -1, -1):
            self.segments[i].draw(self.game.screen)

    def move(self) -> None:
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i-1].x
            self.segments[i].y = self.segments[i-1].y
        self.segments[0].x = (self.segments[0].x + self.cell_width * self.dx) % self.game.screen_size.x
        self.segments[0].y = (self.segments[0].y + self.cell_width * self.dy) % self.game.screen_size.y

    def change_dir(self) -> None:
        if K_UP in self.game.event_map and self.dy != 1:
            self.dy = -1
            self.dx = 0
        elif K_DOWN in self.game.event_map and self.dy != -1:
            self.dy = 1
            self.dx = 0
        elif K_RIGHT in self.game.event_map and self.dx != -1:
            self.dy = 0
            self.dx = 1
        elif K_LEFT in self.game.event_map and self.dx != 1:
            self.dy = 0
            self.dx = -1

    def check_collision(self) -> None:
        if self.head.colliderect(self.apple):
            self.increase()
            self.apple.new_pos(self.segments)

        for i in range(1, len(self.segments)):
            if self.head.colliderect(self.segments[i]):
                self.clear()
                break

    def clear(self) -> None:
        self.segments.clear()
        self.head = Segment(self.game.screen_size.x // 2,
                            self.game.screen_size.y // 2,
                            'green',
                            self.cell_width)
        self.segments.append(self.head)

        self.dx = 1
        self.dy = 0
        for _ in range(2): self.increase()

    def update(self) -> None:
        self.check_collision() 
        self.change_dir()
        self.move()

class Apple(pygame.Rect):
    def __init__(self, game: Game, color, cell_width) -> None:
        self.game = game
        self.color = color
        super().__init__(120, 120, cell_width, cell_width)
        
    def draw(self) -> None:
        pygame.draw.circle(self.game.screen,
                           self.color,
                           self.center,
                           self.width // 2)
        
    def new_pos(self, segments) -> None:
        while True:
            self.x = random.randint(0, int(self.game.screen_size.x - self.width) // self.width) * self.width
            self.y =random.randint(0, int(self.game.screen_size.y - self.width) // self.width) * self.width
            if self.collidelist(segments) <= 0:
                break

if __name__ == '__main__':
    Game().run()