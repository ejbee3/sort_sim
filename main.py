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

BAR_WIDTH = 25
BAR_HEIGHT = 15
BAR_Y = 400


pygame.display.set_caption("Sort Sim")

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def main():
    running = True
    sorting = False
    swapping = False
    swap_needed = True
    sort_completed = False
    
    button = Button(
        left=(SCREEN_WIDTH - 200) // 2,  # Center horizontally
        top=(SCREEN_HEIGHT - 100) // 2,  # Center vertically
        width=200,
        height=100,
        text="Sort list",
        color=GREEN,
        text_color=BLACK
    )

    exit_button = Button(
        left=(SCREEN_WIDTH - 200) // 2,  # Center horizontally
        top=(SCREEN_HEIGHT - 100) // 2,  # Center vertically
        width=200,
        height=100,
        text="You did it!",
        color=GREEN,
        text_color=BLACK
    )

    bar_x = 100

    # custom events
    NEXTITER = pygame.USEREVENT + 1
    SORTING_SPEED = 350
    pygame.time.set_timer(NEXTITER, SORTING_SPEED)

    # make test array
    arr = []
    while len(arr) < 8:
            arr.append(random.randint(1, 18))
   
    # indices for loops
    i = 0
    j = i
    min_index = i
    # dicts for swap
    current_min = {}
    target_swap = {}

    bars = pygame.sprite.Group()

    for index in range(len(arr)):
        total_height = BAR_HEIGHT * arr[index]
        bar = Bar_Sprite(bar_x, BAR_Y - total_height, BAR_WIDTH, total_height)
        bars.add(bar)
        bar_x += 50

    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    with_mouse = pygame.mouse.get_pos()
                    if button.is_clicked(with_mouse):
                        sorting = True
                    elif exit_button.is_clicked(with_mouse):
                        running = False
            elif event.type == NEXTITER and sorting and not swapping:
                bars_list = bars.sprites()
                n = len(bars_list)
                if j == n:
                    pygame.time.wait(SORTING_SPEED)
                else:
                    prev_bar = bars_list[j - 1]
                    prev_val = arr[j - 1]
                    bars_list[min_index].recolor(GREEN)
                    bars_list[min_index].is_smallest = True
                    if arr[j] < arr[min_index]:
                        # changing color and bool of old min
                        bars_list[min_index].recolor(GRAY)
                        bars_list[min_index].is_smallest = False
                        # updating color and bool to new min
                        bars_list[j].recolor(GREEN)
                        bars_list[j].is_smallest = True
                        # check if there is a yellow bar before the new min
                        if prev_val >= arr[min_index]:
                            prev_bar.recolor(GRAY)
                        # assigning last so it's not confusing
                        min_index = j
                    else:
                        if j >= i + 1:
                            if not prev_bar.is_smallest:
                                prev_bar.recolor(GRAY)
                            bars_list[j].recolor(YELLOW)
                # increment
                j += 1
                if j > n:
                    # start swap animation
                    for index, bar in enumerate(bars_list):
                        if bar.is_smallest:
                            current_min['x'] = bar.rect.x
                            current_min['index'] = index
                    if current_min['index'] == 0:
                        swap_needed = False
                    else:
                        target_swap['x'] = bars_list[i].rect.x
                        target_swap['index'] = i
                    
                    pygame.time.set_timer(NEXTITER, 0)
                    swapping = True

                
        # drawing and swapping
        screen.fill(BLACK) 
        if not sorting:
            button.draw(screen, font)
        elif sort_completed:
            exit_button.draw(screen, font)
        else:
            if swapping and swap_needed:
                current_min_bar = bars_list[current_min['index']]
                target_bar = bars_list[target_swap['index']]
                if current_min['index'] != len(bars_list) - 1:
                    bars_list[len(bars_list) - 1].recolor(GRAY)
                target_bar.recolor(YELLOW)
                if (
                        current_min_bar.rect.x <= target_swap['x'] and
                        target_bar.rect.x >= current_min['x']
                    ):
                    # actually swap the bars in the array
                    arr[current_min['index']], arr[target_swap['index']] = arr[target_swap['index']], arr[current_min['index']]
                    bar_x = 100
                    bars.empty()
                    for index in range(len(arr)):
                        total_height = BAR_HEIGHT * arr[index]
                        bar = Bar_Sprite(bar_x, BAR_Y - total_height, BAR_WIDTH, total_height)
                        if index <= target_swap['index']:
                            bar.recolor(DARK_GREEN)
                        bars.add(bar)
                        bar_x += 50
                    # increment loops
                    i += 1

                    j = i
                    min_index = i
                    if i == len(arr):
                        sort_completed = True
                    else:
                        # restart timer
                        swapping = False
                        pygame.time.set_timer(NEXTITER, SORTING_SPEED + 200)
                elif not swap_needed:
                    current_min_bar.recolor(DARK_GREEN)
                    target_bar.recolor(GRAY)

                    swapping = False
                    pygame.time.set_timer(NEXTITER, SORTING_SPEED)
                else:
                    current_min_bar.update(-1)
                    target_bar.update(1)

            bars.draw(screen)
                
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()