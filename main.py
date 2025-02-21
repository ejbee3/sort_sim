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

clock = pygame.time.Clock()

def main():
    running = True
    sorting = False
    swapping = False
    # TODO: if first element is already sorted, no swap needed!
    # no_swap_needed = False
    has_reached_end_point = False
    # make test array
    random_arr = []
    while len(random_arr) < 8:
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
    NEXTITER = pygame.USEREVENT + 1
    pygame.time.set_timer(NEXTITER, 600)

    # set up visual array
    bars = []
    bar_x = 100
    bar_y = 400
    # indices for loops
    i = 0
    j = i
    min_index = i
    # dicts for swap
    current_smallest = {}
    current_swapper = {}

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
            elif event.type == NEXTITER and sorting and not swapping:
                n = len(bars)
                if j == n:
                    pygame.time.wait(600)
                else:
                    prev = bars[j - 1]
                    bars[min_index].color = GREEN
                    bars[min_index].is_smallest = True
                    if bars[j].value < bars[min_index].value:
                        # changing color and bool of old min
                        bars[min_index].color = GRAY
                        bars[min_index].is_smallest = False
                        # updating color and bool to new min
                        bars[j].color = GREEN
                        bars[j].is_smallest = True
                        # check if there is a yellow bar before the new min
                        if prev.value >= bars[min_index].value:
                            prev.color = GRAY
                        # assigning last so its not confusing
                        min_index = j
                    else:
                        if j >= i + 1:
                            if not prev.is_smallest:
                                prev.color = GRAY
                            bars[j].color = YELLOW
                # increment
                j += 1
                if j > n:
                    # start swap animation
                    for i, bar in enumerate(bars):
                        if bar.is_smallest:
                            current_smallest['bar'] = bar.rect.copy()
                            current_smallest['index'] = i
                    current_swapper['bar'] = bars[0].rect.copy()
                    current_swapper['index'] = 0
                    pygame.time.set_timer(NEXTITER, 0)
                    swapping = True

                
        # drawing and swapping
        if not sorting:
            button.draw(screen, font)
        else:
            if swapping:
                speed = 2
                first_bar = bars[current_swapper['index']]
                smallest_bar = bars[current_smallest['index']]
                # target coordinates
                target_swap_x = current_swapper['bar'].x
                print(f'this is the first swap x coord: {target_swap_x}')
                target_smallest_x = current_smallest['bar'].x
                print(f'this is the smallest x coord: {target_smallest_x}')
                
                bars[len(bars) - 1].color = GRAY
                first_bar.color = YELLOW
                if not has_reached_end_point:
                    if smallest_bar.rect.x != target_swap_x:
                            direction = target_swap_x - smallest_bar.rect.x
                            if abs(direction) > speed:
                                smallest_bar.rect.x += speed if direction > 0 else -speed
                    
                    if first_bar.rect.x != target_smallest_x:
                            direction = target_smallest_x - first_bar.rect.x
                            if abs(direction) > speed:
                                first_bar.rect.x += speed if direction > 0 else -speed
                    else:
                        has_reached_end_point = True
                        swapping = False
                        # color smallest bar to dark green and mark as sorted
                        smallest_bar.color = DARK_GREEN
                        smallest_bar.is_sorted = True
                        smallest_bar.is_current_min = False
                        # color swapped bar back to gray
                        first_bar.color = GRAY
                        # actually swap the bars in the array
                        first_bar, smallest_bar = smallest_bar, first_bar
                        # increment loops
                        i += 1
                        j = i
                        min_index = i
                        # restart timer
                        pygame.time.set_timer(NEXTITER, 800)
            for bar in bars:
                pygame.draw.rect(screen, bar.color, bar.rect)
                
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

# TODO: update this method to work with repetitive code
def move_toward(current, target, speed):
    if current < target:
        return min(current + speed, target)
    elif current > target:
        return max(current - speed, target)
    return current


if __name__ == "__main__":
    main()