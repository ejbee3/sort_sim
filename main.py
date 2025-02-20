import pygame
import random
from entities import *
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE
)

pygame.init()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (137, 137, 137)
YELLOW = (255, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

pygame.display.set_caption("Sort Sim")

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

font = pygame.font.Font(None, 36)

def main():
    running = True
    sorting = False
    # make test array
    random_arr = []
    while len(random_arr) < 7:
            num = random.randint(1, 18)
            random_arr.append(num)
    
    button = Button(
        left=(SCREEN_WIDTH - 200) // 2,  # Center horizontally
        top=(SCREEN_HEIGHT - 100) // 2,  # Center vertically
        width=200,
        height=100,
        text="Sort list",
        color=GREEN,
        text_color=BLACK
    )

    # custom events
    NEXTSTEP = pygame.USEREVENT + 1
    pygame.time.set_timer(NEXTSTEP, 350)

    # set up visual array
    bars = []
    bar_x = 100
    bar_y = 400
    # indices for loops
    i = 0
    j = i
    min_index = i

    for num in random_arr:
        bars.append(Bar(bar_x, bar_y, num, GRAY))
        bar_x += 50

    while running:

        screen.fill(BLACK)
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.is_clicked(pygame.mouse.get_pos()):
                        # pygame.event.post(pygame.event.Event(STARTSORT))
                        sorting = True
            elif event.type == NEXTSTEP and sorting:
                n = len(bars)
                bars[min_index].color = GREEN
                if bars[j].value < bars[min_index].value:
                    bars[min_index].color = DARK_GREEN
                    min_index = j
                    bars[j].color = GREEN
                
                j += 1
                if j >= n:
                    
                    i += 1
                    j = i
                    min_index = i
                if i > n - 1:
                    pygame.time.set_timer(NEXTSTEP, 0)



                # bars[i].color = YELLOW
                # if i == 0:
                #     bars[len(bars) - 1].color = GRAY
                # elif i > 0:
                #     bars[i - 1].color = GRAY
                # i = (i + 1) % len(bars)
    
        if not sorting:
            button.draw(screen, font)
        else:
            for bar in bars:
                pygame.draw.rect(screen, bar.color, bar)
            
            

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()