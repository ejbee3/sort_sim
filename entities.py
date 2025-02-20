import pygame

class Bar:
    def __init__(self, pos_x, pos_y, arr_value, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.height = 15 * arr_value
        self.width = 25
        self.value = arr_value
        self.color = color
        self.is_current_min = False
        self.is_sorted = False
        self.rect = pygame.Rect(pos_x, pos_y - self.height, self.width, self.height)


class Button(pygame.Rect):
    def __init__(self, left, top, width, height, text, color, text_color):
        super().__init__(left, top, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen, font):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, self)
        # Render the text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        # Check if the mouse position is within the button
        return self.collidepoint(mouse_pos)
        