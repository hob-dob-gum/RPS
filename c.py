import pygame
from n import Network
import pickle
pygame.font.init()

WIDTH = 700
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Client')

class button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('timesnewroman', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        WIN.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y +self.height:
            return True
        else:
            return False

def draw_window(WIN, game, player):
    WIN.fill((128, 128, 128))

    if not(game.connected()):
        font = pygame.font.SysFont('timesnewroman', 80)
        text = font.render('Waiting', 1, (255, 0, 0), True)
        WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont('timesnewroman', 60)
        text = font.render('Your Move', 1, (0, 255, 255))
        WIN.blit(text, (80, 200))
        text = font.render('Opponents', 1, (0, 255, 255))
        WIN.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_went():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1_went and player == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1_went:
                text1 = font.render('Locked In', 1, (0, 0, 0))
            else:
                text1 = font.render('Waiting...', 1, (0, 0, 0))

            if game.p2_went and player == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2_went:
                text2 = font.render('Locked In', 1, (0, 0, 0))
            else:
                text2 = font.render('Waiting...', 1, (0, 0, 0))

        if player == 1:
            WIN.blit(text2, (100, 350))
            WIN.blit(text1, (400, 350))
        else:
            WIN.blit(text1, (100, 350))
            WIN.blit(text2, (400, 350))
        for btn in btns:
            btn.draw(WIN)

    pygame.display.update()




btns = [button('Rock', 50, 500, (0, 0, 255)),
        button('Scissors', 250, 500, (255, 0, 0)),
        button('Paper', 450, 500, (0, 255, 0))]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_p())
    print('you are player ', player)

    while run:
        clock.tick(60)
        try:
            game = n.send('get')
        except:
            run = False
            print('Couldnt Get Game')
            break

        if game.both_went():
            draw_window(WIN, game, player)
            pygame.time.delay(500)
            try:
                game = n.send('reset')
            except:
                run = False
                print('Couldnt Get Game')
                break

            font = pygame.font.SysFont('timesnewroman', 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render('You Won!!!', 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render('Tie Game', 1, (255, 0, 0))
            else:
                text = font.render('You Lost...', 1, (255, 0, 0))

            WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1_went:
                                n.send(btn.text)
                        else:
                            if not game.p2_went:
                                n.send(btn.text)
        draw_window(WIN, game, player)


main()